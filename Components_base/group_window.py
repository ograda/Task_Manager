from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QFrame, QLabel, QMenu, QCheckBox, QInputDialog, QScrollArea, QSizePolicy
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QAction
import sys


class DraggableFrame(QFrame):
    def __init__(self, group_name, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Box)
        self.setFixedSize(280, 300)  # Example fixed size

        # Store the group name
        self.group_name = group_name

        # Create a layout for the group frame
        self.group_layout = QVBoxLayout(self)
        self.group_layout.setContentsMargins(0, 0, 0, 0)  # No margins in group layout

        # Create the label for the group
        self.group_label = QLabel(group_name, self)
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

        # Add scroll area for tasks with an invisible background
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedSize(280, 250)  # Fixed size for task area
        self.scroll_area.setStyleSheet("""
            QScrollArea {
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
        """)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # Create a widget to hold the tasks and set it as the scroll area's widget
        self.task_container = QWidget()
        self.task_layout = QVBoxLayout(self.task_container)
        self.task_layout.setContentsMargins(10, 5, 10, 5)  # Adjust margins to control spacing
        self.scroll_area.setWidget(self.task_container)

        self.group_layout.addWidget(self.scroll_area)

        # Connect right-click menu for the group label (title)
        self.group_label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.group_label.customContextMenuRequested.connect(self.show_title_context_menu)

        # Enable right-click context menu for tasks
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos: QPoint):
        """Show the context menu for adding or deleting tasks."""
        global_pos = self.mapToGlobal(pos)

        menu = QMenu(self)
        
        # Check if the right-click is on top of an existing task
        clicked_widget = self.childAt(pos)
        if isinstance(clicked_widget, QCheckBox):
            add_task_action = QAction("Add Task", self)
            add_task_action.triggered.connect(self.add_task)
            menu.addAction(add_task_action)

            delete_task_action = QAction("Delete Task", self)
            delete_task_action.triggered.connect(lambda: self.delete_task(clicked_widget))
            menu.addAction(delete_task_action)
        else:
            add_task_action = QAction("Add Task", self)
            add_task_action.triggered.connect(self.add_task)
            menu.addAction(add_task_action)

        menu.exec(global_pos)

    def add_task(self):
        """Add a new task (checkbox) to the group."""
        task_name, ok = QInputDialog.getText(self, "New Task", "Enter task name:")
        if ok and task_name:
            task_checkbox = QCheckBox(task_name, self.task_container)
            task_checkbox.setStyleSheet("""
                QCheckBox::indicator {
                    width: 15px;
                    height: 15px;
                }
                QCheckBox {
                    text-align: center;  /* Center the text */
                }
            """)
            task_checkbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.task_layout.addWidget(task_checkbox)

            # Adjust the scrollbar range and visibility
            self.update_scrollbar()

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 400)
        self.setWindowTitle("Single Draggable Frame with Context Menu")

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout(central_widget)

        # Create and add the draggable frame to the central widget
        group_frame = DraggableFrame("Group 1", central_widget)
        layout.addWidget(group_frame, alignment=Qt.AlignCenter)


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec())