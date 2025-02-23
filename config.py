import yaml

def load_config(file_path="main.yaml"):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)

# Load the configuration from the YAML file
config_data = load_config()

# Expose the API key as a module-level variable
OPENAI_API_KEY = config_data.get("OPENAI_API_KEY")
