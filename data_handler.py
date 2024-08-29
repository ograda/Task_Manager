import json
import uuid
import logging

GROUPS_TASKS_FILE = "user_group_data.json"

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
    def __init__(self, name, group_id=None):
        self.group_id = uuid.uuid4() if group_id is None else group_id # Generate a unique identifier if its a new group
        self.name = name
        self.lists = []
    
    def update_lists(self, lists):
        # Clear the existing lists
        self.lists = []
        
        # Convert old_lists data into List objects
        for position, list_data in enumerate(lists):
            list_name = list_data["group_name"]
            list_instance = List(name=list_name, position=position)  # Provide the position
            
            # Populate the list with tasks
            for task_data in list_data["tasks"]:
                task_instance = Task(name=task_data["name"], checked=task_data["checked"])
                list_instance.tasks.append(task_instance)
            
            self.add_list(list_instance)

    def add_list(self, list_item):
        self.lists.append(list_item)

    def to_dict(self):
        return {
            "group_id": str(self.group_id),
            "name": self.name,
            "lists": [list_obj.to_dict() for list_obj in self.lists]
        }

    @classmethod
    def from_dict(cls, data):
        obj = cls(group_id=data["group_id"], name=data["name"])
        obj.lists = [List.from_dict(list_obj) for list_obj in data["lists"]]
        return obj

    @classmethod
    def populate_group(cls, group_data, group_id, group_name):
        group_instance = cls(group_id=group_id, name=group_name)

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
        return f"Group(group_id={self.group_id}, name={self.name}, lists={self.lists})"
    

class UserGroupsData:
    def __init__(self):
        self.groups = []
        self.active_group_id = None # Track the UUID of the active group

    # Create a new group to the group manager
    def create_group(self, group_name):
        new_group = Group(name=group_name)
        self.groups.append(new_group)
        return new_group.group_id # pass the last group to be saved

    # Remove a group from the group manager
    def remove_group(self, group):
        try:
            logging.debug(f"Group {group.name} removed from the group manager.")
            self.groups.remove(group)
        except ValueError:
            logging.error(f"Group {group.name} not found in the group manager.")

    # Rename a group on the group manager
    def rename_group(self, group_id, new_name):
        group = self.find_group_by_id(group_id)
        if group:
            group.name = new_name
            logging.debug(f"Group with id '{group_id}' renamed to '{new_name}'.")

    # Set a new active group by its ID on group manager
    def set_active_group(self, group_id):
        try:
            for group in self.groups:
                if group.group_id == group_id:
                    self.active_group_id = group_id
                    logging.debug(f"Group with id '{group_id}' set active.")
        except Exception as e:
            logging.critical(f"Couldn't find a group that should be set active: {str(e)}")

    # Get the active group from the group manager uid
    def get_active_group(self):
        for group in self.groups:
            if group.group_id == self.active_group_id:
                logging.debug(f"Found a group active '{group.name}'.")
                return group
        logging.warning("Couldn't find an active group in group manager!")
        return None

    # Find a group by its UID
    def find_group_by_id(self, group_id):
        for group in self.groups:
            if group.group_id == group_id:
                logging.debug(f"Found group '{group.name}' with id '{group_id}'.")
                return group
        logging.warning(f"Couldn't find a group with id '{group_id}' in group manager!")
        return None






    """
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
    """


 




    # If we don't have any groups in the list, lets make sure we add a starting one.
    def create_initial_group(self):
        if not self.groups:
            default_group = Group(name="New Group")
            self.groups.append(default_group)
            self.set_active_group(default_group.group_id)

    # Save the group data to a file
    def save_to_file(self, file_path=GROUPS_TASKS_FILE):
        try:
            logging.debug(f"Trying to save UserGroupsData to {file_path}:\n" + self.__repr__())
            with open(file_path, 'w') as file:
                json.dump(self.to_dict(), file)
            logging.debug(f"UserGroupsData saved successfully to {file_path}.")
        except Exception as e:
            logging.critical(f"Error saving UserGroupsData: {str(e)}")

    # Convert the group manager to a dictionary for saving
    def to_dict(self):
        return {
            "groups": [group.to_dict() for group in self.groups],
             "active_group_id": str(self.active_group_id)  # Save active group UUID as a string
        }
    
    # Load groups, Lists and tasks from a file
    def load_from_file(self, file_path=GROUPS_TASKS_FILE):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.groups = [Group.from_dict(group) for group in data.get('groups', [])]
                self.active_group_id = data.get('active_group_id')
                self.set_active_group(self.active_group_id)
                logging.debug(f"UserGroupsData file successfully from {file_path}.")
        except FileNotFoundError:
            self.groups = []  # Start with an empty list of groups
            self.active_group_id = None
            logging.warning(f"File not found: {file_path}. Returning a new UserGroupsData instance.")
        except Exception as e:
            self.groups = []  # Start with an empty list of groups
            self.active_group_id = None
            logging.critical(f"Error loading UserGroupsData: {str(e)}")

    # Debug: Print the groups and tasks in the group manager by default
    def __repr__(self):
        return f"UserGroupData(groups={self.groups})"