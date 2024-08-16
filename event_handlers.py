import tkinter as tk
from tray import minimize_to_tray_function
from config import save_current_config
from tkcalendar import Calendar

x_offset = 0
y_offset = 0

def start_drag(event):
    global x_offset, y_offset
    x_offset = event.x
    y_offset = event.y

def do_drag(event):
    widget = event.widget
    if isinstance(widget, tk.Tk):  # Ensure we're only trying to move the main window
        x = event.x_root - x_offset
        y = event.y_root - y_offset

        # Snap to screen edges if close enough
        screen_width = widget.winfo_screenwidth()
        screen_height = widget.winfo_screenheight()

        snap_margin = 20  # Pixels to consider for snapping
        window_width = widget.winfo_width()
        window_height = widget.winfo_height()

        if abs(x) < snap_margin:
            x = 0
        elif abs(x + window_width - screen_width) < snap_margin:
            x = screen_width - window_width

        if abs(y) < snap_margin:
            y = 0
        elif abs(y + window_height - screen_height) < snap_margin:
            y = screen_height - window_height

        widget.geometry(f"+{x}+{y}")

def bind_right_click_to_create_group(root, create_group_function):
    root.bind("<Button-3>", create_group_function)       

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

    tk.Checkbutton(settings_window, text="Always on Top", variable=always_on_top,
                   command=lambda: toggle_always_on_top(root, always_on_top)).pack(anchor="w", padx=20, pady=5)
    
    tk.Checkbutton(settings_window, text="Minimize to Tray", variable=minimize_to_tray).pack(anchor="w", padx=20, pady=5)

    tk.Label(settings_window, text="Additional Settings:").pack(anchor="w", padx=20, pady=10)
    
    tk.Label(settings_window, text="(Add more settings here)").pack(anchor="w", padx=20, pady=5)

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