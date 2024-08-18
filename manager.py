from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QPoint
import os
from config import load_config, save_current_config
from ui_components import create_menu, create_main_window, create_group
from event_handlers import start_drag, do_drag, on_closing, bind_right_click_to_create_group

def update_coordinates(event, label):
    x = event.x_root
    y = event.y_root
    label.config(text=f"X: {x}, Y: {y}")


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._drag_active = False
        self._drag_position = QPoint()

        # Custom title bar and other setup...
        self.create_custom_title_bar()

    def create_custom_title_bar(self):
        # Code to create custom title bar...
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
    config = load_config()
    icon_path = os.path.join('assets', 'task_manager_icon.ico')  # Adjust the path as needed

    # Create the main window
    app = QApplication([])
    root = QMainWindow()

    root = MyMainWindow()

     # load config variables, or set default values -- move this elsewhere
    fullscreen = config.get("fullscreen", False)
    always_on_top = config.get("always_on_top", True)
    minimize_to_tray = config.get("minimize_to_tray", False)
    last_geometry = ""  # Variable to store the last geometry

    create_main_window(root, icon_path, config, fullscreen, always_on_top)
    

    #root.bind("<Button-1>", start_drag)
    #root.bind("<B1-Motion>", do_drag)
    create_menu(root, fullscreen, always_on_top, minimize_to_tray, last_geometry)

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
    central_widget = QWidget()  # Create a central widget
    root.setCentralWidget(central_widget)  # Set it as the central widget of the main window

    # Create a vertical layout
    layout = QVBoxLayout(central_widget)

    # Create a QLabel
    label = QLabel(text="X: 0, Y: 0")

   # Add padding by setting margins or using a wrapper layout
    layout.addWidget(label)
    layout.setContentsMargins(0, 20, 0, 0)  # Top padding of 20px

    #root.bind('<Motion>', lambda event: update_coordinates(event, label))

    root.show()
    app.exec()
    #root.mainloop()

if __name__ == "__main__":
    main()