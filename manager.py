import argparse
import logging
from PySide6.QtWidgets import QApplication
from data_handler import UserGroupsData
from config import load_settings
from ui_components import TaskManagerMainWindow, setup_main_window
from event_handlers import close_event_handler, open_calendar, open_settings, manage_add_group_data, manage_swap_group_data, manage_delete_group_data, manage_rename_group_data



################################################################################################################################################################################################
# Setup event handlers
def connect_event_handlers(root, settings, groups_data):
    root.closeEvent = lambda event: close_event_handler(event, root, settings, groups_data)

    # Connect calendar button to open the calendar
    root.bottom_toolbar.calendar_button.triggered.connect(lambda: open_calendar(root))
    # Connect settings button to open the settings
    root.bottom_toolbar.settings_button.triggered.connect(lambda: open_settings(root, settings))

    # Debug buttons for adding, loading, and deleting groups
    root.bottom_toolbar.debug_save_groups_button.triggered.connect(lambda: save_groups_and_tasks(root.central_widget.export_lists(), root.top_toolbar.group_selector.export_all_groups_data()))
    root.bottom_toolbar.debug_load_groups_button.triggered.connect(lambda: root.central_widget.import_lists(fetch_groups_data()))
    root.bottom_toolbar.debug_delete_groups_button.triggered.connect(lambda: root.central_widget.delete_all_lists())

    # Additional debug buttons for managing columns
    root.bottom_toolbar.debug_add_group_button.triggered.connect(lambda: root.central_widget.prompt_add_list())
    root.bottom_toolbar.debug_add_collumn_button.triggered.connect(lambda: root.increase_columns())
    root.bottom_toolbar.debug_remove_collumn_button.triggered.connect(lambda: root.decrease_columns())

    # Connect the group selector to the group manager
    root.top_toolbar.group_selector.currentIndexChanged.connect(lambda: manage_swap_group_data(root, groups_data))
    root.top_toolbar.group_selector.remove_group_menu.triggered.connect(lambda: manage_delete_group_data(root, groups_data))
    root.top_toolbar.group_selector.add_group_menu.triggered.connect(lambda: manage_add_group_data(root, groups_data))
    root.top_toolbar.group_selector.rename_group_menu.triggered.connect(lambda: manage_rename_group_data(root, groups_data))


################################################################################################################################################################################################
# Setup the logging configuration for DEBUG mode
def setup_logging(debug_mode):
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s \n')
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    
    # File Handler (with rotation)
    file_handler = logging.FileHandler('app.log')
    file_handler.setFormatter(log_formatter)
    
    if debug_mode:
        console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.DEBUG)
    else:
        console_handler.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
    
    # Root Logger
    logging.getLogger().setLevel(logging.DEBUG if debug_mode else logging.INFO)
    logging.getLogger().addHandler(console_handler)
    logging.getLogger().addHandler(file_handler)


################################################################################################################################################################################################
# Parse custom arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Task Manager Application")
    parser.add_argument('--debug', action='store_true', help="Run the application in debug mode")
    return parser.parse_args()


################################################################################################################################################################################################
# Main function
def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Set up logging based on debug flag
    setup_logging(args.debug) # Set up logging
    if args.debug:
        logging.debug("Starting the application in DEBUG mode")
    else:
        logging.debug("Starting the application in CONSOLE mode")       

    #app.setStyle("fusion") SKIN ?
    app = QApplication([]) #start the application and manage resources
    root = TaskManagerMainWindow() #create the main window
    groups_data = UserGroupsData()

    # Load the last saved settings and groups/tasks
    settings = load_settings()
    groups_data.load_from_file()
 
    # Create/Set up the main window
    setup_main_window(root, settings, groups_data)
    connect_event_handlers(root, settings, groups_data)

    root.show() #show the main window
    app.exec() #start the application event loop

if __name__ == "__main__":
    main()
