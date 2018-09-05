from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton
import sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "PyQt5 Window"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500
        self.setWindowIcon(QtGui.QIcon("window_icon.jpg"))

        button = QPushButton("AboutBox",self)
        button.move(200,200)

        button2 = QPushButton("QuestionMessage", self)
        button2.move(100,100)

        button.clicked.connect(self.AboutMessage)
        button2.clicked.connect(self.QuestionMessage)

        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def AboutMessage(self):
        QMessageBox.about(self, "About Message", "This Is About Message Box")


    def QuestionMessage(self):
        message = QMessageBox.question(self, "Question Message", "Have You Subscribed My Channel?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if message == QMessageBox.Yes:
            print("Yes I Have Subscribed")

        else:
            print("No I Have Not Subscribed")

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
