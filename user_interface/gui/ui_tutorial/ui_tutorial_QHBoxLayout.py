from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QAction, QStatusBar, QDialog, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout, QGroupBox
import sys


class Window(QDialog):
    def __init__(self):
        super().__init__()

        self.title = "PyQt5 Layouts"
        self.top = 100
        self.left = 100
        self.width = 300
        self.height = 100


        self.InitWindow()


    def InitWindow(self):

        self.setWindowIcon(QtGui.QIcon(r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\gui\ui_tutorial\icon\window_icon.jpg"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.HorizontalLayout()

        vBox = QVBoxLayout()
        vBox.addWidget(self.groupBox)
        self.setLayout(vBox)

        self.show()

    def HorizontalLayout(self):
        self.groupBox = QGroupBox("What is your favorite sport?")
        hBoxlayout = QHBoxLayout()

        button1 = QPushButton("Football", self)
        button1.clicked.connect(self.button1Clicked)
        hBoxlayout.addWidget(button1)

        button2 = QPushButton("Cricket", self)
        button2.clicked.connect(self.button2Clicked)
        hBoxlayout.addWidget(button2)

        button3 = QPushButton("Tennis", self)
        button3.clicked.connect(self.button3Clicked)
        hBoxlayout.addWidget(button3)

        self.groupBox.setLayout(hBoxlayout)

    def button1Clicked(self):
        QMessageBox.information(self, "Footbal", "Yes I like Footbal")

    def button2Clicked(self):
        QMessageBox.information(self, "Cricket", "Yes I like Cricket")

    def button3Clicked(self):
        QMessageBox.information(self, "Tennis", "Yes I like Tennis")

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
