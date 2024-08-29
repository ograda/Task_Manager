import json
import logging
from PySide6.QtCore import Qt

SETTINGS_FILE = "user_config.json"

############################################################################################################################################################################
############################################################################################################################################################################
######################################        SAVES AND LOADS SETTINGS FOR THE WINDOW AND GROUPS AND TASKS        ##########################################################
############################################################################################################################################################################
############################################################################################################################################################################

# Create default settings for our program, assuming that we don't or partially have default settings in SETTINGS_FILE
# This is a definition function, move elsewhere?
def get_default_settings():
    return {
        "always_on_top": False,
        "minimize_to_tray": False,
        "fullscreen": False,
        "window_geometry": "400x300", 
        "window_position": "100x100", 
    }

#OGRADA should we handle this better?
# Execute the save settings function with the current settings of the window
def save_current_settings(root, current_settings):
    settings = {
        "always_on_top": root.windowFlags() & Qt.WindowStaysOnTopHint, #check if the window is always on top at moment.
        "minimize_to_tray": current_settings["minimize_to_tray"],
        "fullscreen": root.isMaximized(), #check if the window is in fullscreen mode at moment.
        "window_geometry": str(root.width()) + "x" + str(root.height()), 
        "window_position": str(root.x()) + "x" + str(root.y())
    }
    save_settings(settings) # create and save settings file with the current settings.

# Load the settings from the file if it exists, otherwise return the default settings
def load_settings():
    settings = get_default_settings() # Get the default settings pattern
    try:
        with open(SETTINGS_FILE, "r") as file:
            loaded_settings = json.load(file)
            settings = {**settings, **loaded_settings} # Merge loaded settings with defaults
            logging.debug(f"Loaded settings file successfully from {SETTINGS_FILE}.")
    except FileNotFoundError:
        logging.warning(f"File not found at: {SETTINGS_FILE}. Starting with default settings.")
    except Exception as e:
        logging.critical(f"Error loading settings data: {str(e)}")
    return settings  

# Save the settings to the file
def save_settings(settings):
    try:
        with open(SETTINGS_FILE, "w") as file:
            json.dump(settings, file)
            logging.debug(f"Settings data saved successfully to {SETTINGS_FILE}.")
    except Exception as e:
        logging.critical(f"Error saving settings: {str(e)}")