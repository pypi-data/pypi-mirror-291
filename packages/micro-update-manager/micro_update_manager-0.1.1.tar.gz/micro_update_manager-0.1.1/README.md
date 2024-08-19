# micro-update-manager

**micro-update-manager** is a Python package designed for monitoring and updating Python packages. It manages and restarts dependent microservices as necessary, making it ideal for maintaining large-scale distributed systems, IoT setups, and embedded systems where package updates and service restarts are crucial.

## Features

- **Monitor Python Packages**: Automatically checks for updates to specified Python packages.
- **Service Management**: Manages and restarts services (microservices, IoT devices, etc.) based on package updates.
- **Configurable Interfaces**: Supports various communication interfaces, including HTTP (with plans for gRPC and REST).
- **Highly Configurable**: Uses a YAML configuration file to specify package monitoring rules, service restart conditions, and more.

## Installation

You can install the package via pip:

```bash
pip install micro_update_manager
```

Or clone the repository and install it locally:

```bash
git clone https://github.com/yourusername/micro_update_manager.git
cd micro_update_manager
pip install .
```

## Usage

### Configuration

Create a `config.yaml` file to define the packages to monitor and the services to manage. Below is an example configuration:

```yaml
refresh_interval: 1800  # 30 minutes

packages:
  - name: "example_package"
    requires_restart: true
    processes_to_restart:
      - "microservice_A"
      - "microservice_B"

processes:
  microservice_A:
    interface:
      type: "http"
      host: "localhost"
      port: 5001
      endpoint: "/can_restart"
    command: "docker restart microservice_A"
    params: ""

  microservice_B:
    interface:
      type: "http"
      host: "localhost"
      port: 5002
      endpoint: "/can_restart"
    command: "docker restart microservice_B"
    params: ""
```

### Running the Manager

To start the `micro-update-manager`, use the following command:

```bash
micro-update-manager
```

This will load the configuration from `config.yaml`, monitor the specified packages, and manage the restarting of services as needed.

### Example Script

Here’s an example of how you can use the `micro-update-manager` in your own Python scripts:

```python
from micro_update_manager import main

if __name__ == "__main__":
    main()
```

### Development Setup

If you want to contribute to the development of `micro_update_manager`, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/yourusername/micro_update_manager.git
```

2. Install the development dependencies:

```bash
pip install -e .[dev]
```

3. Run tests to ensure everything is working:

```bash
pytest
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Thanks to all contributors and users who have provided feedback and ideas.
- Special mention to the open-source community for providing the tools and libraries that made this project possible.

## Contact

If you have any questions, feel free to reach out:

- **Email**: aleksander.stanik@hammerheadsengineers.com
- **GitHub**: [Aleksander Stanik(Olek)](https://github.com/AleksanderStanikHE)