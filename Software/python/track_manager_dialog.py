from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

#-------------------------------------------------------------------------------

class TrackManagerDialog(QtWidgets.QDialog):

    finished_and_transmit_data_signal = QtCore.pyqtSignal('QString')

    def __init__(self, note_tracks, parent = None):

        self.note_tracks = note_tracks

        QtWidgets.QDialog.__init__(self, parent)
        self.setObjectName("TrackManagerDialog")
        self.resize(289, 306)
        self.setWindowTitle("Track Manager")

        self.setup_ui()
        self.setup_func()

        return None

    def setup_ui(self):

        self.buttonBox_close = QtWidgets.QDialogButtonBox(self)
        self.buttonBox_close.setGeometry(QtCore.QRect(75, 260, 191, 32))
        self.buttonBox_close.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)

        self.listWidget_tracks = QtWidgets.QListWidget(self)
        self.listWidget_tracks.setGeometry(QtCore.QRect(20, 60, 251, 192))
        self.listWidget_tracks.setObjectName("listWidget_tracks")

        self.listWidget_tracks.setSelectionMode(2)

        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(20, 40, 251, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.label_title = QtWidgets.QLabel(self)
        self.label_title.setGeometry(QtCore.QRect(20, 20, 251, 16))
        self.label_title.setObjectName("label_title")

        self.retranslate_ui()
        self.buttonBox_close.clicked.connect(self.update_and_close)
        QtCore.QMetaObject.connectSlotsByName(self)

    def setup_func(self):

        self.list_item_track = {}
        self.tracks_selected_labels = {}

        for track in self.note_tracks:
            self.list_item_track[track.name] = QListWidgetItem(track.name)
            self.tracks_selected_labels[track.name] = False
            self.listWidget_tracks.addItem(self.list_item_track[track.name])

            if track.played is True:
                self.list_item_track[track.name].setSelected(True)
                self.tracks_selected_labels[track.name] = True

        return None

    def update_and_close(self):
        print("update and close")

        for track_name, list_item in self.list_item_track.items():
            self.tracks_selected_labels[track_name] = list_item.isSelected()

        self.finished_and_transmit_data_signal.emit(str(self.tracks_selected_labels))

        self.close()
        return None

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_title.setText(_translate("Dialog", "Select the tracks you wish to play."))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = TrackManagerDialog()
    ui.show()
    sys.exit(app.exec_())
