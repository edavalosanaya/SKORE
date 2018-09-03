#Signal and SLots Tutorial

import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QToolTip
from PyQt5.QtCore import QCoreApplication

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
        button = QPushButton("Close", self)
        button.move(200,200)
        button.setToolTip("<h3>This is click button</h3>")
        button.clicked.connect(self.close)
        #To initilize the window
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    #I have no idea why this was added????
    #def close(self):
    #    QCoreApplication.instance().quit()

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
