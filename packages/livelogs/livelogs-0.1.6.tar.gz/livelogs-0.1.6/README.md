# LiveLogs

## Overview

**LiveLogs** is a real-time log streaming application designed to monitor and stream log files dynamically. It leverages Flask and SocketIO for web application and real-time communication, and uses Eventlet for asynchronous processing. The application allows users to observe log file changes live, making it ideal for monitoring applications, debugging, and operational insights.

## Features

- **Real-Time Log Updates**: Monitor log files as they are updated in real-time.
- **Configurable Log File Path**: Specify the path to the log file you want to monitor.
- **Integration with Flask**: Easily integrates with existing Flask applications.
- **SocketIO Support**: Uses SocketIO for real-time communication between the server and clients.
- **Asynchronous Processing**: Uses Eventlet for handling concurrent operations efficiently.

## Installation

To install **LiveLogs**, you can use Poetry, a Python dependency manager:

```bash
poetry add livelogs
```

Or if you're using `pip`, you can install it from PyPI (if published) or directly from the repository:

```bash
pip install livelogs
```

## Usage

1. **Command-Line Arguments**: Run the application with command-line arguments to specify the log file and configuration options.

```bash
livelogs <path_to_log_file> [--name APP_NAME] [--port PORT] [--host HOST] [--debug]
```

- `<path_to_log_file>`: Path to the log file to monitor.
- `--name APP_NAME`: Name of the app to display in the header (default: `App`).
- `--port PORT`: Port to run the app on (default: `5000`).
- `--host HOST`: Host to run the app on (default: `0.0.0.0`).
- `--debug`: Enable debug mode.

2. **Running the Application**:

To run the application, use the command:

```bash
livelogs /path/to/your/logfile.log
```

This will start the LiveLogs application and begin streaming the specified log file.

## Configuration

You can configure the application by modifying the `app` instance in `livelogs/app.py`. The configuration includes:

- **SECRET_KEY**: Secret key for session management.
- **DEBUG**: Enable or disable debug mode.

## Development

To contribute to **LiveLogs**, clone the repository and set up your development environment:

```bash
git clone https://github.com/destinedcodes/livelogs.git
cd livelogs
poetry install
```

Run tests using:

```bash
poetry run pytest
```

## License

**LiveLogs** is licensed under the [MIT License](LICENSE).

## Links

- [Homepage](https://github.com/destinedcodes/livelogs)
- [Issues](https://github.com/destinedcodes/livelogs/issues)
