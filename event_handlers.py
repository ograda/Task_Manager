from PySide6.QtWidgets import QCalendarWidget, QLabel, QVBoxLayout, QCheckBox, QDialog, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from tray import minimize_to_tray
from config import save_current_settings, save_settings, save_groups_and_tasks

def close_event_handler(event, root, settings, groups_data):
    # Save the current settings and groups/tasks
    save_current_settings(root, settings)
    save_groups_and_tasks(groups_data)
    if settings.get("minimize_to_tray", False):
        event.ignore()
        minimize_to_tray(root)
    else:
        event.accept()

# Handle the "Always on Top" toggle
def toggle_always_on_top(root, state):
    root.setWindowFlag(Qt.WindowStaysOnTopHint, state)
    root.show()  # Necessary to apply the change  

# Handle the calendar using PySide6's QCalendarWidget instead of tkcalendar
def open_calendar(root):
    # Create a new dialog for the calendar window
    calendar_window = QDialog(root)
    calendar_window.setWindowTitle("Calendar")
    calendar_window.setGeometry(200, 200, 250, 220)

    # Create the layout for the calendar window
    layout = QVBoxLayout(calendar_window)

    # Add the calendar widget
    calendar = QCalendarWidget(calendar_window)
    layout.addWidget(calendar)

    # Add a close button
    close_button = QPushButton("Close Calendar", calendar_window)
    close_button.clicked.connect(calendar_window.close)
    layout.addWidget(close_button)

    # Set the layout and show the window
    calendar_window.setLayout(layout)
    calendar_window.exec()

# Handle the settings window
def open_settings(root, settings):
    # Create the settings dialog
    settings_window = QDialog(root)
    settings_window.setWindowTitle("Settings")
    settings_window.setGeometry(100, 100, 300, 200)

    # Create the layout for the settings window
    layout = QVBoxLayout(settings_window)

    # Create the "Always on Top" checkbox
    always_on_top_checkbox = QCheckBox("Always on Top", settings_window)
    always_on_top_checkbox.setChecked(settings.get("always_on_top", False))
    layout.addWidget(always_on_top_checkbox)

    # Create the "Minimize to Tray" checkbox
    minimize_to_tray_checkbox = QCheckBox("Minimize to Tray", settings_window)
    minimize_to_tray_checkbox.setChecked(settings.get("minimize_to_tray", False))
    layout.addWidget(minimize_to_tray_checkbox)

    # Add additional labels for more settings
    additional_label = QLabel("Additional Settings:", settings_window)
    layout.addWidget(additional_label)

    more_settings_label = QLabel("(Add more settings here)", settings_window)
    layout.addWidget(more_settings_label)

    # Create the Accept and Cancel buttons
    button_layout = QHBoxLayout()

    accept_button = QPushButton("Accept")
    cancel_button = QPushButton("Cancel")
    button_layout.addWidget(accept_button)
    button_layout.addWidget(cancel_button)

    layout.addLayout(button_layout)

    # Function to commit the changes
    def commit_changes():
        settings["always_on_top"] = always_on_top_checkbox.isChecked()
        settings["minimize_to_tray"] = minimize_to_tray_checkbox.isChecked()
        toggle_always_on_top(root, settings["always_on_top"])
        save_settings(settings)
        settings_window.accept()

    # Connect the buttons
    accept_button.clicked.connect(commit_changes)
    cancel_button.clicked.connect(settings_window.reject)

    # Set the layout and show the window
    settings_window.setLayout(layout)
    settings_window.exec()