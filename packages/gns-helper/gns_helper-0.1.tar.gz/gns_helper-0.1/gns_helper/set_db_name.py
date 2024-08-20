import os
import yaml

config_data = None

def load_config(dir):
    global config_data

    config_file_path = os.path.join(dir, 'config', 'database.yml')
    print("config_file_path",config_file_path)    
    with open(config_file_path, 'r') as f:
        config_data = yaml.safe_load(f)

def get_config():
    print(config_data)
    if config_data is None:
        raise RuntimeError("Configuration not loaded. Call load_config() first.")
    return config_data