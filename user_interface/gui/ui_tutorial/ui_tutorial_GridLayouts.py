from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QAction, QStatusBar, QDialog, QGroupBox, QPushButton, QVBoxLayout, QGridLayout
import sys


class Window(QDialog):
    def __init__(self):
        super().__init__()

        self.title = "PyQt5 GridLayout"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500

        self.InitWindow()


    def InitWindow(self):

        self.setWindowIcon(QtGui.QIcon(r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\gui\ui_tutorial\icon\window_icon.jpg"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.gridLayoutCreation()
        vboxlayout = QVBoxLayout()
        vboxlayout.addWidget(self.groupBox)
        self.setLayout(vboxlayout)
        self.show()

    def gridLayoutCreation(self):
        self.groupBox = QGroupBox("Grid Layout Example")
        gridLayout = QGridLayout()

        gridLayout.addWidget(QPushButton('1'), 0, 0)
        gridLayout.addWidget(QPushButton('2') ,0 ,1)
        gridLayout.addWidget(QPushButton('3') ,0 ,2)

        gridLayout.addWidget(QPushButton('4') ,1 ,0)
        gridLayout.addWidget(QPushButton('5') ,1 ,1)
        gridLayout.addWidget(QPushButton('6') ,1 ,2)

        self.groupBox.setLayout(gridLayout)

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
