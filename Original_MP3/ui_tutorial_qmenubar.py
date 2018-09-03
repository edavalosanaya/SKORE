import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QAction
from PyQt5.QtGui import QIcon

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "QMenuBar"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500
        self.setWindowIcon(QtGui.QIcon("window_icon.jpg"))

        self.InitWindow()

    def InitWindow(self):
        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu("File")

        exitButton = QAction(QIcon("exit.png"), 'Exit', self)
        exitButton.setShortcut("Ctrl+E")
        exitButton.setStatusTip("Exit Application")
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        viewMenu = mainMenu.addMenu("View")
        editMenu = mainMenu.addMenu("Edit")
        searchMenu = mainMenu.addMenu("Search")
        toolMenu = mainMenu.addMenu("Tool")
        helpMenu = mainMenu.addMenu("Help")

        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec())
