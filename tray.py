import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

def create_image():
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), (255, 255, 255))
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2 - 10, height // 2 - 10, width // 2 + 10, height // 2 + 10),
        fill=(0, 0, 0))
    return image

def on_quit(icon, item, root):
    icon.stop()   # Stop the tray icon
    root.quit()   # Quit the Tkinter main loop

def show_window(icon, item, root):
    icon.stop()
    root.after(0, root.deiconify)

def minimize_to_tray_function(root):
    root.withdraw()
    menu = (
        item('Show', lambda: show_window(icon, item, root)),
        item('Quit', lambda: on_quit(icon, item, root))
    )
    icon = pystray.Icon("Task Management", create_image(), "Task Management", menu)
    icon.run()