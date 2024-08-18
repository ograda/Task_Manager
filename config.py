import json
import os

config_file = "user_config.json"

def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(config_file, 'w') as f:
        json.dump(config, f)

def save_current_config(root):
    config = {
        'window_geometry': root.geometry(),
        'always_on_top': root.windowFlags() & Qt.WindowStaysOnTopHint,
        'minimize_to_tray': False,  # Example; adjust as needed
        'fullscreen': False,  # Example; adjust as needed
    }
    save_config(config)