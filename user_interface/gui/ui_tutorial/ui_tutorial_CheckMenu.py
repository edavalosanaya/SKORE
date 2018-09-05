from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QAction, QStatusBar
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

        self.InitWindow()


    def InitWindow(self):

        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Message Is Ready")

        menubar = self.menuBar()
        viewMenu = menubar.addMenu("View")

        viewAction = QAction("View Status", self, checkable = True)
        viewAction.setStatusTip("View StatusBar")
        viewAction.setChecked(True)
        viewAction.triggered.connect(self.toggleMenu)

        viewMenu.addAction(viewAction)

        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()


    def toggleMenu(self, state):
        if state:
            self.statusbar.show()
        else:
            self.statusbar.hide()



App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
