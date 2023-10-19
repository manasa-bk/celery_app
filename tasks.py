import os
import configparser
from celery import Celery

# Determine the environment (e.g., from an environment variable)
env = os.environ.get("ENV")

# Define a dictionary mapping environments to repository names
config_files = {
    "dev": "dev-config.ini",
    "qa": "qa-config.ini",
    "prod": "prod-config.ini"
}

if env in config_files:
    # Construct the path to the configuration file
    config_file_name = config_files[env]
    config_file_path = f"config/{config_file_name}"

    config = configparser.ConfigParser()
    config.read(config_file_path)

    # Use the settings from the configuration file
    broker_url = config['Celery']['broker_url']
    result_backend = config['Celery']['result_backend']
    print(broker_url)
    print(result_backend)
    # Initialize the Celery app with the retrieved settings
    app = Celery('tasks', broker=broker_url, result_backend=result_backend)

    @app.task
    def add(x, y):
        return x + y
else:
    print("Invalid or unspecified environment. Please set the 'ENV' environment variable.")
