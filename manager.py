
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QMenu
from PySide6.QtCore import Qt, QPoint
import os
from config import load_settings, save_current_settings
from ui_components import create_menu, create_main_window, create_group, apply_groups_and_tasks
from event_handlers import start_drag, do_drag, on_closing, bind_right_click_to_create_group, toggle_always_on_top, close_event_handler
from data_manager import load_groups_and_tasks

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._drag_active = False
        self._drag_position = QPoint()

        # Custom title bar and other setup...
        self.create_custom_title_bar()

    def create_custom_title_bar(self):
        # Custom title bar setup (placeholder)
        pass

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_active = True
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_active:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_active = False
            event.accept()

def main():

    app = QApplication([])

    root = MyMainWindow()
    # Setup event handlers
    root.closeEvent = lambda event: close_event_handler(event, root, settings)

    # Load configuration
    settings = load_settings()

     # Apply settings
    always_on_top = settings.get("always_on_top", True)
    toggle_always_on_top(root, always_on_top)


    fullscreen = settings.get("fullscreen", False)
    minimize_to_tray = settings.get("minimize_to_tray", False)
    last_geometry = settings.get("window_geometry", "400x300")

    # Create the main window
    create_main_window(root, settings, fullscreen, always_on_top)

    # Set up the menu
    create_menu(root, fullscreen, always_on_top, minimize_to_tray, last_geometry, settings)

    # Apply saved groups and tasks
    apply_groups_and_tasks(root)

    root.show()

    app.exec()

if __name__ == "__main__":
    main()

#def main():
 #   config = load_config()
  

    # Create the main window
 #   app = QApplication([])
 #   root = QMainWindow()

  #  root = MyMainWindow()

     # load config variables, or set default values -- move this elsewhere
  #  fullscreen = config.get("fullscreen", False)
  #  always_on_top = config.get("always_on_top", True)
  #  minimize_to_tray = config.get("minimize_to_tray", False)
  # last_geometry = ""  # Variable to store the last geometry

 #   create_main_window(root, icon_path, config, fullscreen, always_on_top)
    

    #root.bind("<Button-1>", start_drag)
    #root.bind("<B1-Motion>", do_drag)
  #  create_menu(root, fullscreen, always_on_top, minimize_to_tray, last_geometry)

    # Ensure taskbar icon shows correctly
    #root.after(10, lambda: root.iconify())
   # root.after(20, lambda: root.deiconify())
    # Handle closing
   # root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, minimize_to_tray))

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

