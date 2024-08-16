import tkinter as tk
from config import load_config, save_current_config
from ui_components import create_menu, create_main_window, create_group
from event_handlers import start_drag, do_drag, on_closing, bind_right_click_to_create_group

def main():
    config = load_config()

    # Create the main window
    root = tk.Tk()
    fullscreen = tk.BooleanVar(value=config.get("fullscreen", False))
    always_on_top = tk.BooleanVar(value=config.get("always_on_top", True))
    minimize_to_tray = tk.BooleanVar(value=config.get("minimize_to_tray", False))
    last_geometry = tk.StringVar()  # Variable to store the last geometry

    create_main_window(root, config, fullscreen, always_on_top)

    root.bind("<Button-1>", start_drag)
    root.bind("<B1-Motion>", do_drag)
    create_menu(root, fullscreen, always_on_top, minimize_to_tray, last_geometry)

    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, minimize_to_tray))
    create_group_function = create_group(root)
    bind_right_click_to_create_group(root, create_group_function)

    # Save window location and size when moved or resized
    root.bind("<Configure>", lambda e: save_current_config(root))
    root.mainloop()

if __name__ == "__main__":
    main()