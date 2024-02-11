import os
import yaml

def getConfig():
    # Get the absolute path to the directory of the main script
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Construct the absolute path to the config file
    config_file_path = os.path.join(script_dir, "config.yaml")
    with open(config_file_path, "r") as yaml_file:
        config = yaml.safe_load(yaml_file)

    return config