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

# CRUCIAL!! This ensures that any dialog open within other .py files that import
# settings_dialog can open without crashing the entire application
#warnings.simplefilter("ignore", UserWarning)
#sys.coinit_flags = 2

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
            results.append(str(port.device))

        return results

    def showPopup(self):

        avaliable_arduino_ports = self.avaliable_arduino_com()
        self.clear()

        for avaliable_port in avaliable_arduino_ports:
            self.addItem(avaliable_port)

        super(ArduinoComboBox, self).showPopup()

        return None

class PianoComboBox(QtWidgets.QComboBox):
    # This class allows the combobox to recognize piano connected as soon as the
    # user clicks the combobox

    def avaliable_piano_port(self):
        # This function returns all the available MIDI ports in a list of string.

        temp_midi_in = []
        temp_midi_in = rtmidi.MidiIn()
        avaliable_ports = temp_midi_in.get_ports()

        results = []
        for port_name in avaliable_ports:
            results.append(str(port_name))
        return results

    def showPopup(self):

        avaliable_piano_ports = self.avaliable_piano_port()
        self.clear()

        for avaliable_piano_port_connected in avaliable_piano_ports:
            self.addItem(avaliable_piano_port_connected)

        super(PianoComboBox, self).showPopup()

        return None

class ConfigDialog(QtWidgets.QDialog):

    finish_apply_signal = QtCore.pyqtSignal()

    def __init__(self):
        super(QtWidgets.QDialog, self).__init__()

        self.setObjectName("Dialog")
        self.resize(530, 679)
        self.setWindowTitle("SKORE - General Configuration")
        self.setWindowIcon(QtGui.QIcon('.\images\skore_icon.png'))

        self.setup_ui()
        self.setup_func()
        self.read_all_settings()
        self.update_settings()

        return None

    def setup_ui(self):

        self.apply_cancel_buttonBox = QtWidgets.QDialogButtonBox(self)
        self.apply_cancel_buttonBox.setGeometry(QtCore.QRect(310, 640, 201, 32))
        self.apply_cancel_buttonBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.apply_cancel_buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.apply_cancel_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel)
        self.apply_cancel_buttonBox.setObjectName("apply_cancel_buttonBox")

        #-----------------------------------------------------------------------
        # Tab Widget
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 511, 621))
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setObjectName("tabWidget")

        #-----------------------------------------------------------------------#
        # Tab Widget -> path_and_comm_tab

        self.path_and_comm_tab = QtWidgets.QWidget()
        self.path_and_comm_tab.setObjectName("path_and_comm_tab")

        #-----------------------------------------------------------------------
        # Tab Widget -> path_and_comm_tab -> path section
        self.configure_path_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.configure_path_label.setGeometry(QtCore.QRect(10, 5, 231, 16))
        self.configure_path_label.setObjectName("configure_path_label")

        self.path_line = QtWidgets.QFrame(self.path_and_comm_tab)
        self.path_line.setGeometry(QtCore.QRect(10, 20, 481, 20))
        self.path_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.path_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.path_line.setObjectName("path_line")

        self.audiveris_pushButton = QtWidgets.QPushButton(self.path_and_comm_tab)
        self.audiveris_pushButton.setGeometry(QtCore.QRect(400, 60, 93, 31))
        self.audiveris_pushButton.setObjectName("audiveris_pushButton")
        self.audiveris_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.audiveris_label.setGeometry(QtCore.QRect(10, 40, 101, 16))
        self.audiveris_label.setObjectName("audiveris_label")
        self.audiveris_lineEdit = QtWidgets.QLineEdit(self.path_and_comm_tab)
        self.audiveris_lineEdit.setGeometry(QtCore.QRect(10, 60, 381, 31))
        self.audiveris_lineEdit.setObjectName("audiveris_lineEdit")

        self.amazingmidi_lineEdit = QtWidgets.QLineEdit(self.path_and_comm_tab)
        self.amazingmidi_lineEdit.setGeometry(QtCore.QRect(10, 120, 381, 31))
        self.amazingmidi_lineEdit.setObjectName("amazingmidi_lineEdit")
        self.amazingmidi_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.amazingmidi_label.setGeometry(QtCore.QRect(10, 100, 121, 16))
        self.amazingmidi_label.setObjectName("amazingmidi_label")
        self.amazingmidi_pushButton = QtWidgets.QPushButton(self.path_and_comm_tab)
        self.amazingmidi_pushButton.setGeometry(QtCore.QRect(400, 120, 93, 31))
        self.amazingmidi_pushButton.setObjectName("amazingmidi_pushButton")

        self.anthemscore_pushButton = QtWidgets.QPushButton(self.path_and_comm_tab)
        self.anthemscore_pushButton.setGeometry(QtCore.QRect(400, 180, 93, 31))
        self.anthemscore_pushButton.setObjectName("anthemscore_pushButton")
        self.anthemscore_lineEdit = QtWidgets.QLineEdit(self.path_and_comm_tab)
        self.anthemscore_lineEdit.setGeometry(QtCore.QRect(10, 180, 381, 31))
        self.anthemscore_lineEdit.setObjectName("anthemscore_lineEdit")
        self.anthemscore_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.anthemscore_label.setGeometry(QtCore.QRect(10, 160, 191, 16))
        self.anthemscore_label.setObjectName("anthemscore_label")

        self.muse_score_pushButton = QtWidgets.QPushButton(self.path_and_comm_tab)
        self.muse_score_pushButton.setGeometry(QtCore.QRect(400, 240, 93, 31))
        self.muse_score_pushButton.setObjectName("muse_score_pushButton")
        self.muse_score_lineEdit = QtWidgets.QLineEdit(self.path_and_comm_tab)
        self.muse_score_lineEdit.setGeometry(QtCore.QRect(10, 240, 381, 31))
        self.muse_score_lineEdit.setObjectName("muse_score_linedEdit")
        self.muse_score_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.muse_score_label.setGeometry(QtCore.QRect(10, 220, 191, 16))
        self.muse_score_label.setObjectName("muse_score_label")

        self.mp3_to_midi_converter_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.mp3_to_midi_converter_label.setGeometry(QtCore.QRect(10, 280, 141, 16))
        self.mp3_to_midi_converter_label.setObjectName("mp3_to_midi_converter_label")

        self.open_source_radioButton = QtWidgets.QRadioButton(self.path_and_comm_tab)
        self.open_source_radioButton.setGeometry(QtCore.QRect(240, 280, 111, 20))
        self.open_source_radioButton.setObjectName("open_source_radioButton")
        self.close_source_radioButton = QtWidgets.QRadioButton(self.path_and_comm_tab)
        self.close_source_radioButton.setGeometry(QtCore.QRect(380, 280, 111, 20))
        self.close_source_radioButton.setObjectName("close_source_radioButton")

        #-----------------------------------------------------------------------
        # Tab Widget -> path_and_comm_tab -> comm section

        self.comm_line = QtWidgets.QFrame(self.path_and_comm_tab)
        self.comm_line.setGeometry(QtCore.QRect(10, 300, 481, 20))
        self.comm_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.comm_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.comm_line.setObjectName("comm_line")

        self.portsettings_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.portsettings_label.setGeometry(QtCore.QRect(210, 320, 81, 20))
        self.portsettings_label.setObjectName("portsettings_label")

        self.piano_port_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.piano_port_label.setGeometry(QtCore.QRect(10, 340, 71, 16))
        self.piano_port_label.setObjectName("pianoport_label")
        self.piano_port_comboBox = PianoComboBox(self.path_and_comm_tab)
        self.piano_port_comboBox.setGeometry(QtCore.QRect(10, 360, 481, 31))
        self.piano_port_comboBox.setObjectName("pianoport_comboBox")

        self.piano_size_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.piano_size_label.setGeometry(QtCore.QRect(10, 400, 71, 16))
        self.piano_size_label.setObjectName("pianosize_label")
        self.piano_size_comboBox = QtWidgets.QComboBox(self.path_and_comm_tab)
        self.piano_size_comboBox.setGeometry(QtCore.QRect(10, 420, 481, 31))
        self.piano_size_comboBox.setObjectName("pianosize_comboBox")

        self.arduinoport_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.arduinoport_label.setGeometry(QtCore.QRect(10, 460, 81, 16))
        self.arduinoport_label.setObjectName("arduinoport_label")
        self.arduino_port_comboBox = ArduinoComboBox(self.path_and_comm_tab)
        self.arduino_port_comboBox.setGeometry(QtCore.QRect(10, 480, 481, 31))
        self.arduino_port_comboBox.setObjectName("arduinoport_comboBox")

        self.arduino_baud_rate_label = QtWidgets.QLabel(self.path_and_comm_tab)
        self.arduino_baud_rate_label.setGeometry(QtCore.QRect(10, 520, 200, 20))
        self.arduino_baud_rate_label.setText("Arduino Baud Rate")
        self.arduino_baud_rate_comboBox = QtWidgets.QComboBox(self.path_and_comm_tab)
        self.arduino_baud_rate_comboBox.setGeometry(QtCore.QRect(10, 540, 481, 31))

        self.tabWidget.addTab(self.path_and_comm_tab, "")

        #-----------------------------------------------------------------------
        # Tab Widget -> Lighting and Color Tab

        self.color_tab = QtWidgets.QWidget()
        self.color_tab.setObjectName("color_tab")

        #-----------------------------------------------------------------------
        # Tab Widget -> Tutoring Tab -> Timing Section
        self.timingsettings_label = QtWidgets.QLabel(self.color_tab)
        self.timingsettings_label.setGeometry(QtCore.QRect(200, 10, 151, 20))
        self.timingsettings_label.setObjectName("timingsettings_label")

        self.chord_tick_tolerance_label = QtWidgets.QLabel(self.color_tab)
        self.chord_tick_tolerance_label.setGeometry(QtCore.QRect(20, 40, 200, 20))
        self.chord_tick_tolerance_label.setText("Chord Tick Tolerance:")
        self.chord_tick_tolerance_lineEdit = QtWidgets.QLineEdit(self.color_tab)
        self.chord_tick_tolerance_lineEdit.setGeometry(QtCore.QRect(200, 40, 280, 20))

        self.chord_sum_tolerance_label = QtWidgets.QLabel(self.color_tab)
        self.chord_sum_tolerance_label.setGeometry(QtCore.QRect(20, 80, 200, 20))
        self.chord_sum_tolerance_label.setText("Chord Sum Tolerance:")
        self.chord_sum_tolerance_lineEdit = QtWidgets.QLineEdit(self.color_tab)
        self.chord_sum_tolerance_lineEdit.setGeometry(QtCore.QRect(200, 80, 280, 20))

        self.record_chord_tolerance_label = QtWidgets.QLabel(self.color_tab)
        self.record_chord_tolerance_label.setGeometry(QtCore.QRect(20, 120, 200, 20))
        self.record_chord_tolerance_label.setText("Record Chord Tolerance:")
        self.record_chord_tolerance_lineEdit = QtWidgets.QLineEdit(self.color_tab)
        self.record_chord_tolerance_lineEdit.setGeometry(QtCore.QRect(200, 120, 280, 20))

        self.arduino_handshake_timeout_label = QtWidgets.QLabel(self.color_tab)
        self.arduino_handshake_timeout_label.setGeometry(QtCore.QRect(20, 160, 200, 20))
        self.arduino_handshake_timeout_label.setText("Arduino Handshake Timeout:")
        self.arduino_handshake_timeout_lineEdit = QtWidgets.QLineEdit(self.color_tab)
        self.arduino_handshake_timeout_lineEdit.setGeometry(QtCore.QRect(200, 160, 280, 20))


        self.line = QtWidgets.QFrame(self.color_tab)
        self.line.setGeometry(QtCore.QRect(10, 230, 481, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        #-----------------------------------------------------------------------
        # Tab Widget -> Tutoring Tab -> Color Section

        self.colorsettings_label = QtWidgets.QLabel(self.color_tab)
        self.colorsettings_label.setGeometry(QtCore.QRect(210, 250, 81, 20))
        self.colorsettings_label.setObjectName("colorsettings_label_2")

        bw_y = 250 + 40
        space = 20

        self.black_key_label = QtWidgets.QLabel(self.color_tab)
        self.black_key_label.setGeometry(QtCore.QRect(80, bw_y, 61, 16))
        self.black_key_label.setObjectName("black_key_label")
        self.black_key_pushButton = QtWidgets.QPushButton(self.color_tab)
        self.black_key_pushButton.setGeometry(QtCore.QRect(40, bw_y + space, 141, 61))
        self.black_key_pushButton.setText("")
        self.black_key_pushButton.setObjectName("black_key_pushButton")

        self.white_key_label = QtWidgets.QLabel(self.color_tab)
        self.white_key_label.setGeometry(QtCore.QRect(360, bw_y, 71, 16))
        self.white_key_label.setObjectName("white_key_label")
        self.white_key_pushButton = QtWidgets.QPushButton(self.color_tab)
        self.white_key_pushButton.setGeometry(QtCore.QRect(320, bw_y + space, 141, 61))
        self.white_key_pushButton.setText("")
        self.white_key_pushButton.setObjectName("white_key_pushButton")

        wu_y = 390 + 40

        self.wrong_label = QtWidgets.QLabel(self.color_tab)
        self.wrong_label.setGeometry(QtCore.QRect(75, wu_y, 71, 16))
        self.wrong_label.setObjectName("wrong_label")
        self.wrong_pushButton = QtWidgets.QPushButton(self.color_tab)
        self.wrong_pushButton.setGeometry(QtCore.QRect(40, wu_y + space, 141, 61))
        self.wrong_pushButton.setText("")
        self.wrong_pushButton.setObjectName("wrong_pushButton")


        self.upcoming_label = QtWidgets.QLabel(self.color_tab)
        self.upcoming_label.setGeometry(QtCore.QRect(350, wu_y, 91, 16))
        self.upcoming_label.setObjectName("upcoming_label")
        self.upcoming_pushButton = QtWidgets.QPushButton(self.color_tab)
        self.upcoming_pushButton.setGeometry(QtCore.QRect(320, wu_y + space, 141, 61))
        self.upcoming_pushButton.setText("")
        self.upcoming_pushButton.setObjectName("upcoming_pushButton")

        self.tabWidget.addTab(self.color_tab, "")

        self.retranslate_ui()
        self.tabWidget.setCurrentIndex(0)
        self.apply_cancel_buttonBox.accepted.connect(self.accept)
        self.apply_cancel_buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def setup_func(self):

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

        self.apply_cancel_buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(self.apply_changes)

        return None

    #---------------------------------------------------------------------------
    # Path Section Functions

    def open_file_name_dialog_exe_file(self):

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select .exe File", "", "Executiable files (*.exe)", options=options)

        if fileName:
            file_dialog_output = str(fileName)
        else:
            return ""

        file_dialog_out

        put = file_dialog_output.replace('/' , '\\' )
        return file_dialog_output

    def open_directory_name_dialog_exe_path(self):

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

        if button != self.audiveris_pushButton:
            upload_exe_path = self.open_file_name_dialog_exe_file()
        else:
            upload_exe_path = self.open_directory_name_dialog_exe_path()

        self.browse_button_dict[button][0] = upload_exe_path

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

        # Timing Settings
        for key in self.timing_button_dict.keys():
            self.timing_button_dict[key][0] = cfg['timing'][self.timing_button_dict[key][1]]

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

#-------------------------------------------------------------------------------
# Main Code

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    config_dialog = ConfigDialog()
    config_dialog.show()
    sys.exit(app.exec_())
