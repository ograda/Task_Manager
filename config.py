
import json
import os
from PySide6.QtCore import Qt
from data_manager import save_groups_and_tasks, extract_groups_and_tasks
#from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout, QCheckBox

SETTINGS_FILE = "user_config.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    return {"always_on_top": False, "minimize_to_tray": False}

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file)

def save_current_settings(root, current_settings):
    settings = {
        "always_on_top": root.windowFlags() & Qt.WindowStaysOnTopHint,
        "minimize_to_tray": current_settings["minimize_to_tray"]  # Adjust this based on your logic
    }
    save_settings(settings)
    # Save the groups and tasks
    groups_data = extract_groups_and_tasks(root)
    save_groups_and_tasks(groups_data)
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