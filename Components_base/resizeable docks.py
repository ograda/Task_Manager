from PySide6.QtWidgets import QMainWindow, QApplication, QDockWidget, QLabel, QWidget, QVBoxLayout, QSizeGrip
from PySide6.QtCore import Qt

class ResizableDockWidget(QDockWidget):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea)
        
        # Create a central widget for the dock
        self.central_widget = QWidget(self)
        self.setWidget(self.central_widget)
        
        # Set up layout
        layout = QVBoxLayout(self.central_widget)
        
        # Add a label (or your custom content)
        label = QLabel("Resizable Content", self.central_widget)
        layout.addWidget(label)
        
        # Add a size grip to the bottom-right corner for resizing
        size_grip = QSizeGrip(self.central_widget)
        layout.addWidget(size_grip, alignment=Qt.AlignBottom | Qt.AlignRight)

        self.setMinimumSize(200, 150)  # Set minimum size
        self.setMaximumSize(500, 500)  # Set maximum size

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resizable Dock Example")
        
        # Add resizable dock widgets
        self.addDockWidget(Qt.LeftDockWidgetArea, ResizableDockWidget("Dock 1", self))
        self.addDockWidget(Qt.RightDockWidgetArea, ResizableDockWidget("Dock 2", self))

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()