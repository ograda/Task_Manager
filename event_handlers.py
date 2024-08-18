
from PySide6.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QLabel, QVBoxLayout, QCheckBox, QDialog, QPushButton, QHBoxLayout
from PySide6.QtGui import QAction
from tray import minimize_to_tray
from config import save_current_settings, save_settings
import ctypes
from screeninfo import get_monitors
from PySide6.QtCore import Qt, QPoint
from data_manager import save_groups_and_tasks

x_offset = 0
y_offset = 0

# Handle window closing event
def on_closing(root):
    #save_current_settings(root)
    minimize_to_tray(root)
    QApplication.quit()

# Handle window closing event
def close_event_handler(event, root, settings):
    # Save the current settings and groups/tasks
    save_current_settings(root, settings)
    save_groups_and_tasks(root)
    if settings.get("minimize_to_tray", False):
        event.ignore()
        minimize_to_tray(root, settings)
    else:
        event.accept()    

def toggle_always_on_top(root, state):
    root.setWindowFlag(Qt.WindowStaysOnTopHint, state)
    root.show()  # Necessary to apply the change  

# Get the monitor containing the window
def get_monitor_containing_window(x, y):
    monitors = get_monitors()
    for monitor in monitors:
        if (monitor.x <= x <= monitor.x + monitor.width) and (monitor.y <= y <= monitor.y + monitor.height):
            return monitor
    return monitors[0]  # Default to the first monitor if none are found


# Get the taskbar height
def get_taskbar_height():
    user32 = ctypes.windll.user32
    work_area = ctypes.wintypes.RECT()
    user32.SystemParametersInfoW(0x0030, 0, ctypes.byref(work_area), 0)
    return user32.GetSystemMetrics(1) - work_area.bottom


# Start dragging any part of the window
def start_drag(event):
    global x_offset, y_offset
    x_offset = event.x()
    y_offset = event.y()


# Execute the dragging
def do_drag(root, event):
    if event.buttons() & Qt.LeftButton:
        root.move(event.globalPosition().toPoint() - QPoint(x_offset, y_offset))


# Bind right-click to create group
def bind_right_click_to_create_group(root, create_group_function):
    root.setContextMenuPolicy(Qt.ActionsContextMenu)
    action = QAction("Add Group", root)
    action.triggered.connect(lambda: create_group_function(root))
    root.addAction(action)


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



