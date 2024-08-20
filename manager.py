from PySide6.QtWidgets import QApplication
from config import load_settings
from ui_components import TaskManagerMainWindow, setup_main_window, apply_groups_and_tasks
from event_handlers import close_event_handler

def main():

    app = QApplication([]) #start the application and manage resources
    root = TaskManagerMainWindow() #create the main window

#OGRADAAAAAAAAAAAAAAAA
    # Setup event handlers should we move this  ELSEWHERE??????
    root.closeEvent = lambda event: close_event_handler(event, root, settings)

    # Load the last saved settings
    settings = load_settings()

    # Create/Set up the main window
    setup_main_window(root, settings)

    
#OGRADAAAAAAAAAAAAAAAA
    # Apply saved groups and tasks -- BUGGED
    apply_groups_and_tasks(root)

    root.show()

    app.exec()

if __name__ == "__main__":
    main()