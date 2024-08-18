from PySide6.QtWidgets import QWidget, QMainWindow, QLabel, QPushButton, QVBoxLayout, QFrame, QMenu, QCheckBox, QInputDialog
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from event_handlers import toggle_fullscreen, show_help, hide_help, open_calendar, on_closing, open_settings

 # CREATE THE MAIN WINDOW AND DEFINE ITS PROPERTIES
def create_main_window(root, icon_path, config, fullscreen, always_on_top):
    #set the parent tittle and icon 
  #  parent.title("Task Management Optimizer")  # Set the title of the window
   # parent.iconbitmap(icon_path)  # Set your application icon

    # Set the main window details
    # root.setWindowFlag(Qt.FramelessWindowHint)  # Handled by default in PySide6 # Remove window default decorations
    # root.wm_attributes("-topmost", 1)
    # root.setWindowFlag(Qt.FramelessWindowHint)  # Handled by default in PySide6
   # root.wm_state("normal")

    root.setWindowIcon(QIcon(icon_path))  # Set your custom icon path here  # Set your custom icon path here
    root.setWindowTitle("Task Management Optimizer")  # Set the title of the window

   # root.resizable(True, True)  # Allow resizing of the window
    # root.wm_attributes("-toolwindow", False) # Ensure it shows up in the taskbar

   # geometry_str = config.get("window_geometry", "400x300")
    awidth, aheight = 400,300
    root.setGeometry(100, 100, awidth, aheight)  # Example using default x=100, y=100
   # create_custom_title_bar(root) #create a custom title bar

#    root.attributes("-topmost", config.get("always_on_top", True))


#def create_custom_title_bar(root):
 #   root.title_bar = QFrame(root, bg='gray', relief='raised', bd=2)
 #   root.title_bar.setLayout(side='top', fill='x')

 ##   title_label = QLabel(root.title_bar, text=root.setWindowTitle(), bg='gray')
 #   title_label.setLayout(side='left', padx=5)

  #  close_button = QPushButton(root.title_bar, text='X', command=root.destroy)
 #   close_button.setLayout(side='right', padx=5)


def create_group(root):
    def _create_group(event=None):
        group_name = QInputDialog.getText("Input", "Enter group name:")
        if group_name:
            frame = QFrame(root, borderwidth=2, relief="solid")
            frame.setLayout(fill="x", pady=5)
            label = QLabel(frame, text=group_name, font=("Helvetica", 14), anchor="w")
            label.setLayout(side="left", fill="x", expand=True)
            label.bind("<Button-3>", lambda e, f=frame: show_group_menu(root, e, f))
            frame.bind("<Button-3>", lambda e, f=frame: show_group_menu(root, e, f))

    return _create_group

def show_group_menu(root, event, frame):
    group_menu = Menu(root, tearoff=0)
    group_menu.add_command(label="Add Task", command=lambda: add_task(frame))
    group_menu.add_command(label="Delete Group", command=lambda: frame.destroy())
    group_menu.post(event.x_root, event.y_root)

def add_task(frame):
    task_name = QInputDialog.getText("Input", "Enter task name:")
    if task_name:
        task_frame = QFrame(frame)
        task_frame.setLayout(fill="x", pady=2)
        var = int
        checkbox = QCheckBox(task_frame, text=task_name, variable=var,
                                  onvalue=1, offvalue=0,
                                  command=lambda: mark_task_complete(var, checkbox))
        checkbox.setLayout(side="left")

def mark_task_complete(var, checkbox):
    if var.get() == 1:
        checkbox.config(fg="green")
    else:
        checkbox.config(fg="black")   

def create_menu(root, fullscreen, always_on_top, minimize_to_tray, last_geometry):
    menubar = QMenu(root)

  #  title_bar = QFrame(root, bg='gray', relief='raised', bd=2)
 #   title_bar.setLayout(side='top', fill='x')

    settings_menu = QMenu("Settings", menubar)

    # Add actions or submenus to settings_menu
    settings_menu.addAction("Option 1")
    settings_menu.addAction("Option 2")
    #settings_menu.add_command(label="Settings", command=lambda: open_settings(root, always_on_top, minimize_to_tray))
    #menubar.add_cascade(label="Menu", menu=settings_menu)
    #root.config(menu=menubar)

   # close_button = QPushButton(root, text="Close Application", command=lambda: on_closing(root, minimize_to_tray))
   # close_button.setLayout(pady=5)

  #  fullscreen_button = QPushButton(root, text="Toggle Fullscreen", command=lambda: toggle_fullscreen(root, fullscreen, last_geometry))
  #  fullscreen_button.setLayout(pady=5)

    help_button = QPushButton(root, text="Help")
  #  help_button.setLayout(pady=5)
   # help_button.bind("<Enter>", lambda event: show_help(event, root))
  #  help_button.bind("<Leave>", hide_help)

    db_button = QPushButton(root, text="Connect to DB")
  #  db_button.setLayout(pady=5)

    # Create a QPushButton and connect its clicked signal to the desired function
    calendar_button = QPushButton("Open Calendar", root)
    calendar_button.clicked.connect(lambda: open_calendar(root))
  #  calendar_button.setLayout(side="right", padx=5, pady=5)
    # Add the button to the layout or menu
    root.layout().addWidget(calendar_button)
