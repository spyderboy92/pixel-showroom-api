import yaml
import os
from flask import Flask
from app.config.swagger_config import create_api

# Initialize Flask app
app = Flask(__name__)


def load_env_config():
    """
    Load configuration values from app-base.yml and app-{env}.yml
    and apply them to the Flask app.
    """
    config_path = os.path.join(os.path.dirname(
        __file__), '..', 'config', 'app-base.yml')  # Assuming base.ml is in the same directory

    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Configuration file '{config_path}' not found.")

    with open(config_path, 'r') as f:
        config_data = yaml.safe_load(f)  # Load the YAML file as a dictionary

    # Apply the configurations to the Flask app (or app config)
    for key, value in config_data.items():
        app.config[key] = value


load_env_config()

# Create and configure the API
api = create_api(app)

if __name__ == "__main__":
    app.run()
