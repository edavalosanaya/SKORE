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
from skore_program_controller import setting_read, setting_write

################################VARIABLES#######################################

# Path Tab Variables
app_exe_path = ['','','','','','','','']
possible_app = ['audiveris','amazingmidi','audacity','midiSheetMusic','xenoplay','reddotforever','pianobooster','anthemscore']
app_exe_setting_label = ['audi_app_exe_path','ama_app_exe_path','aud_app_exe_path','midi_app_exe_path','xeno_app_exe_path','red_app_exe_path','pia_app_exe_path','ant_app_exe_path']

# Tutoring Tab Variables
mp3_2_midi_choice = []
file_conversion_choice = []
color_lineedit = ['whitekey_r','whitekey_g','whitekey_b','blackkey_r','blackkey_g','blackkey_b']
color_values = ['','','','','','']
timing_lineedit = ['time_per_tick','increment_counter','chord_timing_tolerance','manual_final_chord_sustain_timing']
timing_values = ['','','','']
port_combobox_titles = ['piano_port','piano_size','arduino_com_port']
port_combobox_values = ['','','']

#####################################PYQT5######################################

class arduino_ComboBox(QtWidgets.QComboBox):
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
        super(arduino_ComboBox, self).showPopup()

class piano_ComboBox(QtWidgets.QComboBox):
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
        super(piano_ComboBox, self).showPopup()

