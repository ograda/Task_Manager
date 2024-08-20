from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QVBoxLayout, QPushButton, QLabel, QFrame, QInputDialog, QScrollArea, QHBoxLayout
from PySide6.QtCore import Qt, QMimeData, QPoint
from PySide6.QtGui import QDrag, QDropEvent
import uuid


class DraggableFrame(QFrame):
    def __init__(self, group_name, unique_id, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Box)
        self.setFixedSize(280, 150)  # Example fixed size
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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()

            # Store the widget's unique ID in the mime data
            mime_data.setText(self.objectName())
            drag.setMimeData(mime_data)

            # Create a visual representation for dragging
            drag.setHotSpot(event.position().toPoint())
            drag.exec(Qt.MoveAction)


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
        self.layout.addWidget(group_frame, self.current_row, self.current_col)

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

            self.layout.addWidget(source_widget, target_row, target_col)
            self.layout.addWidget(target_widget, source_row, source_col)

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
            self.layout.addWidget(widget, self.current_row, self.current_col)
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

        # Create a layout for the buttons
        button_layout = QHBoxLayout()

        # Create the "Add Group" button
        add_group_button = QPushButton("Add Group", self)
        add_group_button.clicked.connect(self.prompt_add_group)
        button_layout.addWidget(add_group_button)

        # Create the "Increase Columns" button
        increase_columns_button = QPushButton("Increase Columns", self)
        increase_columns_button.clicked.connect(self.increase_columns)
        button_layout.addWidget(increase_columns_button)

        # Create the "Decrease Columns" button
        decrease_columns_button = QPushButton("Decrease Columns", self)
        decrease_columns_button.clicked.connect(self.decrease_columns)
        button_layout.addWidget(decrease_columns_button)

        # Add the button layout to the grid
        button_container = QWidget()
        button_container.setLayout(button_layout)
        self.central_widget.layout.addWidget(button_container, 0, 0, 1, self.central_widget.max_columns)

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