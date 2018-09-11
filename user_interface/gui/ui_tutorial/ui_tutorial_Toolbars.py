from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QAction, QStatusBar
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "PyQt5 Toolbars"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500
        self.setWindowIcon(QtGui.QIcon(r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\gui\ui_tutorial\icon\window_icon.jpg"))

        self.InitWindow()


    def InitWindow(self):

        exitAct = QAction(QIcon(r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\gui\ui_tutorial\icon\exit.png"), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(self.CloseApp)

        copyAct = QAction(QIcon(r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\gui\ui_tutorial\icon\copy.png"), 'Copy', self)
        copyAct.setShortcut('Ctrl+C')

        pasteAct = QAction(QIcon(r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\gui\ui_tutorial\icon\paste.png"), 'Paste', self)
        pasteAct.setShortcut('Ctrl+V')

        deleteAct = QAction(QIcon(r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\gui\ui_tutorial\icon\delete.png"), 'Delete', self)
        deleteAct.setShortcut('Ctrl+D')

        saveAct = QAction(QIcon(r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\gui\ui_tutorial\icon\save.png"), 'Save', self)
        saveAct.setShortcut('Ctrl+S')

        self.toolbar = self.addToolBar('Toolbar')

        self.toolbar.addAction(exitAct)
        self.toolbar.addAction(copyAct)
        self.toolbar.addAction(pasteAct)
        self.toolbar.addAction(deleteAct)
        self.toolbar.addAction(saveAct)

        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def CloseApp(self):
        self.close()



App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
