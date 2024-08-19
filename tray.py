
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QAction, QIcon
from utils import get_icon_path

def minimize_to_tray(root):
    # Create tray icon
    tray_icon = QSystemTrayIcon(root)
    tray_icon.setIcon(QIcon(get_icon_path()))
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

    tray_icon.activated.connect(lambda reason: on_tray_icon_activated(reason, root, tray_icon))

    root.hide()

# restore the window from the tray icon on double click
def on_tray_icon_activated(reason, root, tray_icon):
    if reason == QSystemTrayIcon.DoubleClick:
        restore_from_tray(root, tray_icon)

# restore the window and hide the tray icon
def restore_from_tray(root, tray_icon):
    tray_icon.hide()
    root.show()
    
#def close_event_handler(event, root, settings):
 #   if settings.get("minimize_to_tray", False):
 #       event.ignore()
 #       minimize_to_tray(root)
 #   else:
 #       event.accept()