# General Utility Libraries
import sys
import os
import warnings

# PyQt5, GUI Library
from PyQt5 import QtCore, QtGui, QtWidgets

# Serial and Midi Port Library
import rtmidi
import serial
import serial.tools.list_ports

# SKORE Library
from lib_skore import read_config, update_config
import globals

#-------------------------------------------------------------------------------
# Classes

class ArduinoComboBox(QtWidgets.QComboBox):

    """
    This class allows the combobox to recognize arduinos connected as soon as
    the user clicks the combobox.
    """

    def avaliable_arduino_com(self):

        """
        This fuction returns all the available COM ports in a list of strings.
        """

        ports = serial.tools.list_ports.comports(include_links=False)
        results = []

        for port in ports:
            results.append(str(port.device))

        return results

    def showPopup(self):

        """
        This function appends to the original showPopup function from the
        QComboBox by adding the avaliable arduino com ports.
        """

        avaliable_arduino_ports = self.avaliable_arduino_com()
        self.clear()

        for avaliable_port in avaliable_arduino_ports:
            self.addItem(avaliable_port)

        super(ArduinoComboBox, self).showPopup()

        return None

class PianoComboBox(QtWidgets.QComboBox):

    """
    This class allows the combobox to recognize piano connected as soon as the
    user clicks the combobox.
    """

    def avaliable_piano_port(self):

        """
        This function returns all the available MIDI ports in a list of string.
        """

        temp_midi_in = []
        temp_midi_in = rtmidi.MidiIn()
        avaliable_ports = temp_midi_in.get_ports()

        results = []
        for port_name in avaliable_ports:
            results.append(str(port_name))
        return results

    def showPopup(self):

        """
        This function appends to the showPopup function of the QComboBox by
        adding the avaliable MIDI ports to the listed items in the QComboBox.
        """

        avaliable_piano_ports = self.avaliable_piano_port()
        self.clear()

        for avaliable_piano_port_connected in avaliable_piano_ports:
            self.addItem(avaliable_piano_port_connected)

        super(PianoComboBox, self).showPopup()

        return None

