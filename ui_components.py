from PySide6.QtWidgets import QWidget, QMainWindow, QLabel, QPushButton, QVBoxLayout, QFrame, QMenu, QCheckBox, QInputDialog, QHBoxLayout, QComboBox, QSizePolicy, QToolBar
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt,QPoint
from event_handlers import  open_calendar, on_closing, open_settings
from utils import get_icon_path
from data_manager import load_groups_and_tasks

"""  
        self.setFixedHeight(title_bar_height)  # Adjust height as needed

         # Apply style to mimic QMenuBar
        self.setStyleSheet("" "
            QWidget {
                background-color: #f0f0f0;
                border-bottom: 1px solid #cccccc;
            }
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 5px 1px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                padding: 3px 1px;
            }
        " "")

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Set the custom menu bar as the widget's layout
        self.setLayout(layout)
"""
class CustomTopMenuBar(QToolBar):
    def __init__(self, parent=None):
        super().__init__("Custom Top Menu Bar", parent)
        
        # Prevent the toolbar from being moved
        self.setMovable(False)
        
        # Style the toolbar to look like a menu bar
      #  self.setStyleSheet("""
       #     QToolBar {
      #          border: none;
       #         padding: 0px;
       #         margin: 0px;
       #     }
       # """) #background-color: #f0f0f0;

        # Add a spacer to push the group selector to the center
        spacer_left = QWidget(self)
        spacer_left.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.addWidget(spacer_left)

        # Add group selector to the toolbar (center-aligned)
        group_selector = QComboBox(self)
        group_selector.addItems(["Group 1", "Group 2", "Group 3"])
        self.addWidget(group_selector)

        # Add a spacer to push the remaining items to the right
        spacer_right = QWidget(self)
        spacer_right.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.addWidget(spacer_right)


class CustomBottomMenuBar(QToolBar):
    def __init__(self, parent=None):
        super().__init__("Custom Bottom Menu Bar", parent)

        self.setMovable(False) # Prevent the toolbar from being moved

        # Add actions to the bottom toolbar
        self.settings_button = QAction("Settings", self)
        self.addAction(self.settings_button)

        self.calendar_button = QAction("Calendar", self)
        self.addAction(self.calendar_button)

        # Add a spacer to push the next item to the right
        spacer = QWidget(self)
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.addWidget(spacer)

        # Add the help button (right-aligned)
        help_action = QAction("?", self)
        help_action.setToolTip("Help information: Right-click to create or delete groups.\nWithin a group, right-click to create tasks.\nTasks have a checkbox to mark them as complete.")
        help_action.setEnabled(False)  # Make the action unclickable
        self.addAction(help_action)      

class TaskManagerMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._drag_active = False
        self._drag_position = QPoint()
        self.setMinimumSize(400, 300)  # Set minimum window sizewidth = 400, Minimum height = 300
        self.setWindowTitle("Task Management Optimizer")  # Set the window title
        
    def set_window_icon(self, icon_path):
        self.setWindowIcon(QIcon(icon_path))

    def initUI(self, layout):
        # adding other components
        #button = QPushButton("A Button", self)
        #layout.addWidget(button)

        # Create the top toolbar
        self.top_toolbar = CustomTopMenuBar()
        self.addToolBar(Qt.TopToolBarArea, self.top_toolbar)

        # Create the bottom toolbar
        self.bottom_toolbar = CustomBottomMenuBar() 
        self.addToolBar(Qt.BottomToolBarArea, self.bottom_toolbar)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_active = True
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_active:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_active = False
            event.accept()


# CREATE THE MAIN WINDOW AND DEFINE ITS PROPERTIES
def create_main_window(root, settings):
    #configure the basic window properties
    root.set_window_icon(get_icon_path()) 
    # get the last width and height from the settings
    settings_Width, settings_Height = settings.get("window_geometry", "400x300").split("x")
    settings_PosX, settings_PosY = settings.get("window_position", "100x100").split("x")
    root.setGeometry(int(settings_PosX), int(settings_PosY), int(settings_Width), int(settings_Height))

    root.setWindowFlag(Qt.WindowStaysOnTopHint, settings.get("always_on_top")) # Set the window always on top based on settings
    if settings.get("fullscreen"): #set fullscreen if this was the last setting saved
        root.showMaximized()
    else:
        root.showNormal()

    root.setWindowFlag(Qt.WindowStaysOnTopHint, settings.get("always_on_top")) # Set the window always on top based on settings
    root.show()

    # Create the central widget
    central_widget = QWidget(root)
    central_layout = QVBoxLayout(central_widget)
    root.setCentralWidget(central_widget)

    # Additional UI components like buttons, etc.
    root.initUI(central_layout)    

    root.bottom_toolbar.calendar_button.triggered.connect(lambda: open_calendar(root))
    root.bottom_toolbar.settings_button.triggered.connect(lambda: open_settings(root, settings))


def create_menu(root):

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