class SettingsDialog(QtWidgets.QDialog):
    # This class contains all the processes and functions for the settings
    # dialog of the SKORE application

    def __init__(self):
        super(QtWidgets.QDialog, self).__init__()
        self.setupUiDialog()

    def setupUiDialog(self):
        # This functions creates the layout of the settings GUI

        self.resize(530, 679)
        self.setWindowTitle("SKORE Settings")
        self.setStyleSheet("""
            background-color: rgb(50,50,50);
            color: white;
            """)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(310, 630, 201, 32))
        self.buttonBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")

        #Tab Widget
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 511, 611))
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setObjectName("tabWidget")

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Path Settings Tab@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        self.path_tab = QtWidgets.QWidget()
        self.path_tab.setObjectName("path_tab")

        self.configurePath_label = QtWidgets.QLabel(self.path_tab)
        self.configurePath_label.setGeometry(QtCore.QRect(10, 10, 231, 20))
        self.configurePath_label.setObjectName("configurePath_label")
        self.path_line = QtWidgets.QFrame(self.path_tab)
        self.path_line.setGeometry(QtCore.QRect(10, 30, 481, 10))
        self.path_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.path_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.path_line.setObjectName("path_line")

        label_lineEdit_diff = 20
        lineEdit_label_diff = 40
        audi_label_y = 40
        audi_linedEdit_y = audi_label_y + label_lineEdit_diff

        self.audiveris_label = QtWidgets.QLabel(self.path_tab)
        self.audiveris_label.setGeometry(QtCore.QRect(10, audi_label_y, 101, 16))
        self.audiveris_label.setObjectName("audiveris_label")
        self.audiveris_lineEdit = QtWidgets.QLineEdit(self.path_tab)
        self.audiveris_lineEdit.setGeometry(QtCore.QRect(10, audi_linedEdit_y, 381, 31))
        self.audiveris_lineEdit.setObjectName("audiveris_lineEdit")
        self.audiveris_pushButton = QtWidgets.QPushButton(self.path_tab)
        self.audiveris_pushButton.setGeometry(QtCore.QRect(400, audi_linedEdit_y, 93, 31))
        self.audiveris_pushButton.setObjectName("audiveris_pushButton")

        ama_label_y = audi_linedEdit_y + lineEdit_label_diff
        ama_linedEdit_y = ama_label_y + label_lineEdit_diff

        self.amazingmidi_label = QtWidgets.QLabel(self.path_tab)
        self.amazingmidi_label.setGeometry(QtCore.QRect(10, ama_label_y, 121, 16))
        self.amazingmidi_label.setObjectName("amazingmidi_label")
        self.amazingmidi_lineEdit = QtWidgets.QLineEdit(self.path_tab)
        self.amazingmidi_lineEdit.setGeometry(QtCore.QRect(10, ama_linedEdit_y, 381, 31))
        self.amazingmidi_lineEdit.setObjectName("amazingmidi_lineEdit")
        self.amazingmidi_pushButton = QtWidgets.QPushButton(self.path_tab)
        self.amazingmidi_pushButton.setGeometry(QtCore.QRect(400, ama_linedEdit_y, 93, 31))
        self.amazingmidi_pushButton.setObjectName('amazingmidi_pushButton')

        red_label_y = ama_linedEdit_y + lineEdit_label_diff
        red_linedEdit_y = red_label_y + label_lineEdit_diff

        self.reddotforever_label = QtWidgets.QLabel(self.path_tab)
        self.reddotforever_label.setGeometry(QtCore.QRect(10, red_label_y, 131, 16))
        self.reddotforever_label.setObjectName("reddotforever_label")
        self.reddotforever_lineEdit = QtWidgets.QLineEdit(self.path_tab)
        self.reddotforever_lineEdit.setGeometry(QtCore.QRect(10, red_linedEdit_y, 381, 31))
        self.reddotforever_lineEdit.setObjectName("reddotforever_lineEdit")
        self.reddotforever_pushButton = QtWidgets.QPushButton(self.path_tab)
        self.reddotforever_pushButton.setGeometry(QtCore.QRect(400, red_linedEdit_y, 93, 31))
        self.reddotforever_pushButton.setObjectName("reddotforever_pushButton")

        pia_label_y = red_linedEdit_y + lineEdit_label_diff
        pia_linedEdit_y = pia_label_y + label_lineEdit_diff

        self.pianobooster_label = QtWidgets.QLabel(self.path_tab)
        self.pianobooster_label.setGeometry(QtCore.QRect(10, pia_label_y, 121, 16))
        self.pianobooster_label.setObjectName("pianobooster_label")
        self.pianobooster_lineEdit = QtWidgets.QLineEdit(self.path_tab)
        self.pianobooster_lineEdit.setGeometry(QtCore.QRect(10, pia_linedEdit_y, 381, 31))
        self.pianobooster_lineEdit.setObjectName("pianobooster_lineEdit")
        self.pianobooster_pushButton = QtWidgets.QPushButton(self.path_tab)
        self.pianobooster_pushButton.setGeometry(QtCore.QRect(400, pia_linedEdit_y, 93, 31))
        self.pianobooster_pushButton.setObjectName("pianobooster_pushButton")

        midi_label_y = pia_linedEdit_y + lineEdit_label_diff
        midi_linedEdit_y = midi_label_y + label_lineEdit_diff

        self.midisheetmusic_label = QtWidgets.QLabel(self.path_tab)
        self.midisheetmusic_label.setGeometry(QtCore.QRect(10, midi_label_y, 141, 16))
        self.midisheetmusic_label.setObjectName("midisheetmusic_label")
        self.midiSheetMusic_lineEdit = QtWidgets.QLineEdit(self.path_tab)
        self.midiSheetMusic_lineEdit.setGeometry(QtCore.QRect(10, midi_linedEdit_y, 381, 31))
        self.midiSheetMusic_lineEdit.setObjectName("midiSheetMusic_lineEdit")
        self.midiSheetMusic_pushButton = QtWidgets.QPushButton(self.path_tab)
        self.midiSheetMusic_pushButton.setGeometry(QtCore.QRect(400, midi_linedEdit_y, 93, 31))
        self.midiSheetMusic_pushButton.setObjectName("midiSheetMusic_pushButton")

        xeno_label_y = midi_linedEdit_y + lineEdit_label_diff
        xeno_linedEdit_y = xeno_label_y + label_lineEdit_diff

        self.xenoplay_label = QtWidgets.QLabel(self.path_tab)
        self.xenoplay_label.setGeometry(QtCore.QRect(10, xeno_label_y, 121, 16))
        self.xenoplay_label.setObjectName("xenoplay_label")
        self.xenoplay_lineEdit = QtWidgets.QLineEdit(self.path_tab)
        self.xenoplay_lineEdit.setGeometry(QtCore.QRect(10, xeno_linedEdit_y, 381, 31))
        self.xenoplay_lineEdit.setObjectName("xenoplay_lineEdit")
        self.xenoplay_pushButton = QtWidgets.QPushButton(self.path_tab)
        self.xenoplay_pushButton.setGeometry(QtCore.QRect(400, xeno_linedEdit_y, 93, 31))
        self.xenoplay_pushButton.setObjectName("xenoplay_pushButton")

        audi_label_y = xeno_linedEdit_y + lineEdit_label_diff
        audi_linedEdit_y = audi_label_y + label_lineEdit_diff

        self.audacity_label = QtWidgets.QLabel(self.path_tab)
        self.audacity_label.setGeometry(QtCore.QRect(10, audi_label_y, 191, 16))
        self.audacity_label.setObjectName("audacity_label")
        self.audacity_lineEdit = QtWidgets.QLineEdit(self.path_tab)
        self.audacity_lineEdit.setGeometry(QtCore.QRect(10, audi_linedEdit_y, 381, 31))
        self.audacity_lineEdit.setObjectName("audacity_lineEdit")
        self.audacity_pushButton = QtWidgets.QPushButton(self.path_tab)
        self.audacity_pushButton.setGeometry(QtCore.QRect(400, audi_linedEdit_y, 93, 31))
        self.audacity_pushButton.setObjectName("audacity_pushButton")

        ant_label_y = audi_linedEdit_y + lineEdit_label_diff
        ant_lineEdit_y = ant_label_y + label_lineEdit_diff

        self.anthemscore_label = QtWidgets.QLabel(self.path_tab)
        self.anthemscore_label.setGeometry(QtCore.QRect(10, ant_label_y, 191, 16))
        self.anthemscore_label.setObjectName("anthemscore_label")
        self.anthemscore_lineEdit = QtWidgets.QLineEdit(self.path_tab)
        self.anthemscore_lineEdit.setGeometry(QtCore.QRect(10, ant_lineEdit_y, 381, 31))
        self.anthemscore_lineEdit.setObjectName("anthemscore_lineEdit")
        self.anthemscore_pushButton = QtWidgets.QPushButton(self.path_tab)
        self.anthemscore_pushButton.setGeometry(QtCore.QRect(400, ant_lineEdit_y, 93, 31))
        self.anthemscore_pushButton.setObjectName("anthemscore_pushButton")

        # Mp3 to Midi Converter Selection
        radio_buttons_y = ant_lineEdit_y + 40
        self.mp3_2_midi_converter_label = QtWidgets.QLabel(self.path_tab)
        self.mp3_2_midi_converter_label.setGeometry(QtCore.QRect(10, radio_buttons_y, 141, 16))
        self.mp3_2_midi_converter_label.setObjectName("mp3_2_midi_converter_label")
        self.amazingmidi_radioButton = QtWidgets.QRadioButton(self.path_tab)
        self.amazingmidi_radioButton.setGeometry(QtCore.QRect(230, radio_buttons_y, 111, 20))
        self.amazingmidi_radioButton.setObjectName("amazingmidi_radioButton")
        self.anthemscore_radioButton = QtWidgets.QRadioButton(self.path_tab)
        self.anthemscore_radioButton.setGeometry(QtCore.QRect(390, radio_buttons_y, 111, 20))
        self.anthemscore_radioButton.setObjectName("anthemscore_radioButton")

        # File Conversion User Control
        radio_buttons2_y = radio_buttons_y + 35
        self.file_conversion_label = QtWidgets.QLabel(self.path_tab)
        self.file_conversion_label.setGeometry(QtCore.QRect(10, radio_buttons2_y, 180, 16))
        self.file_conversion_label.setObjectName("file_conversion_label")
        self.yes_file_conversion_radioButton = QtWidgets.QRadioButton(self.path_tab)
        self.yes_file_conversion_radioButton.setGeometry(QtCore.QRect(230, radio_buttons2_y, 111, 20))
        self.yes_file_conversion_radioButton.setObjectName('yes_file_conversion_radioButton')
        self.no_file_conversion_radioButton = QtWidgets.QRadioButton(self.path_tab)
        self.no_file_conversion_radioButton.setGeometry(QtCore.QRect(390, radio_buttons2_y, 111, 20))
        self.no_file_conversion_radioButton.setObjectName("no_file_conversion_radioButton")

        # RadioButton Groups
        # This is to separate the radioButtons to ensure that they are paired correctly
        self.mp3_2_midi_converter_group = QButtonGroup()
        self.mp3_2_midi_converter_group.setExclusive(True)
        self.mp3_2_midi_converter_group.addButton(self.amazingmidi_radioButton)
        self.mp3_2_midi_converter_group.addButton(self.anthemscore_radioButton)
        self.file_conversion_group = QButtonGroup()
        self.file_conversion_group.setExclusive(True)
        self.file_conversion_group.addButton(self.yes_file_conversion_radioButton)
        self.file_conversion_group.addButton(self.no_file_conversion_radioButton)

        # Button Browsing Addition
        self.browse_button_group = QButtonGroup()
        self.browse_button_group.setExclusive(True)
        self.browse_button_group.addButton(self.audiveris_pushButton)
        self.browse_button_group.addButton(self.amazingmidi_pushButton)
        self.browse_button_group.addButton(self.audacity_pushButton)
        self.browse_button_group.addButton(self.midiSheetMusic_pushButton)
        self.browse_button_group.addButton(self.xenoplay_pushButton)
        self.browse_button_group.addButton(self.reddotforever_pushButton)
        self.browse_button_group.addButton(self.pianobooster_pushButton)
        self.browse_button_group.addButton(self.anthemscore_pushButton)
        self.browse_button_group.buttonClicked.connect(self.upload_exe_file)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Tutoring Settings Tab@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        self.tabWidget.addTab(self.path_tab, "")
        self.tutor_tab = QtWidgets.QWidget()
        self.tutor_tab.setObjectName("tutor_tab")

        # Port Settings
        self.portsettings_label = QtWidgets.QLabel(self.tutor_tab)
        self.portsettings_label.setGeometry(QtCore.QRect(210, 10, 81, 20))
        self.portsettings_label.setObjectName("portsettings_label")

        # Piano Port ComboBox Class had to be overwritten to make the QComboBox
        # adjustable during the popup function
        self.piano_port_comboBox = piano_ComboBox(self.tutor_tab)
        self.piano_port_comboBox.setGeometry(QtCore.QRect(10, 50, 481, 31))
        self.piano_port_comboBox.setObjectName("piano_port_comboBox")

        self.piano_port_label = QtWidgets.QLabel(self.tutor_tab)
        self.piano_port_label.setGeometry(QtCore.QRect(10, 30, 71, 16))
        self.piano_port_label.setObjectName("piano_port_label")

        self.piano_size_label = QtWidgets.QLabel(self.tutor_tab)
        self.piano_size_label.setGeometry(QtCore.QRect(10, 90, 71, 16))
        self.piano_size_label.setObjectName("piano_size_label")
        self.piano_size_comboBox = QtWidgets.QComboBox(self.tutor_tab)
        self.piano_size_comboBox.setGeometry(QtCore.QRect(10, 111, 231, 31))
        self.piano_size_comboBox.setObjectName("piano_size_comboBox")
        self.piano_size_pushButton = QtWidgets.QPushButton(self.tutor_tab)
        self.piano_size_pushButton.setGeometry(QtCore.QRect(270, 110, 221, 31))
        self.piano_size_pushButton.setObjectName("piano_size_pushButton")

        self.arduino_com_port_label = QtWidgets.QLabel(self.tutor_tab)
        self.arduino_com_port_label.setGeometry(QtCore.QRect(10, 150, 81, 16))
        self.arduino_com_port_label.setObjectName("arduino_com_port_label")

        # Arduino Port ComboBox Class had to be overwritten to make the QComboBox
        # adjustable during the popup function
        #self.arduino_com_port_comboBox = QtWidgets.QComboBox(self.tutor_tab)
        self.arduino_com_port_comboBox = arduino_ComboBox(self.tutor_tab)
        self.arduino_com_port_comboBox.setGeometry(QtCore.QRect(10, 170, 481, 31))
        self.arduino_com_port_comboBox.setObjectName("arduino_com_port_comboBox")

        # Color Settings
        self.color_line = QtWidgets.QFrame(self.tutor_tab)
        self.color_line.setGeometry(QtCore.QRect(10, 210, 481, 20))
        self.color_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.color_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.color_line.setObjectName("color_line")

        self.colorsettings_label = QtWidgets.QLabel(self.tutor_tab)
        self.colorsettings_label.setGeometry(QtCore.QRect(210, 230, 81, 16))
        self.colorsettings_label.setObjectName("colorsettings_label")

        self.colorwheel_label = QtWidgets.QLabel(self.tutor_tab)
        self.colorwheel_label.setGeometry(QtCore.QRect(360, 250, 81, 16))
        self.colorwheel_label.setObjectName("colorwheel_label")

        whitekey_y_value = 275

        self.whitekey_label = QtWidgets.QLabel(self.tutor_tab)
        self.whitekey_label.setGeometry(QtCore.QRect(20, 250, 121, 16))
        self.whitekey_label.setObjectName("whitekey_label")
        self.whitekey_r_label = QtWidgets.QLabel(self.tutor_tab)
        self.whitekey_r_label.setGeometry(QtCore.QRect(20, whitekey_y_value, 21, 16))
        self.whitekey_r_label.setObjectName("whitekey_r_label")
        self.whitekey_g_label = QtWidgets.QLabel(self.tutor_tab)
        self.whitekey_g_label.setGeometry(QtCore.QRect(100, whitekey_y_value, 21, 16))
        self.whitekey_b_label = QtWidgets.QLabel(self.tutor_tab)
        self.whitekey_b_label.setGeometry(QtCore.QRect(180, whitekey_y_value, 21, 16))
        self.whitekey_b_label.setObjectName("whitekey_b_label")
        self.whitekey_r_lineEdit = QtWidgets.QLineEdit(self.tutor_tab)
        self.whitekey_r_lineEdit.setGeometry(QtCore.QRect(40, whitekey_y_value, 51, 22))
        self.whitekey_r_lineEdit.setObjectName("whitekey_r_lineEdit")
        self.whitekey_g_lineEdit = QtWidgets.QLineEdit(self.tutor_tab)
        self.whitekey_g_lineEdit.setGeometry(QtCore.QRect(120, whitekey_y_value, 51, 22))
        self.whitekey_g_lineEdit.setObjectName("whitekey_g_lineEdit")
        self.whitekey_b_lineEdit = QtWidgets.QLineEdit(self.tutor_tab)
        self.whitekey_b_lineEdit.setGeometry(QtCore.QRect(200, whitekey_y_value, 51, 22))
        self.whitekey_b_lineEdit.setObjectName("whitekey_b_lineEdit")
        self.whitekey_colorwheel_pushButton = QtWidgets.QPushButton(self.tutor_tab)
        self.whitekey_colorwheel_pushButton.setGeometry(QtCore.QRect(340, whitekey_y_value, 121, 21))
        self.whitekey_colorwheel_pushButton.setObjectName("whitekey_colorwheel_pushButton")

        # Black Key Arrangment

        blackkey_y_title_value = whitekey_y_value + 40
        blackkey_y_value = blackkey_y_title_value + 25

        self.blackkey_label = QtWidgets.QLabel(self.tutor_tab)
        self.blackkey_label.setGeometry(QtCore.QRect(20, blackkey_y_title_value, 121, 16))
        self.blackkey_label.setObjectName("blackkey_label")
        self.blackkey_r_label = QtWidgets.QLabel(self.tutor_tab)
        self.blackkey_r_label.setGeometry(QtCore.QRect(20, blackkey_y_value, 21, 16))
        self.blackkey_r_label.setObjectName("blackkey_r_label")
        self.whitekey_g_label.setObjectName("whitekey_g_label")
        self.blackkey_g_label = QtWidgets.QLabel(self.tutor_tab)
        self.blackkey_g_label.setGeometry(QtCore.QRect(100, blackkey_y_value, 21, 16))
        self.blackkey_g_label.setObjectName("blackkey_g_label")
        self.blackkey_b_label = QtWidgets.QLabel(self.tutor_tab)
        self.blackkey_b_label.setGeometry(QtCore.QRect(180, blackkey_y_value, 21, 16))
        self.blackkey_b_label.setObjectName("blackkey_b_label")
        self.blackkey_r_lineEdit = QtWidgets.QLineEdit(self.tutor_tab)
        self.blackkey_r_lineEdit.setGeometry(QtCore.QRect(40, blackkey_y_value, 51, 22))
        self.blackkey_r_lineEdit.setObjectName("blackkey_r_lineEdit")
        self.blackkey_g_lineEdit = QtWidgets.QLineEdit(self.tutor_tab)
        self.blackkey_g_lineEdit.setGeometry(QtCore.QRect(120, blackkey_y_value, 51, 22))
        self.blackkey_g_lineEdit.setObjectName("blackkey_g_lineEdit")
        self.blackkey_b_lineEdit = QtWidgets.QLineEdit(self.tutor_tab)
        self.blackkey_b_lineEdit.setGeometry(QtCore.QRect(200, blackkey_y_value, 51, 22))
        self.blackkey_b_lineEdit.setObjectName("blackkey_b_lineEdit")
        self.blackkey_colorwheel_pushButton = QtWidgets.QPushButton(self.tutor_tab)
        self.blackkey_colorwheel_pushButton.setGeometry(QtCore.QRect(340, blackkey_y_value, 121, 21))
        self.blackkey_colorwheel_pushButton.setObjectName("blackkey_colorwheel_pushButton")

        # Timing Settings

        timing_line_y_value = blackkey_y_value + 30

        self.timing_line = QtWidgets.QFrame(self.tutor_tab)
        self.timing_line.setGeometry(QtCore.QRect(10, timing_line_y_value, 481, 20))
        self.timing_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.timing_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.timing_line.setObjectName("timing_line")

        timing_title_y_value = timing_line_y_value + 20

        self.timingsettings_label = QtWidgets.QLabel(self.tutor_tab)
        self.timingsettings_label.setGeometry(QtCore.QRect(210, timing_title_y_value, 101, 16))
        self.timingsettings_label.setObjectName("timingsettings_label")

        time_per_tick_y_value = timing_title_y_value + 30
        increment_counter_y_value = time_per_tick_y_value + 40
        chord_timing_tolerance_y_value = increment_counter_y_value + 40
        manual_final_chord_sustain_y_value = chord_timing_tolerance_y_value + 40

        self.time_per_tick_label = QtWidgets.QLabel(self.tutor_tab)
        self.time_per_tick_label.setGeometry(QtCore.QRect(20, time_per_tick_y_value, 91, 16))
        self.time_per_tick_label.setObjectName("time_per_tick_label")
        self.time_per_tick_lineEdit = QtWidgets.QLineEdit(self.tutor_tab)
        self.time_per_tick_lineEdit.setGeometry(QtCore.QRect(250, time_per_tick_y_value, 241, 22))
        self.time_per_tick_lineEdit.setObjectName("time_per_tick_lineEdit")

        self.increment_counter_label = QtWidgets.QLabel(self.tutor_tab)
        self.increment_counter_label.setGeometry(QtCore.QRect(20, increment_counter_y_value, 151 , 16))
        self.increment_counter_label.setObjectName("increment_counter_label")

        self.increment_counter_lineEdit = QtWidgets.QLineEdit(self.tutor_tab)
        self.increment_counter_lineEdit.setGeometry(QtCore.QRect(250, increment_counter_y_value, 241, 22))
        self.increment_counter_lineEdit.setObjectName("increment_counter_lineEdit")

        self.chord_timing_tolerance_label = QtWidgets.QLabel(self.tutor_tab)
        self.chord_timing_tolerance_label.setGeometry(QtCore.QRect(20, chord_timing_tolerance_y_value, 151, 16))
        self.chord_timing_tolerance_label.setObjectName("chord_timing_tolerance_label")
        self.chord_timing_tolerance_lineEdit = QtWidgets.QLineEdit(self.tutor_tab)
        self.chord_timing_tolerance_lineEdit.setGeometry(QtCore.QRect(250, chord_timing_tolerance_y_value, 241, 22))
        self.chord_timing_tolerance_lineEdit.setObjectName("chord_timing_tolerance_lineEdit")

        self.manual_final_chord_sustain_timing_label = QtWidgets.QLabel(self.tutor_tab)
        self.manual_final_chord_sustain_timing_label.setGeometry(QtCore.QRect(20, manual_final_chord_sustain_y_value, 211, 16))
        self.manual_final_chord_sustain_timing_label.setObjectName("manual_final_chord_sustain_timing_label")
        self.manual_final_chord_sustain_timing_lineEdit = QtWidgets.QLineEdit(self.tutor_tab)
        self.manual_final_chord_sustain_timing_lineEdit.setGeometry(QtCore.QRect(250, manual_final_chord_sustain_y_value, 241, 22))
        self.manual_final_chord_sustain_timing_lineEdit.setObjectName("manual_final_chord_sustain_timing_lineEdit")


        self.tabWidget.addTab(self.tutor_tab, "")

        # Colorwheel Button Group
        self.colorwheel_button_group = QButtonGroup()
        self.colorwheel_button_group.setExclusive(True)
        self.colorwheel_button_group.addButton(self.whitekey_colorwheel_pushButton)
        self.colorwheel_button_group.addButton(self.blackkey_colorwheel_pushButton)
        self.colorwheel_button_group.buttonClicked.connect(self.color_picker)

        # Setting up the Piano Size ComboBox
        self.piano_size_comboBox.addItem('61 Key Piano - S')
        self.piano_size_comboBox.addItem('76 Key Piano - M')
        self.piano_size_comboBox.addItem('88 Key Piano - L')

