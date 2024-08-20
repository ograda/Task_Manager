from PySide6.QtWidgets import QWidget, QSizeGrip, QScrollArea, QMainWindow, QApplication, QLabel, QVBoxLayout, QFrame, QMenu, QCheckBox, QInputDialog, QHBoxLayout, QComboBox, QSizePolicy, QGridLayout, QToolBar, QStyle, QStyleOptionComboBox
from PySide6.QtGui import QAction, QIcon, QLinearGradient, QPainter, QColor, QDrag, QDropEvent, QCursor
from PySide6.QtCore import Qt,QPoint, QMimeData, QSize
from event_handlers import  open_calendar, open_settings
from utils import get_icon_path
from data_manager import load_groups_and_tasks
import uuid



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

class ResizableWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set up layout
        layout = QVBoxLayout(self)
        
        # Add a label (or your custom content)
        label = QLabel("Resizable Content", self)
        layout.addWidget(label)
        
        # Add a size grip to the bottom-right corner for resizing
        size_grip = QSizeGrip(self)
        layout.addWidget(size_grip, alignment=Qt.AlignBottom | Qt.AlignRight)

        self.setMinimumSize(280, 150)  # Set minimum size
        self.setMaximumSize(280, 500)  # Set maximum size

#define the task widget and its properties
class TaskWidget(QFrame):
    def __init__(self, task_name, uid, parent=None):
        super().__init__(parent)

        # Store the unique ID
        self.uid = uid
        self.setObjectName(self.uid)  # Set the object name to the UID

        #self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        #self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Fixed height to control size

        # Apply the border and background to the entire QFrame
        self.setStyleSheet("""
            QFrame {
                border: 3px solid #4DD0E1;  /* Border color */
                border-radius: 5px;         /* Rounded corners */
                background-color: #FFFFFF;  /* Background color */
            }
        """)

        layout = QHBoxLayout(self)
        #layout.setContentsMargins(0, 0, 0, 0)
        layout.setContentsMargins(5, 5, 5, 5)  # Adjust margins to ensure the border looks correct
        layout.setSpacing(10)  # Add some spacing between the checkbox and the label

        # Create the checkbox
        self.checkbox = QCheckBox(self)
        self.checkbox.setStyleSheet("margin: 0px;")  # Ensure checkbox margin does not interfere with the layout
        layout.addWidget(self.checkbox)

        # Create the label for the task text
        self.label = QLabel(task_name, self)
        self.label.setWordWrap(True)  # Enable text wrapping
        #self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        #background-color: transparent;  /* Ensure label background is transparent *
        self.label.setStyleSheet("""
            background-color: #E0F7FA;  /* Light blue background */
            padding: 10px;               /* Padding around the text */
            border: 1px solid #4DD0E1;  /* Border color */
            border-radius: 5px;         /* Rounded corners */
            color: red;               /* White text color */ 
        """)
        layout.addWidget(self.label)

        # Set a fixed height to match the height of a typical task
        self.setFixedHeight(self.sizeHint().height())

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def mousePressEvent(self, event):
        #if event.button() == Qt.RightButton:
            # Trigger the parent context menu for this task
           # self.parentWidget().parentWidget().show_context_menu(event.pos())
        if event.button() == Qt.LeftButton:
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
            super().mousePressEvent(event)


    def show_context_menu(self, pos: QPoint):
        menu = QMenu(self)

        delete_task_action = QAction("Delete Task", self)
        delete_task_action.triggered.connect(lambda: self.delete_task())
        menu.addAction(delete_task_action)

        menu.exec(self.mapToGlobal(pos))

    def delete_task(self):
        """Remove this task from the parent layout and delete it."""
        parent_layout = self.parentWidget().layout()
        parent_layout.removeWidget(self)
        self.deleteLater()
"""
        def mousePressEvent(self, event):
            print(f"entering mouse press event on taskwidget: {self.uid}", flush=True)
            if event.button() == Qt.RightButton:
                print(f"Right-click detected on TaskWidget: {self.uid}", flush=True)
                # Trigger the parent context menu for this task
                self.parentWidget().parentWidget().show_context_menu(event.pos())
            elif event.button() == Qt.LeftButton:
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
                print(f"Left-click detected on TaskWidget: {self.uid}", flush=True)
                super().mousePressEvent(event)
"""

