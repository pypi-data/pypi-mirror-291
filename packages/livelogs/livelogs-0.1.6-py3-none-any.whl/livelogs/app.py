# Import Eventlet and apply monkey patching before importing Flask or other modules
import eventlet
eventlet.monkey_patch()

import os
import sys
import argparse
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    return app

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='LiveLogs - Live Logs Streaming')
    parser.add_argument('filename', type=str, help='Path to the log file')
    parser.add_argument('--name', type=str, default='App', help='Name of the app to display in the header')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the app on')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to run the app on')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    return parser.parse_args()

def configure_socketio(app):
    """Configure and initialize SocketIO."""
    socketio = SocketIO(app)

    @app.route('/')
    def stream_file():
        """Render the main page."""
        return render_template('index.html', app_name=APP_NAME)

    @socketio.on('start_stream')
    def handle_start_stream():
        """Handle the start stream event and initiate file watching."""
        try:
            with open(FILE_PATH, 'r') as f:
                content = f.read()
                emit('file_update', content)
        except Exception as e:
            print(f'Error reading file on initial connection: {e}')

        # Start the background task to watch file changes
        socketio.start_background_task(target=watch_file)

    def watch_file():
        """Watch the file for changes and emit updates."""
        last_modified_time = os.path.getmtime(FILE_PATH)
        try:
            while True:
                current_modified_time = os.path.getmtime(FILE_PATH)
                if current_modified_time != last_modified_time:
                    with open(FILE_PATH, 'r') as f:
                        content = f.read()
                        socketio.emit('file_update', content)
                    last_modified_time = current_modified_time
                eventlet.sleep(1)
        except Exception as e:
            print(f'Error watching file: {e}')

    return socketio

def main():
    """Main function to run the application."""
    args = parse_arguments()

    global FILE_PATH, APP_NAME
    FILE_PATH = args.filename
    APP_NAME = args.name
    PORT = args.port
    HOST = args.host
    DEBUG = args.debug

    if not os.path.isfile(FILE_PATH):
        print(f"File does not exist: {FILE_PATH}")
        sys.exit(1)

    app = create_app()
    socketio = configure_socketio(app)

    # Run the Flask app with SocketIO
    socketio.run(app, host=HOST, port=PORT, debug=DEBUG)

if __name__ == '__main__':
    main()

