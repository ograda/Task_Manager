import os

def get_icon_path():
    icon_path = os.path.join('assets', 'task_manager_icon.ico') # Update this path as needed
    if os.path.exists(icon_path):
        return icon_path
    else:
        print(f"Icon file not found: {icon_path}")
        return None
  
def get_settings_file_path():
    settings_file = "user_config.json"
    icon_path = settings_file
    #icon_path = os.path.join('assets', 'task_manager_icon.ico') # Update this path as needed
    if os.path.exists(icon_path):
        return icon_path
    else:
        print(f"Icon file not found: {icon_path}")
        return None
  
def get_groupsdata_file_path():
    groupsdata_file = "user_group_data.json"
    icon_path = groupsdata_file
    #icon_path = os.path.join('assets', 'task_manager_icon.ico') # Update this path as needed
    if os.path.exists(icon_path):
        return icon_path
    else:
        print(f"Icon file not found: {icon_path}")
        return None
  
