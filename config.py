import json
import os
from PySide6.QtCore import Qt
#from typing import List

SETTINGS_FILE = "user_config.json"
GROUPS_TASKS_FILE = "groups_tasks.json"
#USER_GROUP_DATA: List[GroupData] = []
USER_GROUP_DATA = []


class Task:
    def __init__(self, name, checked=False):
        self.name = name
        self.checked = checked

    def to_dict(self):
        return {
            "name": self.name,
            "checked": self.checked
        }

    @classmethod
    def from_dict(cls, data):
        return cls(name=data["name"], checked=data["checked"])

    def __repr__(self):
        return f"Task(name={self.name}, checked={self.checked})"
    
class List:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def to_dict(self):
        return {
            "name": self.name,
            "position": self.position,
            "tasks": [task.to_dict() for task in self.tasks]
        }

    @classmethod
    def from_dict(cls, data):
        # Provide default values if keys are missing
        name = data.get("name", "Unnamed List")
        position = data.get("position", 0)
        # Create the List object without tasks
        obj = cls(name=name, position=position)
        # Manually assign the tasks
        obj.tasks = [Task.from_dict(task_data) for task_data in data.get("tasks", [])]
        return obj
    
    #@classmethod
   # def from_dict(cls, data):
   #     obj = cls(name=data["name"], position=data["position"])
    #    obj.tasks = [Task.from_dict(task) for task in data["tasks"]]
      #  return obj

    def __repr__(self):
        return f"List(name={self.name}, position={self.position}, tasks={self.tasks})"
    
class Group:
    def __init__(self, group_id, name, active=False):
        self.group_id = group_id
        self.name = name
        self.active = active
        self.lists = []

    def set_active(self, active=True):
        self.active = active
    
    def update_lists(self, new_lists):
        self.lists = new_lists

    def add_list(self, list_item):
        self.lists.append(list_item)

    def to_dict(self):
        return {
            "group_id": self.group_id,
            "name": self.name,
            "active": self.active,
            "lists": [list_obj.to_dict() for list_obj in self.lists]
        }

    @classmethod
    def from_dict(cls, data):
        obj = cls(group_id=data["group_id"], name=data["name"], active=data["active"])
        obj.lists = [List.from_dict(list_obj) for list_obj in data["lists"]]
        return obj

    @classmethod
    def populate_group(cls, group_data, group_id, group_name, active=False):
        group_instance = cls(group_id=group_id, name=group_name, active=active)

        for list_data in group_data:
            list_name = list_data["group_name"]
            position = group_data.index(list_data)  # Assuming position is the index in the list
            list_instance = List(name=list_name, position=position)

            for task_data in list_data["tasks"]:
                task_instance = Task.from_dict(task_data)
                list_instance.tasks.append(task_instance)

            group_instance.add_list(list_instance)

        return group_instance

    def __repr__(self):
        return f"Group(group_id={self.group_id}, name={self.name}, active={self.active}, lists={self.lists})"
    
class UserGroupsData:
    def __init__(self):
        self.groups = []

    def add_or_update_group(self, new_group):
        # Check if the group with the same ID already exists
        for idx, group in enumerate(self.groups):
            if group.group_id == new_group.group_id:
                # Update the existing group
                self.groups[idx] = new_group
                print(f"Group {new_group.name} updated.")
                return

        # If the group doesn't exist, add it
        self.groups.append(new_group)
        print(f"Group {new_group.name} added.")


    def update_group_data(self, group_id, group_name, new_lists):
        group = self.find_group_by_id(group_id)
        if group:
            group.update_lists(new_lists)

    def set_group_inactive(self, group_id):
            group = self.find_group_by_id(group_id)
            if group:
                group.set_active(False)

    def set_group_active(self, group_id):
        group = self.get_group_by_id(group_id)
        if group:
            group.set_active(True)

    def find_group_by_id(self, group_id):
        for group in self.groups:
            if group.group_id == group_id:
                return group
        return None

    def add_group(self, group):
        self.groups.append(group)

    def get_active_group(self):
        for group in self.groups:
            if group.active:
                return group
        return None

    def to_dict(self):
        return {
            "groups": [group.to_dict() for group in self.groups]
        }

    @classmethod
    def from_dict(cls, data):
        obj = cls()
        obj.groups = [Group.from_dict(group) for group in data["groups"]]
        return obj

    def __repr__(self):
        return f"UserGroupData(groups={self.groups})"
    

    #def save_user_group_data(file_path, user_group_data):
   # with open(file_path, 'w') as file:
    #    json.dump(user_group_data.to_dict(), file, indent=4)

    #def load_user_group_data(file_path):
    #with open(file_path, 'r') as file:
   #     data = json.load(file)
   # return UserGroupData.from_dict(data)

