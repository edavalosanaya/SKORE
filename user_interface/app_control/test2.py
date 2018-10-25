import sys
from PyQt5.QtWidgets import QApplication

from PyQt5.QtWidgets import QSlider, QDialog, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

from PyQt5.QtWidgets import QDialog, QProgressBar, QLabel, QHBoxLayout
from PyQt5.QtCore import pyqtSlot

class Slider_Dialog(QDialog):

    changedValue = pyqtSignal(int)

    def __init__(self):
        super(Slider_Dialog, self).__init__()
        self.init_ui()

    def init_ui(self):
        # Creating a label
        self.sliderLabel = QLabel('Slider:', self)

        # Creating a slider and setting its maximum and minimum value
        self.slider = QSlider(self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setOrientation(Qt.Horizontal)

        # Creating a horizontalBoxLayout
        self.hboxLayout = QHBoxLayout(self)

        # Adding the widgets
        self.hboxLayout.addWidget(self.sliderLabel)
        self.hboxLayout.addWidget(self.slider)

        # Setting main layout
        self.setLayout(self.hboxLayout)

        # Setting a connection between slider position change and on_changed_value function we created earlier
        self.slider.valueChanged.connect(self.on_changed_value)

        self.setWindowTitle("Dialog with a Slider")
        self.show()

    def on_changed_value(self, value):
        self.changedValue.emit(value)

class ProgressBar_Dialog(QDialog):

    def __init__(self):
        super(ProgressBar_Dialog ,self).__init__()
        self.init_ui()

    def init_ui(self):
        # Creating a label
        self.progressLabel = QLabel('Progress Bar:', self)

        # Creating a progress bar and setting the value limits
        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximum(100)
        self.progressBar.setMinimum(0)

        # Creating a Horizontal Layout to add all the widgets
        self.hboxLayout = QHBoxLayout(self)

        # Adding the widgets
        self.hboxLayout.addWidget(self.progressLabel)
        self.hboxLayout.addWidget(self.progressBar)

        # Setting the hBoxLayout as the main layout
        self.setLayout(self.hboxLayout)
        self.setWindowTitle('Dialog with Progressbar')

        self.show()

    @pyqtSlot(int)
    def get_slider_value(self, val):
        self.progressBar.setValue(val)

    def make_connection(self, slider_object):
        slider_object.changedValue.connect(self.get_slider_value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sd = Slider_Dialog()
    pb = ProgressBar_Dialog()
    # Making the connection
    pb.make_connection(sd)
    sys.exit(app.exec_())
