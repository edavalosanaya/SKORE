# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_dialog_tab.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")

        #new
        Dialog.resize(530, 679)


        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)

        #new
        self.buttonBox.setGeometry(QtCore.QRect(310, 630, 201, 32))


        self.buttonBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")

        #new
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 511, 611))
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setObjectName("tabWidget")
        self.path_tab = QtWidgets.QWidget()
        self.path_tab.setObjectName("path_tab")


        self.anthemscore_pushButton = QtWidgets.QPushButton(self.path_tab)
        self.anthemscore_pushButton.setGeometry(QtCore.QRect(400, 490, 93, 31))
        self.anthemscore_pushButton.setObjectName("anthemscore_pushButton")
        self.anthemscore_lineEdit = QtWidgets.QLineEdit(self.path_tab)
        self.anthemscore_lineEdit.setGeometry(QtCore.QRect(10, 490, 381, 31))
        self.anthemscore_lineEdit.setObjectName("anthemscore_lineEdit")
        self.audacity_lineEdit = QtWidgets.QLineEdit(self.path_tab)
        self.audacity_lineEdit.setGeometry(QtCore.QRect(10, 430, 381, 31))
        self.audacity_lineEdit.setObjectName("audacity_lineEdit")
        self.pianobooster_pushButton = QtWidgets.QPushButton(self.path_tab)
        self.pianobooster_pushButton.setGeometry(QtCore.QRect(400, 250, 93, 31))
        self.pianobooster_pushButton.setObjectName("pianobooster_pushButton")
        self.midiSheetMusic_pushButton = QtWidgets.QPushButton(self.path_tab)
        self.midiSheetMusic_pushButton.setGeometry(QtCore.QRect(400, 310, 93, 31))
        self.midiSheetMusic_pushButton.setObjectName("midiSheetMusic_pushButton")
        self.audiveris_pushButton = QtWidgets.QPushButton(self.path_tab)
        self.audiveris_pushButton.setGeometry(QtCore.QRect(400, 70, 93, 31))
        self.audiveris_pushButton.setObjectName("audiveris_pushButton")
        self.anthemscore_label = QtWidgets.QLabel(self.path_tab)
        self.anthemscore_label.setGeometry(QtCore.QRect(10, 470, 191, 16))
        self.anthemscore_label.setObjectName("anthemscore_label")
        self.midiSheetMusic_lineEdit = QtWidgets.QLineEdit(self.path_tab)
        self.midiSheetMusic_lineEdit.setGeometry(QtCore.QRect(10, 310, 381, 31))
        self.midiSheetMusic_lineEdit.setObjectName("midiSheetMusic_lineEdit")
        self.midisheetmusic_label = QtWidgets.QLabel(self.path_tab)
        self.midisheetmusic_label.setGeometry(QtCore.QRect(10, 290, 141, 16))
        self.midisheetmusic_label.setObjectName("midisheetmusic_label")
        self.pianobooster_lineEdit = QtWidgets.QLineEdit(self.path_tab)
        self.pianobooster_lineEdit.setGeometry(QtCore.QRect(10, 250, 381, 31))
        self.pianobooster_lineEdit.setObjectName("pianobooster_lineEdit")
        self.pianobooster_label = QtWidgets.QLabel(self.path_tab)
        self.pianobooster_label.setGeometry(QtCore.QRect(10, 230, 121, 16))
        self.pianobooster_label.setObjectName("pianobooster_label")
        self.audacity_label = QtWidgets.QLabel(self.path_tab)
        self.audacity_label.setGeometry(QtCore.QRect(10, 410, 191, 16))
        self.audacity_label.setObjectName("audacity_label")
        self.reddotforever_label = QtWidgets.QLabel(self.path_tab)
        self.reddotforever_label.setGeometry(QtCore.QRect(10, 170, 131, 16))
        self.reddotforever_label.setObjectName("reddotforever_label")

        #new
        self.path_line = QtWidgets.QFrame(self.path_tab)
        self.path_line.setGeometry(QtCore.QRect(10, 30, 481, 20))
        self.path_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.path_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.path_line.setObjectName("path_line")


        self.audiveris_label = QtWidgets.QLabel(self.path_tab)
        self.audiveris_label.setGeometry(QtCore.QRect(10, 50, 101, 16))
        self.audiveris_label.setObjectName("audiveris_label")
        self.audacity_pushButton = QtWidgets.QPushButton(self.path_tab)
        self.audacity_pushButton.setGeometry(QtCore.QRect(400, 430, 93, 31))
        self.audacity_pushButton.setObjectName("audacity_pushButton")
        self.amazingmidi_lineEdit = QtWidgets.QLineEdit(self.path_tab)
        self.amazingmidi_lineEdit.setGeometry(QtCore.QRect(10, 130, 381, 31))
        self.amazingmidi_lineEdit.setObjectName("amazingmidi_lineEdit")
        self.amazingmidi_label = QtWidgets.QLabel(self.path_tab)
        self.amazingmidi_label.setGeometry(QtCore.QRect(10, 110, 121, 16))
        self.amazingmidi_label.setObjectName("amazingmidi_label")
        self.xenoplay_label = QtWidgets.QLabel(self.path_tab)
        self.xenoplay_label.setGeometry(QtCore.QRect(10, 350, 121, 16))
        self.xenoplay_label.setObjectName("xenoplay_label")
        self.configurePath_label = QtWidgets.QLabel(self.path_tab)
        self.configurePath_label.setGeometry(QtCore.QRect(10, 10, 231, 16))
        self.configurePath_label.setObjectName("configurePath_label")
        self.amazingmidi_pushButton = QtWidgets.QPushButton(self.path_tab)
        self.amazingmidi_pushButton.setGeometry(QtCore.QRect(400, 130, 93, 31))
        self.amazingmidi_pushButton.setObjectName("amazingmidi_pushButton")
        self.audiveris_lineEdit = QtWidgets.QLineEdit(self.path_tab)
        self.audiveris_lineEdit.setGeometry(QtCore.QRect(10, 70, 381, 31))
        self.audiveris_lineEdit.setObjectName("audiveris_lineEdit")
        self.xenoplay_lineEdit = QtWidgets.QLineEdit(self.path_tab)
        self.xenoplay_lineEdit.setGeometry(QtCore.QRect(10, 370, 381, 31))
        self.xenoplay_lineEdit.setObjectName("xenoplay_lineEdit")
        self.reddotforever_pushButton = QtWidgets.QPushButton(self.path_tab)
        self.reddotforever_pushButton.setGeometry(QtCore.QRect(400, 190, 93, 31))
        self.reddotforever_pushButton.setObjectName("reddotforever_pushButton")
        self.reddotforever_lineEdit = QtWidgets.QLineEdit(self.path_tab)
        self.reddotforever_lineEdit.setGeometry(QtCore.QRect(10, 190, 381, 31))
        self.reddotforever_lineEdit.setObjectName("reddotforever_lineEdit")
        self.xenoplay_pushButton = QtWidgets.QPushButton(self.path_tab)
        self.xenoplay_pushButton.setGeometry(QtCore.QRect(400, 370, 93, 31))
        self.xenoplay_pushButton.setObjectName("xenoplay_pushButton")

        #new
        self.mp3_2_midi_converter_label = QtWidgets.QLabel(self.path_tab)
        self.mp3_2_midi_converter_label.setGeometry(QtCore.QRect(10, 550, 141, 16))
        self.mp3_2_midi_converter_label.setObjectName("mp3_2_midi_converter_label")
        self.amazingmidi_radioButton = QtWidgets.QRadioButton(self.path_tab)
        self.amazingmidi_radioButton.setGeometry(QtCore.QRect(230, 550, 111, 20))
        self.amazingmidi_radioButton.setObjectName("amazingmidi_radioButton")
        self.anthemscore_radioButton = QtWidgets.QRadioButton(self.path_tab)
        self.anthemscore_radioButton.setGeometry(QtCore.QRect(390, 550, 111, 20))
        self.anthemscore_radioButton.setObjectName("anthemscore_radioButton")

        #new
        self.tabWidget.addTab(self.path_tab, "")
        self.tutor_tab = QtWidgets.QWidget()
        self.tutor_tab.setObjectName("tutor_tab")
        self.timing_line = QtWidgets.QFrame(self.tutor_tab)
        self.timing_line.setGeometry(QtCore.QRect(10, 420, 481, 20))
        self.timing_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.timing_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.timing_line.setObjectName("timing_line")
        self.timingsettings_label = QtWidgets.QLabel(self.tutor_tab)
        self.timingsettings_label.setGeometry(QtCore.QRect(210, 440, 101, 16))
        self.timingsettings_label.setObjectName("timingsettings_label")
        self.color_line = QtWidgets.QFrame(self.tutor_tab)
        self.color_line.setGeometry(QtCore.QRect(10, 210, 481, 20))
        self.color_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.color_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.color_line.setObjectName("color_line")
        self.colorsettings_label = QtWidgets.QLabel(self.tutor_tab)
        self.colorsettings_label.setGeometry(QtCore.QRect(210, 230, 81, 16))
        self.colorsettings_label.setObjectName("colorsettings_label")
        self.portsettings_label = QtWidgets.QLabel(self.tutor_tab)
        self.portsettings_label.setGeometry(QtCore.QRect(210, 10, 81, 20))
        self.portsettings_label.setObjectName("portsettings_label")
        self.pianoport_comboBox = QtWidgets.QComboBox(self.tutor_tab)
        self.pianoport_comboBox.setGeometry(QtCore.QRect(10, 50, 481, 31))
        self.pianoport_comboBox.setObjectName("pianoport_comboBox")
        self.pianoport_label = QtWidgets.QLabel(self.tutor_tab)
        self.pianoport_label.setGeometry(QtCore.QRect(10, 30, 71, 16))
        self.pianoport_label.setObjectName("pianoport_label")
        self.arduinoport_label = QtWidgets.QLabel(self.tutor_tab)
        self.arduinoport_label.setGeometry(QtCore.QRect(10, 150, 81, 16))
        self.arduinoport_label.setObjectName("arduinoport_label")
        self.arduinoport_comboBox = QtWidgets.QComboBox(self.tutor_tab)
        self.arduinoport_comboBox.setGeometry(QtCore.QRect(10, 170, 481, 31))
        self.arduinoport_comboBox.setObjectName("arduinoport_comboBox")
        self.whitekey_label = QtWidgets.QLabel(self.tutor_tab)
        self.whitekey_label.setGeometry(QtCore.QRect(20, 250, 121, 16))
        self.whitekey_label.setObjectName("whitekey_label")
        self.blackkey_label = QtWidgets.QLabel(self.tutor_tab)
        self.blackkey_label.setGeometry(QtCore.QRect(20, 340, 121, 16))
        self.blackkey_label.setObjectName("blackkey_label")
        self.whitekey_r_label = QtWidgets.QLabel(self.tutor_tab)
        self.whitekey_r_label.setGeometry(QtCore.QRect(20, 290, 21, 16))
        self.whitekey_r_label.setObjectName("whitekey_r_label")
        self.blackkey_r_label = QtWidgets.QLabel(self.tutor_tab)
        self.blackkey_r_label.setGeometry(QtCore.QRect(20, 380, 21, 16))
        self.blackkey_r_label.setObjectName("blackkey_r_label")
        self.whitekey_g_label = QtWidgets.QLabel(self.tutor_tab)
        self.whitekey_g_label.setGeometry(QtCore.QRect(100, 290, 21, 16))
        self.whitekey_g_label.setObjectName("whitekey_g_label")
        self.blackkey_g_label = QtWidgets.QLabel(self.tutor_tab)
        self.blackkey_g_label.setGeometry(QtCore.QRect(100, 380, 21, 16))
        self.blackkey_g_label.setObjectName("blackkey_g_label")
        self.whitekey_b_label = QtWidgets.QLabel(self.tutor_tab)
        self.whitekey_b_label.setGeometry(QtCore.QRect(180, 290, 21, 16))
        self.whitekey_b_label.setObjectName("whitekey_b_label")
        self.blackkey_b_label = QtWidgets.QLabel(self.tutor_tab)
        self.blackkey_b_label.setGeometry(QtCore.QRect(180, 380, 21, 16))
        self.blackkey_b_label.setObjectName("blackkey_b_label")
        self.whitekey_r_lineEdit = QtWidgets.QLineEdit(self.tutor_tab)
        self.whitekey_r_lineEdit.setGeometry(QtCore.QRect(40, 290, 51, 22))
        self.whitekey_r_lineEdit.setObjectName("whitekey_r_lineEdit")
        self.whitekey_g_lineEdit = QtWidgets.QLineEdit(self.tutor_tab)
        self.whitekey_g_lineEdit.setGeometry(QtCore.QRect(120, 290, 51, 22))
        self.whitekey_g_lineEdit.setObjectName("whitekey_g_lineEdit")
        self.whitekey_b_lineEdit = QtWidgets.QLineEdit(self.tutor_tab)
        self.whitekey_b_lineEdit.setGeometry(QtCore.QRect(200, 290, 51, 22))
        self.whitekey_b_lineEdit.setObjectName("whitekey_b_lineEdit")
        self.blackkey_r_lineEdit = QtWidgets.QLineEdit(self.tutor_tab)
        self.blackkey_r_lineEdit.setGeometry(QtCore.QRect(40, 380, 51, 22))
        self.blackkey_r_lineEdit.setObjectName("blackkey_r_lineEdit")
        self.blackkey_g_lineEdit = QtWidgets.QLineEdit(self.tutor_tab)
        self.blackkey_g_lineEdit.setGeometry(QtCore.QRect(120, 380, 51, 22))
        self.blackkey_g_lineEdit.setObjectName("blackkey_g_lineEdit")
        self.blackkey_b_lineEdit = QtWidgets.QLineEdit(self.tutor_tab)
        self.blackkey_b_lineEdit.setGeometry(QtCore.QRect(200, 380, 51, 22))
        self.blackkey_b_lineEdit.setObjectName("blackkey_b_lineEdit")
        self.whitekey_colorwheel_pushButton = QtWidgets.QPushButton(self.tutor_tab)
        self.whitekey_colorwheel_pushButton.setGeometry(QtCore.QRect(340, 290, 121, 21))
        self.whitekey_colorwheel_pushButton.setObjectName("whitekey_colorwheel_pushButton")
        self.blackkey_colorwheel_pushButton = QtWidgets.QPushButton(self.tutor_tab)
        self.blackkey_colorwheel_pushButton.setGeometry(QtCore.QRect(340, 380, 121, 21))
        self.blackkey_colorwheel_pushButton.setObjectName("blackkey_colorwheel_pushButton")
        self.colorwheel_label = QtWidgets.QLabel(self.tutor_tab)
        self.colorwheel_label.setGeometry(QtCore.QRect(360, 250, 81, 16))
        self.colorwheel_label.setObjectName("colorwheel_label")
        self.timeperticks_label = QtWidgets.QLabel(self.tutor_tab)
        self.timeperticks_label.setGeometry(QtCore.QRect(20, 470, 91, 16))
        self.timeperticks_label.setObjectName("timeperticks_label")
        self.chordtimingtolerance_label = QtWidgets.QLabel(self.tutor_tab)
        self.chordtimingtolerance_label.setGeometry(QtCore.QRect(20, 510, 151, 16))
        self.chordtimingtolerance_label.setObjectName("chordtimingtolerance_label")
        self.manualfinalchordsustaintiming_label = QtWidgets.QLabel(self.tutor_tab)
        self.manualfinalchordsustaintiming_label.setGeometry(QtCore.QRect(20, 550, 211, 16))
        self.manualfinalchordsustaintiming_label.setObjectName("manualfinalchordsustaintiming_label")
        self.timeperticks_lineEdit = QtWidgets.QLineEdit(self.tutor_tab)
        self.timeperticks_lineEdit.setGeometry(QtCore.QRect(250, 470, 241, 22))
        self.timeperticks_lineEdit.setObjectName("timeperticks_lineEdit")
        self.chordtimingtolerance_lineEdit = QtWidgets.QLineEdit(self.tutor_tab)
        self.chordtimingtolerance_lineEdit.setGeometry(QtCore.QRect(250, 510, 241, 22))
        self.chordtimingtolerance_lineEdit.setObjectName("chordtimingtolerance_lineEdit")
        self.manualfinalchordsustaintiming_lineEdit = QtWidgets.QLineEdit(self.tutor_tab)
        self.manualfinalchordsustaintiming_lineEdit.setGeometry(QtCore.QRect(250, 550, 241, 22))
        self.manualfinalchordsustaintiming_lineEdit.setObjectName("manualfinalchordsustaintiming_lineEdit")
        self.pianosize_label = QtWidgets.QLabel(self.tutor_tab)
        self.pianosize_label.setGeometry(QtCore.QRect(10, 90, 71, 16))
        self.pianosize_label.setObjectName("pianosize_label")
        self.pianosize_comboBox = QtWidgets.QComboBox(self.tutor_tab)
        self.pianosize_comboBox.setGeometry(QtCore.QRect(10, 111, 231, 31))
        self.pianosize_comboBox.setObjectName("pianosize_comboBox")
        self.pianosize_pushButton = QtWidgets.QPushButton(self.tutor_tab)
        self.pianosize_pushButton.setGeometry(QtCore.QRect(270, 110, 221, 31))
        self.pianosize_pushButton.setObjectName("pianosize_pushButton")
        self.tabWidget.addTab(self.tutor_tab, "")

        self.retranslateUi(Dialog)

        #new
        self.tabWidget.setCurrentIndex(0)


        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Settings"))
        self.anthemscore_pushButton.setText(_translate("Dialog", "Browse"))
        self.pianobooster_pushButton.setText(_translate("Dialog", "Browse"))
        self.midiSheetMusic_pushButton.setText(_translate("Dialog", "Browse"))
        self.audiveris_pushButton.setText(_translate("Dialog", "Browse"))
        self.anthemscore_label.setText(_translate("Dialog", "AnthemScore [.exe] (Optional)"))
        self.midisheetmusic_label.setText(_translate("Dialog", "Midi Sheet Music [.exe]"))
        self.pianobooster_label.setText(_translate("Dialog", "PianoBooster [.exe]"))
        self.audacity_label.setText(_translate("Dialog", "Audacity [.exe]"))
        self.reddotforever_label.setText(_translate("Dialog", "Red Dot Forever [.exe]"))
        self.audiveris_label.setText(_translate("Dialog", "Audiveris [folder]"))
        self.audacity_pushButton.setText(_translate("Dialog", "Browse"))
        self.amazingmidi_label.setText(_translate("Dialog", "AmazingMIDI [.exe]"))
        self.xenoplay_label.setText(_translate("Dialog", "Xenoplay [.jar]"))
        self.configurePath_label.setText(_translate("Dialog", "Configure that path for each program."))
        self.amazingmidi_pushButton.setText(_translate("Dialog", "Browse"))
        self.reddotforever_pushButton.setText(_translate("Dialog", "Browse"))
        self.xenoplay_pushButton.setText(_translate("Dialog", "Browse"))
        self.mp3_2_midi_converter_label.setText(_translate("Dialog", "MP3 to MIDI Converter:"))
        self.amazingmidi_radioButton.setText(_translate("Dialog", "AmazingMIDI"))
        self.anthemscore_radioButton.setText(_translate("Dialog", "AnthemScore"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.path_tab), _translate("Dialog", "Path Settings"))
        self.timingsettings_label.setText(_translate("Dialog", "Timing Settings"))
        self.colorsettings_label.setText(_translate("Dialog", "Color Settings"))
        self.portsettings_label.setText(_translate("Dialog", "Port Settings"))
        self.pianoport_label.setText(_translate("Dialog", "Piano Port"))
        self.arduinoport_label.setText(_translate("Dialog", "Arduino Port"))
        self.whitekey_label.setText(_translate("Dialog", "White Key LED Color"))
        self.blackkey_label.setText(_translate("Dialog", "Black Key LED Color"))
        self.whitekey_r_label.setText(_translate("Dialog", "R:"))
        self.blackkey_r_label.setText(_translate("Dialog", "R:"))
        self.whitekey_g_label.setText(_translate("Dialog", "G:"))
        self.blackkey_g_label.setText(_translate("Dialog", "G:"))
        self.whitekey_b_label.setText(_translate("Dialog", "B:"))
        self.blackkey_b_label.setText(_translate("Dialog", "B:"))
        self.whitekey_colorwheel_pushButton.setText(_translate("Dialog", "White Key Selection"))
        self.blackkey_colorwheel_pushButton.setText(_translate("Dialog", "Black Key Selection"))
        self.colorwheel_label.setText(_translate("Dialog", "Color Wheel"))
        self.timeperticks_label.setText(_translate("Dialog", "Time per Ticks:"))
        self.chordtimingtolerance_label.setText(_translate("Dialog", "Chord Timing Tolerance:"))
        self.manualfinalchordsustaintiming_label.setText(_translate("Dialog", "Manual Final Chord Sustain Timing: "))
        self.pianosize_label.setText(_translate("Dialog", "Piano Size"))
        self.pianosize_pushButton.setText(_translate("Dialog", "Piano Size Calibration"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tutor_tab), _translate("Dialog", "Tutoring Settings"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
