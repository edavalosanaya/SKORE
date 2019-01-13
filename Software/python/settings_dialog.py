# General Utility Libraries
import sys
import os
import warnings

# PyQt5, GUI LIbrary
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QAction, QMainWindow, QInputDialog, QLineEdit, QFileDialog, QMessageBox, QLabel, QButtonGroup, QDialogButtonBox, QColorDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

# Serial and Midi Port LIbrary
import rtmidi
import serial
import serial.tools.list_ports

# CRUCIAL!! This ensures that any dialog open within other .py files that import
# settings_dialog can open without crashing the entire application
warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2

# SKORE Library
from skore_lib import setting_read, setting_write

#-------------------------------------------------------------------------------
# PyQt5 Classes

class ArduinoComboBox(QtWidgets.QComboBox):
    # This class allows the combobox to recognize arduinos connected as soon as
    # the user clicks the combobox

    def avaliable_arduino_com(self):
        # This fuction returns all the available COM ports in a list of strings.
        ports = serial.tools.list_ports.comports(include_links=False)
        results = []
        for port in ports:
            #print(port.device)
            results.append(str(port.device))
        return results

    def showPopup(self):
        avaliable_arduino_ports = self.avaliable_arduino_com()
        #print(avaliable_arduino_ports)
        self.clear()
        for avaliable_port in avaliable_arduino_ports:
            self.addItem(avaliable_port)
        super(ArduinoComboBox, self).showPopup()


class PianoComboBox(QtWidgets.QComboBox):
    # This class allows the combobox to recognize piano connected as soon as the
    # user clicks the combobox

    def avaliable_piano_port(self):
        # This function returns all the available MIDI ports in a list of string.
        temp_midi_in = []

        temp_midi_in = rtmidi.MidiIn()

        avaliable_ports = temp_midi_in.get_ports()
        #print("Avaliable Ports:")

        results = []
        for port_name in avaliable_ports:
            #print(port_name)
            results.append(str(port_name))
        return results

    def showPopup(self):
        avaliable_piano_ports = self.avaliable_piano_port()
        #print(avaliable_piano_ports)
        self.clear()
        for avaliable_piano_port_connected in avaliable_piano_ports:
            self.addItem(avaliable_piano_port_connected)
        super(PianoComboBox, self).showPopup()


