from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QAction, QMainWindow, QInputDialog, QLineEdit, QFileDialog, QMessageBox, QLabel, QProgressBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import sys
import time
from skore_program_controller import *

class ProgressBarDialog(QtWidgets.QDialog):

    def __init__(self):
        super(QtWidgets.QDialog, self).__init__()
        self.init_dialog()

    def init_dialog(self):
        self.setObjectName("ProgressBarDialog")
        self.resize(350,150)
        print("Initializing Progress Bar Dialog")
        self.setWindowTitle("Progress Bar")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.relocate()


        self.progress = QProgressBar(self)
        self.progress.setGeometry(60,40,270,25)

        self.current_action_label = QtWidgets.QLabel(self)
        self.current_action_label.setGeometry(QtCore.QRect(60,70,270,25))
        self.current_action_label.setObjectName("current_action_label")
        self.current_action_label.setText("Current Action: None")

        #self.quit_pushButton = QPushButton("Quit",self)
        #self.quit_pushButton.setGeometry(193,100,100,30)

        print("Finished Initializing Progress Bar Dialog")

        #self.show()

    def relocate(self):
        # Relocates the ProgressBarDialog in the center of the fourth quadrant
        # of the screen. This is to ensure that the ProgressBarDialog does not
        # affect the image processing to click the buttons.

        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        x_center = centerPoint.x()
        y_center = centerPoint.y()
        x_desired = int(x_center + x_center/2)
        y_desired = int(y_center + y_center/2)
        centerPoint.setX(x_desired)
        centerPoint.setY(y_desired)
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        return

"""
#Initializing Live Settings UI
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = ProgressBarDialog()
    app.exec_()
"""