class ConfigDialog(QtWidgets.QDialog):

    """
    This class is the settings dialog that provides the user the capability
    of changing the settings of the SKORE application.
    """

    finish_apply_signal = QtCore.pyqtSignal()

    def __init__(self):

        """
        This function sets the settings dialog by changing the title, size, icon,
        and placing the widgets.
        """

        super(QtWidgets.QDialog, self).__init__()

        self.setObjectName("Dialog")
        self.resize(530 * globals.S_W_R, 679 * globals.S_H_R)
        self.setWindowTitle("SKORE - General Configuration")
        self.setWindowIcon(QtGui.QIcon('.\images\skore_icon.png'))

        self.setup_ui()
        self.setup_func()
        self.read_all_settings()
        self.update_settings()

        return None

    def setup_ui(self):

        """
        This function places all the widgets in the settings dialog.
        """

        self.apply_close_buttonBox = QtWidgets.QDialogButtonBox(self)
        self.apply_close_buttonBox.setGeometry(QtCore.QRect(310 * globals.S_W_R, 640 * globals.S_H_R, 201 * globals.S_W_R, 32 * globals.S_H_R))
        self.apply_close_buttonBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.apply_close_buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.apply_close_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Close)
        self.apply_close_buttonBox.setObjectName("apply_cancel_buttonBox")

        #-----------------------------------------------------------------------
        # Tab Widget
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(10 * globals.S_W_R, 10 * globals.S_H_R, 511 * globals.S_W_R, 621 * globals.S_H_R))
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setObjectName("tabWidget")

        #-----------------------------------------------------------------------#
        # Tab Widget -> path_and_comm_tab

        self.path_and_comm_tab = QtWidgets.QWidget()
        self.path_and_comm_tab.setObjectName("path_and_comm_tab")

        #-----------------------------------------------------------------------
        # Tab Widget -> path_and_comm_tab -> path section
        self.configure_path_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.configure_path_label.setGeometry(QtCore.QRect(10 * globals.S_W_R, 5 * globals.S_H_R, 231 * globals.S_W_R, 16 * globals.S_H_R))
        self.configure_path_label.setObjectName("configure_path_label")

        self.path_line = QtWidgets.QFrame(self.path_and_comm_tab)
        self.path_line.setGeometry(QtCore.QRect(10 * globals.S_W_R, 20 * globals.S_H_R, 481 * globals.S_W_R, 20 * globals.S_H_R))
        self.path_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.path_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.path_line.setObjectName("path_line")

        self.audiveris_pushButton = QtWidgets.QPushButton(self.path_and_comm_tab)
        self.audiveris_pushButton.setGeometry(QtCore.QRect(400 * globals.S_W_R, 60 * globals.S_H_R, 93 * globals.S_W_R, 31 * globals.S_H_R))
        self.audiveris_pushButton.setObjectName("audiveris_pushButton")
        self.audiveris_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.audiveris_label.setGeometry(QtCore.QRect(10 * globals.S_W_R, 40 * globals.S_H_R, 101 * globals.S_W_R, 16 * globals.S_H_R))
        self.audiveris_label.setObjectName("audiveris_label")
        self.audiveris_lineEdit = QtWidgets.QLineEdit(self.path_and_comm_tab)
        self.audiveris_lineEdit.setGeometry(QtCore.QRect(10 * globals.S_W_R, 60 * globals.S_H_R, 381 * globals.S_W_R, 31 * globals.S_H_R))
        self.audiveris_lineEdit.setObjectName("audiveris_lineEdit")

        self.amazingmidi_lineEdit = QtWidgets.QLineEdit(self.path_and_comm_tab)
        self.amazingmidi_lineEdit.setGeometry(QtCore.QRect(10 * globals.S_W_R, 120 * globals.S_H_R, 381 * globals.S_W_R, 31 * globals.S_H_R))
        self.amazingmidi_lineEdit.setObjectName("amazingmidi_lineEdit")
        self.amazingmidi_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.amazingmidi_label.setGeometry(QtCore.QRect(10 * globals.S_W_R, 100 * globals.S_H_R, 121 * globals.S_W_R, 16 * globals.S_H_R))
        self.amazingmidi_label.setObjectName("amazingmidi_label")
        self.amazingmidi_pushButton = QtWidgets.QPushButton(self.path_and_comm_tab)
        self.amazingmidi_pushButton.setGeometry(QtCore.QRect(400 * globals.S_W_R, 120 * globals.S_H_R, 93 * globals.S_W_R, 31 * globals.S_H_R))
        self.amazingmidi_pushButton.setObjectName("amazingmidi_pushButton")

        self.anthemscore_pushButton = QtWidgets.QPushButton(self.path_and_comm_tab)
        self.anthemscore_pushButton.setGeometry(QtCore.QRect(400 * globals.S_W_R, 180 * globals.S_H_R, 93 * globals.S_W_R, 31 * globals.S_H_R))
        self.anthemscore_pushButton.setObjectName("anthemscore_pushButton")
        self.anthemscore_lineEdit = QtWidgets.QLineEdit(self.path_and_comm_tab)
        self.anthemscore_lineEdit.setGeometry(QtCore.QRect(10 * globals.S_W_R, 180 * globals.S_H_R, 381 * globals.S_W_R, 31 * globals.S_H_R))
        self.anthemscore_lineEdit.setObjectName("anthemscore_lineEdit")
        self.anthemscore_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.anthemscore_label.setGeometry(QtCore.QRect(10 * globals.S_W_R, 160 * globals.S_H_R, 191 * globals.S_W_R, 16 * globals.S_H_R))
        self.anthemscore_label.setObjectName("anthemscore_label")

        self.muse_score_pushButton = QtWidgets.QPushButton(self.path_and_comm_tab)
        self.muse_score_pushButton.setGeometry(QtCore.QRect(400 * globals.S_W_R, 240 * globals.S_H_R, 93 * globals.S_W_R, 31 * globals.S_H_R))
        self.muse_score_pushButton.setObjectName("muse_score_pushButton")
        self.muse_score_lineEdit = QtWidgets.QLineEdit(self.path_and_comm_tab)
        self.muse_score_lineEdit.setGeometry(QtCore.QRect(10 * globals.S_W_R, 240 * globals.S_H_R, 381 * globals.S_W_R, 31 * globals.S_H_R))
        self.muse_score_lineEdit.setObjectName("muse_score_linedEdit")
        self.muse_score_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.muse_score_label.setGeometry(QtCore.QRect(10 * globals.S_W_R, 220 * globals.S_H_R, 191 * globals.S_W_R, 16 * globals.S_H_R))
        self.muse_score_label.setObjectName("muse_score_label")

        self.mp3_to_midi_converter_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.mp3_to_midi_converter_label.setGeometry(QtCore.QRect(10 * globals.S_W_R, 280 * globals.S_H_R, 141 * globals.S_W_R, 16 * globals.S_H_R))
        self.mp3_to_midi_converter_label.setObjectName("mp3_to_midi_converter_label")

        self.open_source_radioButton = QtWidgets.QRadioButton(self.path_and_comm_tab)
        self.open_source_radioButton.setGeometry(QtCore.QRect(240 * globals.S_W_R, 280 * globals.S_H_R, 111 * globals.S_W_R, 20 * globals.S_H_R))
        self.open_source_radioButton.setObjectName("open_source_radioButton")
        self.close_source_radioButton = QtWidgets.QRadioButton(self.path_and_comm_tab)
        self.close_source_radioButton.setGeometry(QtCore.QRect(380 * globals.S_W_R, 280 * globals.S_H_R, 111 * globals.S_W_R, 20 * globals.S_H_R))
        self.close_source_radioButton.setObjectName("close_source_radioButton")

        #-----------------------------------------------------------------------
        # Tab Widget -> path_and_comm_tab -> comm section

        self.comm_line = QtWidgets.QFrame(self.path_and_comm_tab)
        self.comm_line.setGeometry(QtCore.QRect(10 * globals.S_W_R, 300 * globals.S_H_R, 481 * globals.S_W_R, 20 * globals.S_H_R))
        self.comm_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.comm_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.comm_line.setObjectName("comm_line")

        self.portsettings_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.portsettings_label.setGeometry(QtCore.QRect(210 * globals.S_W_R, 320 * globals.S_H_R, 81* globals.S_W_R, 20 * globals.S_H_R))
        self.portsettings_label.setObjectName("portsettings_label")

        self.piano_port_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.piano_port_label.setGeometry(QtCore.QRect(10 * globals.S_W_R, 340 * globals.S_H_R, 71 * globals.S_W_R, 16 * globals.S_H_R))
        self.piano_port_label.setObjectName("pianoport_label")
        self.piano_port_comboBox = PianoComboBox(self.path_and_comm_tab)
        self.piano_port_comboBox.setGeometry(QtCore.QRect(10 * globals.S_W_R, 360 * globals.S_H_R, 481 * globals.S_W_R, 31 * globals.S_H_R))
        self.piano_port_comboBox.setObjectName("pianoport_comboBox")

        self.piano_size_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.piano_size_label.setGeometry(QtCore.QRect(10 * globals.S_W_R, 400 * globals.S_H_R, 71* globals.S_W_R, 16* globals.S_H_R))
        self.piano_size_label.setObjectName("pianosize_label")
        self.piano_size_comboBox = QtWidgets.QComboBox(self.path_and_comm_tab)
        self.piano_size_comboBox.setGeometry(QtCore.QRect(10 * globals.S_W_R, 420 * globals.S_H_R, 481 * globals.S_W_R, 31 * globals.S_H_R))
        self.piano_size_comboBox.setObjectName("pianosize_comboBox")

        self.arduinoport_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.arduinoport_label.setGeometry(QtCore.QRect(10 * globals.S_W_R, 460 * globals.S_H_R, 81 * globals.S_W_R, 16* globals.S_H_R))
        self.arduinoport_label.setObjectName("arduinoport_label")
        self.arduino_port_comboBox = ArduinoComboBox(self.path_and_comm_tab)
        self.arduino_port_comboBox.setGeometry(QtCore.QRect(10 * globals.S_W_R, 480 * globals.S_H_R, 481 * globals.S_W_R, 31 * globals.S_H_R))
        self.arduino_port_comboBox.setObjectName("arduinoport_comboBox")

        self.arduino_baud_rate_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.arduino_baud_rate_label.setGeometry(QtCore.QRect(10 * globals.S_W_R, 520 * globals.S_H_R, 200 * globals.S_W_R, 20* globals.S_H_R))
        self.arduino_baud_rate_label.setText("Arduino Baud Rate")
        self.arduino_baud_rate_comboBox = QtWidgets.QComboBox(self.path_and_comm_tab)
        self.arduino_baud_rate_comboBox.setGeometry(QtCore.QRect(10 * globals.S_W_R, 540 * globals.S_H_R, 481* globals.S_W_R, 31 * globals.S_H_R))

        self.tabWidget.addTab(self.path_and_comm_tab, "")

        #-----------------------------------------------------------------------
        # Tab Widget -> Lighting and Color Tab

        self.color_tab = QtWidgets.QWidget()
        self.color_tab.setObjectName("color_tab")

        #-----------------------------------------------------------------------
        # Tab Widget -> Tutoring Tab -> Timing Section
        self.timingsettings_label = QtWidgets.QLabel(self.color_tab)
        self.timingsettings_label.setGeometry(QtCore.QRect(200 * globals.S_W_R, 10 * globals.S_H_R, 151 * globals.S_W_R, 20 * globals.S_H_R))
        self.timingsettings_label.setObjectName("timingsettings_label")

        self.chord_tick_tolerance_label = QtWidgets.QLabel(self.color_tab)
        self.chord_tick_tolerance_label.setGeometry(QtCore.QRect(20 * globals.S_W_R, 40* globals.S_H_R, 200 * globals.S_W_R, 20 * globals.S_H_R))
        self.chord_tick_tolerance_label.setText("Chord Tick Tolerance:")
        self.chord_tick_tolerance_lineEdit = QtWidgets.QLineEdit(self.color_tab)
        self.chord_tick_tolerance_lineEdit.setGeometry(QtCore.QRect(200 * globals.S_W_R, 40 * globals.S_H_R, 280 * globals.S_W_R, 20 * globals.S_H_R))

        self.chord_sum_tolerance_label = QtWidgets.QLabel(self.color_tab)
        self.chord_sum_tolerance_label.setGeometry(QtCore.QRect(20 * globals.S_W_R, 80 * globals.S_H_R, 200 * globals.S_W_R, 20 * globals.S_H_R))
        self.chord_sum_tolerance_label.setText("Chord Sum Tolerance:")
        self.chord_sum_tolerance_lineEdit = QtWidgets.QLineEdit(self.color_tab)
        self.chord_sum_tolerance_lineEdit.setGeometry(QtCore.QRect(200 * globals.S_W_R, 80 * globals.S_H_R, 280 * globals.S_W_R, 20 * globals.S_H_R))

        self.record_chord_tolerance_label = QtWidgets.QLabel(self.color_tab)
        self.record_chord_tolerance_label.setGeometry(QtCore.QRect(20* globals.S_W_R, 120 * globals.S_H_R, 200* globals.S_W_R, 20 * globals.S_H_R))
        self.record_chord_tolerance_label.setText("Record Chord Tolerance:")
        self.record_chord_tolerance_lineEdit = QtWidgets.QLineEdit(self.color_tab)
        self.record_chord_tolerance_lineEdit.setGeometry(QtCore.QRect(200* globals.S_W_R, 120 * globals.S_H_R, 280 * globals.S_W_R, 20 * globals.S_H_R))

        self.arduino_handshake_timeout_label = QtWidgets.QLabel(self.color_tab)
        self.arduino_handshake_timeout_label.setGeometry(QtCore.QRect(20 * globals.S_W_R, 160* globals.S_H_R, 200 * globals.S_W_R, 20 * globals.S_H_R))
        self.arduino_handshake_timeout_label.setText("Arduino Handshake Timeout:")
        self.arduino_handshake_timeout_lineEdit = QtWidgets.QLineEdit(self.color_tab)
        self.arduino_handshake_timeout_lineEdit.setGeometry(QtCore.QRect(200 * globals.S_W_R, 160 * globals.S_H_R, 280 * globals.S_W_R, 20 * globals.S_H_R))


        self.line = QtWidgets.QFrame(self.color_tab)
        self.line.setGeometry(QtCore.QRect(10 * globals.S_W_R, 230 * globals.S_H_R, 481 * globals.S_W_R, 16 * globals.S_H_R))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        #-----------------------------------------------------------------------
        # Tab Widget -> Tutoring Tab -> Color Section

        self.colorsettings_label = QtWidgets.QLabel(self.color_tab)
        self.colorsettings_label.setGeometry(QtCore.QRect(210 * globals.S_W_R, 250  * globals.S_H_R, 81 * globals.S_W_R, 20 * globals.S_H_R))
        self.colorsettings_label.setObjectName("colorsettings_label_2")

        bw_y = ( 250 + 40 ) * globals.S_H_R
        space = 20 * globals.S_H_R

        self.black_key_label = QtWidgets.QLabel(self.color_tab)
        self.black_key_label.setGeometry(QtCore.QRect(80 * globals.S_W_R, bw_y, 61  * globals.S_W_R, 16  * globals.S_H_R))
        self.black_key_label.setObjectName("black_key_label")
        self.black_key_pushButton = QtWidgets.QPushButton(self.color_tab)
        self.black_key_pushButton.setGeometry(QtCore.QRect(40 * globals.S_W_R, bw_y + space, 141 * globals.S_W_R, 61 * globals.S_H_R))
        self.black_key_pushButton.setText("")
        self.black_key_pushButton.setObjectName("black_key_pushButton")

        self.white_key_label = QtWidgets.QLabel(self.color_tab)
        self.white_key_label.setGeometry(QtCore.QRect(360 * globals.S_W_R, bw_y, 71 * globals.S_W_R, 16 * globals.S_H_R))
        self.white_key_label.setObjectName("white_key_label")
        self.white_key_pushButton = QtWidgets.QPushButton(self.color_tab)
        self.white_key_pushButton.setGeometry(QtCore.QRect(320 * globals.S_W_R, bw_y + space, 141 * globals.S_W_R, 61 * globals.S_W_R))
        self.white_key_pushButton.setText("")
        self.white_key_pushButton.setObjectName("white_key_pushButton")

        wu_y = ( 390 + 40 ) * globals.S_H_R

        self.wrong_label = QtWidgets.QLabel(self.color_tab)
        self.wrong_label.setGeometry(QtCore.QRect(75 * globals.S_W_R, wu_y, 71 * globals.S_W_R, 16 * globals.S_H_R))
        self.wrong_label.setObjectName("wrong_label")
        self.wrong_pushButton = QtWidgets.QPushButton(self.color_tab)
        self.wrong_pushButton.setGeometry(QtCore.QRect(40 * globals.S_W_R, wu_y + space, 141 * globals.S_W_R, 61 * globals.S_H_R))
        self.wrong_pushButton.setText("")
        self.wrong_pushButton.setObjectName("wrong_pushButton")


        self.upcoming_label = QtWidgets.QLabel(self.color_tab)
        self.upcoming_label.setGeometry(QtCore.QRect(350 * globals.S_W_R, wu_y, 91 * globals.S_W_R, 16 * globals.S_H_R))
        self.upcoming_label.setObjectName("upcoming_label")
        self.upcoming_pushButton = QtWidgets.QPushButton(self.color_tab)
        self.upcoming_pushButton.setGeometry(QtCore.QRect(320 * globals.S_W_R, wu_y + space, 141 * globals.S_W_R, 61 * globals.S_H_R))
        self.upcoming_pushButton.setText("")
        self.upcoming_pushButton.setObjectName("upcoming_pushButton")

        self.tabWidget.addTab(self.color_tab, "")

        self.retranslate_ui()
        self.tabWidget.setCurrentIndex(0)
        self.apply_close_buttonBox.accepted.connect(self.accept)
        self.apply_close_buttonBox.rejected.connect(self.close)
        QtCore.QMetaObject.connectSlotsByName(self)

    def setup_func(self):

        """
        This function places all the slot and signals for the widgets of the
        settings dialog.
        """

        self.browse_button_group = QtWidgets.QButtonGroup()
        self.browse_button_group.addButton(self.audiveris_pushButton)
        self.browse_button_group.addButton(self.amazingmidi_pushButton)
        self.browse_button_group.addButton(self.anthemscore_pushButton)
        self.browse_button_group.addButton(self.muse_score_pushButton)
        self.browse_button_group.buttonClicked.connect(self.upload_exe_file)

        self.browse_button_dict = {self.audiveris_pushButton: ['', self.audiveris_lineEdit, 'audiveris'], self.amazingmidi_pushButton: ['',self.amazingmidi_lineEdit, 'amazing_midi'],
                                   self.anthemscore_pushButton: ['', self.anthemscore_lineEdit,'anthemscore'], self.muse_score_pushButton: ['', self.muse_score_lineEdit, 'muse_score']}

        self.port_dict = {self.piano_port_comboBox: ['','piano'], self.piano_size_comboBox: ['','piano_size'],
                          self.arduino_port_comboBox: ['','arduino'], self.arduino_baud_rate_comboBox: ['', 'arduino baud rate']}

        self.piano_size_comboBox.addItem('76 Key Piano')
        self.piano_size_comboBox.addItem('88 Key Piano')

        self.arduino_baud_rate_comboBox.addItem('300')
        self.arduino_baud_rate_comboBox.addItem('600')
        self.arduino_baud_rate_comboBox.addItem('1200')
        self.arduino_baud_rate_comboBox.addItem('4800')
        self.arduino_baud_rate_comboBox.addItem('9600')
        self.arduino_baud_rate_comboBox.addItem('14400')
        self.arduino_baud_rate_comboBox.addItem('19200')
        self.arduino_baud_rate_comboBox.addItem('28800')
        self.arduino_baud_rate_comboBox.addItem('38400')
        self.arduino_baud_rate_comboBox.addItem('57600')
        self.arduino_baud_rate_comboBox.addItem('115200')
        self.arduino_baud_rate_comboBox.addItem('230400')

        self.timing_button_dict = {self.chord_tick_tolerance_lineEdit: ['', 'chord tick tolerance'], self.chord_sum_tolerance_lineEdit: ['','chord sum tolerance'],
                                   self.record_chord_tolerance_lineEdit: ['', 'record chord tolerance'], self.arduino_handshake_timeout_lineEdit: ['', 'count timeout']
                                   }

        self.color_button_group = QtWidgets.QButtonGroup()
        self.color_button_group.addButton(self.black_key_pushButton)
        self.color_button_group.addButton(self.white_key_pushButton)
        self.color_button_group.addButton(self.wrong_pushButton)
        self.color_button_group.addButton(self.upcoming_pushButton)
        self.color_button_group.buttonClicked.connect(self.color_picker)

        self.color_button_dict = {self.black_key_pushButton: ['','black'], self.white_key_pushButton: ['','white'],
                                  self.wrong_pushButton: ['','wrong'], self.upcoming_pushButton: ['','upcoming']
                                  }

        self.apply_close_buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(self.apply_changes)

        return None

    #---------------------------------------------------------------------------
    # Path Section Functions

    def open_file_name_dialog_exe_file(self):

        """
        This file dialog is used to obtain the file location of the .exe file.
        """

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select .exe/.bat File", "", "Executiable Files (*.exe);; Batch Files (*.bat)", options=options)

        if fileName:
            file_dialog_output = str(fileName)
        else:
            return ""

        file_dialog_output = file_dialog_output.replace('/' , '\\' )
        return file_dialog_output

    def open_directory_name_dialog_exe_path(self):

        """
        This file dialog is used to obtain the folder directory of the desired
        exe folder location.
        """

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ShowDirsOnly
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, caption = 'Select a folder', options = options)

        if directory:
            file_dialog_output = str(directory)
        else:
            return ""

        file_dialog_output = file_dialog_output.replace('/' , '\\' )
        return file_dialog_output

    def upload_exe_file(self, button):

        """
        This function decides wether to use the exe file or exe path function.
        If the pushButton is for audiveris, utlize the exe path. Else, use the
        standard exe file function.
        """

        upload_exe_path = self.open_file_name_dialog_exe_file()

        if upload_exe_path != '':
            self.browse_button_dict[button][0] = upload_exe_path
            self.update_settings()

        return None

    #---------------------------------------------------------------------------
    # Color

    def color_picker(self, button):

        """
        This function creates a QColorDialog when the user clicks the color
        wheel color. Once the user selects a color, it will display the RGB
        colors in the lineedits.
        """

        color = QtWidgets.QColorDialog.getColor()

        if color.isValid():
            # Converting Hexadecimal to RGB values
            value = color.name()
            value = value.lstrip('#')
            rgb = tuple(int(value[i:i+2], 16) for i in (0, 2, 4))
            rgb = str(rgb)[1:-1].replace(" ","")
            self.color_button_dict[button][0] = rgb
            button.setStyleSheet('background-color:rgb({})'.format(rgb))

        return None

    #---------------------------------------------------------------------------
    # Reading Settings

    def read_all_settings(self):

        """
        This function reads all the settings in the config.yml and stores them
        in dictionaries that correlate the settings to the widgets.
        """

        cfg = read_config()

        # Path Settings
        for key in self.browse_button_dict.keys():
            self.browse_button_dict[key][0] = cfg['app_path'][self.browse_button_dict[key][2]]

        # Mp3 to midi Settings
        self.mp3_to_midi_setting = cfg['app_path']['open_close_source']

        # Port Settings
        for key in self.port_dict.keys():
            self.port_dict[key][0] = cfg['port'][self.port_dict[key][1]]

        # Timing Settings
        for key in self.timing_button_dict.keys():
            self.timing_button_dict[key][0] = cfg['timing'][self.timing_button_dict[key][1]]

        # Color Settings
        for key in self.color_button_dict.keys():
            self.color_button_dict[key][0] = cfg['color'][self.color_button_dict[key][1]]

        return None

    def update_settings(self):

        """
        This function places the information of the settings into the widgets,
        such as placing the value or color to the widget.
        """

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
            elif key == self.arduino_baud_rate_comboBox:
                key.setCurrentText(str(self.port_dict[key][0]))
            else:
                key.addItem(str(self.port_dict[key][0]))
                key.setCurrentText(str(self.port_dict[key][0]))

        # Timing Settings
        for key in self.timing_button_dict.keys():
            key.setText(str(self.timing_button_dict[key][0]))

        # Color Settings
        for key in self.color_button_dict.keys():
            rgb = self.color_button_dict[key][0]
            key.setStyleSheet('background-color:rgb({})'.format(rgb))

        return None

    def apply_changes(self):

        """
        This fuction applies any of the changes done by the user to the settings.
        This changes are recorded in the config.yml file.
        """

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

        for key in self.timing_button_dict.keys():
            cfg['timing'][self.timing_button_dict[key][1]] = int(key.text())

        # Port Settings
        for key in self.port_dict.keys():
            index = key.currentIndex()

            if index == -1:
                continue

            if key == self.piano_port_comboBox or key == self.arduino_port_comboBox:
                cfg['port'][self.port_dict[key][1]] = key.currentText()

            elif key == self.piano_size_comboBox:
                cfg['port'][self.port_dict[key][1]] = key.currentText()[:2]

            elif key == self.arduino_baud_rate_comboBox:
                cfg['port'][self.port_dict[key][1]] = int(key.currentText())

        update_config(cfg)
        print("Applied Changes")
        self.finish_apply_signal.emit()

        return None

    #---------------------------------------------------------------------------
    # Misc Functions

    def retranslate_ui(self):

        """
        This function places all the text content in the configuration dialog
        widgets.
        """

        _translate = QtCore.QCoreApplication.translate

        self.anthemscore_pushButton.setText(_translate("Dialog", "Browse"))
        self.anthemscore_label.setText(_translate("Dialog", "AnthemScore [.exe] (Optional)"))

        self.audiveris_pushButton.setText(_translate("Dialog", "Browse"))
        self.audiveris_label.setText(_translate("Dialog", "Audiveris [folder]"))

        self.amazingmidi_pushButton.setText(_translate("Dialog", "Browse"))
        self.amazingmidi_label.setText(_translate("Dialog", "AmazingMIDI [.exe]"))

        self.muse_score_label.setText(_translate("Dialog", "MuseScore [.exe]"))
        self.muse_score_pushButton.setText(_translate("Dialog", "Browse"))

        self.configure_path_label.setText(_translate("Dialog", "Configure the path for each program."))

        self.mp3_to_midi_converter_label.setText(_translate("Dialog", "MP3 to MIDI Converter:"))
        self.open_source_radioButton.setText(_translate("Dialog", "Open-Source"))
        self.close_source_radioButton.setText(_translate("Dialog", "Close-Source"))

        self.piano_port_label.setText(_translate("Dialog", "Piano Port"))
        self.piano_size_label.setText(_translate("Dialog", "Piano Size"))
        self.portsettings_label.setText(_translate("Dialog", "Port Settings"))
        self.arduinoport_label.setText(_translate("Dialog", "Arduino Port"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.path_and_comm_tab), _translate("Dialog", "Path and Communication Settings"))

        self.timingsettings_label.setText(_translate("Dialog", "Timing Settings"))
        self.colorsettings_label.setText(_translate("Dialog", "Color Settings"))
        self.black_key_label.setText(_translate("Dialog", "Black Keys"))
        self.white_key_label.setText(_translate("Dialog", "White Keys"))
        self.wrong_label.setText(_translate("Dialog", "Wrong Note"))
        self.upcoming_label.setText(_translate("Dialog", "Upcoming Note"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.color_tab), _translate("Dialog", "Tutoring Settings"))

        #-----------------------------------------------------------------------
        # Text Scaling

        font = self.anthemscore_label.font()

        font.setPixelSize(13)
        print("Prescaling Font Pixel Size: ", font.pixelSize())
        font.setPixelSize(font.pixelSize() * globals.S_W_R)
        print("Postscaling Font Pixel Size: ", font.pixelSize())

        text_group = [self.anthemscore_pushButton, self.anthemscore_label, self.anthemscore_lineEdit,
                      self.audiveris_pushButton, self.audiveris_label, self.audiveris_lineEdit,
                      self.amazingmidi_pushButton, self.amazingmidi_label, self.amazingmidi_lineEdit,
                      self.muse_score_pushButton, self.muse_score_label, self.muse_score_lineEdit,
                      self.configure_path_label, self. mp3_to_midi_converter_label,
                      self.piano_port_label, self.piano_size_label, self.piano_size_comboBox,
                      self.portsettings_label, self.arduinoport_label, self.piano_port_comboBox,
                      self.arduino_port_comboBox, self.timingsettings_label, self.colorsettings_label,
                      self.black_key_label, self.white_key_label, self.wrong_label, self.upcoming_label,
                      self.arduino_baud_rate_comboBox, self.open_source_radioButton,
                      self.close_source_radioButton, self.chord_tick_tolerance_label,
                      self.chord_tick_tolerance_lineEdit, self.chord_sum_tolerance_label,
                      self.chord_sum_tolerance_lineEdit, self.record_chord_tolerance_label,
                      self.record_chord_tolerance_lineEdit, self.arduino_handshake_timeout_label,
                      self.arduino_handshake_timeout_lineEdit, self.apply_close_buttonBox,
                      self.tabWidget]

        for element in text_group:
            element.setFont(font)

#-------------------------------------------------------------------------------
# Main Code

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    config_dialog = ConfigDialog()
    config_dialog.show()
    sys.exit(app.exec_())
