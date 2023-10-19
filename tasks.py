import os
import requests
import configparser

# Define the GitHub base URL for your configuration repositories
GITHUB_BASE_URL = "https://github.com/manasa-bk/celery_app"

# Determine the environment (e.g., from an environment variable)
env = os.environ.get("ENV")

# Define a dictionary mapping environments to repository names
repos = {
    "dev": "dev-config",
    "qa": "qa-config",
    "prod": "prod-config"
}

# Check if the specified environment is valid
if env in repos:
    # Construct the URL for the configuration file
    repo_name = repos[env]
    repo_url = f"{GITHUB_BASE_URL}/{repo_name}/blob/main/config.ini"
    print(f"Fetching configuration file from: {repo_url}")


    # Fetch the configuration file
    response = requests.get(repo_url)
    print(response.text)
    if response.status_code == 200:
        # Read the configuration file
        config = configparser.ConfigParser()
        config.read_string(response.text)

        # Use the settings from the configuration file
        broker_url = config['Celery']['broker_url']
        result_backend = config['Celery']['result_backend']

        # Initialize the Celery app with the retrieved settings
        app = Celery('tasks', broker=broker_url, result_backend=result_backend)

        @app.task
        def add(x, y):
            return x + y
    else:
        print("Failed to fetch the configuration file.")
else:
    print("Invalid or unspecified environment. Please set the 'ENV' environment variable.")