class TaskContainer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAcceptDrops(True)
       # self.setLayout(QVBoxLayout())
       # self.layout().setContentsMargins(10, 5, 10, 5)
       # self.layout().setAlignment(Qt.AlignTop)


        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos: QPoint):
        global_pos = self.mapToGlobal(pos)
        clicked_widget = self.childAt(pos)
        menu = QMenu(self)

        # Traverse up the widget hierarchy to find the DraggableFrame
        parent_widget = self.parentWidget()
        while parent_widget is not None and not isinstance(parent_widget, DraggableFrame):
            parent_widget = parent_widget.parentWidget()

        draggable_frame = parent_widget

        if isinstance(draggable_frame, DraggableFrame):
            if isinstance(clicked_widget, TaskWidget):
                delete_task_action = QAction("Delete Task", self)
                delete_task_action.triggered.connect(lambda: self.delete_task(clicked_widget))
                menu.addAction(delete_task_action)

                add_task_action = QAction("Add Task", self)
                add_task_action.triggered.connect(draggable_frame.add_task)
                menu.addAction(add_task_action)
            else:
                add_task_action = QAction("Add Task", self)
                add_task_action.triggered.connect(draggable_frame.add_task)
                menu.addAction(add_task_action)

            menu.exec(global_pos)
        else:
            print("DraggableFrame not found in hierarchy.", flush=True)

    def delete_task(self, task_widget: TaskWidget):
        """Delete the specified task."""
        self.layout().removeWidget(task_widget)
        task_widget.deleteLater()
        self.update()  # Update the container to adjust layout

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        source_uid = event.mimeData().text()
        source_widget = self.find_task_widget_by_uid(source_uid)
        target_widget = self.childAt(event.pos())

        # Find the correct target widget (may be nested inside another widget)
        while target_widget and not isinstance(target_widget, TaskWidget):
            target_widget = target_widget.parentWidget()

        if source_widget is None:
            print("Source widget not found during drop event.")
            return

        if target_widget is not None and source_widget != target_widget:
            source_index = self.layout().indexOf(source_widget)
            target_index = self.layout().indexOf(target_widget)

            # Insert the source widget before the target widget
            self.layout().insertWidget(target_index, source_widget)

        event.acceptProposedAction()

    def find_task_widget_by_uid(self, uid):
        """Helper function to find a TaskWidget by its UID."""
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if widget and widget.objectName() == uid:
                return widget
        return None  


#defines a gradient label
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
class DraggableFrame(QFrame):
    def __init__(self, group_name, unique_id, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Box)
        self.setFixedSize(280, 150)  # Example fixed size
        
        self.setMinimumFrameHeight = 150  # Initial height
        self.setMaximumFrameHeight = 500 # Maximum height

        #identification of the groupobject
        self.unique_id = unique_id
        # Store the group name
        self.group_name = group_name

        # Create a layout for the group frame
        self.group_layout = QVBoxLayout(self)
        self.group_layout.setContentsMargins(10, 5, 10, 5)  # Left, Top, Right, Bottom margins
        self.group_layout.setAlignment(Qt.AlignTop)  # Align tasks to the top

        # Create the label for the group
        self.group_label = GradientLabel(group_name, self)
        self.group_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.group_label.setStyleSheet("""
            background-color: rgba(76, 175, 80, 150);  /* Green background color with 150/255 transparency */
            border: 1px solid #2E7D32;  /* Dark green border */
            padding: 4px;               /* Padding around the text */
            font-weight: bold;          /* Bold font */
            color: white;               /* White text color */
        """)
        self.group_label.adjustSize()
        self.group_layout.addWidget(self.group_label, alignment=Qt.AlignTop)
        

