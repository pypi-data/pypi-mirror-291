import yaml


def load_config(config_file):
    """
    Load the configuration from a YAML file.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        dict: The loaded configuration as a dictionary.
    """
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config
