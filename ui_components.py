import tkinter as tk
from tkinter import simpledialog, Menu
from event_handlers import toggle_fullscreen, show_help, hide_help, open_calendar, on_closing, open_settings

def create_main_window(root, config, fullscreen, always_on_top):
    root.title("Task Management Application")
    root.geometry(config.get("window_geometry", "400x300"))
    root.overrideredirect(True)
    root.attributes("-topmost", config.get("always_on_top", True))
    root.resizable(True, True)

def create_group(root):
    def _create_group(event=None):
        group_name = simpledialog.askstring("Input", "Enter group name:")
        if group_name:
            frame = tk.Frame(root, borderwidth=2, relief="solid")
            frame.pack(fill="x", pady=5)
            label = tk.Label(frame, text=group_name, font=("Helvetica", 14), anchor="w")
            label.pack(side="left", fill="x", expand=True)
            label.bind("<Button-3>", lambda e, f=frame: show_group_menu(root, e, f))
            frame.bind("<Button-3>", lambda e, f=frame: show_group_menu(root, e, f))

    return _create_group

def show_group_menu(root, event, frame):
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

def create_menu(root, fullscreen, always_on_top, minimize_to_tray, last_geometry):
    menubar = tk.Menu(root)
    settings_menu = tk.Menu(menubar, tearoff=0)
    settings_menu.add_command(label="Settings", command=lambda: open_settings(root, always_on_top, minimize_to_tray))
    menubar.add_cascade(label="Menu", menu=settings_menu)
    root.config(menu=menubar)

    close_button = tk.Button(root, text="Close Application", command=lambda: on_closing(root, minimize_to_tray))
    close_button.pack(pady=5)

    fullscreen_button = tk.Button(root, text="Toggle Fullscreen", command=lambda: toggle_fullscreen(root, fullscreen, last_geometry))
    fullscreen_button.pack(pady=5)

    help_button = tk.Button(root, text="Help")
    help_button.pack(pady=5)
    help_button.bind("<Enter>", lambda event: show_help(event, root))
    help_button.bind("<Leave>", hide_help)

    db_button = tk.Button(root, text="Connect to DB")
    db_button.pack(pady=5)

    calendar_button = tk.Button(root, text="Open Calendar", command=lambda: open_calendar(root))
    calendar_button.pack(side="right", padx=5, pady=5)