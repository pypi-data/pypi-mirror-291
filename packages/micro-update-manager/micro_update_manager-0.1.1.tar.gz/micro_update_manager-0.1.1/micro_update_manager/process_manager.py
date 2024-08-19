import subprocess
from micro_update_manager.interfaces.http_interface import can_restart_process


def start_interface(interface_type, interface_config, process_name):
    """
    Start the specified communication interface based on the configuration.

    Args:
        interface_type (str): Type of the interface (e.g., "rest", "grpc", "http").
        interface_config (dict): Configuration dictionary for the interface.
        process_name (str): Name of the process to manage.

    Returns:
        bool: True if the process can be restarted, False otherwise.
    """
    if interface_type == "rest":
        print(f"REST interface is not yet implemented for process '{process_name}'.")
        return True  # Assume process can restart by default if not implemented
    elif interface_type == "grpc":
        print(f"gRPC interface is not yet implemented for process '{process_name}'.")
        return True  # Assume process can restart by default if not implemented
    elif interface_type == "http":
        if not can_restart_process(interface_config, process_name):
            print(f"Process '{process_name}' cannot be restarted based on HTTP interface check.")
            return False
        print(f"Process '{process_name}' can be restarted based on HTTP interface check.")
        return True
    else:
        raise ValueError(f"Unsupported interface type: {interface_type}")


def restart_processes(process_list, config):
    """
    Restart the specified list of processes based on their configuration.

    Args:
        process_list (list): List of process names to restart.
        config (dict): Configuration dictionary containing process information.
    """
    for process_name in process_list:
        process_config = config["processes"].get(process_name)
        if not process_config:
            print(f"Process '{process_name}' not found in the configuration.")
            continue

        interface_type = process_config.get("interface", {}).get("type", "rest")  # Default to "rest" if not specified
        interface_config = process_config.get("interface", {})

        # Check if the process can be restarted based on the interface check
        if not start_interface(interface_type, interface_config, process_name):
            print(f"Skipping restart of process '{process_name}'.")
            continue

        command = process_config.get("command")
        params = process_config.get("params", "")
        full_command = f"{command} {params}"

        print(f"Executing command to restart process: {full_command}")
        subprocess.run(full_command, shell=True)