class SettingsDialog(QtWidgets.QDialog):

    def __init__(self):
        super(QtWidgets.QDialog, self).__init__()
        self.setui_dialog()

    def setui_dialog(self):
        self.setWindowTitle("SKORE Settings")
        self.setStyleSheet("""
            background-color: rgb(50,50,50);
            color: white;
            """)
        self.setObjectName("SettingsDialog")
        self.resize(530, 679)

        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(310, 630, 201, 32))
        self.buttonBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 511, 611))
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setObjectName("tabWidget")
        self.path_tab = QtWidgets.QWidget()
        self.path_tab.setObjectName("path_tab")

        #-----------------------------------------------------------------------
        # Path Tab
        # Path Settings within Path Tab

        self.anthemscore_pushButton = QtWidgets.QPushButton(self.path_tab)
        self.anthemscore_pushButton.setGeometry(QtCore.QRect(400, 380, 93, 31))
        self.anthemscore_pushButton.setObjectName("anthemscore_pushButton")
        self.anthemscore_lineEdit = QtWidgets.QLineEdit(self.path_tab)
        self.anthemscore_lineEdit.setGeometry(QtCore.QRect(10, 380, 381, 31))
        self.anthemscore_lineEdit.setObjectName("anthemscore_lineEdit")
        self.pianobooster_pushButton = QtWidgets.QPushButton(self.path_tab)
        self.pianobooster_pushButton.setGeometry(QtCore.QRect(400, 260, 93, 31))
        self.pianobooster_pushButton.setObjectName("pianobooster_pushButton")
        self.audiveris_pushButton = QtWidgets.QPushButton(self.path_tab)
        self.audiveris_pushButton.setGeometry(QtCore.QRect(400, 80, 93, 31))
        self.audiveris_pushButton.setObjectName("audiveris_pushButton")
        self.anthemscore_label = QtWidgets.QLabel(self.path_tab)
        self.anthemscore_label.setGeometry(QtCore.QRect(10, 360, 191, 16))
        self.anthemscore_label.setObjectName("anthemscore_label")
        self.pianobooster_lineEdit = QtWidgets.QLineEdit(self.path_tab)
        self.pianobooster_lineEdit.setGeometry(QtCore.QRect(10, 260, 381, 31))
        self.pianobooster_lineEdit.setObjectName("pianobooster_lineEdit")
        self.pianobooster_label = QtWidgets.QLabel(self.path_tab)
        self.pianobooster_label.setGeometry(QtCore.QRect(10, 240, 121, 16))
        self.pianobooster_label.setObjectName("pianobooster_label")
        self.reddotforever_label = QtWidgets.QLabel(self.path_tab)
        self.reddotforever_label.setGeometry(QtCore.QRect(10, 180, 131, 16))
        self.reddotforever_label.setObjectName("reddotforever_label")
        self.path_line = QtWidgets.QFrame(self.path_tab)
        self.path_line.setGeometry(QtCore.QRect(10, 30, 481, 20))
        self.path_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.path_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.path_line.setObjectName("path_line")
        self.audiveris_label = QtWidgets.QLabel(self.path_tab)
        self.audiveris_label.setGeometry(QtCore.QRect(10, 60, 101, 16))
        self.audiveris_label.setObjectName("audiveris_label")
        self.amazingmidi_lineEdit = QtWidgets.QLineEdit(self.path_tab)
        self.amazingmidi_lineEdit.setGeometry(QtCore.QRect(10, 140, 381, 31))
        self.amazingmidi_lineEdit.setObjectName("amazingmidi_lineEdit")
        self.amazingmidi_label = QtWidgets.QLabel(self.path_tab)
        self.amazingmidi_label.setGeometry(QtCore.QRect(10, 120, 121, 16))
        self.amazingmidi_label.setObjectName("amazingmidi_label")
        self.configurePath_label = QtWidgets.QLabel(self.path_tab)
        self.configurePath_label.setGeometry(QtCore.QRect(10, 10, 231, 16))
        self.configurePath_label.setObjectName("configurePath_label")
        self.amazingmidi_pushButton = QtWidgets.QPushButton(self.path_tab)
        self.amazingmidi_pushButton.setGeometry(QtCore.QRect(400, 140, 93, 31))
        self.amazingmidi_pushButton.setObjectName("amazingmidi_pushButton")
        self.audiveris_lineEdit = QtWidgets.QLineEdit(self.path_tab)
        self.audiveris_lineEdit.setGeometry(QtCore.QRect(10, 80, 381, 31))
        self.audiveris_lineEdit.setObjectName("audiveris_lineEdit")
        self.reddotforever_pushButton = QtWidgets.QPushButton(self.path_tab)
        self.reddotforever_pushButton.setGeometry(QtCore.QRect(400, 200, 93, 31))
        self.reddotforever_pushButton.setObjectName("reddotforever_pushButton")
        self.reddotforever_lineEdit = QtWidgets.QLineEdit(self.path_tab)
        self.reddotforever_lineEdit.setGeometry(QtCore.QRect(10, 200, 381, 31))
        self.reddotforever_lineEdit.setObjectName("reddotforever_lineEdit")
        self.muse_score_label = QtWidgets.QLabel(self.path_tab)
        self.muse_score_label.setGeometry(QtCore.QRect(10, 300, 121, 16))
        self.muse_score_label.setObjectName("muse_score_label")
        self.muse_score_lineEdit = QtWidgets.QLineEdit(self.path_tab)
        self.muse_score_lineEdit.setGeometry(QtCore.QRect(10, 320, 381, 31))
        self.muse_score_lineEdit.setObjectName("muse_score_lineEdit")
        self.muse_score_pushButton = QtWidgets.QPushButton(self.path_tab)
        self.muse_score_pushButton.setGeometry(QtCore.QRect(400, 320, 93, 31))
        self.muse_score_pushButton.setObjectName("muse_score_pushButton")

        self.browse_button_group = QButtonGroup()
        self.browse_button_group.addButton(self.audiveris_pushButton)
        self.browse_button_group.addButton(self.amazingmidi_pushButton)
        self.browse_button_group.addButton(self.reddotforever_pushButton)
        self.browse_button_group.addButton(self.pianobooster_pushButton)
        self.browse_button_group.addButton(self.anthemscore_pushButton)
        self.browse_button_group.addButton(self.muse_score_pushButton)
        self.browse_button_group.buttonClicked.connect(self.upload_exe_file)

        self.browse_button_dict = {self.audiveris_pushButton: ['', self.audiveris_lineEdit, 'aud_app_exe_path'], self.amazingmidi_pushButton: ['',self.amazingmidi_lineEdit, 'ama_app_exe_path'],
                                   self.reddotforever_pushButton: ['', self.reddotforever_lineEdit, 'red_app_exe_path'], self.pianobooster_pushButton: ['', self.pianobooster_lineEdit, 'pia_app_exe_path'],
                                   self.anthemscore_pushButton: ['', self.anthemscore_lineEdit,'ant_app_exe_path'], self.muse_score_pushButton: ['', self.muse_score_lineEdit, 'mus_app_exe_path']}

        #-----------------------------------------------------------------------
        # Mp3 to Midi Converter Settings within Path Tab

        self.mp3_to_midi_converter_label = QtWidgets.QLabel(self.path_tab)
        self.mp3_to_midi_converter_label.setGeometry(QtCore.QRect(10, 440, 141, 16))
        self.mp3_to_midi_converter_label.setObjectName("mp3_to_midi_converter_label")
        self.open_source_radioButton = QtWidgets.QRadioButton(self.path_tab)
        self.open_source_radioButton.setGeometry(QtCore.QRect(230, 440, 111, 20))
        self.open_source_radioButton.setObjectName("open_source_radioButton")
        self.close_source_radioButton = QtWidgets.QRadioButton(self.path_tab)
        self.close_source_radioButton.setGeometry(QtCore.QRect(390, 440, 111, 20))
        self.close_source_radioButton.setObjectName("close_source_radioButton")
        self.mp3_to_mid_textBrowser = QtWidgets.QTextBrowser(self.path_tab)
        self.mp3_to_mid_textBrowser.setGeometry(QtCore.QRect(10, 480, 481, 91))
        self.mp3_to_mid_textBrowser.setObjectName("mp3_to_mid_textBrowser")

        #-----------------------------------------------------------------------
        # Tutor Tab
        # Port Settings within Tutor Tab

        self.tabWidget.addTab(self.path_tab, "")
        self.tutor_tab = QtWidgets.QWidget()
        self.tutor_tab.setObjectName("tutor_tab")
        self.port_settings_label = QtWidgets.QLabel(self.tutor_tab)
        self.port_settings_label.setGeometry(QtCore.QRect(210, 10, 81, 20))
        self.port_settings_label.setObjectName("port_settings_label")

        #self.piano_port_comboBox = QtWidgets.QComboBox(self.tutor_tab)
        self.piano_port_comboBox = PianoComboBox(self.tutor_tab)
        self.piano_port_comboBox.setGeometry(QtCore.QRect(10, 50, 481, 31))
        self.piano_port_comboBox.setObjectName("piano_port_comboBox")
        self.piano_port_label = QtWidgets.QLabel(self.tutor_tab)
        self.piano_port_label.setGeometry(QtCore.QRect(10, 30, 71, 16))
        self.piano_port_label.setObjectName("piano_port_label")
        self.piano_size_label = QtWidgets.QLabel(self.tutor_tab)
        self.piano_size_label.setGeometry(QtCore.QRect(10, 90, 71, 16))
        self.piano_size_label.setObjectName("piano_size_label")
        self.piano_size_comboBox = QtWidgets.QComboBox(self.tutor_tab)
        self.piano_size_comboBox.setGeometry(QtCore.QRect(10, 111, 481, 31))
        self.piano_size_comboBox.setObjectName("piano_size_comboBox")

        self.piano_size_comboBox.addItem('61 Key Piano - S')
        self.piano_size_comboBox.addItem('76 Key Piano - M')
        self.piano_size_comboBox.addItem('88 Key Piano - L')

        self.arduino_port_label = QtWidgets.QLabel(self.tutor_tab)
        self.arduino_port_label.setGeometry(QtCore.QRect(10, 150, 81, 16))
        self.arduino_port_label.setObjectName("arduino_port_label")
        #self.arduino_port_comboBox = QtWidgets.QComboBox(self.tutor_tab)
        self.arduino_port_comboBox = ArduinoComboBox(self.tutor_tab)
        self.arduino_port_comboBox.setGeometry(QtCore.QRect(10, 170, 481, 31))
        self.arduino_port_comboBox.setObjectName("arduino_port_comboBox")

        self.port_dict = {self.piano_port_comboBox: ['','piano_port'], self.piano_size_comboBox: ['','piano_size'],
                          self.arduino_port_comboBox: ['','arduino_port']}

        #-----------------------------------------------------------------------
        # Color Settings within Tutor Tab

        self.color_line = QtWidgets.QFrame(self.tutor_tab)
        self.color_line.setGeometry(QtCore.QRect(10, 210, 481, 20))
        self.color_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.color_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.color_line.setObjectName("color_line")
        self.colorsettings_label = QtWidgets.QLabel(self.tutor_tab)
        self.colorsettings_label.setGeometry(QtCore.QRect(210, 230, 81, 16))
        self.colorsettings_label.setObjectName("colorsettings_label")
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

        self.color_key_dict = {self.blackkey_r_lineEdit: ['0','blackkey_r'], self.blackkey_g_lineEdit: ['0','blackkey_g'],
                               self.blackkey_b_lineEdit: ['0','blackkey_b'], self.whitekey_r_lineEdit: ['0','whitekey_r'],
                               self.whitekey_g_lineEdit: ['0','whitekey_g'], self.whitekey_b_lineEdit: ['0','whitekey_b']}

        # Colorwheel Button Group

        self.whitekey_colorwheel_pushButton = QtWidgets.QPushButton(self.tutor_tab)
        self.whitekey_colorwheel_pushButton.setGeometry(QtCore.QRect(300, 280, 191, 41))
        self.whitekey_colorwheel_pushButton.setObjectName("whitekey_colorwheel_pushButton")
        self.blackkey_colorwheel_pushButton = QtWidgets.QPushButton(self.tutor_tab)
        self.blackkey_colorwheel_pushButton.setGeometry(QtCore.QRect(300, 370, 191, 41))
        self.blackkey_colorwheel_pushButton.setObjectName("blackkey_colorwheel_pushButton")
        self.colorwheel_label = QtWidgets.QLabel(self.tutor_tab)
        self.colorwheel_label.setGeometry(QtCore.QRect(360, 250, 81, 16))
        self.colorwheel_label.setObjectName("colorwheel_label")

        self.colorwheel_button_group = QButtonGroup()
        self.colorwheel_button_group.setExclusive(True)
        self.colorwheel_button_group.addButton(self.whitekey_colorwheel_pushButton)
        self.colorwheel_button_group.addButton(self.blackkey_colorwheel_pushButton)
        self.colorwheel_button_group.buttonClicked.connect(self.color_picker)


        #-----------------------------------------------------------------------
        # Timing Settings within Tutor Tab

        self.timing_line = QtWidgets.QFrame(self.tutor_tab)
        self.timing_line.setGeometry(QtCore.QRect(10, 420, 481, 20))
        self.timing_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.timing_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.timing_line.setObjectName("timing_line")
        self.timingsettings_label = QtWidgets.QLabel(self.tutor_tab)
        self.timingsettings_label.setGeometry(QtCore.QRect(210, 440, 101, 16))
        self.timingsettings_label.setObjectName("timingsettings_label")
        self.chord_tick_tolerance_label = QtWidgets.QLabel(self.tutor_tab)
        self.chord_tick_tolerance_label.setGeometry(QtCore.QRect(20, 470, 151, 16))
        self.chord_tick_tolerance_label.setObjectName("chord_tick_tolerance_label")
        self.chord_tick_tolerance_lineEdit = QtWidgets.QLineEdit(self.tutor_tab)
        self.chord_tick_tolerance_lineEdit.setGeometry(QtCore.QRect(250, 470, 241, 22))
        self.chord_tick_tolerance_lineEdit.setObjectName("chord_tick_tolerance_lineEdit")
        self.delay_early_tolerance_label = QtWidgets.QLabel(self.tutor_tab)
        self.delay_early_tolerance_label.setGeometry(QtCore.QRect(20, 510, 141, 16))
        self.delay_early_tolerance_label.setObjectName("delay_early_tolerance_label")
        self.delay_early_tolerance_lineEdit = QtWidgets.QLineEdit(self.tutor_tab)
        self.delay_early_tolerance_lineEdit.setGeometry(QtCore.QRect(250, 510, 241, 22))
        self.delay_early_tolerance_lineEdit.setObjectName("delay_early_tolerance_lineEdit")
        self.delay_late_tolerance_label = QtWidgets.QLabel(self.tutor_tab)
        self.delay_late_tolerance_label.setGeometry(QtCore.QRect(20, 550, 141, 16))
        self.delay_late_tolerance_label.setObjectName("delay_late_tolerance_label")
        self.delay_late_tolerance_lineEdit = QtWidgets.QLineEdit(self.tutor_tab)
        self.delay_late_tolerance_lineEdit.setGeometry(QtCore.QRect(250, 550, 241, 22))
        self.delay_late_tolerance_lineEdit.setObjectName("delay_late_tolerance_lineEdit")

        self.timing_dict = {self.chord_tick_tolerance_lineEdit: ['0','chord_tick_tolerance'], self.delay_early_tolerance_lineEdit: ['0','delay_early_tolerance'],
                            self.delay_late_tolerance_lineEdit: ['0','delay_late_tolerance']}

        self.tabWidget.addTab(self.tutor_tab, "")

        #-----------------------------------------------------------------------
        # Final Touches to GUI setup

        self.retranslate_ui()
        self.tabWidget.setCurrentIndex(0)

        self.read_all_settings()
        self.update_settings()

        self.buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.apply_changes)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslate_ui(self):

        _translate = QtCore.QCoreApplication.translate
        self.anthemscore_pushButton.setText(_translate("Dialog", "Browse"))
        self.pianobooster_pushButton.setText(_translate("Dialog", "Browse"))
        self.audiveris_pushButton.setText(_translate("Dialog", "Browse"))
        self.anthemscore_label.setText(_translate("Dialog", "AnthemScore [.exe] (Optional)"))
        self.pianobooster_label.setText(_translate("Dialog", "PianoBooster [.exe]"))
        self.reddotforever_label.setText(_translate("Dialog", "Red Dot Forever [.exe]"))
        self.audiveris_label.setText(_translate("Dialog", "Audiveris [folder]"))
        self.amazingmidi_label.setText(_translate("Dialog", "AmazingMIDI [.exe]"))
        self.configurePath_label.setText(_translate("Dialog", "Configure that path for each program."))
        self.amazingmidi_pushButton.setText(_translate("Dialog", "Browse"))
        self.reddotforever_pushButton.setText(_translate("Dialog", "Browse"))
        self.mp3_to_midi_converter_label.setText(_translate("Dialog", "MP3 to MIDI Converter:"))
        self.open_source_radioButton.setText(_translate("Dialog", "Open-Source"))
        self.close_source_radioButton.setText(_translate("Dialog", "Close-Source"))
        self.mp3_to_mid_textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Open-Source referes to the freeware called AmazingMIDI. Close-Source refers to AnthemScore, which can be bought here: https://www.lunaverus.com/. Although this software is not free, the mp3 to midi conversion of AnthemScore is much better than AmazingMidi\'s conversion and is one of the cheapest mp3 to midi converters in the market.</span></p></body></html>"))
        self.muse_score_label.setText(_translate("Dialog", "Muse Score [.exe]"))
        self.muse_score_pushButton.setText(_translate("Dialog", "Browse"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.path_tab), _translate("Dialog", "Path Settings"))
        self.timingsettings_label.setText(_translate("Dialog", "Timing Settings"))
        self.colorsettings_label.setText(_translate("Dialog", "Color Settings"))
        self.port_settings_label.setText(_translate("Dialog", "Port Settings"))
        self.piano_port_label.setText(_translate("Dialog", "Piano Port"))
        self.arduino_port_label.setText(_translate("Dialog", "Arduino Port"))
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
        self.delay_early_tolerance_label.setText(_translate("Dialog", "Delay Early Tolerance:"))
        self.chord_tick_tolerance_label.setText(_translate("Dialog", "Chord Tick Tolerance:"))
        self.delay_late_tolerance_label.setText(_translate("Dialog", "Delay Late Tolerance:"))
        self.piano_size_label.setText(_translate("Dialog", "Piano Size"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tutor_tab), _translate("Dialog", "Tutoring Settings"))

