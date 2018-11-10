from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# General Utility
import win32api
import psutil
import time
import inspect
import pywinauto
import sys
from pywinauto.controls.win32_controls import ButtonWrapper
from time import sleep
import os
import warnings

app = QtWidgets.QApplication(sys.argv)

my_message_box = QMessageBox()
my_message_box.setParent(None)
my_message_box.setWindowTitle("Filter Control")
my_message_box.setText("Please select the desired filtering and continue")
my_message_box.setWindowFlag(Qt.WindowStaysOnTopHint)
#my_message_box.show()
my_message_box.exec_()
#my_message_box.about(None, "Filter Control", "Please select the desired filtering and continue")

#my_message_box.raise()
#my_message_box.show()


sys.exit(app.exec_())
