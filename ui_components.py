from PySide6.QtWidgets import QWidget, QMainWindow, QLabel, QPushButton, QVBoxLayout, QFrame, QMenu, QCheckBox, QInputDialog, QHBoxLayout, QComboBox
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from event_handlers import  open_calendar, on_closing, open_settings
from utils import set_window_icon
from data_manager import load_groups_and_tasks


# CREATE THE MAIN WINDOW AND DEFINE ITS PROPERTIES
def create_main_window(root, config, fullscreen, always_on_top):
    #create_custom_title_bar(root) # test custom title bar
    # Set the window title
    root.setWindowTitle(config.get("window_title", "Task Management Optimizer"))

     # Set the window icon using the utility function
    set_window_icon(root)

    # Create the central widget and layout
    central_widget = QWidget(root)
    central_layout = QVBoxLayout(central_widget)
    root.setCentralWidget(central_widget)


    # GROUP SELECT
    selection_box = QComboBox()
    selection_box.addItems(["Option 1", "Option 2", "Option 3"])
    central_layout.addWidget(selection_box, alignment=Qt.AlignCenter)


    # Add the Calendar button to the bottom left
    bottom_layout = QHBoxLayout()
    calendar_button = QPushButton("Open Calendar")
    calendar_button.clicked.connect(lambda: open_calendar(root))
    bottom_layout.addWidget(calendar_button, alignment=Qt.AlignLeft)


    # Add the Settings button to the bottom right
    settings_button = QPushButton("Settings")
    settings_button.clicked.connect(lambda: open_settings(root, config))
    bottom_layout.addWidget(settings_button, alignment=Qt.AlignRight)



   # help_button.leaveEvent = lambda event: hide_help(event, root)

    # Add the Help button next to the Settings button
    # Add the Help button next to the Settings button
    help_button = QPushButton("Help")
    bottom_layout.addWidget(help_button, alignment=Qt.AlignRight)
    help_button.setToolTip("Help information: Right-click to create or delete groups.\nWithin a group, right-click to create tasks.\nTasks have a checkbox to mark them as complete.")

    # Add the bottom layout to the central layout
    central_layout.addLayout(bottom_layout)

    # Parse the geometry string and set the window size
    geometry_str = config.get("window_geometry", "400x300")
    awidth, aheight = 400, 300
    root.setGeometry(100, 100, awidth, aheight)

  #  if fullscreen:
  #      root.showFullScreen()
 #   else:
  #      root.showNormal()

    if always_on_top:
        root.setWindowFlag(Qt.WindowStaysOnTopHint, True)

#create the custom tittle bar
def create_custom_title_bar(root):
    # Create a title bar frame
    title_bar = QFrame(root)
    title_bar.setFixedHeight(30)  # Adjust the height as needed
    title_bar.setStyleSheet("background-color: #444; color: white;")

    # Create a horizontal layout for the title bar
    title_layout = QHBoxLayout(title_bar)
    title_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

    # Add a label for the title
    title_label = QLabel("Task AAAAAAAAAA Manager", title_bar)
    title_layout.addWidget(title_label)

    # Spacer to push buttons to the right
    title_layout.addStretch()

 # Add custom buttons
    custom_button = QPushButton("Custom", title_bar)
    custom_button.setFixedSize(30, 30)  # Adjust size as needed
    custom_button.setStyleSheet("background-color: #555; border: none; color: white;")
    custom_button.clicked.connect(lambda: print("Custom button clicked"))
    title_layout.addWidget(custom_button)

    # Add minimize, maximize, and close buttons
    minimize_button = QPushButton("-", title_bar)
    minimize_button.setFixedSize(30, 30)
    minimize_button.setStyleSheet("background-color: #555; border: none; color: white;")
    minimize_button.clicked.connect(root.showMinimized)
    title_layout.addWidget(minimize_button)

    maximize_button = QPushButton("+", title_bar)
    maximize_button.setFixedSize(30, 30)
    maximize_button.setStyleSheet("background-color: #555; border: none; color: white;")
    maximize_button.clicked.connect(lambda: root.showNormal() if root.isMaximized() else root.showMaximized())
    title_layout.addWidget(maximize_button)

    close_button = QPushButton("x", title_bar)
    close_button.setFixedSize(30, 30)
    close_button.setStyleSheet("background-color: #555; border: none; color: white;")
    close_button.clicked.connect(root.close)
    title_layout.addWidget(close_button)

    # Set the custom title bar as the layout of a QWidget
    title_widget = QWidget()
    title_widget.setLayout(title_layout)
    root.setMenuWidget(title_widget)  # Use setMenuWidget to replace the title bar

def create_menu(root, fullscreen, always_on_top, minimize_to_tray, last_geometry, settings):
    menubar = root.menuBar()
    
    # Create settings menu without tearoff
    settings_menu = QMenu("Settings", menubar)
    settings_menu.addAction("Option 1")
    settings_menu.addAction("Option 2")
    menubar.addMenu(settings_menu)

    # Add right-click context menu for adding groups
    root.setContextMenuPolicy(Qt.ActionsContextMenu)
    add_group_action = QAction("Add Group", root)
    add_group_action.triggered.connect(lambda: create_group(root))
    root.addAction(add_group_action)