#-------------------------------------------------------------------------------
# Path Tab Functions

    def openFileNameDialog_ExecPath(self):
        # This file dialog is used to obtain the file location of the .exe file.

        fileName, _ = QFileDialog.getOpenFileName(caption = "Select .exe File", filter = "Executiable files (*.exe)")

        if fileName:
            fileName = str(fileName)
        else:
            return ""

        fileName = fileName.replace('/' , '\\' )
        return fileName

    def openDirectoryDialog_ExecPath(self):
        # This file dialog is used to obtain the folder directory of the desired
        # save location for the generated files

        options = QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(caption = 'Open a folder', options = options)

        if directory:
            file_dialog_output = str(directory)
        else:
            return ""

        file_dialog_output = file_dialog_output.replace('/' , '\\' )
        return file_dialog_output

    def upload_exe_file(self, button):
        # This function allows the user to upload a file for file conversion.

        if button == self.audiveris_pushButton:
            upload_exe_path = self.openDirectoryDialog_ExecPath()
        else:
            upload_exe_path = self.openFileNameDialog_ExecPath()

        self.browse_button_dict[button][0] = upload_exe_path
        #self.update_path()

        return None

#-------------------------------------------------------------------------------
# Color
    def color_picker(self, button):
        # This function creates a QColorDialog when the user clicks the color
        # wheel color. Once the user selects a color, it will display the RGB
        # colors in the lineedits

        color = QtWidgets.QColorDialog.getColor()

        if color.isValid():
            # Converting Hexadecimal to RGB values
            value = color.name()
            value = value.lstrip('#')
            [r,g,b] = tuple(int(value[i:i+2], 16) for i in (0, 2, 4))

            if button == self.whitekey_colorwheel_pushButton:
                self.whitekey_r_lineEdit.setText(str(r))
                self.whitekey_g_lineEdit.setText(str(g))
                self.whitekey_b_lineEdit.setText(str(b))

            elif button == self.blackkey_colorwheel_pushButton:
                self.blackkey_r_lineEdit.setText(str(r))
                self.blackkey_g_lineEdit.setText(str(g))
                self.blackkey_b_lineEdit.setText(str(b))

        return

