from PySide6.QtWidgets import QApplication
from config import UserGroupsData, load_settings, save_groups_and_tasks, load_groups_and_tasks, swap_groups_and_tasks
from ui_components import TaskManagerMainWindow, setup_main_window
from event_handlers import close_event_handler, open_calendar, open_settings

user_groups_data = UserGroupsData()



def manage_groups_swap_data(root, groups_data, current_tasks):
    old_index, new_index = groups_data.handle_group_swap()
    new_lists = swap_groups_and_tasks(old_index, new_index, current_tasks)
    print(new_lists, flush=True)    
    root.central_widget.import_lists(new_lists)

def connect_event_handlers(root, settings):
    # Setup event handlers
    root.closeEvent = lambda event: close_event_handler(event, root, settings, root.central_widget.export_lists(),root.top_toolbar.group_selector.export_all_groups_data())

    # Connect calendar button to open the calendar
    root.bottom_toolbar.calendar_button.triggered.connect(lambda: open_calendar(root))
    # Connect settings button to open the settings
    root.bottom_toolbar.settings_button.triggered.connect(lambda: open_settings(root, settings))

    # Debug buttons for adding, loading, and deleting groups
    root.bottom_toolbar.debug_save_groups_button.triggered.connect(lambda: save_groups_and_tasks(root.central_widget.export_lists(), root.top_toolbar.group_selector.export_all_groups_data()))
    root.bottom_toolbar.debug_load_groups_button.triggered.connect(lambda: root.central_widget.import_lists(load_groups_and_tasks()))
    root.bottom_toolbar.debug_delete_groups_button.triggered.connect(lambda: root.central_widget.delete_all_lists())

    # Additional debug buttons for managing columns
    root.bottom_toolbar.debug_add_group_button.triggered.connect(lambda: root.central_widget.prompt_add_list())
    root.bottom_toolbar.debug_add_collumn_button.triggered.connect(lambda: root.increase_columns())
    root.bottom_toolbar.debug_remove_collumn_button.triggered.connect(lambda: root.decrease_columns())

    root.top_toolbar.group_selector.currentIndexChanged.connect(lambda: manage_groups_swap_data(root, root.top_toolbar.group_selector, root.central_widget.export_lists()))


def main():
    app = QApplication([]) #start the application and manage resources
    #app.setStyle("fusion")
    root = TaskManagerMainWindow() #create the main window

    # Load the last saved settings and groups/tasks
    settings = load_settings()
    groups_data = load_groups_and_tasks()
 
    # Create/Set up the main window
    setup_main_window(root, settings, groups_data)
    connect_event_handlers(root, settings)

    root.show() #show the main window
    app.exec() #start the application event loop


if __name__ == "__main__":
    main()