################################################################################

        # Enabling text changes
        self.retranslateUi()
        self.tabWidget.setCurrentIndex(0)

        # Path Tab Initalization
        self.settings_path_read()
        self.update_paths()

        # Tutoring Tab Initalization
        self.settings_file_conversion_choice()
        self.update_file_conversion_choice()

        self.settings_mp3_2_midi_choice()
        self.update_mp3_2_midi_choice()

        self.settings_color_read()
        self.update_color_values()

        self.settings_timing_read()
        self.update_timing_values()

        self.settings_combobox_read()
        self.update_combobox_values()

        # Apply and Cancel Button Information
        self.buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.apply_changes)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

##############################PATH TAB FUNCTIONS################################

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
        directory = QFileDialog.getExistingDirectory(caption = 'Open a folder', directory = skore_path, options = options)

        if directory:
            file_dialog_output = str(directory)
        else:
            return ""

        file_dialog_output = file_dialog_output.replace('/' , '\\' )
        return file_dialog_output

    def upload_exe_file(self, button):
        # This function allows the user to upload a file for file conversion.

        button_name = str(button.objectName())
        app_name = button_name.split('_')[0]
        #print(button_name)
        #print(app_name)

        if(app_name == 'audiveris'):
            upload_exe_path = self.openDirectoryDialog_ExecPath()
        else:
            upload_exe_path = self.openFileNameDialog_ExecPath()

        for i in range(len(possible_app)):
            if(possible_app[i] == app_name):
                app_exe_path[i] = upload_exe_path
                #print(app_exe_path[i])

        self.update_paths()

        return

    def settings_path_read(self):
        # This function reads the settings for the exe paths of the applications
        # and stores the paths into a variable called app_exe_path

        global app_exe_path

        for i in range(len(possible_app)):
            #app_exe_path[i] = setting_read(app_exe_setting_label[i], default_or_temp_mode)
            app_exe_path[i] = setting_read(app_exe_setting_label[i])

        return

    def update_paths(self):
        # This function displays the paths within the app_exe_path into the
        # lineEdit QWidgets in the settings

        for i in range(len(possible_app)):
            lineEdit_attribute = getattr(self, possible_app[i] + '_lineEdit')
            lineEdit_attribute.setText(app_exe_path[i])

        return

    def apply_path(self):
        # This function compares the text in the lineEdit and the variable called
        # app_exe_path. If they are different, that means that the settings are
        # meant to be changed. The changes are noted and written into the
        # settings.txt

        self.settings_path_read()

        for i in range(len(possible_app)):
            lineEdit_attribute = getattr(self, possible_app[i] + '_lineEdit')
            text = lineEdit_attribute.text()
            if(app_exe_path[i] != text):
                app_exe_path[i] = text
                setting_write(app_exe_setting_label[i], app_exe_path[i])

        return

    def settings_mp3_2_midi_choice(self):
        # This function reads the settings regarding which mp3 to midi converter

        global mp3_2_midi_choice

        mp3_2_midi_choice = setting_read("mp3_2_midi_converter")

        return

    def update_mp3_2_midi_choice(self):
        # This function sets the state of the radioButtons to indicate which
        # converter is selected

        if mp3_2_midi_choice == "amazingmidi":
            #print("amazingmidi")
            self.amazingmidi_radioButton.setChecked(True)
            self.anthemscore_radioButton.setChecked(False)
        elif mp3_2_midi_choice == "anthemscore":
            #print("anthemscore")
            self.anthemscore_radioButton.setChecked(True)
            self.amazingmidi_radioButton.setChecked(False)

        return

    def apply_mp3_2_midi_choice(self):
        # This function applies any changes indicated by the user

        self.settings_mp3_2_midi_choice()

        if self.amazingmidi_radioButton.isChecked():
            if mp3_2_midi_choice != 'amazingmidi':
                print("Settings Changed: AmazingMIDI Converter has been selected")
                setting_write("mp3_2_midi_converter", "amazingmidi")

        elif self.anthemscore_radioButton.isChecked():
            if mp3_2_midi_choice != 'anthemscore':
                print("Settings Changed: AnthemScore Converter has been selected")
                setting_write("mp3_2_midi_converter", "anthemscore")

    def settings_file_conversion_choice(self):
        # This function reads the settings regarding if the user wishes to partake
        # in the file conversion process

        global file_conversion_choice

        file_conversion_choice = setting_read('file_conversion_user_control')
        return

    def update_file_conversion_choice(self):
        # This function sets the state of the radioButtons to indicate if the
        # file conversion user control is enabled or disabled

        if file_conversion_choice == 'True':
            #print("True")
            self.yes_file_conversion_radioButton.setChecked(True)
            self.no_file_conversion_radioButton.setChecked(False)
        elif file_conversion_choice == 'False':
            #print("False")
            self.yes_file_conversion_radioButton.setChecked(False)
            self.no_file_conversion_radioButton.setChecked(True)
        return

    def apply_file_conversion_choice(self):
        # This function applies any changes indicated by the user

        self.settings_file_conversion_choice()

        if self.yes_file_conversion_radioButton.isChecked():
            if file_conversion_choice != 'True':
                print("Settings Changed: File Conversion User Control Enabled")
                setting_write('file_conversion_user_control','True')
        elif self.no_file_conversion_radioButton.isChecked():
            if file_conversion_choice != 'False':
                print("Settings Changed: File Conversion User Control Disabled")
                setting_write('file_conversion_user_control','False')
        return

