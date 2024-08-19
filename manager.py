
from PySide6.QtWidgets import QApplication
from config import load_settings
from ui_components import TaskManagerMainWindow, create_menu, create_main_window, apply_groups_and_tasks
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
    create_main_window(root, settings)

    # Set up the menu -- THIS CHANGED INTO A CLASS ON UI COMPONENTS, MANAGING ONLY THE GROUP ACTIONS FOR NOW.
    create_menu(root)

    # Apply saved groups and tasks
    apply_groups_and_tasks(root)

    root.show()

    app.exec()

if __name__ == "__main__":
    main()


 #   create_main_window(root, icon_path, config, fullscreen, always_on_top)
    #root.bind("<Button-1>", start_drag)
    #root.bind("<B1-Motion>", do_drag)
  #  create_menu(root, fullscreen, always_on_top, minimize_to_tray, last_geometry)
    # Ensure taskbar icon shows correctly
    #root.after(10, lambda: root.iconify())
   # root.after(20, lambda: root.deiconify())
    # Handle closing
   # root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, minimize_to_tray))
 #   create_group_function = create_group(root)
   # bind_right_click_to_create_group(root, create_group_function)

    # Save window location and size when moved or resized
   # root.bind("<Configure>", lambda e: save_current_config(root))

 # Assuming root is your QMainWindow
   # central_widget = QWidget()  # Create a central widget
   # root.setCentralWidget(central_widget)  # Set it as the central widget of the main window

    # Create a vertical layout
   # layout = QVBoxLayout(central_widget)

    # Create a QLabel
  #  label = QLabel(text="X: 0, Y: 0")

   # Add padding by setting margins or using a wrapper layout
  #  layout.addWidget(label)
   # layout.setContentsMargins(0, 20, 0, 0)  # Top padding of 20px

    #root.bind('<Motion>', lambda event: update_coordinates(event, label))
    #root.mainloop()

