import tkinter as tk
from tkinter import simpledialog, Menu, messagebox, Toplevel
from tkcalendar import Calendar
import json
import os
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

# Configuration file path
config_file = "user_config.json"

# Load user configuration
def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return {}

# Save user configuration
def save_config(config):
    with open(config_file, 'w') as f:
        json.dump(config, f)

# Default configuration
config = load_config()

# Create the main window
root = tk.Tk()
root.title("Task Management Application")
root.geometry(config.get("window_geometry", "400x300"))
root.overrideredirect(True)
root.attributes("-topmost", config.get("always_on_top", True))
root.resizable(True, True)

fullscreen = config.get("fullscreen", False)
always_on_top = tk.BooleanVar(value=config.get("always_on_top", True))
minimize_to_tray = tk.BooleanVar(value=config.get("minimize_to_tray", False))

x_offset = 0
y_offset = 0

def start_drag(event):
    global x_offset, y_offset
    x_offset = event.x
    y_offset = event.y

def do_drag(event):
    x = event.x_root - x_offset
    y = event.y_root - y_offset

    # Snap to screen edges if close enough
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    snap_margin = 20  # Pixels to consider for snapping
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    if abs(x) < snap_margin:
        x = 0
    elif abs(x + window_width - screen_width) < snap_margin:
        x = screen_width - window_width

    if abs(y) < snap_margin:
        y = 0
    elif abs(y + window_height - screen_height) < snap_margin:
        y = screen_height - window_height

    root.geometry(f"+{x}+{y}")

root.bind("<Button-1>", start_drag)
root.bind("<B1-Motion>", do_drag)

def on_closing():
    if minimize_to_tray.get():
        minimize_to_tray_function()
    else:
        close_application()

root.protocol("WM_DELETE_WINDOW", on_closing)

def minimize_to_tray_function():
    root.withdraw()
    menu = (item('Show', lambda: show_window(icon, item)), item('Quit', on_quit))
    icon = pystray.Icon("Task Management", create_image(), "Task Management", menu)
    icon.run()


def close_application():
    save_current_config()
    root.destroy()

def create_group(event=None):
    # Check if the right-click was outside of any group
    if event.widget == root:
        group_name = simpledialog.askstring("Input", "Enter group name:")
        if group_name:
            frame = tk.Frame(root, borderwidth=2, relief="solid")
            frame.pack(fill="x", pady=5)
            label = tk.Label(frame, text=group_name, font=("Helvetica", 14), anchor="w")
            label.pack(side="left", fill="x", expand=True)
            label.bind("<Button-3>", lambda e, f=frame: show_group_menu(e, f))
            frame.bind("<Button-3>", lambda e, f=frame: show_group_menu(e, f))

def show_group_menu(event, frame):
    group_menu = Menu(root, tearoff=0)
    group_menu.add_command(label="Add Task", command=lambda: add_task(frame))
    group_menu.add_command(label="Delete Group", command=lambda: frame.destroy())
    group_menu.post(event.x_root, event.y_root)

def add_task(frame):
    task_name = simpledialog.askstring("Input", "Enter task name:")
    if task_name:
        task_frame = tk.Frame(frame)
        task_frame.pack(fill="x", pady=2)
        var = tk.IntVar()
        checkbox = tk.Checkbutton(task_frame, text=task_name, variable=var,
                                  onvalue=1, offvalue=0,
                                  command=lambda: mark_task_complete(var, checkbox))
        checkbox.pack(side="left")

def mark_task_complete(var, checkbox):
    if var.get() == 1:
        checkbox.config(fg="green")
    else:
        checkbox.config(fg="black")

def toggle_fullscreen():
    global fullscreen
    if fullscreen:
        root.geometry("400x300")  # Restore original size
    else:
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")  # Maximize window
    fullscreen = not fullscreen

def show_help(event):
    help_label = tk.Label(root, text="Right-click to create or delete groups.\nWithin a group, right-click to create tasks.\nTasks have a checkbox to mark them as complete.", bg="yellow", relief="solid")
    help_label.place(x=event.x_root, y=event.y_root)
    event.widget.help_label = help_label

def hide_help(event):
    event.widget.help_label.destroy()

# System Tray Icon Functions
def create_image():
    # Generate an image to use as an icon for the system tray
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), (255, 255, 255))
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2 - 10, height // 2 - 10, width // 2 + 10, height // 2 + 10),
        fill=(0, 0, 0))
    return image

def on_quit(icon, item):
    icon.stop()
    root.quit()

def show_window(icon, item):
    icon.stop()
    root.after(0, root.deiconify)

def minimize_to_tray_function():
    root.withdraw()
    menu = (item('Show', show_window), item('Quit', on_quit))
    icon = pystray.Icon("Task Management", create_image(), "Task Management", menu)
    icon.run()

def toggle_always_on_top():
    root.attributes("-topmost", always_on_top.get())

def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("300x200")

    tk.Checkbutton(settings_window, text="Always on Top", variable=always_on_top,
                   command=toggle_always_on_top).pack(anchor="w", padx=20, pady=5)
    
    tk.Checkbutton(settings_window, text="Minimize to Tray", variable=minimize_to_tray).pack(anchor="w", padx=20, pady=5)

    tk.Label(settings_window, text="Additional Settings:").pack(anchor="w", padx=20, pady=10)
    
    # Placeholder for additional settings
    tk.Label(settings_window, text="(Add more settings here)").pack(anchor="w", padx=20, pady=5)

def open_calendar():
    calendar_window = Toplevel(root)
    calendar_window.title("Calendar")
    calendar_window.geometry("250x220")

    calendar = Calendar(calendar_window, selectmode="day", year=2024, month=8, day=15)
    calendar.pack(pady=20)

    close_button = tk.Button(calendar_window, text="Close Calendar", command=calendar_window.destroy)
    close_button.pack(pady=5)

def save_current_config():
    config['window_geometry'] = root.winfo_geometry()
    config['always_on_top'] = always_on_top.get()
    config['minimize_to_tray'] = minimize_to_tray.get()
    config['fullscreen'] = fullscreen
    save_config(config)

# Right-click menu to create a group
root.bind("<Button-3>", create_group)

# Menu bar
menubar = tk.Menu(root)
settings_menu = tk.Menu(menubar, tearoff=0)
settings_menu.add_command(label="Settings", command=open_settings)
menubar.add_cascade(label="Menu", menu=settings_menu)
root.config(menu=menubar)

# Close application button
close_button = tk.Button(root, text="Close Application", command=on_closing)
close_button.pack(pady=5)

# Fullscreen toggle button
fullscreen_button = tk.Button(root, text="Toggle Fullscreen", command=toggle_fullscreen)
fullscreen_button.pack(pady=5)

# Help button with hover text
help_button = tk.Button(root, text="Help")
help_button.pack(pady=5)
help_button.bind("<Enter>", show_help)
help_button.bind("<Leave>", hide_help)

# Placeholder for DB connect button
db_button = tk.Button(root, text="Connect to DB")
db_button.pack(pady=5)

# Calendar button (right side of the window)
calendar_button = tk.Button(root, text="Open Calendar", command=open_calendar)
calendar_button.pack(side="right", padx=5, pady=5)

# Bind the close button to minimize to tray if the option is enabled
def on_closing():
    if minimize_to_tray.get():
        minimize_to_tray_function()
    else:
        close_application()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Save window location and size when moved or resized
root.bind("<Configure>", lambda e: save_current_config())

root.mainloop()