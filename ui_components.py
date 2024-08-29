from PySide6.QtWidgets import QWidget, QScrollArea, QMainWindow, QApplication, QLabel, QVBoxLayout, QFrame, QMenu, QCheckBox, QInputDialog, QHBoxLayout, QComboBox, QSizePolicy, QGridLayout, QToolBar, QStyle, QStyleOptionComboBox
from PySide6.QtGui import QAction, QIcon, QLinearGradient, QPainter, QColor, QDrag, QDropEvent, QCursor, QDragMoveEvent
from PySide6.QtCore import Qt,QPoint, QMimeData, QSize, QEvent
from utils import get_icon_path
import uuid
import logging

# Define the task widget and its properties
class TaskWidget(QFrame):
    def __init__(self, task_name, uid, checked, parent=None):
        super().__init__(parent)
        self.uid = uid # Store the unique ID
        self.setObjectName(self.uid)  # Set the object name to the UID
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed) # expanding width to fit the container and Fixed height to make the pattern of task with a minimum height

        # Create the task container for the checkbox and label
        layout = QHBoxLayout(self)
        layout.setContentsMargins(1, 5, 1, 5)   # Left, Top, Right, Bottom margins
        layout.setSpacing(0)  # Add some spacing between the checkbox and the label
        # Apply the border and background to the entire QFrame
        self.setStyleSheet("""
            QFrame {
                border: 1px solid #4DD0E1;  /* Border color */
                background-color: #FFFFFF;  /* Background color */
            }
        """)

        # Create the checkbox
        self.checkbox = QCheckBox(self)
        self.checkbox.setChecked(checked)
        self.checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border: 2px solid #2E7D32;
            }
            QCheckBox::indicator:unchecked {
                background-color: #f0f0f0;
                border: 2px solid #ccc;
            }
        """)

        # Create the label for the task text
        self.label = QLabel(task_name, self)
        self.label.setWordWrap(True)  # Enable text wrapping
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed) # the height should be fixed even tough it is expanding with the text in order to prevent expanding with resize
        self.label.setStyleSheet("""
        QLabel {
            font-weight: bold;  /* Set the text to bold */
            font-size: 12px;    /* Increase the font size */
        }
            background-color: #E0F7FA;  /* Light blue background */
            padding: 5px;               /* Padding around the text */
            border: 1px solid #4DD0E1;  /* Border color */
            color: red;               /* White text color */ 
        """)

        # Add the checkbox and label to the layout block
        layout.addWidget(self.checkbox)
        layout.addWidget(self.label)

    """
    # Manage the drag move event
    def dragMoveEvent(self, event: QDragMoveEvent):
        pos = event.position().toPoint()
        target_widget = self.childAt(pos)

        # Traverse up the widget hierarchy to find the TaskWidget
        print("LOOKING FOR FATHER", flush=True)
        while target_widget is not None and not isinstance(target_widget, TaskWidget):
            print(f"Currently checking widget: {target_widget}, parent: {target_widget.parentWidget()}", flush=True)
            target_widget = target_widget.parentWidget()
        print("ENDED", flush=True)
        if isinstance(target_widget, TaskWidget):
            event.acceptProposedAction()  # Show "permitted" cursor
        else:
            event.ignore()  # Show "blocked" cursor
    """ 
      
    # Enable dragging for the task widget
    def mousePressEvent(self, event):
        #print("TASK_WIDGET entering event", flush=True)
        #if event.button() == Qt.RightButton:
            # Trigger the parent context menu for this task
           # self.parentWidget().parentWidget().show_context_menu(event.pos())
        if event.button() == Qt.LeftButton:
         #   print("TASK_WIDGET event button left", flush=True)
            drag = QDrag(self)
            mime_data = QMimeData()

            # Store the widget's UID in the mime data
            mime_data.setText(self.uid)
            drag.setMimeData(mime_data)

            # Create a visual representation for dragging
            pixmap = self.grab()  # Grabs an image of the widget
            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos())  # Adjust hotspot to the click position
            drag.exec(Qt.MoveAction)
        else:
        #    print("TASK_WIDGET event button ELSE", flush=True)
            super().mousePressEvent(event)

# Container for the tasks (TaskWidget)
class TaskContainer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.task_layout = QVBoxLayout(self)
        self.task_layout.setContentsMargins(8, 5, 1, 5)   # Left, Top, Right, Bottom margins
        self.task_layout.setAlignment(Qt.AlignTop)  # Align tasks to the top
        self.setContextMenuPolicy(Qt.CustomContextMenu) # Define a custom context menu
        self.customContextMenuRequested.connect(self.show_context_menu) # Connect the context menu to the function

    # Show the context menu for adding or deleting tasks when clicking inside the task container
    def show_context_menu(self, pos: QPoint):
        # Find the widget that was clicked
        clicked_widget = self.childAt(pos)
        while clicked_widget is not None and not isinstance(clicked_widget, TaskWidget):
            # print(f"Currently checking widget: {clicked_widget}, parent: {clicked_widget.parentWidget()}")
            clicked_widget = clicked_widget.parentWidget()
        
        #create the menu and add task button if clicked inside the the task container
        menu = QMenu(self)
        add_task_action = QAction("Add Task", self)
        add_task_action.triggered.connect(lambda: self.prompt_add_task())
        menu.addAction(add_task_action)

        #create remove button if clicked on a task
        if isinstance(clicked_widget, TaskWidget):
            delete_task_action = QAction("Delete Task", self)
            delete_task_action.triggered.connect(lambda: self.delete_task(clicked_widget))
            menu.addAction(delete_task_action)
        global_pos = self.mapToGlobal(pos)
        menu.exec(global_pos) #show the menu at the global position

    # send the create group event
    def prompt_add_task(self):
        task_name, ok = QInputDialog.getText(self, "New Task", "Enter task name:")
        if ok and task_name:
            self.add_task(task_name)

    # Add a new task widget to the task container
    def add_task(self, task_name, checked=False):
        unique_id = str(uuid.uuid4())
        # Create a new TaskWidget and pass the unique ID
        task_widget = TaskWidget(task_name, unique_id, checked, self)
        self.task_layout.addWidget(task_widget)

    # Delete the specified task widget from the task container
    def delete_task(self, task_widget: TaskWidget):
        self.layout().removeWidget(task_widget)
        task_widget.deleteLater()
        self.update()  # Update the container to adjust layout

    # Manage the drag enter event
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event: QDragMoveEvent):
        event.acceptProposedAction()  # Show "permitted" cursor

    # Manage the drop event (swap the source and target task widgets)
    def dropEvent(self, event):
        source_uid = event.mimeData().text()
        source_widget = self.find_task_widget_by_uid(source_uid)
        target_widget = self.childAt(event.position().toPoint()) #self.childAt(event.pos())

        # Find the correct target widget (may be nested inside another widget)
        while target_widget and not isinstance(target_widget, TaskWidget):
            target_widget = target_widget.parentWidget()

        if target_widget is not None and source_widget != target_widget:
            source_index = self.layout().indexOf(source_widget)
            target_index = self.layout().indexOf(target_widget)

            # Insert the source widget before the target widget
            self.layout().insertWidget(target_index, source_widget)

        event.acceptProposedAction()

    # Helper function to find a TaskWidget by its UID (this is necessary for drag and drop operations)
    def find_task_widget_by_uid(self, uid):
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if widget and widget.objectName() == uid:
                return widget
        return None  


#defines a gradient label for group. (and tasks?)
class GradientLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())

        # Set up gradient stops with more points for a smoother transition
        gradient.setColorAt(0, QColor(76, 175, 80, 0))      # Transparent at the edges
        gradient.setColorAt(0.3, QColor(76, 175, 80, 60))  # Slightly opaque closer to the center
        gradient.setColorAt(0.5, QColor(76, 175, 80, 180))   # Fully opaque at the center
        gradient.setColorAt(0.7, QColor(76, 175, 80, 60))  # Slightly opaque as it transitions back to transparent
        gradient.setColorAt(1, QColor(76, 175, 80, 0))       # Transparent at the other edge

        painter.fillRect(self.rect(), gradient)
        painter.setPen(self.palette().windowText().color())
        painter.drawText(self.rect(), self.alignment(), self.text())

        painter.end() 

# create the group frame class with tasks and its functions
class ListOfTaks(QFrame):
    def __init__(self, list_name, unique_id, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Box)
        self.setFixedSize(280, 150)  # Example fixed size
        self.setMinimumFrameHeight = 150  # Initial height
        self.setMaximumFrameHeight = 500 # Maximum height
        self.unique_id = unique_id #identification of the groupobject
        self.list_name = list_name # Store the group name

        # Create a layout for the group frame
        self.list_layout = QVBoxLayout(self)
        self.list_layout.setContentsMargins(10, 5, 10, 5)  # Left, Top, Right, Bottom margins
        self.list_layout.setAlignment(Qt.AlignTop)  # Align tasks to the top

        # Create the label for the group
        self.list_label = GradientLabel(list_name, self)
        self.list_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.list_label.setStyleSheet("""
            background-color: rgba(76, 175, 80, 150);  /* Green background color with 150/255 transparency */
            border: 1px solid #2E7D32;  /* Dark green border */
            padding: 4px;               /* Padding around the text */
            font-weight: bold;          /* Bold font */
            color: white;               /* White text color */
        """)
        self.list_label.adjustSize()
        self.list_layout.addWidget(self.list_label, alignment=Qt.AlignTop)
        
        # Add scroll area for tasks with an invisible background
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # Create a widget to hold the tasks and set it as the scroll area's widget
        self.task_container = TaskContainer(self)
        self.scroll_area.setWidget(self.task_container)
        self.list_layout.addWidget(self.scroll_area)

        # Connect right-click menu for the group label (title)
        self.list_label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_label.customContextMenuRequested.connect(self.show_title_context_menu)

        # Enable dragging
        self.setAcceptDrops(True)
        self.setObjectName(str(self.unique_id))

        # Initialize resizing variables
        self.setMouseTracking(True) # Set the mouse tracking to true to track the mouse movements
        self._resizing = False
        self._drag_start_position = None
        self._initial_height = None

    # Show the context menu for renaming or deleting the group (clicking inside the group label/gradient laberl)
    def show_title_context_menu(self, pos: QPoint):
        global_pos = self.list_label.mapToGlobal(pos)

        menu = QMenu(self)
        rename_action = QAction("Rename List", self)
        delete_action = QAction("Delete List", self)

        rename_action.triggered.connect(self.rename_list)
        delete_action.triggered.connect(self.delete_list)

        menu.addAction(rename_action)
        menu.addAction(delete_action)

        menu.exec(global_pos)

    # Rename this group
    def rename_list(self):
        new_name, ok = QInputDialog.getText(self, "Rename List", "Enter new list name:", text=self.list_name)
        if ok and new_name:
            self.list_name = new_name
            self.list_label.setText(new_name)

    # Delete the group
    def delete_list(self):
        self.setParent(None)
        self.deleteLater()

     # Manage the drag enter event
    def mousePressEvent(self, event):
        clicked_widget = self.childAt(event.pos())

        if isinstance(clicked_widget, TaskWidget):
            print(f"Forwarding event to TaskWidget: {clicked_widget.uid}", flush=True)
            # Forward the event to the TaskWidget
            clicked_widget.mousePressEvent(event)
        elif event.button() == Qt.LeftButton:
            if self.is_near_bottom_border(event.position().toPoint()):
                self._resizing = True
                self._drag_start_position = event.position().toPoint()
                self._initial_height = self.height()
                event.accept()
            elif self.list_label.geometry().contains(event.position().toPoint()):
                print(f"Mouse press event on GradientLabel at position: {event.position().toPoint()}", flush=True)
                drag = QDrag(self)
                mime_data = QMimeData()

                # Store the widget's unique ID in the mime data
                mime_data.setText(self.objectName())
                drag.setMimeData(mime_data)

                # Create a visual representation for dragging
                pixmap = self.grab()  # Grabs an image of the widget
                drag.setPixmap(pixmap)
                drag.setHotSpot(event.position().toPoint())  # Adjust hotspot to the click position
                drag.exec(Qt.MoveAction)
                print("Dragging group initiated", flush=True)
        elif event.button() == Qt.RightButton and self.list_label.geometry().contains(event.position().toPoint()):
            print(f"Right-click detected on GradientLabel; triggering context menu", flush=True)
            self.show_title_context_menu(event.position().toPoint())
        else:
            # If the click is not on the GradientLabel or a TaskWidget, propagate it normally
            print(f"ELSE DRAGGABLEFRAME: ", flush=True)
            super().mousePressEvent(event)

    # Handle the mouse move event and resize the frame if necessary
    def mouseMoveEvent(self, event):
        if self._resizing:
            delta_y = event.position().toPoint().y() - self._drag_start_position.y()
            new_height = self._initial_height + delta_y
            if new_height < self.setMinimumFrameHeight:
                new_height = self.setMinimumFrameHeight
            elif new_height > self.setMaximumFrameHeight:
                new_height = self.setMaximumFrameHeight
            self.setFixedHeight(new_height)
            event.accept()
        else:
            if self.is_near_bottom_border(event.position().toPoint()):
                self.setCursor(QCursor(Qt.SizeVerCursor))
            else:
                self.setCursor(QCursor(Qt.ArrowCursor))
        super().mouseMoveEvent(event)

    # Handle the mouse release event and stop resizing
    def mouseReleaseEvent(self, event):
        if self._resizing:
            self._resizing = False
            event.accept()
        super().mouseReleaseEvent(event)

    # Figure if we need to show the resize cursor or not
    def is_near_bottom_border(self, pos):
        return abs(pos.y() - self.height()) < 5  # Check if the mouse is within 5 pixels of the bottom border        



# Manage the group of taks (create, delete, rename) -- still need the proper save/load functions
class CustomComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.previous_index = self.currentIndex()  # Initialize the previous index
        self.remove_group_menu = QAction("Remove Group", self)
        self.add_group_menu = QAction("Create Group", self)
        self.rename_group_menu = QAction("Rename Group", self)

        self.setStyleSheet("""
            QComboBox {
                padding: 2px;                   /* Padding inside the combo box */
                min-width: 120px;               /* Minimum width of the combo box */
            }
            QComboBox::drop-down {
                border: none;
                background: none;
                width: 0px;
            }
            QComboBox::down-arrow {
                image: none;
                width: 0px;                        /* Width of the arrow */
                height: 0px;                       /* Height of the arrow */
            }
            QAbstractItemView {
                padding: 1px;
            }
        """)
    
    # Override the paint event to customize the combo box appearance
    def paintEvent(self, event):
        painter = QPainter(self)
        opt = QStyleOptionComboBox()
        self.initStyleOption(opt)

        # Remove the down arrow by not drawing the arrow
        # Set iconSize to 0 to remove the space for the arrow
        opt.iconSize = QSize(0, 0)

        # Draw the combo box frame
        self.style().drawComplexControl(QStyle.CC_ComboBox, opt, painter, self)

        # Draw the text centered
        text_rect = self.style().subControlRect(QStyle.CC_ComboBox, opt, QStyle.SC_ComboBoxEditField, self)
        painter.drawText(text_rect, Qt.AlignCenter, self.currentText())

        # End the painter to avoid QBackingStore errors
        painter.end()

    # Center align the text of each item in the drop-down menu
    def showPopup(self):
        for i in range(self.count()):
            self.setItemData(i, Qt.AlignCenter, Qt.TextAlignmentRole)
        super().showPopup()
    
    # Add a new item to the combobox with a unique ID (this overrides the addItem method.)
    def addItem(self, group_name, uid=None):
        if uid is None:
            logging.error("UID not provided for the group. Generating a new UID. THIS SHOULD NOT HAPPEN IN PRODUCTION.")
            uid = str(uuid.uuid4())  # Generate a UID if not provided

        super().addItem(group_name)  # Call the base class method to add the item
        self.setItemData(self.count() - 1, uid)  # Store the UID as item data

    # Add a new group and update the groups data (this calls addItem)
    def add_new_group(self, groups_data):
        new_group_name, ok = QInputDialog.getText(self, "Add Group", "Enter new group name:")
        if ok and new_group_name:
            newGroupId = groups_data.create_group(new_group_name)
            self.addItem(new_group_name, newGroupId)
            self.setCurrentIndex(self.count() - 1)

    # Remove the selected group from the ComboBox
    def remove_selected_group(self):
        current_index = self.currentIndex()
        if current_index >= 0:
            # Get the group ID before removing
            removed_group_id = self.itemData(current_index)
            # Remove the item from the ComboBox
            self.removeItem(current_index)
            return removed_group_id
        return None

    # Rename the selected group in the ComboBox
    def rename_selected_group(self):
        current_index = self.currentIndex()
        if current_index >= 0:
            current_text = self.currentText()
            new_group_name, ok = QInputDialog.getText(self, "Rename Group", "Enter new group name:", text=current_text)
            if ok and new_group_name:
                self.setItemText(current_index, new_group_name)
                return self.itemData(current_index), new_group_name






 
    # Handles the process of swapping groups (override the default method)
    def handle_group_swap(self):
        # Get the new group UID using the current index
        new_index = self.currentIndex()
        new_uid = self.itemData(new_index)

        # can we remove this?
        self.previous_index = new_index
        return new_uid

    # load all active groups and return the active group
    def load_and_activate_lists(self, groups_data):
        self.blockSignals(True) # stop the signal to avoid the signal to be triggered, and reload groups without swapping
        self.clear()  # Clear any existing items
        active_index = 0

        # Create an initial group if no groups are available
        if not groups_data.groups:
            groups_data.create_initial_group()
            logging.debug(f"we didn't had any groups, creating a starter group.")   

        # Load groups into the combo box
        for index, group in enumerate(groups_data.groups):
            self.addItem(group.name, group.group_id)
            logging.debug(f"looking for active_id '{groups_data.active_group_id}' and we are comparing index '{index}' for group '{group.name}' id '{group.group_id}'.")  
            if group.group_id == groups_data.active_group_id:
                active_group = group
                active_index = index
      
        # If no group is marked as active, set and return the first group if available
        if active_index == 0 and self.count() > 0:
            active_group = groups_data.groups[active_index]
            groups_data.set_active_group(active_group.group_id)
            logging.warning(f"No active group found after loading. Defaulting to first group.")

        self.setCurrentIndex(active_index)
        self.blockSignals(False) # begin handling the signal again
        return active_group

    # Manage the lists -- create list, delete list, rename list 
    def showContextMenu(self, position):
        menu = QMenu(self)
        menu.addAction(self.add_group_menu)
        menu.addAction(self.rename_group_menu)

        # Should we let the user delete the last group?
        if self.count() > 1:
            menu.addAction(self.remove_group_menu)

        # Show the context menu at the position of the right-click
        menu.exec(self.mapToGlobal(position))

    # Handle the mouse events to override the right-click context menu
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.showContextMenu(event.position().toPoint())
        else:
            super().mousePressEvent(event)



#defines the top menu bar 
class CustomTopMenuBar(QToolBar):
    def __init__(self, parent=None):
        super().__init__("Custom Top Menu Bar", parent)
        self.setMovable(False) # Prevent the toolbar from being moved

        # Disable the context menu policy
        self.setContextMenuPolicy(Qt.NoContextMenu)
        
        # set the toolbar style (we just need to adjust its padding
        self.setStyleSheet("padding: 5px;")

        # Add a spacer to push the group selector to the center
        spacer_left = QWidget(self)
        spacer_left.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.addWidget(spacer_left)

        # Add group selector to the toolbar (center-aligned)
        self.group_selector = CustomComboBox(self)
        self.addWidget(self.group_selector)


        # Add a spacer to push the remaining items to the right
        spacer_right = QWidget(self)
        spacer_right.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.addWidget(spacer_right)

    # Disable the event filter for the context menu
        self.installEventFilter(self)

    def getActiveGroup(self):
        return self.group_selector.currentIndex()

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu:
            return True  # Block context menu event
        return super().eventFilter(source, event)

#define the bottom menu bar
class CustomBottomMenuBar(QToolBar):
    def __init__(self, parent=None):
        super().__init__("Custom Bottom Menu Bar", parent)
        self.setMovable(False) # Prevent the toolbar from being moved

         # Disable the context menu policy
        self.setContextMenuPolicy(Qt.NoContextMenu)

        # Add actions to the bottom toolbar
        self.settings_button = QAction("Settings", self)
        self.addAction(self.settings_button)
        self.calendar_button = QAction("Calendar", self)
        self.addAction(self.calendar_button)

        # Add developer buttons to the bottom toolbar
        self.debug_save_groups_button = QAction("Save gs", self)
        self.addAction(self.debug_save_groups_button)
        self.debug_load_groups_button = QAction("Load gs", self)
        self.addAction(self.debug_load_groups_button)
        self.debug_delete_groups_button = QAction("Del gs", self)
        self.addAction(self.debug_delete_groups_button)

        # Add a spacer to push the next item to the right
        spacer = QWidget(self)
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.addWidget(spacer)

        # Add the help button (right-aligned)
        help_action = QAction("?", self)
        help_action.setToolTip("Help information: Right-click to create or delete groups.\nWithin a group, right-click to create tasks.\nTasks have a checkbox to mark them as complete.")
        help_action.setEnabled(False)  # Make the action unclickable
        self.addAction(help_action)

        # Add developer buttons to the bottom toolbar
        self.debug_add_group_button = QAction("add group", self)
        self.addAction(self.debug_add_group_button)
        self.debug_add_collumn_button = QAction("add col", self)
        self.addAction(self.debug_add_collumn_button)
        self.debug_remove_collumn_button = QAction("rem col", self)
        self.addAction(self.debug_remove_collumn_button)

    # Disable the event filter for the context menu
        self.installEventFilter(self)
    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu:
            return True  # Block context menu event
        return super().eventFilter(source, event)

class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)
        self.setAcceptDrops(True) # Enable dropping
        self.current_row = 1 # Initial row
        self.current_col = 0 # Initial column
        self.max_columns = 3  # Maximum number of columns before wrapping to the next row

    # send the create group event
    def prompt_add_list(self):
        list_name, ok = QInputDialog.getText(self, "List Name", "Enter the list name:")
        if ok and list_name:
            self.add_list(list_name)

    # Add a new group of tasks to the grid layout
    def add_list(self, list_name, returning=False):
        # Generate a unique ID for each group
        unique_id = uuid.uuid4()
        # Create a new draggable frame for the group
        list_frame = ListOfTaks(list_name, unique_id, self)
        # Add the group frame to the grid layout at the current position
        self.layout.addWidget(list_frame, self.current_row, self.current_col)
        # Update column and row for the next widget
        self.current_col += 1
        if self.current_col >= self.max_columns:
            self.current_col = 0
            self.current_row += 1
        if returning:
            return list_frame

    # Manage the Mouse Press Event (right click create a new group of tasks)
    def mousePressEvent(self, event):
        clicked_widget = self.childAt(event.pos())
        if clicked_widget is None:  # If the click is on the background (no child widget)
            if event.button() == Qt.RightButton:
                self.prompt_add_list()
            else:
                super().mousePressEvent(event)
        else:
            event.ignore()  # Pass the event to the child widget

    def dragEnterEvent(self, event):
        print("Drag parent", flush=True)
        if event.mimeData().hasText():
            print("Drag parent two", flush=True)
            event.acceptProposedAction()

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    #custumize the drag move event (draging groups #OGRADAAAAAAAAAAAAAAAA)
    def dragMoveEvent(self, event):
       event.acceptProposedAction()

    #execute the drag event
    def dropEvent(self, event: QDropEvent):
        # Find the widget that was dropped using the unique ID
        source_widget = self.findChild(ListOfTaks, event.mimeData().text())
        if not source_widget:
            return

        # Get the position where the widget is dropped
        drop_position = event.position().toPoint()
        target_widget = self.childAt(drop_position)

        # If the drop target is not a DraggableFrame, find the closest DraggableFrame parent
        while target_widget and not isinstance(target_widget, ListOfTaks):
            target_widget = target_widget.parentWidget()

        if isinstance(target_widget, ListOfTaks) and target_widget != source_widget:
            # Swap the source and target widgets
            source_index = self.layout.indexOf(source_widget)
            target_index = self.layout.indexOf(target_widget)

            source_row, source_col, _, _ = self.layout.getItemPosition(source_index)
            target_row, target_col, _, _ = self.layout.getItemPosition(target_index)

            self.layout.addWidget(source_widget, target_row, target_col)
            self.layout.addWidget(target_widget, source_row, source_col)

        event.acceptProposedAction()

    #update the grid layout (rearrange the grid layout based on the current max_columns setting)
    def update_grid_layout(self):
        widgets = []
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, ListOfTaks):
                widgets.append(widget)

        # Clear the layout
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                self.layout.removeWidget(widget)

        # Re-add widgets based on the new max_columns setting
        self.current_row = 1
        self.current_col = 0
        for widget in widgets:
            self.layout.addWidget(widget, self.current_row, self.current_col)
            self.current_col += 1
            if self.current_col >= self.max_columns:
                self.current_col = 0
                self.current_row += 1

    # Delete all GroupOfTaks in the central widget
    def delete_all_lists(self):
        for list_frame in self.findChildren(ListOfTaks):
            list_frame.delete_list()  
        self.update_grid_layout()

    # Save all GroupOfTaks and tasks inside them to a file
    def export_lists(self):
        lists_data = []

        for list_frame in self.findChildren(ListOfTaks):
            list_name = list_frame.list_name
            tasks = []

            for task_widget in list_frame.task_container.findChildren(TaskWidget):
                task_data = {
                    "name": task_widget.label.text(),
                    "checked": task_widget.checkbox.isChecked()
                }
                tasks.append(task_data)

            lists_data.append({
                "group_name": list_name,
                "tasks": tasks
            })

        return lists_data
    
    # Load all GroupOfTaks and tasks inside them from a file
    def import_lists(self, lists_data):
        self.delete_all_lists()  # Clear existing groups first (self.clear?)

        logging.debug("Start creating the imported lists.")
        for list in lists_data.lists:
            list_name = list.name
            list_frame = self.add_list(list_name, True)

            for task in list.tasks:
                task_name = task.name
                task_checked = task.checked
                # Add task to the group
                list_frame.task_container.add_task(task_name, task_checked)
        self.update_grid_layout()





#defines the main window
class TaskManagerMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(300, 250)  # Set minimum window sizewidth = 400, Minimum height = 300
        self.setWindowTitle("Task Management Optimizer")  # Set the window title

        self.snap_threshold = 50  # Distance to the screen edge where snapping occurs
        self._drag_active = False
        self._drag_position = QPoint()

        # Create the central widget
        self.central_widget = CentralWidget()

        # Wrap the central widget in a scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.central_widget)

        # Set the scroll area as the central widget
        self.setCentralWidget(self.scroll_area)

    def increase_columns(self):
        self.central_widget.max_columns += 1
        self.central_widget.update_grid_layout()

    def decrease_columns(self):
        if self.central_widget.max_columns > 1:
            self.central_widget.max_columns -= 1
            self.central_widget.update_grid_layout()      

    def set_window_icon(self, icon_path):
        self.setWindowIcon(QIcon(icon_path))

    def initUI(self, layout):
        # Create the top toolbar
        self.top_toolbar = CustomTopMenuBar()
        self.addToolBar(Qt.TopToolBarArea, self.top_toolbar)
        self.top_toolbar.setContextMenuPolicy(Qt.NoContextMenu)

        # Create the bottom toolbar
        self.bottom_toolbar = CustomBottomMenuBar() 
        self.addToolBar(Qt.BottomToolBarArea, self.bottom_toolbar)
        self.bottom_toolbar.setContextMenuPolicy(Qt.NoContextMenu)

   # def resizeEvent(self, event):
        # Adjust the number of frames based on window size
      #  self.central_widget.adjust_layout(self.size())  # Assuming a method to adjust layout based on size
        #super().resizeEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_active = True
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_active:
            self.move(self.calculate_snap_position(event.globalPosition().toPoint() - self._drag_position))
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_active = False
            event.accept()

    def calculate_snap_position(self, new_pos):
        screens = QApplication.screens()

        snapped_pos = new_pos

        for screen in screens:
            screen_geometry = screen.availableGeometry()
            window_geometry = self.frameGeometry()

            x, y = new_pos.x(), new_pos.y()
            right = x + window_geometry.width()
            bottom = y + window_geometry.height()

            # Snap to left or right edges of the screen
            if abs(x - screen_geometry.left()) < self.snap_threshold:
                snapped_pos.setX(screen_geometry.left())
            elif abs(right - screen_geometry.right()) < self.snap_threshold:
                snapped_pos.setX(screen_geometry.right() - window_geometry.width())

            # Snap to top or bottom edges of the screen
            if abs(y - screen_geometry.top()) < self.snap_threshold:
                snapped_pos.setY(screen_geometry.top())
            elif abs(bottom - screen_geometry.bottom()) < self.snap_threshold:
                snapped_pos.setY(screen_geometry.bottom() - window_geometry.height())

        return snapped_pos
    


# sets up the main window (change name?)
def setup_main_window(root, settings, group_data):
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

    # Additional UI components like buttons, and load the group data
    central_layout = root.central_widget
    root.initUI(central_layout)
  #  central_layout.import_groups(group_data)

    logging.debug(f"returning group data:\n {group_data}")
    active_group = root.top_toolbar.group_selector.load_and_activate_lists(group_data)
    logging.debug(f"returning active group:\n {active_group}")
    central_layout.import_lists(active_group)

   # active_group = root.top_toolbar.group_selector.populate_and_get_active_group(group_data)
   # populate_and_get_active_group(groups_data):

   # Populate the group selector with group data
    #populate_group_selector(root.top_toolbar, groups_data)

    # Identify and load the active group into the central widget
    #active_group = get_active_group(groups_data)
   # load_active_group_into_central_widget(central_layout, active_group)