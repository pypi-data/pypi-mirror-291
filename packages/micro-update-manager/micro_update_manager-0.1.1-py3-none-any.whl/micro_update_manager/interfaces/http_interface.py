import requests


def can_restart_process(interface_config, process_name):
    """
    Check if the process can be restarted by sending an HTTP GET request.

    Args:
        interface_config (dict): Configuration dictionary for the HTTP interface.
        process_name (str): Name of the process to check.

    Returns:
        bool: True if the process can be restarted, False otherwise.
    """
    url = f"http://{interface_config['host']}:{interface_config['port']}{interface_config['endpoint']}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('can_restart', False)
    except requests.RequestException as e:
        print(f"Failed to check if process '{process_name}' can restart via HTTP interface: {e}")
        return False
