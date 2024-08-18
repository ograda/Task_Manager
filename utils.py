import os
from PySide6.QtGui import QIcon

def set_window_icon(root):
    icon_path = os.path.join('assets', 'task_manager_icon.ico') # Update this path as needed
    if os.path.exists(icon_path):
        # Set the window icon
        root.setWindowIcon(QIcon(icon_path))
    else:
        print(f"Icon file not found: {icon_path}")
  
