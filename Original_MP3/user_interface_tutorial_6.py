import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QToolTip

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        #To define the window geometry
        self.title = "PyQ5 Push Button"
        self.left = 100
        self.top = 100
        self.width = 680
        self.height = 540
        self.setWindowIcon(QtGui.QIcon("window_icon.jpg"))

        #To place a button on the window_icon
        button = QPushButton("Click Me", self)
        button.move(200,200)
        button.setToolTip("<h3>This is click button</h3>")
        #To initilize the window
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