"""
def show_help(event, root):
    help_text = "Help information: Right-click to create or delete groups.\nWithin a group, right-click to create tasks.\nTasks have a checkbox to mark them as complete."
    help_label = QLabel(help_text, root)
    help_label.setStyleSheet("background-color: yellow; color: black; border: 1px solid black;")
    help_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
    help_label.setFixedSize(300, 100)
    
    # Position the label near the mouse position with a small offset
    x = event.globalPosition().x() + 10
    y = event.globalPosition().y() + 10
    help_label.move(x, y)

    help_label.show()
    root.help_label = help_label  # Store the label in the root object


def hide_help(event):
    root = event.widget().parent()  # Get the parent widget (root) from the event
    if hasattr(root, 'help_label'):
        root.help_label.deleteLater()
        del root.help_label

from PySide6.QtWidgets import QApplication, QMainWindow
from tray import minimize_to_tray_function
from config import save_current_config
from tkcalendar import Calendar
import ctypes
from screeninfo import get_monitors

x_offset = 0
y_offset = 0

#get the monitor containing the window
def get_monitor_containing_window(x, y):
    monitors = get_monitors()
    for monitor in monitors:
        if (monitor.x <= x <= monitor.x + monitor.width) and (monitor.y <= y <= monitor.y + monitor.height):
            return monitor
    return monitors[0]  # Default to the first monitor if none are found

#get the taskbar height
def get_taskbar_height():
    user32 = ctypes.windll.user32
    work_area = ctypes.wintypes.RECT()
    user32.SystemParametersInfoW(0x0030, 0, ctypes.byref(work_area), 0)
    return user32.GetSystemMetrics(1) - work_area.bottom

#start dragging an part of the window
def start_drag(event):
    global x_offset, y_offset
    x_offset = event.x
    y_offset = event.y

#execute the drag
def do_drag(event):
    #widget = event.widget
    widget = event.widget.winfo_toplevel()
    #check if the widget is the main window
    if isinstance(widget, tk.Tk): 
        x = event.x_root - x_offset
        y = event.y_root - y_offset

        # get the window width and height and taskbar height
        window_width = widget.winfo_width()
        window_height = widget.winfo_height()
        taskbar_height = get_taskbar_height()

        #get monitor information and set the snap margin and offset
        monitor = get_monitor_containing_window(x, y)
        snap_margin = 50  # Pixels to consider for snapping

        # Snap to screen edges if close enough
        if abs(x - monitor.x) < snap_margin: # Snap LEFT (WIDTH--)
            x = monitor.x

        if abs((x + window_width) - (monitor.x + monitor.width)) < snap_margin: # Snap RIGHT (WIDTH++)
            x = (monitor.x + monitor.width) - window_width

        if abs(y - monitor.y) < snap_margin: # Snap TOP (HEIGHT--)
            y = monitor.y
        
        if abs((y + window_height) - (monitor.y + monitor.height - taskbar_height)) < snap_margin: # Snap BOTTOM (HEIGHT++) - some offset needed?
            y = (monitor.y + monitor.height) - window_height - taskbar_height

        widget.geometry(f"+{x}+{y}")


def on_closing(root, minimize_to_tray):
    if minimize_to_tray.get():
        minimize_to_tray_function(root)
    else:
        save_current_config(root)
        root.destroy()

def open_settings(root, always_on_top, minimize_to_tray):
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("300x200")

 #   tk.Checkbutton(settings_window, text="Always on Top", variable=always_on_top,
 #                  command=lambda: toggle_always_on_top(root, always_on_top)).pack(anchor="w", padx=20, pady=5)
    
#    tk.Checkbutton(settings_window, text="Minimize to Tray", variable=minimize_to_tray).pack(anchor="w", padx=20, pady=5)

 #   tk.Label(settings_window, text="Additional Settings:").pack(anchor="w", padx=20, pady=10)
    
  #  tk.Label(settings_window, text="(Add more settings here)").pack(anchor="w", padx=20, pady=5)

def toggle_fullscreen(root, fullscreen, last_geometry):
    if fullscreen.get():
        # Exiting fullscreen
        root.overrideredirect(False)  # Restore window decorations
        root.geometry(last_geometry.get())  # Restore the original position and size
        root.overrideredirect(True)  # Remove window decorations again
    else:
        # Entering fullscreen
        last_geometry.set(root.winfo_geometry())  # Save the current geometry
        root.overrideredirect(True)  # Remove window decorations
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")  # Maximize window

    fullscreen.set(not fullscreen.get())  # Toggle the fullscreen state

def show_help(event, root):
    help_text = "Help information: Right-click to create or delete groups.\nWithin a group, right-click to create tasks.\nTasks have a checkbox to mark them as complete."
    help_label = tk.Label(root, text=help_text, bg="yellow", fg="black", relief="solid", width=50, height=5)

    # Position the label at the mouse position with a small offset
    x = event.x_root - root.winfo_rootx() + 10  # Offset to avoid covering the cursor
    y = event.y_root - root.winfo_rooty() + 10
    help_label.place(x=x, y=y)

    event.widget.help_label = help_label

def hide_help(event):
    # Destroy the help label if it exists
    if hasattr(event.widget, 'help_label'):
        event.widget.help_label.destroy()
        del event.widget.help_label  # Clean up the attribute

def open_calendar(root):
    calendar_window = tk.Toplevel(root)
    calendar_window.title("Calendar")
    calendar_window.geometry("250x220")

    calendar = Calendar(calendar_window, selectmode="day")
    calendar.pack(pady=20)

    close_button = tk.Button(calendar_window, text="Close Calendar", command=calendar_window.destroy)
    close_button.pack(pady=5)

def toggle_always_on_top(root, always_on_top):
    root.attributes("-topmost", always_on_top.get())

def close_application(root):
    save_current_config(root)
    root.destroy()

    """	