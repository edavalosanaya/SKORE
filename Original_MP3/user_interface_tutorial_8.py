#Signal and SLots Tutorial

import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QToolTip, QMessageBox
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
        #button.clicked.connect(self.Close_Clicked)
        button.clicked.connect(self.CloseApp)

        #To initilize the window
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

#    def Close_Clicked(self):
#        QCoreApplication.instance().quit()

    def CloseApp(self):
        reply = QMessageBox.question(self, "Close Message", "Are you sure to close window", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if(reply == QMessageBox.Yes):
            self.close()


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