#OGRADAAAAAAAAAAAAAAAA
        # Add scroll area for tasks with an invisible background
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        #self.scroll_area.setFixedSize(280, 250)  # Fixed size for task area
       # self.scroll_area.setStyleSheet("""
        """    QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: rgba(76, 175, 80, 0);  /* Invisible scrollbar background */
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(76, 175, 80, 150);  /* Handle matching group color */
                border-radius: 5px;
            }
        """#)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # Create a widget to hold the tasks and set it as the scroll area's widget
        self.task_container = TaskContainer(self)
        self.task_layout = QVBoxLayout(self.task_container)
        self.task_layout.setContentsMargins(10, 5, 10, 5)  # Adjust margins to control spacing
        self.task_layout.setAlignment(Qt.AlignTop)  # Align tasks to the top
        self.scroll_area.setWidget(self.task_container)
        self.group_layout.addWidget(self.scroll_area)

        # Connect right-click menu for the group label (title)
        self.group_label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.group_label.customContextMenuRequested.connect(self.show_title_context_menu)

        # Enable right-click context menu for tasks
        #self.setContextMenuPolicy(Qt.CustomContextMenu)
       # self.customContextMenuRequested.connect(self.show_context_menu)

        # Enable dragging
        self.setAcceptDrops(False)
        self.setObjectName(str(self.unique_id))

        # Set the mouse tracking to true to track the mouse movements
        self.setMouseTracking(True)

        # Initialize resizing variables
        self._resizing = False
        self._drag_start_position = None
        self._initial_height = None

    def show_context_menu(self, pos: QPoint):
        global_pos = self.mapToGlobal(pos)
        clicked_widget = self.childAt(pos)

        # Debugging information
        print(f"Context menu triggered at position: {pos}, global position: {global_pos}")
        print(f"Clicked widget: {clicked_widget}")

        if isinstance(clicked_widget, TaskWidget):
            print(f"Task widget detected: {clicked_widget.uid}")
            menu = QMenu(self)

            delete_task_action = QAction("Delete Task", self)
            delete_task_action.triggered.connect(lambda: self.delete_task(clicked_widget))
            menu.addAction(delete_task_action)

            menu.exec(global_pos)
        else:
            print("No task widget found; showing group context menu")
            self.show_title_context_menu(pos)
    """ 
    def show_context_menu(self, pos: QPoint):
        #Show the context menu for adding or deleting tasks.
        global_pos = self.mapToGlobal(pos)

        menu = QMenu(self)

        # Determine if we're clicking on an existing task
        clicked_widget = self.childAt(pos)

        # Add an "Add Task" action
        add_task_action = QAction("Add Task", self)
        add_task_action.triggered.connect(self.add_task)
        menu.addAction(add_task_action)

        # Traverse up the widget tree to find the TaskWidget, if clicked on its child
        while clicked_widget is not None and not isinstance(clicked_widget, TaskWidget):
            clicked_widget = clicked_widget.parentWidget()
        if isinstance(clicked_widget, TaskWidget):
            # Add a "Delete Task" action
            delete_task_action = QAction("Delete Task", self)
            delete_task_action.triggered.connect(lambda: self.delete_task(clicked_widget))
            menu.addAction(delete_task_action)

        menu.exec(global_pos)
    """
    def add_task(self):
        """Add a new task (checkbox) to the group."""
        task_name, ok = QInputDialog.getText(self, "New Task", "Enter task name:")
        if ok and task_name:
            unique_id = str(uuid.uuid4())
            # Create a new TaskWidget and pass the unique ID
            task_widget = TaskWidget(task_name, unique_id, self.task_container)
            self.task_layout.addWidget(task_widget)
            print(f"Task {task_name} with UID {unique_id} added to group {self.group_name}", flush=True)

            # Print widget hierarchy
            print("Widget Hierarchy:", flush=True)
            print(self.task_container.findChildren(QWidget), flush=True)
        #if ok and task_name:
           # task_checkbox = QCheckBox(task_name, self.task_container)
          #  task_checkbox.setStyleSheet(
            """
                QCheckBox::indicator {
                    width: 15px;
                    height: 15px;
                }
                QCheckBox {
                    background-color: #E0F7FA;  /* Light blue background */
                    padding: 10px;               /* Padding around the text */
                    border: 1px solid #4DD0E1;  /* Border color */
                    border-radius: 5px;         /* Rounded corners */
                    word-wrap: true;            /* Allow line breaks */
                }
            """
                       # task_checkbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
         #   task_checkbox.setWordWrap(True)  # Allow text to wrap within the checkbox
            #task_checkbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
           # self.task_layout.addWidget(task_checkbox)

            # Adjust the scrollbar range and visibility
           # self.update_scrollbar()
    """
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    #custumize the drag move event (draging groups #OGRADAAAAAAAAAAAAAAAA)
    def dragMoveEvent(self, event):
       event.acceptProposedAction()

    #execute the drag event
    def dropEvent(self, event: QDropEvent):
        # Find the widget that was dropped using the unique ID
        source_widget = self.findChild(DraggableFrame, event.mimeData().text())
        if not source_widget:
            return

        # Get the position where the widget is dropped
        drop_position = event.position().toPoint()
        target_widget = self.childAt(drop_position)

        # If the drop target is not a DraggableFrame, find the closest DraggableFrame parent
        while target_widget and not isinstance(target_widget, DraggableFrame):
            target_widget = target_widget.parentWidget()

        if isinstance(target_widget, DraggableFrame) and target_widget != source_widget:
            # Swap the source and target widgets
            source_index = self.layout.indexOf(source_widget)
            target_index = self.layout.indexOf(target_widget)

            source_row, source_col, _, _ = self.layout.getItemPosition(source_index)
            target_row, target_col, _, _ = self.layout.getItemPosition(target_index)

            self.layout.addWidget(source_widget, target_row, target_col)
            self.layout.addWidget(target_widget, source_row, source_col)

        event.acceptProposedAction()
    """

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            print("Drag enter event accepted.", flush=True)
            event.acceptProposedAction()
        else:
            print("Drag enter event rejected.", flush=True)
            event.ignore()

    #custumize the drag move event (draging groups #OGRADAAAAAAAAAAAAAAAA)
    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            print("Drag move event accepted.", flush=True)
            event.acceptProposedAction()
        else:
            print("Drag move event rejected.", flush=True)
            event.ignore()

    def dropEvent(self, event):
        print(f"Drop event initiated at position: {event.position().toPoint()}", flush=True)

        # Find the widget that was dropped using the unique ID
        source_widget = self.findChild(DraggableFrame, event.mimeData().text())
        if not source_widget:
            print("Source widget not found during drop event.", flush=True)
            return

        drop_position = event.position().toPoint()
        print(f"Drop position: {drop_position}", flush=True)

        # Identify the target widget where the item is being dropped
        target_widget = self.childAt(drop_position)
        print(f"Target widget identified at drop position: {target_widget}", flush=True)

        # If the drop target is not a DraggableFrame, find the closest DraggableFrame parent
        while target_widget and not isinstance(target_widget, DraggableFrame):
            print(f"Traversing to parent widget: {target_widget.parentWidget()}", flush=True)
            target_widget = target_widget.parentWidget()

        if isinstance(target_widget, DraggableFrame) and target_widget != source_widget:
            print(f"Swapping positions between source ({source_widget}) and target ({target_widget}).", flush=True)
            
            source_index = self.parent().layout().indexOf(source_widget)
            target_index = self.parent().layout().indexOf(target_widget)

            print(f"Source index: {source_index}, Target index: {target_index}", flush=True)

            # Get the row and column positions
            source_row, source_col, _, _ = self.parent().layout().getItemPosition(source_index)
            target_row, target_col, _, _ = self.parent().layout().getItemPosition(target_index)

            print(f"Source position: (Row: {source_row}, Col: {source_col}), Target position: (Row: {target_row}, Col: {target_col})", flush=True)

            # Swap the widgets
            self.parent().layout().addWidget(source_widget, target_row, target_col)
            self.parent().layout().addWidget(target_widget, source_row, source_col)
        else:
            print("Drop target is not valid or is the same as the source widget.", flush=True)

        event.acceptProposedAction()
        print("Drop event completed.", flush=True)

    def find_task_widget_by_uid(self, uid):
        """Helper function to find a TaskWidget by its UID."""
        for i in range(self.task_layout.count()):
            widget = self.task_layout.itemAt(i).widget()
            if widget and widget.objectName() == uid:
                return widget
        return None


    def delete_task(self, task_widget: QCheckBox):
        """Delete the specified task."""
        self.task_layout.removeWidget(task_widget)
        task_widget.deleteLater()

        # Adjust the scrollbar range and visibility
        self.update_scrollbar()

    def update_scrollbar(self):
        """Update the scrollbar based on the number of tasks."""
        self.task_container.adjustSize()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def show_title_context_menu(self, pos: QPoint):
        """Show the context menu for renaming or deleting the group."""
        global_pos = self.group_label.mapToGlobal(pos)

        menu = QMenu(self)
        rename_action = QAction("Rename Group", self)
        delete_action = QAction("Delete Group", self)

        rename_action.triggered.connect(self.rename_group)
        delete_action.triggered.connect(self.delete_group)

        menu.addAction(rename_action)
        menu.addAction(delete_action)

        menu.exec(global_pos)

    def rename_group(self):
        """Rename the group."""
        new_name, ok = QInputDialog.getText(self, "Rename Group", "Enter new group name:", text=self.group_name)
        if ok and new_name:
            self.group_name = new_name
            self.group_label.setText(new_name)

    def delete_group(self):
        """Delete the group."""
        self.setParent(None)
        self.deleteLater()

    #def mousePressEvent(self, event):
    #    if event.button() == Qt.LeftButton:
     #       if self.is_near_bottom_border(event.position().toPoint()):
     #           self._resizing = True
      ##         drag = QDrag(self)
       #         mime_data = QMimeData()


    def mousePressEvent(self, event):
        clicked_widget = self.childAt(event.pos())

        if isinstance(clicked_widget, TaskWidget):
            print(f"Forwarding event to TaskWidget: {clicked_widget.uid}")
            # Forward the event to the TaskWidget
            clicked_widget.mousePressEvent(event)
        elif event.button() == Qt.LeftButton:
            if self.is_near_bottom_border(event.position().toPoint()):
                self._resizing = True
                self._drag_start_position = event.position().toPoint()
                self._initial_height = self.height()
                event.accept()
            elif self.group_label.geometry().contains(event.pos()):
                print(f"Mouse press event on GradientLabel at position: {event.pos()}")
                drag = QDrag(self)
                mime_data = QMimeData()

                # Store the widget's unique ID in the mime data
                mime_data.setText(self.objectName())
                drag.setMimeData(mime_data)

                # Create a visual representation for dragging
                pixmap = self.grab()  # Grabs an image of the widget
                drag.setPixmap(pixmap)
                drag.setHotSpot(event.pos())  # Adjust hotspot to the click position
                drag.exec(Qt.MoveAction)
                print("Dragging group initiated")
        elif event.button() == Qt.RightButton and self.group_label.geometry().contains(event.pos()):
            print(f"Right-click detected on GradientLabel; triggering context menu")
            self.show_title_context_menu(event.pos())
        else:
            # If the click is not on the GradientLabel or a TaskWidget, propagate it normally
            print(f"ELSE DRAGGABLEFRAME: ", flush=True)
            super().mousePressEvent(event)


    def mouseMoveEvent(self, event):
        if self._resizing:
            delta_y = event.position().toPoint().y() - self._drag_start_position.y()
            new_height = self._initial_height + delta_y

            if new_height < self.setMinimumFrameHeight:
                print(f"Blocked resizing at minimum height. Attempted Height: {new_height}, Min Height: {self.setMinimumFrameHeight}", flush=True)
                new_height = self.setMinimumFrameHeight
            elif new_height > self.setMaximumFrameHeight:
                print(f"Blocked resizing at maximum height. Attempted Height: {new_height}, Max Height: {self.setMaximumFrameHeight}", flush=True)
                new_height = self.setMaximumFrameHeight
            else:
                print(f"Resizing... New Height: {new_height}", flush=True)

            self.setFixedHeight(new_height)
            event.accept()
        else:
            if self.is_near_bottom_border(event.position().toPoint()):
                self.setCursor(QCursor(Qt.SizeVerCursor))
            else:
                self.setCursor(QCursor(Qt.ArrowCursor))

        super().mouseMoveEvent(event)


    def mouseReleaseEvent(self, event):
        if self._resizing:
            self._resizing = False
            event.accept()
        super().mouseReleaseEvent(event)

    def is_near_bottom_border(self, pos):
        return abs(pos.y() - self.height()) < 10  # Check if the mouse is within 10 pixels of the bottom border        


class CustomComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)

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

    def showPopup(self):
        # Center align the text of each item in the drop-down menu
        for i in range(self.count()):
            self.setItemData(i, Qt.AlignCenter, Qt.TextAlignmentRole)
        super().showPopup()

#OGRADAAAAAAAAAAAAAAAA
    #manage the lists -- greate list, delete list, rename list 
    def showContextMenu(self, position):
        # Create the context menu
        menu = QMenu(self)

        # Add actions to the menu
        option_one = QAction("Option One", self)
        option_two = QAction("Option Two", self)
        option_three = QAction("Option Three", self)

        # Connect actions to their respective handlers
        option_one.triggered.connect(self.optionOneSelected)
        option_two.triggered.connect(self.optionTwoSelected)
        option_three.triggered.connect(self.optionThreeSelected)

        # Add actions to the context menu
        menu.addAction(option_one)
        menu.addAction(option_two)
        menu.addAction(option_three)

        # Show the context menu at the position of the right-click
        menu.exec(self.mapToGlobal(position))

    def optionOneSelected(self):
        print("Option One selected", flush=True)

    def optionTwoSelected(self):
        print("Option Two selected", flush=True)

    def optionThreeSelected(self):
        print("Option Three selected", flush=True)   

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            # create the management Lists menu
            self.showContextMenu(event.pos())
     #   elif event.button() == Qt.LeftButton:
            # Do something else with the left mouse button
         #   self.showPopup()
        else:
            # Default behavior for other buttons
            super().mousePressEvent(event)