# Example of using GroupManager
group_manager = UserGroupsData()

"""
USER_GROUP_DATA = {
    "group_id_1": {
        "name": "Group Name 1",
        "groups": {
            "subgroup_id_1": {
                "name": "Subgroup Name 1",
                "tasks": [
                    {"description": "Task 1", "checked": True},
                    {"description": "Task 2", "checked": False},
                    # More tasks...
                ]
            },
            "subgroup_id_2": {
                "name": "Subgroup Name 2",
                "tasks": [
                    {"description": "Task 3", "checked": True},
                    {"description": "Task 4", "checked": False},
                    # More tasks...
                ]
            }
            # More subgroups...
        }
    },
    "group_id_2": {
        "name": "Group Name 2",
        "groups": {
            # Subgroups similar to above...
        }
    }
    # More top-level groups...
}
"""

def fetch_group_data():
    print(USER_GROUP_DATA, flush=True)
    return USER_GROUP_DATA

"""
def swap_groups_and_tasks(old_index, new_index, current_tasks):
    # Step 1: Find the old group by its index
    old_group = group_manager.groups[old_index]

    # Step 2: Update the old group with the current tasks
    old_group.lists = [List.from_dict(task) for task in current_tasks]
    old_group.active = False  # Set the old group to inactive

    # Step 3: Find the new group by its index
    new_group = group_manager.groups[new_index]
    new_group.active = True  # Set the old group to inactive

    # Step 5: Save the updated groups back to the group manager
    group_manager.groups[old_index] = old_group
    group_manager.groups[new_index] = new_group

    return new_group.lists
"""

def swap_groups_and_tasks(old_index, new_index, current_tasks):
    # Debug: Print the indices and the current state of the groups
    print(f"Attempting to swap groups. Old index: {old_index}, New index: {new_index}", flush=True)
    
    # Assuming group_manager is available in the context
    print(f"Total groups available: {len(group_manager.groups)}",   flush=True)
    
    # Print the list of group IDs for reference
    print("Current groups in manager:", flush=True)
    for idx, group in enumerate(group_manager.groups):
        print(f"Index: {idx}, Group ID: {group.group_id}, Name: {group.name}", flush=True)

    try:
        # Retrieve the old and new groups based on the indices
        old_group = group_manager.groups[old_index]
        new_group = group_manager.groups[new_index]

        print(f"Swapping tasks from group '{old_group.name}' to group '{new_group.name}'", flush=True)

        # Update the tasks in the old group
        old_group.lists = [List.from_dict(list_data) for list_data in current_tasks]

        # Set the new group as active
        for group in group_manager.groups:
            group.active = False
        new_group.active = True

        print(f"Swapping tasks from group '{old_group.name}' to group '{new_group.name}'")
        print([list_obj.to_dict() for list_obj in new_group.lists])

        # Return the lists of the new group to be loaded in the UI
        return new_group

    except IndexError as e:
        print(f"IndexError occurred: {str(e)}. Check the indices and the list size.", flush=True)
        return None
    
# save_user_group_data('user_group_data.json', user_group_data)
def save_user_group_data(file_path, user_group_data):
    with open(file_path, 'w') as file:
        json.dump(user_group_data.to_dict(), file, indent=4)


# loaded_data = load_user_group_data('user_group_data.json')
#def load_user_group_data(file_path):
    #if not os.path.exists(file_path):
        # If the file doesn't exist, return a new UserGroupsData instance
      #  return UserGroupsData(groups=[])  # or whatever default you want
    #with open(file_path, 'r') as file:
       # return UserGroupsData.from_dict(json.load(file))
    