def create_group(root, group_name=None):
    if not group_name:
        group_name, ok = QInputDialog.getText(root, "Group Name", "Enter the group name:")
        if not ok or not group_name:
            return
    # Prompt for group name
    group_name, ok = QInputDialog.getText(root, "Group Name", "Enter the group name:")
    if ok and group_name:
        # Create a new frame for the group
        group_frame = QFrame(root.centralWidget())
        group_frame.setFrameShape(QFrame.Box)
        group_layout = QVBoxLayout(group_frame)

        # Create a label for the group
        group_label = QLabel(group_name)
        group_layout.addWidget(group_label)

        # Right-click menu for the group
        group_frame.setContextMenuPolicy(Qt.CustomContextMenu)
        group_frame.customContextMenuRequested.connect(lambda pos: show_group_menu(pos, group_frame, group_layout, root))

        # Add the group to the central widget's layout
        root.centralWidget().layout().addWidget(group_frame)

def show_group_menu(pos, group_frame, group_layout, root):
    menu = QMenu()

    add_task_action = QAction("Create Task")
    add_task_action.triggered.connect(lambda: create_task(group_layout, group_frame)) 
    menu.addAction(add_task_action)

    delete_group_action = QAction("Delete Group")
    delete_group_action.triggered.connect(lambda: delete_group(group_frame, root))
    menu.addAction(delete_group_action)

    menu.exec_(group_frame.mapToGlobal(pos))

#def add_task(group_layout, group_frame, root):
def create_task(group_layout, group_frame, task_name=None, task_checked=False):
    if not task_name:
        task_name, ok = QInputDialog.getText(None, "Task Name", "Enter the task name:")
        if not ok or not task_name:
            return
    # Prompt for task name
    task_name, ok = QInputDialog.getText(None, "Task Name", "Enter the task name:")
    if ok and task_name:
        # Create a new horizontal layout for the task
        task_layout = QHBoxLayout()  # Ensure this is a new layout every time

        # Create a checkbox and label for the task
        task_checkbox = QCheckBox()
        task_label = QLabel(task_name)

        # Connect checkbox to change label color when checked
        task_checkbox.stateChanged.connect(lambda: toggle_task_color(task_checkbox, task_label))

        # Add the checkbox and label to the task layout
        task_layout.addWidget(task_checkbox)
        task_layout.addWidget(task_label)

        # Right-click menu for the task
        task_label.setContextMenuPolicy(Qt.CustomContextMenu)
        task_label.customContextMenuRequested.connect(lambda pos: show_task_menu(pos, task_layout, group_layout, group_frame, root))

        # Add the task layout to the group
        group_layout.addLayout(task_layout)  # Add the new layout to the group

def show_task_menu(pos, task_layout, group_layout, group_frame, root):
    menu = QMenu()

    add_task_action = QAction("Add Task")
    add_task_action.triggered.connect(lambda: add_task(group_layout, group_frame, root))
    menu.addAction(add_task_action)

    remove_task_action = QAction("Remove Task")
    remove_task_action.triggered.connect(lambda: remove_task(task_layout, group_layout))
    menu.addAction(remove_task_action)

    delete_group_action = QAction("Delete Group")
    delete_group_action.triggered.connect(lambda: delete_group(group_frame, root))
    menu.addAction(delete_group_action)

    menu.exec_(task_layout.parentWidget().mapToGlobal(pos))

def delete_group(group_frame, root):
    # Remove the group frame from the main window
    root.centralWidget().layout().removeWidget(group_frame)
    group_frame.deleteLater()

def remove_task(task_layout, group_layout):
    # Remove the task layout from the group
    group_layout.removeItem(task_layout)
    for i in reversed(range(task_layout.count())):
        widget = task_layout.itemAt(i).widget()
        if widget is not None:
            widget.deleteLater()

def toggle_task_color(checkbox, label):
    if checkbox.isChecked():
        label.setStyleSheet("color: green;")
    else:
        label.setStyleSheet("") # Reset to default color

def apply_groups_and_tasks(root, groups_data):
    for group in groups_data:
        group_frame = create_group(root, group["group_name"])
        for task in group["tasks"]:
            create_task(group_frame.layout(), task["label"], task["checked"])

def apply_groups_and_tasks(root):
    groups_data = load_groups_and_tasks()
    for group in groups_data:
        group_frame = create_group(root, group["group_name"])
        for task in group["tasks"]:
            create_task(group_frame.layout(), task["label"], task["checked"])

def extract_groups_and_tasks(root):
    groups_data = []
    for group_frame in root.centralWidget().findChildren(QFrame):
        group_label = group_frame.findChild(QLabel)
        if group_label is not None:
            group_name = group_label.text()
            tasks = []
            for task_layout in group_frame.findChildren(QHBoxLayout):
                task_label = task_layout.findChild(QLabel)
                task_checkbox = task_layout.findChild(QCheckBox)
                
                if task_label is not None and task_checkbox is not None:
                    task_checked = task_checkbox.isChecked()
                    tasks.append({"label": task_label.text(), "checked": task_checked})
                
            groups_data.append({"group_name": group_name, "tasks": tasks})
    return groups_data                 

"""
def add_task(group_layout):
    # Prompt the user for a task name
    task_name, ok = QInputDialog.getText(None, "Input", "Enter task name:")
    
    if ok and task_name:
        # Create a horizontal layout for the task
        task_layout = QHBoxLayout()
        
        # Create a checkbox and label for the task
        task_checkbox = QCheckBox()
        task_label = QLabel(task_name)
        
        # Add the checkbox and label to the task layout
        task_layout.addWidget(task_checkbox)
        task_layout.addWidget(task_label)
        
        # Add the task layout to the group
        group_layout.addLayout(task_layout)

"""
"""

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

"""