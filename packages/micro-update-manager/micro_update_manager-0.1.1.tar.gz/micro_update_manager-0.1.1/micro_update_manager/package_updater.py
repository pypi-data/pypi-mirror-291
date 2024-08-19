import subprocess


def get_outdated_packages():
    """
    Get a list of outdated packages using `pip list --outdated`.

    Returns:
        dict: A dictionary where the keys are package names and values are a tuple (installed_version, latest_version).
    """
    result = subprocess.run(['pip', 'list', '--outdated'], stdout=subprocess.PIPE, text=True)
    lines = result.stdout.splitlines()

    outdated_packages = {}

    # Skip the header (first two lines)
    for line in lines[2:]:
        parts = line.split()
        package_name = parts[0]
        installed_version = parts[1]
        latest_version = parts[2]

        outdated_packages[package_name] = (installed_version, latest_version)

    return outdated_packages


def check_for_updates(package):
    """
    Check if there are updates available for the given package.

    Args:
        package (dict): Package configuration dictionary.

    Returns:
        bool: True if a newer version of the package is available, False otherwise.
    """
    package_name = package['name']

    # Get the list of outdated packages
    outdated_packages = get_outdated_packages()

    if package_name in outdated_packages:
        installed_version, latest_version = outdated_packages[package_name]
        print(f"Package {package_name} is outdated. Current version: {installed_version}, Latest version: {latest_version}")
        return True
    else:
        print(f"Package {package_name} is up to date.")
        return False


def monitor_packages(config):
    """
    Monitor and update the packages based on the configuration.

    Args:
        config (dict): Configuration dictionary containing package information.

    Returns:
        list: A list of updated packages that require a restart.
    """
    updated_packages = []
    for package in config['packages']:
        if check_for_updates(package):
            print(f"Package {package['name']} updated.")
            if package['requires_restart']:
                updated_packages.append(package)
    return updated_packages
