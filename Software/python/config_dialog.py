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
from lib_skore import read_config, update_config

#-------------------------------------------------------------------------------
# Classes

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

class ConfigDialog(QtWidgets.QDialog):

    finish_apply_signal = QtCore.pyqtSignal()

    def __init__(self):
        super(QtWidgets.QDialog, self).__init__()

        self.setObjectName("Dialog")
        self.resize(530, 679)
        self.setWindowTitle("SKORE - General Configuration")

        self.setup_ui()
        self.setup_func()
        self.read_all_settings()
        self.update_settings()

        return None

    def setup_ui(self):
        self.apply_cancel_buttonBox = QtWidgets.QDialogButtonBox(self)
        self.apply_cancel_buttonBox.setGeometry(QtCore.QRect(310, 630, 201, 32))
        self.apply_cancel_buttonBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.apply_cancel_buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.apply_cancel_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel)
        self.apply_cancel_buttonBox.setObjectName("apply_cancel_buttonBox")

        #-----------------------------------------------------------------------
        # Tab Widget
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 511, 611))
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setObjectName("tabWidget")

        #-----------------------------------------------------------------------#
        # Tab Widget -> path_and_comm_tab

        self.path_and_comm_tab = QtWidgets.QWidget()
        self.path_and_comm_tab.setObjectName("path_and_comm_tab")

        #-----------------------------------------------------------------------
        # Tab Widget -> path_and_comm_tab -> path section
        self.configure_path_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.configure_path_label.setGeometry(QtCore.QRect(10, 10, 231, 16))
        self.configure_path_label.setObjectName("configure_path_label")

        self.audiveris_pushButton = QtWidgets.QPushButton(self.path_and_comm_tab)
        self.audiveris_pushButton.setGeometry(QtCore.QRect(400, 70, 93, 31))
        self.audiveris_pushButton.setObjectName("audiveris_pushButton")
        self.audiveris_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.audiveris_label.setGeometry(QtCore.QRect(10, 50, 101, 16))
        self.audiveris_label.setObjectName("audiveris_label")
        self.audiveris_lineEdit = QtWidgets.QLineEdit(self.path_and_comm_tab)
        self.audiveris_lineEdit.setGeometry(QtCore.QRect(10, 70, 381, 31))
        self.audiveris_lineEdit.setObjectName("audiveris_lineEdit")

        self.amazingmidi_lineEdit = QtWidgets.QLineEdit(self.path_and_comm_tab)
        self.amazingmidi_lineEdit.setGeometry(QtCore.QRect(10, 130, 381, 31))
        self.amazingmidi_lineEdit.setObjectName("amazingmidi_lineEdit")
        self.amazingmidi_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.amazingmidi_label.setGeometry(QtCore.QRect(10, 110, 121, 16))
        self.amazingmidi_label.setObjectName("amazingmidi_label")
        self.amazingmidi_pushButton = QtWidgets.QPushButton(self.path_and_comm_tab)
        self.amazingmidi_pushButton.setGeometry(QtCore.QRect(400, 130, 93, 31))
        self.amazingmidi_pushButton.setObjectName("amazingmidi_pushButton")

        self.anthemscore_pushButton = QtWidgets.QPushButton(self.path_and_comm_tab)
        self.anthemscore_pushButton.setGeometry(QtCore.QRect(400, 190, 93, 31))
        self.anthemscore_pushButton.setObjectName("anthemscore_pushButton")
        self.anthemscore_lineEdit = QtWidgets.QLineEdit(self.path_and_comm_tab)
        self.anthemscore_lineEdit.setGeometry(QtCore.QRect(10, 190, 381, 31))
        self.anthemscore_lineEdit.setObjectName("anthemscore_lineEdit")
        self.anthemscore_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.anthemscore_label.setGeometry(QtCore.QRect(10, 170, 191, 16))
        self.anthemscore_label.setObjectName("anthemscore_label")

        self.muse_score_pushButton = QtWidgets.QPushButton(self.path_and_comm_tab)
        self.muse_score_pushButton.setGeometry(QtCore.QRect(400, 250, 93, 31))
        self.muse_score_pushButton.setObjectName("muse_score_pushButton")
        self.muse_score_lineEdit = QtWidgets.QLineEdit(self.path_and_comm_tab)
        self.muse_score_lineEdit.setGeometry(QtCore.QRect(10, 250, 381, 31))
        self.muse_score_lineEdit.setObjectName("muse_score_linedEdit")
        self.muse_score_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.muse_score_label.setGeometry(QtCore.QRect(10, 230, 191, 16))
        self.muse_score_label.setObjectName("muse_score_label")

        self.mp3_to_midi_converter_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.mp3_to_midi_converter_label.setGeometry(QtCore.QRect(10, 300, 141, 16))
        self.mp3_to_midi_converter_label.setObjectName("mp3_to_midi_converter_label")

        self.open_source_radioButton = QtWidgets.QRadioButton(self.path_and_comm_tab)
        self.open_source_radioButton.setGeometry(QtCore.QRect(240, 300, 111, 20))
        self.open_source_radioButton.setObjectName("open_source_radioButton")
        self.close_source_radioButton = QtWidgets.QRadioButton(self.path_and_comm_tab)
        self.close_source_radioButton.setGeometry(QtCore.QRect(380, 300, 111, 20))
        self.close_source_radioButton.setObjectName("close_source_radioButton")

        self.path_line = QtWidgets.QFrame(self.path_and_comm_tab)
        self.path_line.setGeometry(QtCore.QRect(10, 30, 481, 20))
        self.path_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.path_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.path_line.setObjectName("path_line")

        #-----------------------------------------------------------------------
        # Tab Widget -> path_and_comm_tab -> comm section

        self.pianoport_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.pianoport_label.setGeometry(QtCore.QRect(10, 360, 71, 16))
        self.pianoport_label.setObjectName("pianoport_label")
        self.pianosize_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.pianosize_label.setGeometry(QtCore.QRect(10, 420, 71, 16))
        self.pianosize_label.setObjectName("pianosize_label")

        self.portsettings_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.portsettings_label.setGeometry(QtCore.QRect(210, 340, 81, 20))
        self.portsettings_label.setObjectName("portsettings_label")

        #self.piano_port_comboBox = QtWidgets.QComboBox(self.path_and_comm_tab)
        self.piano_port_comboBox = PianoComboBox(self.path_and_comm_tab)
        self.piano_port_comboBox.setGeometry(QtCore.QRect(10, 380, 481, 31))
        self.piano_port_comboBox.setObjectName("pianoport_comboBox")

        self.arduinoport_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.arduinoport_label.setGeometry(QtCore.QRect(10, 480, 81, 16))
        self.arduinoport_label.setObjectName("arduinoport_label")

        #self.arduino_port_comboBox = QtWidgets.QComboBox(self.path_and_comm_tab)
        self.arduino_port_comboBox = ArduinoComboBox(self.path_and_comm_tab)
        self.arduino_port_comboBox.setGeometry(QtCore.QRect(10, 500, 481, 31))
        self.arduino_port_comboBox.setObjectName("arduinoport_comboBox")

        self.piano_size_comboBox = QtWidgets.QComboBox(self.path_and_comm_tab)
        self.piano_size_comboBox.setGeometry(QtCore.QRect(10, 441, 481, 31))
        self.piano_size_comboBox.setObjectName("pianosize_comboBox")

        self.comm_line = QtWidgets.QFrame(self.path_and_comm_tab)
        self.comm_line.setGeometry(QtCore.QRect(10, 320, 481, 20))
        self.comm_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.comm_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.comm_line.setObjectName("comm_line")
        self.tabWidget.addTab(self.path_and_comm_tab, "")

        #-----------------------------------------------------------------------
        # Tab Widget -> Lighting and Color Tab

        self.color_tab = QtWidgets.QWidget()
        self.color_tab.setObjectName("color_tab")

        #-----------------------------------------------------------------------
        # Tab Widget -> Lighting and Color Tab -> Lighting Section
        self.colorsettings_label = QtWidgets.QLabel(self.color_tab)
        self.colorsettings_label.setGeometry(QtCore.QRect(170, 10, 151, 20))
        self.colorsettings_label.setObjectName("colorsettings_label")

        self.beginner_comboBox = QtWidgets.QComboBox(self.color_tab)
        self.beginner_comboBox.setGeometry(QtCore.QRect(10, 60, 481, 31))
        self.beginner_comboBox.setObjectName("beginner_comboBox")
        self.beginner_label = QtWidgets.QLabel(self.color_tab)
        self.beginner_label.setGeometry(QtCore.QRect(10, 40, 191, 16))
        self.beginner_label.setObjectName("beginner_label")

        self.intermediate_label = QtWidgets.QLabel(self.color_tab)
        self.intermediate_label.setGeometry(QtCore.QRect(10, 100, 221, 16))
        self.intermediate_label.setObjectName("intermediate_label")
        self.intermediate_comboBox = QtWidgets.QComboBox(self.color_tab)
        self.intermediate_comboBox.setGeometry(QtCore.QRect(10, 120, 481, 31))
        self.intermediate_comboBox.setObjectName("intermediate_comboBox")

        self.expert_label = QtWidgets.QLabel(self.color_tab)
        self.expert_label.setGeometry(QtCore.QRect(10, 160, 251, 16))
        self.expert_label.setObjectName("expert_label")
        self.expert_comboBox = QtWidgets.QComboBox(self.color_tab)
        self.expert_comboBox.setGeometry(QtCore.QRect(10, 180, 481, 31))
        self.expert_comboBox.setObjectName("expert_comboBox")

        self.line = QtWidgets.QFrame(self.color_tab)
        self.line.setGeometry(QtCore.QRect(10, 230, 481, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        #-----------------------------------------------------------------------
        # Tab Widget -> Lighting and Color Tab -> Color Section

        self.colorsettings_label_2 = QtWidgets.QLabel(self.color_tab)
        self.colorsettings_label_2.setGeometry(QtCore.QRect(210, 250, 81, 20))
        self.colorsettings_label_2.setObjectName("colorsettings_label_2")

        #-----------------------------------------------------------------------
        # Tab Widget -> Lighting and Color Tab -> Color Section -> toolBox
        self.toolBox = QtWidgets.QToolBox(self.color_tab)
        self.toolBox.setGeometry(QtCore.QRect(10, 276, 481, 291))
        self.toolBox.setObjectName("toolBox")

        #-----------------------------------------------------------------------
        # Tab Widget -> Lighting and Color Tab -> Color Section -> toolBox -> BW page
        self.black_and_white_page = QtWidgets.QWidget()
        self.black_and_white_page.setGeometry(QtCore.QRect(0, 0, 481, 198))
        self.black_and_white_page.setObjectName("black_and_white_page")

        self.black_key_pushButton = QtWidgets.QPushButton(self.black_and_white_page)
        self.black_key_pushButton.setGeometry(QtCore.QRect(30, 80, 141, 61))
        self.black_key_pushButton.setText("")
        self.black_key_pushButton.setObjectName("black_key_pushButton")
        self.black_key_label = QtWidgets.QLabel(self.black_and_white_page)
        self.black_key_label.setGeometry(QtCore.QRect(70, 40, 61, 16))
        self.black_key_label.setObjectName("black_key_label")

        self.white_key_label = QtWidgets.QLabel(self.black_and_white_page)
        self.white_key_label.setGeometry(QtCore.QRect(340, 40, 71, 16))
        self.white_key_label.setObjectName("white_key_label")
        self.white_key_pushButton = QtWidgets.QPushButton(self.black_and_white_page)
        self.white_key_pushButton.setGeometry(QtCore.QRect(300, 80, 141, 61))
        self.white_key_pushButton.setText("")
        self.white_key_pushButton.setObjectName("white_key_pushButton")
        self.toolBox.addItem(self.black_and_white_page, "")

        #-----------------------------------------------------------------------
        # Tab Widget -> Lighting and Color Tab -> Color Section -> toolBox -> RWU Page
        self.right_wrong_and_upcoming_page = QtWidgets.QWidget()
        self.right_wrong_and_upcoming_page.setGeometry(QtCore.QRect(0, 0, 481, 198))
        self.right_wrong_and_upcoming_page.setObjectName("right_wrong_and_upcoming_page")

        self.right_pushButton = QtWidgets.QPushButton(self.right_wrong_and_upcoming_page)
        self.right_pushButton.setGeometry(QtCore.QRect(10, 70, 141, 61))
        self.right_pushButton.setText("")
        self.right_pushButton.setObjectName("right_pushButton")

        self.wrong_pushButton = QtWidgets.QPushButton(self.right_wrong_and_upcoming_page)
        self.wrong_pushButton.setGeometry(QtCore.QRect(170, 70, 141, 61))
        self.wrong_pushButton.setText("")
        self.wrong_pushButton.setObjectName("wrong_pushButton")

        self.upcoming_pushButton = QtWidgets.QPushButton(self.right_wrong_and_upcoming_page)
        self.upcoming_pushButton.setGeometry(QtCore.QRect(330, 70, 141, 61))
        self.upcoming_pushButton.setText("")
        self.upcoming_pushButton.setObjectName("upcoming_pushButton")

        self.right_label = QtWidgets.QLabel(self.right_wrong_and_upcoming_page)
        self.right_label.setGeometry(QtCore.QRect(50, 30, 61, 16))
        self.right_label.setObjectName("right_label")

        self.wrong_label = QtWidgets.QLabel(self.right_wrong_and_upcoming_page)
        self.wrong_label.setGeometry(QtCore.QRect(200, 30, 71, 16))
        self.wrong_label.setObjectName("wrong_label")

        self.upcoming_label = QtWidgets.QLabel(self.right_wrong_and_upcoming_page)
        self.upcoming_label.setGeometry(QtCore.QRect(360, 30, 91, 16))
        self.upcoming_label.setObjectName("upcoming_label")
        self.toolBox.addItem(self.right_wrong_and_upcoming_page, "")

        #-----------------------------------------------------------------------
        # Tab Widget -> Lighting and Color Tab -> Color Section -> toolBox -> UI page
        self.upcoming_and_immediate_page = QtWidgets.QWidget()
        self.upcoming_and_immediate_page.setObjectName("upcoming_and_immediate_page")

        self.upcoming_pushButton_page3 = QtWidgets.QPushButton(self.upcoming_and_immediate_page)
        self.upcoming_pushButton_page3.setGeometry(QtCore.QRect(30, 80, 141, 61))
        self.upcoming_pushButton_page3.setText("")
        self.upcoming_pushButton_page3.setObjectName("upcoming_pushButton_page3")

        self.immediate_pushButton = QtWidgets.QPushButton(self.upcoming_and_immediate_page)
        self.immediate_pushButton.setGeometry(QtCore.QRect(300, 80, 141, 61))
        self.immediate_pushButton.setText("")
        self.immediate_pushButton.setObjectName("immediate_pushButton")

        self.upcoming_label_page3 = QtWidgets.QLabel(self.upcoming_and_immediate_page)
        self.upcoming_label_page3.setGeometry(QtCore.QRect(70, 40, 55, 16))
        self.upcoming_label_page3.setObjectName("upcoming_label_page3")

        self.immediate_label = QtWidgets.QLabel(self.upcoming_and_immediate_page)
        self.immediate_label.setGeometry(QtCore.QRect(340, 40, 71, 16))
        self.immediate_label.setObjectName("immediate_label")
        self.toolBox.addItem(self.upcoming_and_immediate_page, "")
        self.tabWidget.addTab(self.color_tab, "")

        self.retranslate_ui()
        self.tabWidget.setCurrentIndex(0)
        self.toolBox.setCurrentIndex(0)
        self.apply_cancel_buttonBox.accepted.connect(self.accept)
        self.apply_cancel_buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def setup_func(self):

        self.browse_button_group = QButtonGroup()
        self.browse_button_group.addButton(self.audiveris_pushButton)
        self.browse_button_group.addButton(self.amazingmidi_pushButton)
        self.browse_button_group.addButton(self.anthemscore_pushButton)
        self.browse_button_group.addButton(self.muse_score_pushButton)
        self.browse_button_group.buttonClicked.connect(self.upload_exe_file)

        self.browse_button_dict = {self.audiveris_pushButton: ['', self.audiveris_lineEdit, 'audiveris'], self.amazingmidi_pushButton: ['',self.amazingmidi_lineEdit, 'amazing_midi'],
                                   self.anthemscore_pushButton: ['', self.anthemscore_lineEdit,'anthemscore'], self.muse_score_pushButton: ['', self.muse_score_lineEdit, 'muse_score']}

        self.port_dict = {self.piano_port_comboBox: ['','piano'], self.piano_size_comboBox: ['','piano_size'],
                          self.arduino_port_comboBox: ['','arduino']}

        self.piano_size_comboBox.addItem('76 Key Piano')
        self.piano_size_comboBox.addItem('88 Key Piano')

        self.beginner_comboBox.addItem("Black and White Key Distinction")
        self.beginner_comboBox.addItem("Right, Wrong, and Upcoming Note Distinction")
        self.beginner_comboBox.addItem("Upcoming and Immediate Note Distinction")

        self.intermediate_comboBox.addItem("Black and White Key Distinction")
        self.intermediate_comboBox.addItem("Right, Wrong, and Upcoming Note Distinction")
        self.intermediate_comboBox.addItem("Upcoming and Immediate Note Distinction")

        self.expert_comboBox.addItem("Black and White Key Distinction")
        self.expert_comboBox.addItem("Right, Wrong, and Upcoming Note Distinction")

        self.lighting_combobox_dict = {self.beginner_comboBox: ['','beginner'], self.intermediate_comboBox: ['','intermediate'],
                                       self.expert_comboBox: ['','expert']}

        self.color_button_group = QButtonGroup()
        self.color_button_group.addButton(self.black_key_pushButton)
        self.color_button_group.addButton(self.white_key_pushButton)
        self.color_button_group.addButton(self.right_pushButton)
        self.color_button_group.addButton(self.wrong_pushButton)
        self.color_button_group.addButton(self.upcoming_pushButton)
        self.color_button_group.addButton(self.upcoming_pushButton_page3)
        self.color_button_group.addButton(self.immediate_pushButton)
        self.color_button_group.buttonClicked.connect(self.color_picker)

        """
        self.color_button_dict = {self.black_key_pushButton: ['','black'], self.white_key_pushButton: ['','white'],
                                  self.right_pushButton: ['','right'], self.wrong_pushButton: ['','wrong'], self.upcoming_pushButton: ['','upcoming'],
                                  self.upcoming_pushButton_page3: ['','upcoming'], self.immediate_pushButton: ['','immediate']}
        """

        self.color_button_dict = {self.black_key_pushButton: ['','black'], self.white_key_pushButton: ['','white'],
                                  self.right_pushButton: ['','right'], self.wrong_pushButton: ['','wrong'], self.upcoming_pushButton: ['','upcoming'],
                                  self.upcoming_pushButton_page3: ['','upcoming']}

        self.apply_cancel_buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.apply_changes)

        return None

    #---------------------------------------------------------------------------
    # Path Section Functions

    def open_file_name_dialog_exe_file(self):

        #fileName, _ = QFileDialog.getOpenFileName(caption = "Select Audio File", filter = "All Supported Files (*.mid *.mp3 *.pdf);;All Files (*.*);;MIDI Files(*.mid);;MP3 Files(*.mp3);;PDF Files (*.pdf)")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select .exe File", "", "Executiable files (*.exe)", options=options)

        if fileName:
            file_dialog_output = str(fileName)
        else:
            return ""

        file_dialog_out

        put = file_dialog_output.replace('/' , '\\' )
        return file_dialog_output

    def open_directory_name_dialog_exe_path(self):

        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        options |= QFileDialog.DontUseNativeDialog
        #directory = QFileDialog.getExistingDirectory(self, caption = 'Open a folder', directory = skore_path, options = options)
        directory = QFileDialog.getExistingDirectory(self, caption = 'Select a folder', options = options)

        if directory:
            file_dialog_output = str(directory)
        else:
            return ""

        file_dialog_output = file_dialog_output.replace('/' , '\\' )
        return file_dialog_output

    def upload_exe_file(self, button):

        if button == self.audiveris_pushButton:
            upload_exe_path = self.openDirectoryDialog_ExecPath()
        else:
            upload_exe_path = self.openFileNameDialog_ExecPath()

        self.browse_button_dict[button][0] = upload_exe_path
        #self.update_path()

        return None

    #---------------------------------------------------------------------------
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
            rgb = tuple(int(value[i:i+2], 16) for i in (0, 2, 4))
            rgb = str(rgb)[1:-1].replace(" ","")
            self.color_button_dict[button][0] = rgb
            button.setStyleSheet('background-color:rgb({})'.format(rgb))

            if button == self.upcoming_pushButton_page3:
                self.color_button_dict[self.upcoming_pushButton][0] = rgb
                self.upcoming_pushButton.setStyleSheet('background-color:rgb({})'.format(rgb))
            elif button == self.upcoming_pushButton:
                self.color_button_dict[self.upcoming_pushButton_page3][0] = rgb
                self.upcoming_pushButton_page3.setStyleSheet('background-color:rgb({})'.format(rgb))

        return None

    #---------------------------------------------------------------------------
    # Reading Settings

    def read_all_settings(self):
        cfg = read_config()

        # Path Settings
        for key in self.browse_button_dict.keys():
            self.browse_button_dict[key][0] = cfg['app_path'][self.browse_button_dict[key][2]]

        # Mp3 to midi Settings
        self.mp3_to_midi_setting = cfg['app_path']['open_close_source']

        # Port Settings
        for key in self.port_dict.keys():
            self.port_dict[key][0] = cfg['port'][self.port_dict[key][1]]


        # Lighting Settings
        for key in self.lighting_combobox_dict.keys():
            self.lighting_combobox_dict[key][0] = cfg['lighting scheme'][self.lighting_combobox_dict[key][1]]

        # Color Settings
        for key in self.color_button_dict.keys():
            self.color_button_dict[key][0] = cfg['color'][self.color_button_dict[key][1]]

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

        # Port Settings
        for key in self.port_dict.keys():
            if self.port_dict[key][1] == 'piano_size':
                key.setCurrentText(str(self.port_dict[key][0]) + ' Key Piano')
            else:
                key.addItem(self.port_dict[key][0])
                key.setCurrentText(self.port_dict[key][0])

        # Lighting Settings
        for key in self.lighting_combobox_dict.keys():
            if self.lighting_combobox_dict[key][0] == 'BW':
                key.setCurrentText("Black and White Key Distinction")
            elif self.lighting_combobox_dict[key][0] == "RWU":
                key.setCurrentText("Right, Wrong, and Upcoming Note Distinction")
            else:
                key.setCurrentText("Upcoming and Immediate Note Distinction")

        # Color Settings
        for key in self.color_button_dict.keys():
            rgb = self.color_button_dict[key][0]
            key.setStyleSheet('background-color:rgb({})'.format(rgb))

        return None

    def apply_changes(self):
        print("Applied Changes")
        cfg = read_config()

        # Apply Path
        for button in self.browse_button_dict:
            text = self.browse_button_dict[button][1].text()
            cfg['app_path'][self.browse_button_dict[button][2]] = text

        # Mp3 to midi Settings
        if self.open_source_radioButton.isChecked():
            cfg['app_path']['open_close_source'] = 'open_source'
        elif self.close_source_radioButton.isChecked():
            cfg['app_path']['open_close_source'] = 'close_source'

        # Color Settings
        for key in self.color_button_dict.keys():
            rgb = self.color_button_dict[key][0]
            cfg['color'][self.color_button_dict[key][1]] = rgb

        # Ligthing Scheme Settings
        for key in self.lighting_combobox_dict.keys():
            if key.currentText() == 'Black and White Key Distinction':
                cfg['lighting scheme'][self.lighting_combobox_dict[key][1]] = 'BW'
            elif key.currentText() == 'Right, Wrong, and Upcoming Note Distinction':
                cfg['lighting scheme'][self.lighting_combobox_dict[key][1]] = 'RWU'
            elif key.currentText() == 'Upcoming and Immediate Note Distinction':
                cfg['lighting scheme'][self.lighting_combobox_dict[key][1]] = 'UI'

        # Port Settings
        for key in self.port_dict.keys():
            index = key.currentIndex()

            if index == -1:
                continue

            if key == self.piano_port_comboBox or key == self.arduino_port_comboBox:
                cfg['port'][self.port_dict[key][1]] = key.currentText()

            elif key == self.piano_size_comboBox:
                cfg['port'][self.port_dict[key][1]] = key.currentText()[:2]


        self.finish_apply_signal.emit()

        update_config(cfg)

        return None

    #---------------------------------------------------------------------------
    # Misc Functions

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.anthemscore_pushButton.setText(_translate("Dialog", "Browse"))
        self.audiveris_pushButton.setText(_translate("Dialog", "Browse"))
        self.anthemscore_label.setText(_translate("Dialog", "AnthemScore [.exe] (Optional)"))
        self.audiveris_label.setText(_translate("Dialog", "Audiveris [folder]"))
        self.amazingmidi_label.setText(_translate("Dialog", "AmazingMIDI [.exe]"))
        self.muse_score_label.setText(_translate("Dialog", "MuseScore [.exe]"))
        self.muse_score_pushButton.setText(_translate("Dialog", "Browse"))
        self.configure_path_label.setText(_translate("Dialog", "Configure the path for each program."))
        self.amazingmidi_pushButton.setText(_translate("Dialog", "Browse"))
        self.mp3_to_midi_converter_label.setText(_translate("Dialog", "MP3 to MIDI Converter:"))
        self.open_source_radioButton.setText(_translate("Dialog", "Open-Source"))
        self.close_source_radioButton.setText(_translate("Dialog", "Close-Source"))
        self.pianoport_label.setText(_translate("Dialog", "Piano Port"))
        self.pianosize_label.setText(_translate("Dialog", "Piano Size"))
        self.portsettings_label.setText(_translate("Dialog", "Port Settings"))
        self.arduinoport_label.setText(_translate("Dialog", "Arduino Port"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.path_and_comm_tab), _translate("Dialog", "Path and Communication Settings"))
        self.colorsettings_label.setText(_translate("Dialog", "Lighting Scheme Settings"))
        self.beginner_label.setText(_translate("Dialog", "Beginner Mode Lighting Scheme"))
        self.intermediate_label.setText(_translate("Dialog", "Intermediate Mode Lighting Scheme"))
        self.expert_label.setText(_translate("Dialog", "Expert Mode Lighting Scheme"))
        self.colorsettings_label_2.setText(_translate("Dialog", "Color Settings"))
        self.black_key_label.setText(_translate("Dialog", "Black Keys"))
        self.white_key_label.setText(_translate("Dialog", "White Keys"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.black_and_white_page), _translate("Dialog", "Black and White Key Distinction"))
        self.right_label.setText(_translate("Dialog", "Right Note"))
        self.wrong_label.setText(_translate("Dialog", "Wrong Note"))
        self.upcoming_label.setText(_translate("Dialog", "Upcoming Note"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.right_wrong_and_upcoming_page), _translate("Dialog", "Right, Wrong, and Upcoming Note Distinction"))
        self.upcoming_label_page3.setText(_translate("Dialog", "Upcoming"))
        self.immediate_label.setText(_translate("Dialog", "Immediate"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.upcoming_and_immediate_page), _translate("Dialog", "Upcoming and Immediate Note Distinction"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.color_tab), _translate("Dialog", "Lighting and Color Settings"))

#-------------------------------------------------------------------------------
# Main Code

"""
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    config_dialog = ConfigDialog()
    config_dialog.show()
    sys.exit(app.exec_())
"""
