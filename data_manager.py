import json
import os
from PySide6.QtWidgets import QFrame, QLabel, QCheckBox, QHBoxLayout

GROUPS_TASKS_FILE = "groups_tasks.json"

def extract_groups_and_tasks(root):
    groups_data = []
    for group_frame in root.centralWidget().findChildren(QFrame):
        group_label = group_frame.findChild(QLabel)
        if group_label is not None:
            group_name = group_label.text()
            tasks = []
            for task_layout in group_frame.findChildren(QHBoxLayout):
                task_label = task_layout.findChild(QLabel)
                task_checkbox = task_layout.findChild(QCheckBox)
                
                if task_label is not None and task_checkbox is not None:
                    task_checked = task_checkbox.isChecked()
                    tasks.append({"label": task_label.text(), "checked": task_checked})
                
            groups_data.append({"group_name": group_name, "tasks": tasks})
    return groups_data

def save_groups_and_tasks(root):
    groups_data = extract_groups_and_tasks(root)
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