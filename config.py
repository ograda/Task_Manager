import json
import os
from PySide6.QtCore import Qt

SETTINGS_FILE = "user_config.json"
GROUPS_TASKS_FILE = "groups_tasks.json"

def save_groups_and_tasks(groups_data):
    with open(GROUPS_TASKS_FILE, "w") as file:
        json.dump(groups_data, file)

def load_groups_and_tasks():
    if os.path.exists(GROUPS_TASKS_FILE):
        with open(GROUPS_TASKS_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print("Warning: JSON file is empty or corrupted. Starting with an empty task list.", flush=True)
                return []  # Return an empty list if the file is empty or corrupted
    return []  # Return an empty list if the file doesn't exist

# Create default settings for our program, assuming that we don't or partially have default settings in SETTINGS_FILE
def get_default_settings():
    return {
        "always_on_top": False,
        "minimize_to_tray": False,
        "fullscreen": False,
        "window_geometry": "400x300", 
        "window_position": "100x100", 
    }

# Load the settings from the file if it exists, otherwise return the default settings
def load_settings():
    settings = get_default_settings() # Get the default settings pattern
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            loaded_settings = json.load(file)
            settings = {**settings, **loaded_settings} # Merge loaded settings with defaults
    return settings

# Save the settings to the file
def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file)


def save_current_settings(root, current_settings):
    settings = {
        "always_on_top": root.windowFlags() & Qt.WindowStaysOnTopHint, #check if the window is always on top at moment.
        "minimize_to_tray": current_settings["minimize_to_tray"],
        "fullscreen": root.isMaximized(), #check if the window is in fullscreen mode at moment.
        "window_geometry": str(root.width()) + "x" + str(root.height()), 
        "window_position": str(root.x()) + "x" + str(root.y())
    }
    save_settings(settings) # create and save settings file with the current settings.