from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QAction, QStatusBar, QLabel
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "PyQt5 Positioning"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500
        self.setWindowIcon(QtGui.QIcon(r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\gui\ui_tutorial\icon\window_icon.jpg"))

        self.InitWindow()


    def InitWindow(self):

        self.label1 = QLabel("Please", self)
        self.label1.move(50,50)

        self.label2 = QLabel("Subscribe", self)
        self.label2.move(100,100)

        self.label3 = QLabel("To My", self)
        self.label3.move(150,150)

        self.label4 = QLabel("Stupid Channel", self)
        self.label4.move(200,200)

        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()



App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
