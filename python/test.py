from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QFrame, QPushButton
from PyQt5.QtCore import QRect, QPropertyAnimation
import sys

"""
class Example(QWidget):

    def __init__(self):
        super().__init__()


        self.initUI()

    def initUI(self):

        self.button = QPushButton("Start", self)
        self.button.clicked.connect(self.doAnim)
        self.button.move(30, 30)

        self.frame = QFrame(self)
        self.frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.frame.setGeometry(150, 30, 100, 100)

        self.setGeometry(300, 300, 380, 300)
        self.setWindowTitle('Animation')
        self.show()


    def doAnim(self):

        effect = QtWidgets.QGraphicsColorizeEffect(self)
        self.button.setGraphicsEffect(effect)

        self.animation = QtCore.QPropertyAnimation(effect, b'color')
        self.animation.setStartValue(QtGui.QColor(50,50,50))
        self.animation.setKeyValueAt(0.5,QtGui.QColor(0,255,0))
        self.animation.setEndValue(QtGui.QColor(50,50,50))

        #self.animation.setLoopCount(5)
        #self.animation.setDuration('infinite')
        self.animation.start()

if __name__ == "__main__":

    app = QApplication([])
    ex = Example()
    ex.show()
    app.exec_()
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class BlinkButton(QPushButton):
    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        self.default_color = self.getColor()

    def getColor(self):
        return self.palette().color(QPalette.Button)

    def setColor(self, value):
        if value == self.getColor():
            return
        palette = self.palette()
        palette.setColor(self.backgroundRole(), value)
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def reset_color(self):
        self.setColor(self.default_color)

    color = pyqtProperty(QColor, getColor, setColor)


class Widget(QWidget):

    def __init__(self):
        super(Widget, self).__init__()

        self.resize(300,200)
        layout = QVBoxLayout(self)

        self.button_stop = BlinkButton("Stop")
        layout.addWidget(self.button_stop)

        self.button_start = QPushButton("Start", self)
        layout.addWidget(self.button_start)

        self.animation = QPropertyAnimation(self.button_stop, b"color", self)
        self.animation.setDuration(1000)
        self.animation.setLoopCount(100)
        self.animation.setStartValue(self.button_stop.default_color)
        self.animation.setEndValue(self.button_stop.default_color)
        self.animation.setKeyValueAt(0.1, QColor(0,255,0))

        self.button_start.clicked.connect(self.animation.start)
        self.button_stop.clicked.connect(self.stop)

    def stop(self):
        self.animation.stop()
        self.button_stop.reset_color()

if __name__ == "__main__":
    app = QApplication([])
    w = Widget()
    w.show()
    app.exec_()