#defines the top menu bar 
class CustomTopMenuBar(QToolBar):
    def __init__(self, parent=None):
        super().__init__("Custom Top Menu Bar", parent)
        
        # Prevent the toolbar from being moved
        self.setMovable(False)
        
        # set the toolbar style (we just need to adjust its padding
        self.setStyleSheet("padding: 5px;")

        # Add a spacer to push the group selector to the center
        spacer_left = QWidget(self)
        spacer_left.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.addWidget(spacer_left)

        # Add group selector to the toolbar (center-aligned)
        group_selector = CustomComboBox(self)
        group_selector.addItems(["Group 1", "Group 2", "Group 3"])
        self.addWidget(group_selector)

        # Add a spacer to push the remaining items to the right
        spacer_right = QWidget(self)
        spacer_right.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.addWidget(spacer_right)

#define the bottom menu bar
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

        # Add developer buttons to the bottom toolbar
        self.debug_add_group_button = QAction("add group", self)
        self.addAction(self.debug_add_group_button)

        self.debug_add_collumn_button = QAction("add col", self)
        self.addAction(self.debug_add_collumn_button)

        self.debug_remove_collumn_button = QAction("rem col", self)
        self.addAction(self.debug_remove_collumn_button)

class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)
        self.setAcceptDrops(True) # Enable dropping

        # manage the columns and rows
        self.current_row = 1
        self.current_col = 0
        self.max_columns = 3  # Maximum number of columns before wrapping to the next row

        # Add a size grip to the bottom-right corner for resizing
        #size_grip = QSizeGrip(self)
      #  self.layout.addWidget(size_grip, alignment=Qt.AlignBottom | Qt.AlignRight)
        # Add a QSizeGrip to the bottom-right corner for resizing the entire widget
       # size_grip = QSizeGrip(self)
     #  self.layout.addWidget(size_grip, self.layout.rowCount(), self.layout.columnCount() - 1, 1, 1, alignment=Qt.AlignBottom | Qt.AlignRight)


    def prompt_add_group(self):
        group_name, ok = QInputDialog.getText(self, "Group Name", "Enter the group name:")
        if ok and group_name:
            self.add_group(group_name)   

    def add_group(self, group_name):
        # Generate a unique ID for each group
        unique_id = uuid.uuid4()

        # Create a new draggable frame for the group
        group_frame = DraggableFrame(group_name, unique_id, self)

        # Add the group frame to the grid layout at the current position
        self.layout.addWidget(group_frame, self.current_row, self.current_col)

        # Update column and row for the next widget
        self.current_col += 1
        if self.current_col >= self.max_columns:
            self.current_col = 0
            self.current_row += 1


    def mousePressEvent(self, event):
        clicked_widget = self.childAt(event.pos())

        if clicked_widget is None:  # If the click is on the background (no child widget)
            if event.button() == Qt.RightButton:
                self.prompt_add_group()
            else:
                super().mousePressEvent(event)
        else:
            event.ignore()  # Pass the event to the child widget


    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    #custumize the drag move event (draging groups #OGRADAAAAAAAAAAAAAAAA)
    def dragMoveEvent(self, event):
       event.acceptProposedAction()

    def dropEvent(self, event):
        source_widget = self.findChild(DraggableFrame, event.mimeData().text())
        if not source_widget:
            print("Source widget not found during drop event.", flush=True)
            event.ignore()
            return

        drop_position = event.position().toPoint()
        target_widget = self.childAt(drop_position)

        # Ensure target_widget is a valid DraggableFrame
        while target_widget and not isinstance(target_widget, DraggableFrame):
            target_widget = target_widget.parentWidget()

        if isinstance(target_widget, DraggableFrame) and target_widget != source_widget:
            print(f"Dropping on valid target: {target_widget.objectName()}", flush=True)
            source_index = self.layout.indexOf(source_widget)
            target_index = self.layout.indexOf(target_widget)

            source_row, source_col, _, _ = self.layout.getItemPosition(source_index)
            target_row, target_col, _, _ = self.layout.getItemPosition(target_index)

            self.layout.addWidget(source_widget, target_row, target_col)
            self.layout.addWidget(target_widget, source_row, source_col)

            event.acceptProposedAction()
        else:
            print("Invalid drop target or same as source.", flush=True)
            event.ignore()

    """
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    #custumize the drag move event (draging groups #OGRADAAAAAAAAAAAAAAAA)
    def dragMoveEvent(self, event):
       event.acceptProposedAction()

    #execute the drag event
    def dropEvent(self, event: QDropEvent):
        # Find the widget that was dropped using the unique ID
        source_widget = self.findChild(DraggableFrame, event.mimeData().text())
        if not source_widget:
            return

        # Get the position where the widget is dropped
        drop_position = event.position().toPoint()
        target_widget = self.childAt(drop_position)

        # If the drop target is not a DraggableFrame, find the closest DraggableFrame parent
        while target_widget and not isinstance(target_widget, DraggableFrame):
            target_widget = target_widget.parentWidget()

        if isinstance(target_widget, DraggableFrame) and target_widget != source_widget:
            # Swap the source and target widgets
            source_index = self.layout.indexOf(source_widget)
            target_index = self.layout.indexOf(target_widget)

            source_row, source_col, _, _ = self.layout.getItemPosition(source_index)
            target_row, target_col, _, _ = self.layout.getItemPosition(target_index)

            self.layout.addWidget(source_widget, target_row, target_col)
            self.layout.addWidget(target_widget, source_row, source_col)

        event.acceptProposedAction()
    """
    #update the grid layout (rearrange the grid layout based on the current max_columns setting)
    def update_grid_layout(self):
        """Rearrange the grid layout based on the current max_columns setting."""
        widgets = []
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, DraggableFrame):
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