##############################TUTORING TAB FUNCTIONS############################

    def color_picker(self, button):
        # This function creates a QColorDialog when the user clicks the color
        # wheel color. Once the user selects a color, it will display the RGB
        # colors in the lineedits

        button_name = str(button.objectName())
        color = QtWidgets.QColorDialog.getColor()

        if color.isValid():
            # Converting Hexadecimal to RGB values
            value = color.name()
            value = value.lstrip('#')
            [r,g,b] = tuple(int(value[i:i+2], 16) for i in (0, 2, 4))

            if button_name == 'whitekey_colorwheel_pushButton':
                self.whitekey_r_lineEdit.setText(str(r))
                self.whitekey_g_lineEdit.setText(str(g))
                self.whitekey_b_lineEdit.setText(str(b))

            elif button_name == 'blackkey_colorwheel_pushButton':
                self.blackkey_r_lineEdit.setText(str(r))
                self.blackkey_g_lineEdit.setText(str(g))
                self.blackkey_b_lineEdit.setText(str(b))

        return

    def settings_color_read(self):
        # This function reads the settings for the color values of the LEDs

        global color_values

        for i in range(len(color_lineedit)):
            color_values[i] = setting_read(color_lineedit[i])
        return

    def update_color_values(self):
        # This function updates the lineedits of the color values of the LEDS

        for i in range(len(color_lineedit)):
            lineEdit_attribute = getattr(self, color_lineedit[i] + '_lineEdit')
            lineEdit_attribute.setText(color_values[i])
        return

    def apply_color_values(self):
        # This function applies the changes of the color values of the LEDs to
        # the settings file

        self.settings_color_read()

        for i in range(len(color_lineedit)):
            lineEdit_attribute = getattr(self, color_lineedit[i] + '_lineEdit')
            text = lineEdit_attribute.text()
            if color_values[i] != text:
                color_values[i] = text
                setting_write(color_lineedit[i], color_values[i])

        return

    def settings_timing_read(self):
        # This function reads the settings for the timing values

        global timing_values

        for i in range(len(timing_lineedit)):
            timing_values[i] = setting_read(timing_lineedit[i])
        return

    def update_timing_values(self):
        # This function updates the lineedits of the timing values

        for i in range(len(timing_lineedit)):
            lineEdit_attribute = getattr(self, timing_lineedit[i] + '_lineEdit')
            lineEdit_attribute.setText(timing_values[i])
        return

    def apply_timing_values(self):
        # This function applies the changes of the timings values to the settings file

        self.settings_timing_read()

        for i in range(len(timing_lineedit)):
            lineEdit_attribute = getattr(self, timing_lineedit[i] + '_lineEdit')
            text = lineEdit_attribute.text()
            if timing_values[i] != text:
                timing_values[i] = text
                setting_write(timing_lineedit[i], timing_values[i])

        return

    def settings_combobox_read(self):
        # This function reads the settings for the combobox values

        global port_combobox_values

        for i in range(len(port_combobox_titles)):
            port_combobox_values[i] = setting_read(port_combobox_titles[i])

        print(port_combobox_values)
        return

    def update_combobox_values(self):
        # This function updates the lineedits of the combobox values

        for i in range(len(port_combobox_titles)):
            combobox_attribute = getattr(self, port_combobox_titles[i] + '_comboBox')

            if port_combobox_titles[i] == 'piano_size':

                if port_combobox_values[i] == 'S':
                    key_number = '61'
                elif port_combobox_values[i] == 'M':
                    key_number = '76'
                elif port_combobox_values[i] == 'L':
                    key_number = '88'

                combobox_attribute.setCurrentText(key_number + ' Key Piano - ' + port_combobox_values[i])

            else:

                combobox_attribute.addItem(port_combobox_values[i])
                combobox_attribute.setCurrentText(port_combobox_values[i])

        return

    def apply_combobox_values(self):
        # This function applies the changes of the combobox values to the settings file

        for i in range(len(port_combobox_titles)):
            combobox_attribute = getattr(self, port_combobox_titles[i] + '_comboBox')
            index = combobox_attribute.currentIndex()
            text = combobox_attribute.currentText()

            if index == -1: # If no choice selected, don't change settings
                print(port_combobox_titles[i] + " had no avaliable options. Settings were not changed.")
                continue

            if i == 0: # Piano Port Setting
                if port_combobox_values[i] != text:
                    #print("Piano Port Change")
                    #print(port_combobox_values[i])
                    #print(text)
                    setting_write(port_combobox_titles[i], text)

            if i == 1: # Piano Size Settings
                important_text = text[-1:]
                if port_combobox_values[i] != important_text:
                    #print("Piano Size Change")
                    #print(port_combobox_values[i])
                    #print(important_text)
                    setting_write(port_combobox_titles[i], important_text)

            if i == 2: # Arduino Port Setting
                if port_combobox_values[i] != text:
                    #print("Arduino Port Change")
                    #print(port_combobox_values[i])
                    #print(text)
                    setting_write(port_combobox_titles[i], text)
        return


