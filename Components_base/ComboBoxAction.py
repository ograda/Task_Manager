from PySide6.QtWidgets import QApplication, QMainWindow, QComboBox, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QStyle, QStyleOptionComboBox
import sys

class CenteredComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("""
            QComboBox {
                qproperty-alignment: 'AlignCenter';
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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Center Text in QComboBox")

        # Create a CenteredComboBox
        combo_box = CenteredComboBox(self)
        combo_box.setGeometry(200, 150, 150, 30)

        # Add items to the combo box
        combo_box.addItems(["Option 1", "Option 2", "Option 3", "Option 4"])

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(combo_box)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

""" 
from PySide6.QtWidgets import QApplication, QMainWindow, QComboBox, QVBoxLayout, QWidget
from PySide6.QtCore  import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QStyle, QStyleOptionComboBox
import sys

class CenteredComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        opt = QStyleOptionComboBox()
        self.initStyleOption(opt)
        
        # Draw the combo box frame
        self.style().drawComplexControl(QStyle.CC_ComboBox, opt, painter, self)

        # Draw the text centered
        text_rect = self.style().subControlRect(QStyle.CC_ComboBox, opt, QStyle.SC_ComboBoxEditField, self)
        painter.drawText(text_rect, Qt.AlignCenter, self.currentText())

        # Draw the arrow
        self.style().drawPrimitive(QStyle.PE_IndicatorArrowDown, opt, painter, self)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Center Text in QComboBox")

        # Create a CenteredComboBox
        combo_box = CenteredComboBox(self)
        combo_box.setGeometry(200, 150, 150, 30)

        # Add items to the combo box
        combo_box.addItems(["Option 1", "Option 2", "Option 3", "Option 4"])

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(combo_box)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

"""