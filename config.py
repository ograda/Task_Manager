
import json
import os
from PySide6.QtCore import Qt
#from data_manager import save_groups_and_tasks, extract_groups_and_tasks
#from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout, QCheckBox

SETTINGS_FILE = "user_config.json"

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

    # Save the groups and tasks
  #  groups_data = extract_groups_and_tasks(root)
   # save_groups_and_tasks(groups_data)


"""
def save_groups_and_tasks(root):
    groups_data = []
    for group_frame in root.centralWidget().findChildren(QFrame):
        group_name = group_frame.findChild(QLabel).text()
        tasks = []
        for task_layout in group_frame.findChildren(QHBoxLayout):
            task_label = task_layout.findChild(QLabel).text()
            task_checked = task_layout.findChild(QCheckBox).isChecked()
            tasks.append({"label": task_label, "checked": task_checked})
        groups_data.append({"group_name": group_name, "tasks": tasks})

    with open("groups_tasks.json", "w") as file:
        json.dump(groups_data, file)

def load_groups_and_tasks(root):
    if os.path.exists("groups_tasks.json"):
        with open("groups_tasks.json", "r") as file:
            groups_data = json.load(file)
            for group in groups_data:
                group_frame = create_group(root, group["group_name"])
                for task in group["tasks"]:
                    create_task(group_frame.layout(),group_frame, task["label"], task["checked"])

"""