#defines the main window
class TaskManagerMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._drag_active = False
        self._drag_position = QPoint()
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

        # Create the bottom toolbar
        self.bottom_toolbar = CustomBottomMenuBar() 
        self.addToolBar(Qt.BottomToolBarArea, self.bottom_toolbar)

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
def setup_main_window(root, settings):
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
  #  central_widget = QWidget(root)
   # central_layout = QVBoxLayout(central_widget)
  #  root.setCentralWidget(central_widget)

    central_layout = root.central_widget

    # Additional UI components like buttons, etc.
    root.initUI(central_layout)    

    root.bottom_toolbar.calendar_button.triggered.connect(lambda: open_calendar(root))
    root.bottom_toolbar.settings_button.triggered.connect(lambda: open_settings(root, settings))

    root.bottom_toolbar.debug_add_group_button.triggered.connect(lambda: root.central_widget.prompt_add_group())
    root.bottom_toolbar.debug_add_collumn_button.triggered.connect(lambda: root.increase_columns())
    root.bottom_toolbar.debug_remove_collumn_button.triggered.connect(lambda: root.decrease_columns())



#FIX IT AFTER MOVING GROUPS OUT OF CREATE MENU
def apply_groups_and_tasks(root):
    groups_data = load_groups_and_tasks()
  #  for group in groups_data:
    #    group_frame = create_group(root, group["group_name"])
     ##   for task in group["tasks"]:
          #  create_task(group_frame.layout(), task["label"], task["checked"])

#THIS SHOULD BE ELSEWHERE - DATA MANAGER OR UTILS
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