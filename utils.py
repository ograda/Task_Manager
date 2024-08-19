import os

def get_icon_path():
    icon_path = os.path.join('assets', 'task_manager_icon.ico') # Update this path as needed
    if os.path.exists(icon_path):
        return icon_path
    else:
        print(f"Icon file not found: {icon_path}")
        return None
  
