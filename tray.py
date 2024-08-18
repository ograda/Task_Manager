
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QAction, QIcon
import os

def create_tray_icon(root):
    # Create the system tray icon
    tray_icon = QSystemTrayIcon(QIcon("path/to/icon.png"), root)  # Update the icon path as needed

    # Create the context menu for the tray icon
    tray_menu = QMenu()

    # Add actions to the context menu
    show_action = QAction("Show", root)
    show_action.triggered.connect(lambda: show_window(root))
    tray_menu.addAction(show_action)

    quit_action = QAction("Quit", root)
    quit_action.triggered.connect(lambda: on_quit(root))
    tray_menu.addAction(quit_action)

    tray_icon.setContextMenu(tray_menu)
    tray_icon.show()

    return tray_icon

def on_quit(root):
    # Quit the application
    root.close()
    QApplication.quit()

def show_window(root):
    # Show the main window
    root.showNormal()
    root.activateWindow()

#def minimize_to_tray_function(root, tray_icon):
    # Minimize the window to the tray
  #  root.hide()
  #  tray_icon.showMessage("Task Management", "Application minimized to tray", QSystemTrayIcon.Information, 2000)

def minimize_to_tray(root, settings):
    icon_path = os.path.join('assets', 'task_manager_icon.ico') # Update this path as needed
    tray_icon = QSystemTrayIcon(root)
    if os.path.exists(icon_path):
        tray_icon.setIcon(QIcon(icon_path))
    else:
        print(f"Warning: Icon file not found at {icon_path}", flush=True)
    tray_icon.setToolTip("Task Manager ograda")

    # Create the context menu for the tray icon
    tray_menu = QMenu()

    restore_action = QAction("Restore", root)
    restore_action.triggered.connect(lambda: restore_from_tray(root, tray_icon))
    tray_menu.addAction(restore_action)

    quit_action = QAction("Quit", root)
    quit_action.triggered.connect(lambda: QApplication.instance().quit())
    tray_menu.addAction(quit_action)

    tray_icon.setContextMenu(tray_menu)
    tray_icon.show()

    root.hide()

def restore_from_tray(root, tray_icon):
    root.show()
    tray_icon.hide()

def close_event_handler(event, root, settings):
    if settings.get("minimize_to_tray", False):
        event.ignore()
        minimize_to_tray(root, settings)
    else:
        event.accept()