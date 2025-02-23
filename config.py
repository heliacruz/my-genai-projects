import os
import yaml

def load_config(file_path=None):
    if file_path is None:
        # Build the path to main.yaml relative to this file's location.
        file_path = os.path.join(os.path.dirname(__file__), "main.yaml")
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Configuration file not found at {file_path}") from e

# Load the configuration from the YAML file
config_data = load_config()

# Expose the API key as a module-level variable
OPENAI_API_KEY = config_data.get("OPENAI_API_KEY")
