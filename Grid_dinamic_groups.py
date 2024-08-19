from PySide6.QtWidgets import QWidget, QScrollArea, QMainWindow, QApplication, QLabel, QVBoxLayout, QFrame, QMenu, QCheckBox, QInputDialog, QHBoxLayout, QComboBox, QSizePolicy, QPushButton, QGridLayout, QToolBar
from PySide6.QtGui import QAction, QIcon, QRegion, QLinearGradient, QPainter, QColor, QDrag
from PySide6.QtCore import Qt,QPoint, QRect, QMimeData

class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()  # Use grid layout for multi-directional placements
        self.layout.setSpacing(20)  # Set spacing between widgets (groups)
        self.layout.setContentsMargins(20, 20, 20, 20)  # Set margins around the grid layout
        self.setLayout(self.layout)
        self.current_row = 1  # Start from row 1 (row 0 is for the button)
        self.current_col = 0
        self.max_columns = 3  # Maximum number of columns before wrapping to the next row

    def add_group(self, group_name):
        # Create a new frame for the group
        group_frame = QFrame(self)  # Use the central widget as the parent
        group_frame.setFrameShape(QFrame.Box)
        group_frame.setFixedSize(280, 150)  # Example fixed size

        # Create a layout for the group frame
        group_layout = QVBoxLayout(group_frame)
        group_layout.setContentsMargins(10, 5, 10, 5)  # Left, Top, Right, Bottom margins

        # Create the label for the group
        group_label = QLabel(group_name)
        group_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        group_label.setStyleSheet("""
            background-color: rgba(76, 175, 80, 150);  /* Green background color with 150/255 transparency */
            border: 1px solid #2E7D32;  /* Dark green border */
            padding: 4px;               /* Padding around the text */
            font-weight: bold;          /* Bold font */
            color: white;               /* White text color */
        """)
        group_label.adjustSize()
        group_layout.addWidget(group_label, alignment=Qt.AlignTop)

        # Add the group frame to the grid layout at the current position
        self.layout.addWidget(group_frame, self.current_row, self.current_col)

        # Update column and row for the next widget
        self.current_col += 1
        if self.current_col >= self.max_columns:
            self.current_col = 0
            self.current_row += 1


class TaskManagerMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 400)  # Set minimum window size
        self.setWindowTitle("Task Manager - Dynamic Grid Layout")

        # Create the central widget
        self.central_widget = CentralWidget()

        # Wrap the central widget in a scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.central_widget)

        # Set the scroll area as the central widget
        self.setCentralWidget(self.scroll_area)

        # Create an initial button to add groups
        add_group_button = QPushButton("Add Group", self)
        add_group_button.clicked.connect(self.prompt_add_group)
        self.central_widget.layout.addWidget(add_group_button, 0, 0, 1, self.central_widget.max_columns)  # Initial button spanning all columns in the top row

    def prompt_add_group(self):
        # Prompt for group name
        group_name, ok = QInputDialog.getText(self, "Group Name", "Enter the group name:")
        if ok and group_name:
            # Add the new group to the grid layout
            self.central_widget.add_group(group_name)


if __name__ == "__main__":
    app = QApplication([])

    # Create the main window
    window = TaskManagerMainWindow()
    window.show()

    # Run the application
    app.exec()