# In the config.py or wherever you're loading the group data
def load_user_group_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            user_group_data = UserGroupsData.from_dict(data)
            
            # Debug: Print the loaded groups
            print("Loaded groups from file:")
            for group in user_group_data.groups:
                print(f"Group ID: {group.group_id}, Name: {group.name}, Active: {group.active}")
            
            return user_group_data
    except FileNotFoundError:
        print(f"File not found: {file_path}. Starting with empty group data.")
        return UserGroupsData()  # Return an empty UserGroupsData if file not found
    except Exception as e:
        print(f"Error loading group data: {str(e)}")
        return UserGroupsData()  # Return empty if there's any error


def save_groups_and_tasks(lists_data, current_group): #export_all_groups_data
    for group_info in current_group:
        current_id = group_info["group_id"]
        current_name = group_info["name"]
        current_active = group_info["active"]

        # Check if the group already exists
        existing_group = group_manager.find_group_by_id(current_id)
        if existing_group:
            print(f"Updating existing group: {current_name}", flush=True)
            if current_active:
                # Update lists data if the group is active
                existing_group.lists = [List.from_dict(list_data) for list_data in lists_data]
            existing_group.active = current_active
        else:
            print(f"Creating new group: {current_name}", flush=True)
            # Create and add the new group
            new_group = Group(group_id=current_id, name=current_name, active=current_active)
            if current_active:
                # Populate the new group with the lists data if it's active
                new_group.lists = [List.from_dict(list_data) for list_data in lists_data]
            group_manager.add_group(new_group)

    print("groups info...", flush=True)
    print(current_group, flush=True)
    print("post print groups and tasks...", flush=True)
    
    #operation = group_manager.add_or_update_group(new_group)

    # Save the data to a file
    # Save the updated group manager to a file
    save_user_group_data('user_group_data.json', group_manager)
    print("Saving all groups and tasks...", flush=True)
    USER_GROUP_DATA = lists_data
    save_groups_file()

   # USER_GROUP_DATA = lists_data
   # print("Saving groups and tasks...", flush=True)
   # print(current_group, flush=True)
  #  print("post print groups and tasks...", flush=True)
   # save_groups_file()

def load_groups_and_tasks():
    global group_manager
    group_manager = load_user_group_data('user_group_data.json')
    print("Groups in group_manager after loading:")
    for idx, group in enumerate(group_manager.groups):
        print(f"Index: {idx}, Group ID: {group.group_id}, Name: {group.name}, Active: {group.active}")
    # Print the loaded data to verify it's the same
    print(group_manager.to_dict(), flush=True)
    USER_GROUP_DATA = load_groups_file()
    return group_manager

def save_groups_file():
    with open(GROUPS_TASKS_FILE, "w") as file:
        json.dump(USER_GROUP_DATA, file)

def load_groups_file():
    if os.path.exists(GROUPS_TASKS_FILE):
        with open(GROUPS_TASKS_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print("Warning: JSON file is empty or corrupted. Starting with an empty task list.", flush=True)
                return []  # Return an empty list if the file is empty or corrupted
    return []  # Return an empty list if the file doesn't exist


"""
def load_groups_and_tasks():
    if os.path.exists(GROUPS_TASKS_FILE):
        with open(GROUPS_TASKS_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print("Warning: JSON file is empty or corrupted. Starting with an empty task list.", flush=True)
                return []  # Return an empty list if the file is empty or corrupted
    return []  # Return an empty list if the file doesn't exist
"""

# Create default settings for our program, assuming that we don't or partially have default settings in SETTINGS_FILE
def get_default_settings():
    return {
        "always_on_top": False,
        "minimize_to_tray": False,
        "fullscreen": False,
        "window_geometry": "400x300", 
        "window_position": "100x100", 
    }

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
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            loaded_settings = json.load(file)
            settings = {**settings, **loaded_settings} # Merge loaded settings with defaults
    return settings

# Save the settings to the file
def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file)