################################OVERALL FUNCTIONS###############################

    def apply_changes(self):
        # This functions applies all the changes of the settings once the apply
        # button has been pressed

        self.apply_path()
        self.apply_mp3_2_midi_choice()
        self.apply_color_values()
        self.apply_timing_values()
        self.apply_combobox_values()
        self.apply_file_conversion_choice()

        return

################################################################################

    def retranslateUi(self):
        # This functions applies all the text features of the settings GUI

        _translate = QtCore.QCoreApplication.translate
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
        self.file_conversion_label.setText(_translate("Dialog","File Conversion User Control:"))
        self.yes_file_conversion_radioButton.setText(_translate("Dialog","Enabled"))
        self.no_file_conversion_radioButton.setText(_translate("Dialog","Disabled"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.path_tab), _translate("Dialog", "Path Settings"))
        self.timingsettings_label.setText(_translate("Dialog", "Timing Settings"))
        self.colorsettings_label.setText(_translate("Dialog", "Color Settings"))
        self.portsettings_label.setText(_translate("Dialog", "Port Settings"))
        self.piano_port_label.setText(_translate("Dialog", "Piano Port"))
        self.arduino_com_port_label.setText(_translate("Dialog", "Arduino Port"))
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
        self.time_per_tick_label.setText(_translate("Dialog", "Time per Ticks:"))
        self.increment_counter_label.setText(_translate("Dialog","Increment Counter Value:"))
        self.chord_timing_tolerance_label.setText(_translate("Dialog", "Chord Timing Tolerance:"))
        self.manual_final_chord_sustain_timing_label.setText(_translate("Dialog", "Manual Final Chord Sustain Timing: "))
        self.piano_size_label.setText(_translate("Dialog", "Piano Size"))
        self.piano_size_pushButton.setText(_translate("Dialog", "Piano Size Calibration"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tutor_tab), _translate("Dialog", "Tutoring Settings"))

################################################################################

"""
# This section allows you to
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    setting_dialog = SettingsDialog()
    setting_dialog.show()
    sys.exit(app.exec_())
"""