#-------------------------------------------------------------------------------
# Overall Settings Handeling

    def read_all_settings(self):

        # Path Settings
        for key in self.browse_button_dict.keys():
            self.browse_button_dict[key][0] = setting_read(self.browse_button_dict[key][2])

        # Mp3 to midi Settings
        self.mp3_to_midi_setting = setting_read('mp3_to_midi_converter')

        # Color Settings
        for key in self.color_key_dict.keys():
            self.color_key_dict[key][0] = setting_read(self.color_key_dict[key][1])

        # Timing Settings
        for key in self.timing_dict.keys():
            self.timing_dict[key][0] = setting_read(self.timing_dict[key][1])

        # Port Settings
        for key in self.port_dict.keys():
            self.port_dict[key][0] = setting_read(self.port_dict[key][1])

        return None

    def update_settings(self):

        # Path Settings
        for button in self.browse_button_dict:
            self.browse_button_dict[button][1].setText(self.browse_button_dict[button][0])

        # Mp3 to midi Settings
        if self.mp3_to_midi_setting == 'open_source':
            self.open_source_radioButton.setChecked(True)
            self.close_source_radioButton.setChecked(False)
        elif self.mp3_to_midi_setting == 'close_source':
            self.close_source_radioButton.setChecked(True)
            self.open_source_radioButton.setChecked(False)

        # Color Settings
        for key in self.color_key_dict.keys():
            key.setText(self.color_key_dict[key][0])

        # Timing Settings
        for key in self.timing_dict.keys():
            key.setText(self.timing_dict[key][0])

        # Port Settings
        for key in self.port_dict.keys():
            if self.port_dict[key][1] == 'piano_size':
                if self.port_dict[key][0] == 'S':
                    key_number = '61'
                elif self.port_dict[key][0] == 'M':
                    key_number = '76'
                elif self.port_dict[key][0] == 'L':
                    key_number = '88'

                key.setCurrentText(key_number + ' Key Piano - ' + self.port_dict[key][0])

            else:

                key.addItem(self.port_dict[key][0])
                key.setCurrentText(self.port_dict[key][0])

        return None

    def apply_changes(self):

        # Apply Path
        for button in self.browse_button_dict:
            text = self.browse_button_dict[button][1].text()
            setting_write(self.browse_button_dict[button][2], text)

        # Mp3 to midi Settings
        self.mp3_to_midi_setting = setting_read('mp3_to_midi_converter')
        if self.open_source_radioButton.isChecked():
            if self.mp3_to_midi_setting != 'open_source':
                setting_write('mp3_to_midi_converter', 'open_source')
        elif self.close_source_radioButton.isChecked():
            if self.mp3_to_midi_setting != 'close_source':
                setting_write('mp3_to_midi_converter', 'close_source')

        # Color Settings
        for key in self.color_key_dict.keys():
            text = key.text()
            setting_write(self.color_key_dict[key][1], text)

        # Timing Settings
        for key in self.timing_dict.keys():
            text = key.text()
            setting_write(self.timing_dict[key][1], text)

        # Port Settings
        for key in self.port_dict.keys():
            index = key.currentIndex()

            if index == -1:
                continue

            if key == self.piano_port_comboBox or key == self.arduino_port_comboBox:
                setting_write(self.port_dict[key][1], key.currentText())

            elif key == self.piano_size_comboBox:
                setting_write(self.port_dict[key][1], key.currentText()[-1])

        return None

#-------------------------------------------------------------------------------
# Main Code

"""
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    settings_dialog = SettingsDialog()
    settings_dialog.show()
    sys.exit(app.exec_())
"""
