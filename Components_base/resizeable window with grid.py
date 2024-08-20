from PySide6.QtWidgets import QApplication , QMainWindow, QWidget, QGridLayout, QVBoxLayout, QPushButton, QLabel, QFrame, QInputDialog, QScrollArea, QHBoxLayout, QStatusBar
from PySide6.QtCore import Qt, QSize, QMimeData
from PySide6.QtGui import QDrag, QDropEvent, QCursor
import uuid


class DraggableFrame(QFrame):
    def __init__(self, group_name, unique_id, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Box)
        self.setFixedWidth(280)  # Fixed width
        self.setFixedHeight(250)  # Fixed width
        self.setMinimumFrameHeight = 150  # Initial height
        self.setMaximumFrameHeight = 500 # Maximum height

        self.unique_id = unique_id

        # Create a layout for the group frame
        self.group_layout = QVBoxLayout(self)
        self.group_layout.setContentsMargins(10, 5, 10, 5)  # Left, Top, Right, Bottom margins

        # Create the label for the group
        group_label = QLabel(group_name, self)
        group_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        group_label.setStyleSheet("""
            background-color: rgba(76, 175, 80, 150);  /* Green background color with 150/255 transparency */
            border: 1px solid #2E7D32;  /* Dark green border */
            padding: 4px;               /* Padding around the text */
            font-weight: bold;          /* Bold font */
            color: white;               /* White text color */
        """)
        group_label.adjustSize()
        self.group_layout.addWidget(group_label, alignment=Qt.AlignTop)

        # Enable dragging
        self.setAcceptDrops(False)
        self.setObjectName(str(self.unique_id))

        # Set the mouse tracking to true to track the mouse movements
        self.setMouseTracking(True)

        # Initialize resizing variables
        self._resizing = False
        self._drag_start_position = None
        self._initial_height = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.is_near_bottom_border(event.position().toPoint()):
                self._resizing = True
                self._drag_start_position = event.position().toPoint()
                self._initial_height = self.height()
                event.accept()
            else:
                drag = QDrag(self)
                mime_data = QMimeData()

                # Store the widget's unique ID in the mime data
                mime_data.setText(self.objectName())
                drag.setMimeData(mime_data)

                # Create a visual representation for dragging
                drag.setHotSpot(event.position().toPoint())
                drag.exec(Qt.MoveAction)

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


class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)
        self.current_row = 1
        self.current_col = 0
        self.max_columns = 3  # Maximum number of columns before wrapping to the next row

        # Enable dropping
        self.setAcceptDrops(True)

    def add_group(self, group_name):
        # Generate a unique ID for each group
        unique_id = uuid.uuid4()

        # Create a new draggable frame for the group
        group_frame = DraggableFrame(group_name, unique_id, self)

        # Add the group frame to the grid layout at the current position
        self.layout.addWidget(group_frame, self.current_row, self.current_col, alignment=Qt.AlignTop)

        # Update column and row for the next widget
        self.current_col += 1
        if self.current_col >= self.max_columns:
            self.current_col = 0
            self.current_row += 1

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        # Find the widget that was dropped using the unique ID
        source_widget = self.findChild(DraggableFrame, event.mimeData().text())
        if not source_widget:
            return

        # Get the position where the widget is dropped
        target_widget = self.childAt(event.position().toPoint())
        if isinstance(target_widget, DraggableFrame) and target_widget != source_widget:
            # Swap the source and target widgets
            source_index = self.layout.indexOf(source_widget)
            target_index = self.layout.indexOf(target_widget)

            source_row, source_col, _, _ = self.layout.getItemPosition(source_index)
            target_row, target_col, _, _ = self.layout.getItemPosition(target_index)

            self.layout.addWidget(source_widget, target_row, target_col, alignment=Qt.AlignTop)
            self.layout.addWidget(target_widget, source_row, source_col, alignment=Qt.AlignTop)

        event.acceptProposedAction()

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
            self.layout.addWidget(widget, self.current_row, self.current_col, alignment=Qt.AlignTop)
            self.current_col += 1
            if self.current_col >= self.max_columns:
                self.current_col = 0
                self.current_row += 1


class TaskManagerMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 400)
        self.setWindowTitle("Task Manager - Dynamic Grid Layout with Drag-and-Drop")

        # Create the central widget
        self.central_widget = CentralWidget()

        # Wrap the central widget in a scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.central_widget)

        # Set the scroll area as the central widget
        self.setCentralWidget(self.scroll_area)

        # Create a bottom bar (status bar) for the buttons
        self.bottom_bar = QStatusBar()

        # Create the "Add Group" button
        add_group_button = QPushButton("Add Group", self)
        add_group_button.clicked.connect(self.prompt_add_group)
        self.bottom_bar.addWidget(add_group_button)

        # Create the "Increase Columns" button
        increase_columns_button = QPushButton("Increase Columns", self)
        increase_columns_button.clicked.connect(self.increase_columns)
        self.bottom_bar.addWidget(increase_columns_button)

        # Create the "Decrease Columns" button
        decrease_columns_button = QPushButton("Decrease Columns", self)
        decrease_columns_button.clicked.connect(self.decrease_columns)
        self.bottom_bar.addWidget(decrease_columns_button)

        # Set the status bar (bottom bar)
        self.setStatusBar(self.bottom_bar)

    def prompt_add_group(self):
        group_name, ok = QInputDialog.getText(self, "Group Name", "Enter the group name:")
        if ok and group_name:
            self.central_widget.add_group(group_name)

    def increase_columns(self):
        self.central_widget.max_columns += 1
        self.central_widget.update_grid_layout()

    def decrease_columns(self):
        if self.central_widget.max_columns > 1:
            self.central_widget.max_columns -= 1
            self.central_widget.update_grid_layout()


if __name__ == "__main__":
    app = QApplication([])

    window = TaskManagerMainWindow()
    window.show()

    app.exec()