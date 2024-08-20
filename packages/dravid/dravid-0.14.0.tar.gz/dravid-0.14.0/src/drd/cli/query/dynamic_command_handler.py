import traceback
import click
from ...api.main import call_dravid_api
import xml.etree.ElementTree as ET
from ...utils import print_error, print_success, print_info, print_step, print_debug
from ...metadata.common_utils import generate_file_description
from ...prompts.error_resolution_prompt import get_error_resolution_prompt


def execute_commands(commands, executor, metadata_manager, is_fix=False, debug=False):
    all_outputs = []
    total_steps = len(commands)

    for i, cmd in enumerate(commands, 1):
        step_description = "fix" if is_fix else "command"

        if cmd['type'] == 'explanation':
            all_outputs.append(
                f"Step {i}/{total_steps}: Explanation - {cmd['content']}")
        else:
            try:
                if cmd['type'] == 'shell':
                    output = handle_shell_command(cmd, executor)
                elif cmd['type'] == 'file':
                    output = handle_file_operation(
                        cmd, executor, metadata_manager)
                elif cmd['type'] == 'metadata':
                    output = handle_metadata_operation(cmd, metadata_manager)
                elif cmd['type'] == 'requires_restart':
                    output = 'requires restart if the server is running'
                else:
                    raise ValueError(f"Unknown command type: {cmd['type']}")

                if isinstance(output, str) and output.startswith("Skipping"):
                    print_info(f"Step {i}/{total_steps}: {output}")
                    all_outputs.append(f"Step {i}/{total_steps}: {output}")
                else:
                    all_outputs.append(
                        f"Step {i}/{total_steps}: {cmd['type'].capitalize()} command - {cmd.get('command', '')} {cmd.get('operation', '')}\nOutput: {output}")

            except Exception as e:
                error_message = f"Step {i}/{total_steps}: Error executing {step_description}: {cmd}\nError details: {str(e)}"
                print_error(error_message)
                all_outputs.append(error_message)
                return False, i, str(e), "\n".join(all_outputs)

        if debug:
            print_debug(f"Completed step {i}/{total_steps}")

    return True, total_steps, None, "\n".join(all_outputs)


def handle_shell_command(cmd, executor):
    output = executor.execute_shell_command(cmd['command'])
    if isinstance(output, str) and output.startswith("Skipping"):
        print_info(output)
        return output
    if output is None:
        raise Exception(f"Command failed: {cmd['command']}")
    print_success(f"Successfully executed: {cmd['command']}")
    if output:
        click.echo(f"Command output:\n{output}")
    return output


def handle_file_operation(cmd, executor, metadata_manager):
    operation_performed = executor.perform_file_operation(
        cmd['operation'],
        cmd['filename'],
        cmd.get('content'),
        force=True
    )
    if isinstance(operation_performed, str) and operation_performed.startswith("Skipping"):
        print_info(operation_performed)
        return operation_performed
    elif operation_performed:
        print_success(
            f"Successfully performed {cmd['operation']} on file: {cmd['filename']}")
        if cmd['operation'] in ['CREATE', 'UPDATE']:
            update_file_metadata(cmd, metadata_manager, executor)
        return "Success"
    else:
        raise Exception(
            f"File operation failed: {cmd['operation']} on {cmd['filename']}")


def handle_metadata_operation(cmd, metadata_manager):
    if cmd['operation'] == 'UPDATE_FILE':
        if metadata_manager.update_metadata_from_file():
            print_success(f"Updated metadata for file: {cmd['filename']}")
            return f"Updated metadata for {cmd['filename']}"
        else:
            raise Exception(
                f"Failed to update metadata for file: {cmd['filename']}")
    else:
        raise Exception(f"Unknown operation: {cmd['operation']}")


def update_file_metadata(cmd, metadata_manager, executor):
    file_info = metadata_manager.analyze_file_sync(cmd['filename'])
    if file_info:
        metadata_manager.update_file_metadata(
            file_info['path'],
            file_info['type'],
            cmd.get('content', ''),
            file_info['summary'],
            file_info['exports'],
            file_info['imports']
        )

        # Handle dependencies from the XML response
        handle_dependencies(file_info, metadata_manager)


def handle_dependencies(file_info, metadata_manager):
    if 'xml_response' in file_info:
        try:
            root = ET.fromstring(file_info['xml_response'])
            dependencies = root.find('.//external_dependencies')
            if dependencies is not None:
                for dep in dependencies.findall('dependency'):
                    dependency_info = dep.text.strip()
                    metadata_manager.add_external_dependency(dependency_info)
                print_info(
                    f"Added {len(dependencies)} dependencies to the project metadata.")

            # Handle other metadata updates
            update_project_info(root, metadata_manager)
            update_dev_server_info(root, metadata_manager)
        except ET.ParseError:
            print_error("Failed to parse XML response for dependencies")


def update_project_info(root, metadata_manager):
    project_info = root.find('.//project_info')
    if project_info is not None:
        for field in ['name', 'version', 'description']:
            element = project_info.find(field)
            if element is not None and element.text:
                metadata_manager.metadata['project_info'][field] = element.text.strip(
                )


def update_dev_server_info(root, metadata_manager):
    dev_server = root.find('.//dev_server')
    if dev_server is not None:
        start_command = dev_server.find('start_command')
        if start_command is not None and start_command.text:
            metadata_manager.metadata['dev_server']['start_command'] = start_command.text.strip(
            )


def handle_error_with_dravid(error, cmd, executor, metadata_manager, depth=0, previous_context="", debug=False):
    if depth > 3:
        print_error(
            "Max error handling depth reached. Unable to resolve the issue.")
        return False

    print_error(f"Error executing command: {error}")

    error_message = str(error)
    error_type = type(error).__name__
    error_trace = ''.join(traceback.format_exception(
        type(error), error, error.__traceback__))

    project_context = metadata_manager.get_project_context()
    error_query = get_error_resolution_prompt(
        previous_context, cmd, error_type, error_message, error_trace, project_context
    )

    print_info(
        "🏏 Sending error information to dravid for analysis(1 LLM call)...\n")

    try:
        fix_commands = call_dravid_api(
            error_query, include_context=True)
    except ValueError as e:
        print_error(f"Error parsing dravid's response: {str(e)}")
        return False

    print_info("🩺 Dravid's suggested fix:", indent=2)
    print_info("🔨 Applying dravid's suggested fix...", indent=2)

    fix_applied, step_completed, error_message, all_outputs = execute_commands(
        fix_commands, executor, metadata_manager, is_fix=True, debug=debug
    )

    if fix_applied:
        print_success("All fix steps successfully applied.")
        click.echo(all_outputs)
        return True
    else:
        print_error(f"Failed to apply the fix at step {step_completed}.")
        print_error(f"Error message: {error_message}")
        click.echo(all_outputs)

        return handle_error_with_dravid(
            Exception(error_message),
            {"type": "fix", "command": f"apply fix step {step_completed}"},
            executor,
            metadata_manager,
            depth + 1,
            all_outputs,
            debug
        )
