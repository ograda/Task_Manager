import tkinter as tk

# Create the main window
root = tk.Tk()

# Set the window title
root.title("Task Management Application")

# Set the window size
root.geometry("400x300")  # Width x Height

# Remove the title bar and window decorations
root.overrideredirect(True)

# Make the window an overlay (always on top)
root.attributes("-topmost", True)

# Variables to store mouse position
x_offset = 0
y_offset = 0

# Function to update window position on mouse drag
def start_drag(event):
    global x_offset, y_offset
    x_offset = event.x
    y_offset = event.y

def do_drag(event):
    x = event.x_root - x_offset
    y = event.y_root - y_offset
    root.geometry(f"+{x}+{y}")

# Bind the mouse events to the window
root.bind("<Button-1>", start_drag)
root.bind("<B1-Motion>", do_drag)

# Create a function to close the application
def close_application():
    root.destroy()

# Create a "Close Application" button
close_button = tk.Button(root, text="Close Application", command=close_application)
close_button.pack(pady=20)  # Add some padding

# Run the application
root.mainloop()