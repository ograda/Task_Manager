import argparse
import logging
from logging.handlers import RotatingFileHandler
from PySide6.QtWidgets import QApplication
from config import UserGroupsData, load_settings, save_groups_and_tasks, swap_groups_and_tasks, remove_group_data
from ui_components import TaskManagerMainWindow, setup_main_window
from event_handlers import close_event_handler, open_calendar, open_settings


def manage_groups_add_data(root, groups_data, group_manager):
    #removed_id, new_id = 
    groups_data.add_new_group()
   # new_lists = remove_group_data(removed_id, new_id, group_manager)
   # print(new_lists, flush=True)  
   # root.central_widget.import_lists(new_lists)

def manage_groups_delete_data(root, groups_data, group_manager):
    removed_id, new_id = groups_data.remove_selected_group()
    new_lists = remove_group_data(removed_id, new_id, group_manager)
    print(new_lists, flush=True)  
    root.central_widget.import_lists(new_lists)

def manage_groups_swap_data(root, groups_data, current_tasks, group_manager):
    old_index, new_index = groups_data.handle_group_swap()
    new_lists = swap_groups_and_tasks(old_index, new_index, current_tasks, group_manager)
    print(new_lists, flush=True)    
    root.central_widget.import_lists(new_lists)

def connect_event_handlers(root, settings, groups_data):
    # Setup event handlers
    root.closeEvent = lambda event: close_event_handler(event, root, settings, root.central_widget.export_lists(),root.top_toolbar.group_selector.export_all_groups_data())

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
    root.top_toolbar.group_selector.currentIndexChanged.connect(lambda: manage_groups_swap_data(root, root.top_toolbar.group_selector, root.central_widget.export_lists(), groups_data))
    root.top_toolbar.group_selector.remove_group_menu.triggered.connect(lambda: manage_groups_delete_data(root, root.top_toolbar.group_selector, groups_data))
    root.top_toolbar.group_selector.add_group_menu.triggered.connect(lambda: manage_groups_add_data(root, root.top_toolbar.group_selector, groups_data))

        #    remove_group.triggered.connect(self.remove_selected_group)

    def remove_selected_group(self):
        current_index = self.currentIndex()
        if current_index >= 0:
            # Get the group ID before removing
            removed_group_id = self.itemData(current_index)

            # Remove the item from the ComboBox
            self.removeItem(current_index)

            # Update the group manager to remove the group
            group_manager.remove_group(removed_group_id)

            # Adjust the indices of the remaining groups
            for i in range(current_index, self.count()):
                group_id = self.itemData(i)
                group_manager.update_group_id(group_id, i)

            # Load the new selected group (if any)
            if self.count() > 0:
                new_index = max(0, current_index - 1)
                self.setCurrentIndex(new_index)
                new_group = group_manager.groups[new_index]
                root.central_widget.import_lists(new_group.lists)
            else:
                # No groups left, clear the UI
                root.central_widget.delete_all_lists()

# Setup the logging configuration for DEBUG mode
def setup_logging(debug_mode):
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    
    # File Handler (with rotation)
    file_handler = RotatingFileHandler('app.log', maxBytes=10**6, backupCount=5)
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

# Parse custom arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Task Manager Application")
    parser.add_argument('--debug', action='store_true', help="Run the application in debug mode")
    return parser.parse_args()

# Main function
def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Set up logging based on debug flag
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Debug mode is enabled")
    setup_logging(args.debug) # Set up logging
    logging.info("Starting application")

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
