# General Utility Libraries
import time
import sys
import os
import difflib
import webbrowser
import ast
import pathlib
import ntpath

# PyQt5, GUI Library
from PyQt5 import QtCore, QtGui, QtWidgets

# Serial and Midi Port Library
import mido
import serial
import rtmidi

# SKORE Modules
import globals

from tutor_and_midi_classes import Tutor, TutorMidiHandler, SkoreMetaEvent, SkoreMidiEvent
from main_window_graphics import GraphicsSystemMessage, GraphicsPlayedLabel, GraphicsPlayedNameLabel
from main_window_graphics import GraphicsController, GraphicsNote
from lib_skore import FileContainer, read_config, is_mid, is_mp3, is_pdf
from recorder_dialog import RecorderDialog, RecorderMidiHandler
from config_dialog import ConfigDialog
from track_manager_dialog import TrackManagerDialog
from device_event_detector import DeviceDetector
from about_dialog import AboutDialog
from loading_animation_dialog import LoadingAnimationDialog
from file_conversion_threads import FileConverter


#-------------------------------------------------------------------------------
# Classes

class SkoreWindow(QtWidgets.QMainWindow):

    """
    This class is the main window of the SKORE application. It handles the
    majority of the higher level functions and is in direct contact to the user.
    """

    def __init__(self):

        """
        This function setups up the entire application, from communication
        to the GUI. Other major setup aspects happen within this function.
        """

        super(QtWidgets.QMainWindow, self).__init__()

        # Main Window Information
        self.setObjectName("MainWindow")
        self.setWindowTitle("SKORE")
        self.resize(1944 * globals.S_W_R, 984 * globals.S_H_R)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setWindowIcon(QtGui.QIcon('.\images\skore_icon.png'))

        # Variable Initialization
        self.midi_in = None
        self.arduino = None

        # Setup functions
        self.setup_ui()
        self.setup_graphics()
        self.setup_comm()
        self.setup_func()

        # File Handling
        self.file_container = FileContainer()
        self.midi_file_path = None

        # Tutor setup
        self.tutor = None
        self.tutor_enable = False

        self.tracks_selected_labels = None

        self.update_globals()

        # Timer Setup
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.clock)
        self.timer.start(globals.CLOCK_DELAY) # 60 FPS, 16ms, 30 FPS, 33ms

    def setup_ui(self):

        """ This function creates the GUI by placing all the necessary widgets."""

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.setObjectName("centralwidget")

        self.grid_layout_widget = QtWidgets.QWidget(self.centralwidget)
        self.grid_layout_widget.setGeometry(QtCore.QRect(-1, 0, globals.S_W_R * 1922, globals.S_H_R * 950))
        self.grid_layout_widget.setObjectName("grid_layout_widget")

        #-----------------------------------------------------------------------
        # grid_layout_central
        self.grid_layout_central = QtWidgets.QGridLayout(self.grid_layout_widget)
        self.grid_layout_central.setContentsMargins(0, 0, 0, 0)
        self.grid_layout_central.setObjectName("grid_layout_central")

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setItemIndexMethod(-1)
        self.graphics_view_game = QtWidgets.QGraphicsView(self.scene, self.grid_layout_widget)
        self.graphics_view_game.setObjectName("graphics_view_game")
        self.grid_layout_central.addWidget(self.graphics_view_game, 1, 0, 1, 1)

        #-----------------------------------------------------------------------
        # grid_layout_central -> horizontal_layout_live_settings

        self.horizontal_layout_live_settings = QtWidgets.QHBoxLayout()
        self.horizontal_layout_live_settings.setObjectName("horizontal_layout_live_settings")

        spacerItem = QtWidgets.QSpacerItem(10 * globals.S_W_R, 40 * globals.S_H_R, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.horizontal_layout_live_settings.addItem(spacerItem)

        self.toolbutton_restart = QtWidgets.QToolButton(self.grid_layout_widget)
        self.toolbutton_restart.setObjectName("toolbutton_restart")
        self.horizontal_layout_live_settings.addWidget(self.toolbutton_restart)

        self.toolbutton_play = QtWidgets.QToolButton(self.grid_layout_widget)
        self.toolbutton_play.setObjectName("toolbutton_play")
        self.horizontal_layout_live_settings.addWidget(self.toolbutton_play)

        #-----------------------------------------------------------------------
        # Divider

        spacerItem2 = QtWidgets.QSpacerItem(2 * globals.S_W_R, 40 * globals.S_H_R, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.horizontal_layout_live_settings.addItem(spacerItem2)

        self.first_line = QtWidgets.QFrame(self.grid_layout_widget)
        self.first_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.first_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.first_line.setObjectName("main_button_line")
        self.horizontal_layout_live_settings.addWidget(self.first_line)

        self.toolbutton_track_manager = QtWidgets.QToolButton(self.grid_layout_widget)
        self.toolbutton_track_manager.setObjectName("toolbutton_track_manager")
        self.horizontal_layout_live_settings.addWidget(self.toolbutton_track_manager)

        self.label_tutoring_mode = QtWidgets.QLabel(self.grid_layout_widget)
        self.label_tutoring_mode.setObjectName("label_tutoring_mode")
        self.horizontal_layout_live_settings.addWidget(self.label_tutoring_mode)

        self.combobox_tutoring_mode = QtWidgets.QComboBox(self.grid_layout_widget)
        self.combobox_tutoring_mode.setObjectName("combobox_tutoring_mode")
        self.horizontal_layout_live_settings.addWidget(self.combobox_tutoring_mode)

        self.label_speed = QtWidgets.QLabel(self.grid_layout_widget)
        self.label_speed.setObjectName("label_speed")
        self.horizontal_layout_live_settings.addWidget(self.label_speed)

        self.spinbox_speed = QtWidgets.QSpinBox(self.grid_layout_widget)
        self.spinbox_speed.setObjectName("spinbox_speed")
        self.horizontal_layout_live_settings.addWidget(self.spinbox_speed)

        self.label_transpose = QtWidgets.QLabel(self.grid_layout_widget)
        self.label_transpose.setObjectName("label_transpose")
        self.horizontal_layout_live_settings.addWidget(self.label_transpose)

        self.spinbox_transpose = QtWidgets.QSpinBox(self.grid_layout_widget)
        self.spinbox_transpose.setObjectName("spinbox_transpose")
        self.horizontal_layout_live_settings.addWidget(self.spinbox_transpose)

        spacerItem3 = QtWidgets.QSpacerItem(2 * globals.S_W_R, 40 * globals.S_H_R, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.horizontal_layout_live_settings.addItem(spacerItem3)

        #-----------------------------------------------------------------------
        # Divider

        self.second_line = QtWidgets.QFrame(self.grid_layout_widget)
        self.second_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.second_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.second_line.setObjectName("secondary_button_line")
        self.horizontal_layout_live_settings.addWidget(self.second_line)

        self.label_current_event = QtWidgets.QLabel(self.grid_layout_widget)
        self.label_current_event.setObjectName('label_current_event')
        self.horizontal_layout_live_settings.addWidget(self.label_current_event)

        self.label_current_event_value = QtWidgets.QLabel(self.grid_layout_widget)
        self.label_current_event_value.setObjectName('label_current_event_value')
        self.horizontal_layout_live_settings.addWidget(self.label_current_event_value)

        spacerItem4 = QtWidgets.QSpacerItem(10 * globals.S_W_R, 40 * globals.S_H_R, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.horizontal_layout_live_settings.addItem(spacerItem4)

        self.label_go_to_event = QtWidgets.QLabel(self.grid_layout_widget)
        self.label_go_to_event.setObjectName('label_go_to_event')
        self.horizontal_layout_live_settings.addWidget(self.label_go_to_event)

        self.spinbox_go_to = QtWidgets.QSpinBox(self.grid_layout_widget)
        self.spinbox_go_to.setObjectName("spinbox_go_to")
        self.horizontal_layout_live_settings.addWidget(self.spinbox_go_to)

        self.toolbutton_skip_event = QtWidgets.QToolButton(self.grid_layout_widget)
        self.toolbutton_skip_event.setObjectName("toolbutton_skip_event")
        self.horizontal_layout_live_settings.addWidget(self.toolbutton_skip_event)

        spacerItem5 = QtWidgets.QSpacerItem(2 * globals.S_W_R, 40 * globals.S_H_R, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.horizontal_layout_live_settings.addItem(spacerItem5)

        self.third_line = QtWidgets.QFrame(self.grid_layout_widget)
        self.third_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.third_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.third_line.setObjectName("secondary_button_line")
        self.horizontal_layout_live_settings.addWidget(self.third_line)

        #-----------------------------------------------------------------------
        # Divider

        self.label_interval_enable = QtWidgets.QLabel(self.grid_layout_widget)
        self.label_interval_enable.setObjectName("label_interval_enable")
        self.horizontal_layout_live_settings.addWidget(self.label_interval_enable)

        self.checkbox_interval = QtWidgets.QCheckBox(self.grid_layout_widget)
        self.checkbox_interval.setObjectName("checkbox_interval")
        self.horizontal_layout_live_settings.addWidget(self.checkbox_interval)

        self.label_interval = QtWidgets.QLabel(self.grid_layout_widget)
        self.label_interval.setObjectName("label_interval")
        self.horizontal_layout_live_settings.addWidget(self.label_interval)

        self.spinbox_initial_location = QtWidgets.QSpinBox(self.grid_layout_widget)
        self.spinbox_initial_location.setObjectName("spinbox_inital_location")
        self.horizontal_layout_live_settings.addWidget(self.spinbox_initial_location)

        """
        self.horizontal_line = QtWidgets.QFrame(self.grid_layout_widget)
        self.horizontal_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.horizontal_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontal_line.setObjectName("horizontal_line")
        self.horizontal_line.setFrameRect(QtCore.QRect(0,0,1,10))
        self.horizontal_layout_live_settings.addWidget(self.horizontal_line)
        """

        self.spinbox_final_location = QtWidgets.QSpinBox(self.grid_layout_widget)
        self.spinbox_final_location.setObjectName("lineedit_inital_location")
        self.horizontal_layout_live_settings.addWidget(self.spinbox_final_location)

        spacerItem_final = QtWidgets.QSpacerItem(10 * globals.S_W_R, 40 * globals.S_H_R, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.horizontal_layout_live_settings.addItem(spacerItem_final)

        self.grid_layout_central.addLayout(self.horizontal_layout_live_settings, 0, 0, 1, 1)

        #-----------------------------------------------------------------------
        # Menubar
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1944 * globals.S_W_R, 26 * globals.S_H_R))
        self.menubar.setObjectName("menubar")
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        self.menu_settings = QtWidgets.QMenu(self.menubar)
        self.menu_settings.setObjectName("menu_settings")
        self.menu_help = QtWidgets.QMenu(self.menubar)
        self.menu_help.setObjectName("menu_help")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)


        self.action_open_file = QtWidgets.QAction(self)
        self.action_open_file.setObjectName("action_open_file")
        self.action_record = QtWidgets.QAction(self)
        self.action_record.setObjectName("action_record")
        self.action_create_midi = QtWidgets.QAction(self)
        self.action_create_midi.setObjectName("action_create_midi")
        self.action_create_pdf = QtWidgets.QAction(self)
        self.action_create_pdf.setObjectName("action_create_pdf")

        self.action_exit = QtWidgets.QAction(self)
        self.action_exit.setObjectName("action_exit")

        self.action_config = QtWidgets.QAction(self)
        self.action_config.setObjectName("action_config")

        self.action_website = QtWidgets.QAction(self)
        self.action_website.setObjectName("action_website")
        self.action_about = QtWidgets.QAction(self)
        self.action_about.setObjectName("action_about")

        #-----------------------------------------------------------------------
        # MenuFile

        self.menu_file.addAction(self.action_open_file)
        self.menu_file.addAction(self.action_record)
        self.menu_file.addSeparator()

        self.menu_file.addAction(self.action_create_midi)
        self.menu_file.addAction(self.action_create_pdf)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_exit)

        self.menu_settings.addAction(self.action_config)

        self.menu_help.addAction(self.action_website)
        self.menu_help.addAction(self.action_about)
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_settings.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())


        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setTabOrder(self.toolbutton_restart, self.toolbutton_play)
        self.setTabOrder(self.toolbutton_play, self.spinbox_transpose)
        self.setTabOrder(self.spinbox_transpose, self.graphics_view_game)
        self.setTabOrder(self.graphics_view_game, self.spinbox_speed)

        return None

    def setup_func(self):

        """
        This function organizes the slots and signals for the widgets placed
        down by the setup_ui function.
        """

        #-----------------------------------------------------------------------
        # MenuBar Actions
        self.action_open_file.setShortcut('Ctrl+O')
        self.action_open_file.triggered.connect(self.upload_file)

        self.action_record.setShortcut("Ctrl+Shift+R")
        self.action_record.triggered.connect(self.skore_recorder)

        self.action_create_midi.setShortcut("Ctrl+M")
        self.action_create_midi.triggered.connect(self.generate_midi_file)

        self.action_create_pdf.setShortcut("Ctrl+P")
        self.action_create_pdf.triggered.connect(self.generate_pdf_file)

        self.action_exit.triggered.connect(self.close)

        self.action_config.triggered.connect(self.open_settings_dialog)

        self.action_website.triggered.connect(self.open_skore_website)

        self.action_about.triggered.connect(self.open_about_dialog)

        #-----------------------------------------------------------------------
        # Live Settings
        self.toolbutton_play.clicked.connect(self.play_stop)
        self.toolbutton_restart.clicked.connect(self.restart)
        self.toolbutton_track_manager.clicked.connect(self.open_track_manager_dialog)

        self.spinbox_speed.setRange(globals.MIN_SPEED, globals.MAX_SPEED)
        self.spinbox_speed.setSingleStep(1)
        self.spinbox_speed.setValue(100)
        self.spinbox_speed.valueChanged.connect(self.speed_change)

        self.spinbox_transpose.setRange(-12, 12)
        self.spinbox_transpose.setSingleStep(1)
        self.spinbox_transpose.setValue(0)
        self.spinbox_transpose.valueChanged.connect(self.transpose_change)

        self.spinbox_go_to.setRange(0, globals.TOTAL_EVENTS)
        self.spinbox_go_to.setSingleStep(1)
        self.spinbox_go_to.setValue(0)
        self.spinbox_go_to.valueChanged.connect(self.go_to_change)

        self.checkbox_interval.stateChanged.connect(self.interval_state_change)
        self.spinbox_initial_location.valueChanged.connect(self.interval_initial_change)
        self.spinbox_final_location.valueChanged.connect(self.interval_final_change)

        self.toolbutton_skip_event.clicked.connect(self.skip_event)
        #-----------------------------------------------------------------------
        # ComboBox Settings

        self.combobox_tutoring_mode.addItem("Beginner")
        self.combobox_tutoring_mode.addItem("Intermediate")
        self.combobox_tutoring_mode.addItem("Expert")

        self.combobox_tutoring_mode.currentIndexChanged.connect(self.mode_change)

        #-----------------------------------------------------------------------
        # Disable Everything

        self.widget_list = [self.toolbutton_play, self.toolbutton_restart, self.toolbutton_track_manager,
                            self.spinbox_speed, self.spinbox_transpose, self.spinbox_go_to,
                            self.checkbox_interval, self.spinbox_initial_location, self.spinbox_final_location,
                            self.toolbutton_skip_event, self.combobox_tutoring_mode]

        self.disable_live_settings()

        return None

    def disable_live_settings(self):

        """ Helper function for disabling live settings widgets. """

        for widget in self.widget_list:
            widget.setEnabled(False)

        return None

    def enable_live_settings(self):

        """ Helper function for enabling live settings widgets. """

        for widget in self.widget_list:
            widget.setEnabled(True)

        return None

    #---------------------------------------------------------------------------
    # Communication Setup

    def setup_comm(self):

        """
        This function establishes the communication between the application,
        arduino, and piano. Additionally, it creates a independent thread to
        detect and reestablish the communication lines with the arduino and piano.
        """

        self.arduino_setup()
        self.piano_port_setup()
        self.comm_status_report()

        # Setting up the device detector
        self.device_detector = DeviceDetector(self)
        self.device_detector.arduino_change_signal.connect(self.arduino_setup_and_report)
        self.device_detector.piano_change_signal.connect(self.piano_setup_and_report)
        self.device_detector.start()

        return False

    def arduino_setup(self):

        """
        This functions sets up the communication between PC and the Arduino.
        """

        cfg = read_config()
        self.arduino_setup_ready = False

        # Closing any previous Arduino Serial Ports
        if self.arduino:
            self.arduino.close()
            self.arduino = []
            time.sleep(globals.ARDUINO_STARTUP_DELAY)

        com_port = cfg['port']['arduino']
        self.arduino_color_palet = cfg['color']

        try:
            self.arduino = serial.Serial(com_port, globals.ARDUINO_BAUD_RATE, writeTimeout = globals.COMM_TIMEOUT)
        except serial.serialutil.SerialException:
            print("ARDUINO AT {0} NOT FOUND".format(com_port))
            self.arduino_status = False
            self.arduino_setup_ready = True
            return None

        transmitted_string = {}

        # Sending the Arduino the colors for the notes settings

        for key, values in cfg['color'].items():
            rgb = cfg['color'][key].split(',')
            rgb = ','.join([str(int(val) // 10) for val in rgb])
            transmitted_string[key] = rgb

        # Color Setup Order: White/Black/Right/Wrong/Upcoming
        setup_transmitted_string = transmitted_string['white'] + ',' + transmitted_string['black']
        setup_transmitted_string = setup_transmitted_string + ',' + transmitted_string['wrong'] + ',' + transmitted_string['upcoming'] + ','

        time.sleep(2)
        self.arduino.write(b'1')
        time.sleep(2)
        print("SENDING SETUP STRING")

        while True:
            try:
                self.arduino.write(setup_transmitted_string.encode('utf-8'))
                break
            except serial.serialutil.SerialException:
                self.arduino.close()
                print("PermissionError for ARDUINO")
                print("Trying again in 1 sec")
                time.sleep(2)
                self.arduino = serial.Serial(com_port, globals.ARDUINO_BAUD_RATE, writeTimeout = globals.COMM_TIMEOUT)
                time.sleep(2)

        # Reporting to the user the Arduino Configurations
        print("""
--------------------------Arduino Configuration-------------------------
COM PORT: {0}
SETUP STRING: {1}

        """.format(com_port, setup_transmitted_string))

        if self.arduino_handshake() is not True:
            print("Arduino Handshake failed")

        self.arduino_status = True
        self.arduino_setup_ready = True

        return None

    def piano_port_setup(self):

        """
        This function sets up the communication between PC and the MIDI device.
        """

        self.piano_setup_ready = False

        # Closing any previous MIDI ports
        if self.midi_in is not []:
            try:
                self.midi_in.close_port()
                time.sleep(2)
            except:
                self.midi_in = None

        #-----------------------------------------------------------------------
        # Establising Midi In

        self.midi_in = rtmidi.MidiIn()
        in_avaliable_ports = self.midi_in.get_ports()
        cfg = read_config()
        selected_port = cfg['port']['piano']

        try:
            self.closes_match_in_port = difflib.get_close_matches(selected_port, in_avaliable_ports)[0]
        except IndexError:
            print("{0} NOT FOUND".format(selected_port))
            self.midi_in = None
            self.piano_status = False
            self.piano_setup_ready = True
            return None


        try:
            self.midi_in.open_port(in_avaliable_ports.index(self.closes_match_in_port))
        except:
            print("Piano Port Setup Failure")
            self.midi_in = None
            self.piano_status = False
            self.piano_setup_ready = True
            return None

        self.tutor_midi_handler = TutorMidiHandler(self)
        self.midi_in.set_callback(self.tutor_midi_handler)

        print("PIANO MIDI IN SUCCESSFUL")
        #-----------------------------------------------------------------------
        # Establishing Midi Out

        self.midi_out = rtmidi.MidiOut()
        out_avaliable_ports = self.midi_out.get_ports()
        try:
            self.closes_match_out_port = difflib.get_close_matches(selected_port, out_avaliable_ports)[0]
        except IndexError:
            print("OUTPUT PORT TO {0} NOT FOUND".format(selected_port))
            self.midi_in = None
            self.midi_out = None
            self.piano_status = False
            self.piano_setup_ready = True
            return None

        try:
            self.midi_out.open_port(out_avaliable_ports.index(self.closes_match_out_port))
        except:
            print("Piano MIDI OUT Port Setup Failure")
            self.midi_out = None
            self.piano_status = False
            self.piano_setup_ready = True
            return None

        # Recording the necessary keyboard shift to match the right piano size.
        if cfg['port']['piano_size'] == '76':
            globals.KEYBOARD_SHIFT = 27 - 1
        elif cfg['port']['piano_size'] == '88':
            globals.KEYBOARD_SHIFT = 20 - 1

        # Reporting to the user the piano configuration
        print("""
----------------------------Piano Configuration-------------------------
MIDI IN & OUT
PIANO PORT: {0} (SUCCESSFUL)
PIANO PORT HANDLER SETUP (SUCCESSFUL)
KEYBOARD_SHIFT: {1}

        """.format(self.closes_match_in_port, globals.KEYBOARD_SHIFT))

        self.piano_status = True
        self.piano_setup_ready = True
        return None

    def comm_status_report(self):

        """
        This function utlizes the graphics_system_message to inform the user
        the status of the both arduino and piano communication lines.
        """

        if self.arduino_status is False and self.piano_status is False:
            self.graphics_system_message.set_text("Piano and Arduino Comm Failed")

        elif self.arduino_status is False:
            self.graphics_system_message.set_text("Arduino Comm Failed")
            print("ARDUINO COMMUNICATION SETUP FAILURE")

        elif self.piano_status is False:
            self.graphics_system_message.set_text("Piano Comm Failed")
            print("PIANO COMMUNICATION SETUP FAILURE")

        else:
            self.graphics_system_message.set_text("")
            print("ARDUINO AND PIANO COMMUNICATION SETUP SUCCESS")

        return None

    @QtCore.pyqtSlot('QString')
    def arduino_setup_and_report(self, state):

        """
        This function is purposely only for the DeviceDetector to use. This allows
        the DeviceDetector to reestablish the arduino communication and to inform
        the user about its new connection.
        """

        if (state == 'ON' and self.arduino_status is False) or (state == 'OFF' and self.arduino_status is True):

            while self.piano_setup_ready is False:
                time.sleep(1)

            print("ARDUINO COMMUNICATION RECONNECTION ATTEMPT")

            self.arduino_setup()
            self.comm_status_report()

            if self.tutor_enable is True:
                self. arduino_comm(globals.KEYBOARD_STATE['TARGET'], 'timing')

        return None

    @QtCore.pyqtSlot('QString')
    def piano_setup_and_report(self, state):

        """
        This function is purposely only for the DeviceDetector to use. This allows
        the DeviceDetector to reestablish the piano communication and to inform
        the user about its new connection.
        """

        if (state == 'ON' and self.piano_status is False) or (state == 'OFF' and self.piano_status is True):

            while self.piano_setup_ready is False:
                time.sleep(1)

            print("PIANO COMMUNICATION RECONNECTION ATTEMPT")

            self.piano_port_setup()
            self.comm_status_report()

        return None

    #---------------------------------------------------------------------------
    # Communication Transmittion

    def white_keys_string(self, notes):

        """ Determines which inputted notes are white notes. """

        white_keys_string_value = ','.join(str(note - globals.KEYBOARD_SHIFT) for note in notes if note in globals.NOTE_PITCH_WHITE_KEYS)

        return white_keys_string_value

    def black_keys_string(self, notes):

        """ Determines which inputted notes are black notes. """

        black_keys_string_value = ','.join(str(note - globals.KEYBOARD_SHIFT) for note in notes if note in globals.NOTE_PITCH_BLACK_KEYS)

        return black_keys_string_value

    def black_white_send_string(self, notes):

        """
        Obtaining the send_string while consider which notes are white and
        black.
        """

        notes_to_send = notes

        black_keys_string_value = self.black_keys_string(notes_to_send)
        white_keys_string_value = self.white_keys_string(notes_to_send)

        send_string = '<'
        if black_keys_string_value != '':
            send_string += 'b,' + black_keys_string_value + ','
        if white_keys_string_value != '':
            send_string += 'w,' + white_keys_string_value
        send_string += ',>'

        return send_string

    def arduino_write_and_handshake(self, send_string):

        """ Sending to the arduino the send string and waiting for the handshake. """

        print("STRING SENT:", send_string)
        self.arduino.write(send_string.encode('utf-8'))

        if self.arduino_handshake() is not True:
            raise RuntimeError("Communication Desync with Arduino")
            #print("Continue eventhough Arduino Handshake Failed")

        return None

    def arduino_handshake(self):

        """
        This function performs the Arduino Handshake. The handshake is complete
        when the Arduino send the '+' character.
        """

        count = 0

        while True:
            time.sleep(globals.HANDSHAKE_DELAY)
            read_data = self.arduino.read()

            if read_data == b'+':
                #print("HANDSHAKE COMPLETED")
                return True

            if count > globals.COUNT_TIMEOUT:
                break
            else:
                count += 1

            print("$", end = "")

        print("HANDSHAKE FAILED!")

        return False

    def arduino_comm(self, notes, operation = None):

        """
        This function performs common operations [clean, incorrect, upcoming,
        and white/black] to send to the arduino.
        """

        #print("Arduino Comm - Notes: {0}\tOperation: {1}".format(notes, operation))

        if self.arduino_status is False:
            return None

        while globals.HANDLER_ENABLE is False:
            print("$", end = "")
            time.sleep(globals.TUTOR_THREAD_DELAY)

        globals.HANDLER_ENABLE = False

        #-----------------------------------------------------------------------
        # Clear All

        if notes == []:
            globals.HANDLER_ENABLE = True
            return None

        if notes == '!':
            send_string = '<!,>'

            self.arduino_write_and_handshake(send_string)
            print("! complete handshake")
            globals.KEYBOARD_STATE['ARDUINO']['TARGET'] = []
            globals.KEYBOARD_STATE['ARDUINO']['RW'] = []
            globals.HANDLER_ENABLE = True

            return None

        #-----------------------------------------------------------------------
        # Play/Stop SKORE logo indicator
        if operation == 'play':
            send_string = '<p,>'
            self.arduino_write_and_handshake(send_string)
            globals.HANDLER_ENABLE = True
            return None

        elif operation == 'stop':
            send_string = '<s,>'
            self.arduino_write_and_handshake(send_string)
            globals.HANDLER_ENABLE = True
            return None

        #-----------------------------------------------------------------------
        # Wrong Notes

        if operation[0] == 'i': # Incorrect

            if operation.endswith('on'): # on
                if notes not in globals.KEYBOARD_STATE['ARDUINO']['RW'] and notes not in globals.KEYBOARD_STATE['TARGET']:
                    send_string = '<i' + ',' + str(notes - globals.KEYBOARD_SHIFT) + ',>'
                    self.arduino_write_and_handshake(send_string)
                    globals.KEYBOARD_STATE['ARDUINO']['RW'].append(notes)
            else: # off

                if notes in globals.KEYBOARD_STATE['TARGET'] and notes in globals.KEYBOARD_STATE['ARDUINO']['RW']:
                    try:
                        globals.KEYBOARD_STATE['ARDUINO']['RW'].remove(notes)
                    except ValueError:
                        print("Trying to remove a wrong note that does not exist")

                elif notes in globals.KEYBOARD_STATE['ARDUINO']['RW']:
                    send_string = '<f,' + str(notes - globals.KEYBOARD_SHIFT) + ',>'
                    self.arduino_write_and_handshake(send_string)
                    try:
                        globals.KEYBOARD_STATE['ARDUINO']['RW'].remove(notes)
                    except ValueError: # Tripy buisness
                        print("Trying to remove a wrong note that does not exist")

            globals.HANDLER_ENABLE = True
            return None

        #-----------------------------------------------------------------------
        # Upcoming and Timing Notes

        if self.tutor.options['timing notification'] is False:
            if operation != 'correct' and operation != 'incorrect':
                send_string = self.black_white_send_string(notes)

        else:
            if operation == 'timing':
                send_string = self.black_white_send_string(notes)
                globals.KEYBOARD_STATE['ARDUINO']['TARGET'] = notes
            elif operation == 'upcoming':
                send_string = '<u,' + ','.join(str(note - globals.KEYBOARD_SHIFT) for note in notes) + ',>'
                globals.KEYBOARD_STATE['ARDUINO']['TARGET'] = notes
            elif operation == 'off':
                send_string = '<f,' + ','.join(str(note - globals.KEYBOARD_SHIFT) for note in notes) + ',>'
                globals.KEYBOARD_STATE['ARDUINO']['TARGET'] = [note for note in globals.KEYBOARD_STATE['ARDUINO']['TARGET'] if note not in notes]

        self.arduino_write_and_handshake(send_string)
        globals.HANDLER_ENABLE = True

        return None

    #---------------------------------------------------------------------------
    # Graphics Functions

    def clock(self):

        """ This function updates the GUI graphical elements. """

        """
        if self.tutor_enable is True:
            self.set_tick_per_frame()
            self.speed_change()
        """

        self.scene.update()

        return None

    def setup_graphics(self):

        """ This function setups all the static graphical elements in the GUI. """

        self.graphics_view_game.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.black))

        #-----------------------------------------------------------------------
        # Setting up the Staff
        green_pen = QtGui.QPen(QtCore.Qt.green)
        w = 1500
        x = round(w/2) * -1
        y = 200
        group = []

        for i in range(5):
            #group.append(self.scene.addLine(x, y, x+w, y, green_pen))
            group.append(self.scene.addLine(x * globals.S_W_R, y * globals.S_W_R, (x+w) * globals.S_W_R, y * globals.S_W_R, green_pen))
            y -= 20

        y = -200

        for i in range(5):
            #group.append(self.scene.addLine(x, y, x+w, y, green_pen))
            group.append(self.scene.addLine(x * globals.S_W_R, y * globals.S_W_R, (x+w) * globals.S_W_R, y * globals.S_W_R, green_pen))
            y -= 20

        #-----------------------------------------------------------------------
        # Setting up Visible note box
        w = 1210
        x = round(w/2) * -1 + round(w/20) + 80
        h = 810
        y = round(h/2) * -1 - round(h/10) + 15

        red_pen = QtGui.QPen(QtCore.Qt.red)
        red_brush = QtGui.QBrush(QtCore.Qt.red)

        globals.VISIBLE_NOTE_BOX = self.scene.addRect(x * globals.S_W_R, y * globals.S_W_R, w * globals.S_W_R, h * globals.S_W_R, red_pen, red_brush)
        globals.VISIBLE_NOTE_BOX.setOpacity(globals.HIDDEN)

        #-----------------------------------------------------------------------
        # Setting up timing note bar
        w = 50 # tolerances of 25 on each side
        x = globals.LEFT_TICK_SHIFT - round(w/2)
        h = 810
        y = -470

        magenta_brush = QtGui.QBrush(QtGui.QColor(153, 0, 153))
        magenta_pen = QtGui.QPen(QtGui.QColor(153, 0, 153))

        globals.TIMING_NOTE_BOX = self.scene.addRect(x * globals.S_W_R, y * globals.S_W_R, w * globals.S_W_R, h * globals.S_W_R, magenta_pen, magenta_brush)
        globals.TIMING_NOTE_BOX.setOpacity(0.5)

        globals.TIMING_NOTE_LINE = self.scene.addLine(globals.LEFT_TICK_SHIFT * globals.S_W_R, y * globals.S_W_R, globals.LEFT_TICK_SHIFT * globals.S_W_R, (h + y) * globals.S_W_R, magenta_pen)

        #-----------------------------------------------------------------------
        # Setting up timing note line catch
        w = 25
        x = globals.LEFT_TICK_SHIFT - round(w/2) - round(25/2) - 1
        h = 810
        y = -470

        white_brush = QtGui.QBrush(QtCore.Qt.white)
        white_pen = QtGui.QPen(QtCore.Qt.white)

        globals.LATE_NOTE_BOX = self.scene.addRect(x * globals.S_W_R, y * globals.S_W_R, w * globals.S_W_R, h * globals.S_W_R, white_pen, white_brush)
        globals.LATE_NOTE_BOX.setOpacity(globals.HIDDEN)

        #-----------------------------------------------------------------------
        # Placing Treble and Bass Clef
        treble_clef = QtGui.QPixmap(r".\images\graphics_assets\green_treble_clef.png")
        treble_clef = treble_clef.scaledToHeight(180 * globals.S_W_R)

        treble_clef_pointer = self.scene.addPixmap(treble_clef)
        treble_clef_pointer.setOffset(-750 * globals.S_W_R, -331 * globals.S_W_R)

        bass_clef = QtGui.QPixmap(r".\images\graphics_assets\green_bass_clef.png")
        bass_clef = bass_clef.scaledToHeight(70 * globals.S_W_R)

        bass_clef_pointer = self.scene.addPixmap(bass_clef)
        bass_clef_pointer.setOffset(-720 * globals.S_W_R, 120 * globals.S_W_R)

        #-----------------------------------------------------------------------
        # Placing Note Labels
        self.note_labels = {'NEUTRAL':{},'RIGHT':{},'WRONG':{}}

        for note in globals.NOTE_NAME_TO_Y_LOCATION.keys():

            self.note_labels['NEUTRAL'][note] = GraphicsPlayedLabel(note, None)
            self.note_labels['NEUTRAL'][note].setOpacity(globals.HIDDEN)
            self.scene.addItem(self.note_labels['NEUTRAL'][note])

            self.note_labels['RIGHT'][note] = GraphicsPlayedLabel(note, True)
            self.note_labels['RIGHT'][note].setOpacity(globals.HIDDEN)
            self.scene.addItem(self.note_labels['RIGHT'][note])

            self.note_labels['WRONG'][note] = GraphicsPlayedLabel(note, False)
            self.note_labels['WRONG'][note].setOpacity(globals.HIDDEN)
            self.scene.addItem(self.note_labels['WRONG'][note])

        #-----------------------------------------------------------------------
        # Placing Note Label Names
        self.note_name_labels = {}

        for note in globals.NOTE_NAME_TO_Y_LOCATION.keys():

            self.note_name_labels[note] = GraphicsPlayedNameLabel(note)
            self.note_name_labels[note].setOpacity(globals.HIDDEN)
            self.scene.addItem(self.note_name_labels[note])

        #-----------------------------------------------------------------------
        # Setup Graphics Controller

        globals.GRAPHICS_CONTROLLER = GraphicsController()
        globals.GRAPHICS_CONTROLLER.stop_signal.connect(self.stop_all_notes)

        #-----------------------------------------------------------------------
        # Setup Graphics System Messages

        self.graphics_system_message = GraphicsSystemMessage()
        self.scene.addItem(self.graphics_system_message)

        # Graphics
        self.drawn_notes_group = []

        #-----------------------------------------------------------------------

        # Note
        globals.PIXMAPS['GREEN'].append(QtGui.QPixmap(r".\images\graphics_assets\green_music_note_head.png").scaled(19 * globals.S_W_R, 19 * globals.S_W_R))
        globals.PIXMAPS['YELLOW'].append(QtGui.QPixmap(r".\images\graphics_assets\yellow_music_note_head.png").scaled(19 * globals.S_W_R, 19 * globals.S_W_R))
        globals.PIXMAPS['CYAN'].append(QtGui.QPixmap(r".\images\graphics_assets\cyan_music_note_head.png").scaled(19 * globals.S_W_R, 19 * globals.S_W_R))

        # Sharp
        globals.PIXMAPS['GREEN'].append(QtGui.QPixmap(r".\images\graphics_assets\green_sharp.png").scaled(20 * globals.S_W_R, 45 * globals.S_W_R))
        globals.PIXMAPS['YELLOW'].append(QtGui.QPixmap(r".\images\graphics_assets\yellow_sharp.png").scaled(20 * globals.S_W_R, 45 * globals.S_W_R))
        globals.PIXMAPS['CYAN'].append(QtGui.QPixmap(r".\images\graphics_assets\cyan_sharp.png").scaled(20 * globals.S_W_R, 45 * globals.S_W_R))

        # Flat
        globals.PIXMAPS['GREEN'].append(QtGui.QPixmap(r".\images\graphics_assets\green_flat.png").scaled(13 * globals.S_W_R, 35 * globals.S_W_R))
        globals.PIXMAPS['YELLOW'].append(QtGui.QPixmap(r".\images\graphics_assets\yellow_flat.png").scaled(13 * globals.S_W_R, 35 * globals.S_W_R))
        globals.PIXMAPS['CYAN'].append(QtGui.QPixmap(r".\images\graphics_assets\cyan_flat.png").scaled(13 * globals.S_W_R, 35 * globals.S_W_R))

        # Natural
        globals.PIXMAPS['GREEN'].append(QtGui.QPixmap(r".\images\graphics_assets\green_natural.png").scaled(40 * globals.S_W_R, 48 * globals.S_W_R))
        globals.PIXMAPS['YELLOW'].append(QtGui.QPixmap(r".\images\graphics_assets\yellow_natural.png").scaled(40 * globals.S_W_R, 48 * globals.S_W_R))
        globals.PIXMAPS['CYAN'].append(QtGui.QPixmap(r".\images\graphics_assets\cyan_natural.png").scaled(40 * globals.S_W_R, 48 * globals.S_W_R))

        return None

    def draw_filtered_sequence(self):

        """ This function draws all the notes in the filtered sequence. """

        tick_count = globals.LEFT_TICK_SHIFT

        for event in self.filtered_sequence:

            if event[0] == "META":
                self.drawn_notes_group.append(["META"])
                continue

            note_array = event[0]
            tick = event[1]
            tick_count += tick
            temp_list = []

            if note_array == []:
                continue

            top_note = max(note_array)
            for note in note_array:
                drawn_note = GraphicsNote(note, tick_count, self)
                self.scene.addItem(drawn_note)
                temp_list.append(drawn_note)

                if note == top_note:
                    drawn_note.top_note = True

            self.drawn_notes_group.append(temp_list)

        return True

    def stop_all_notes(self):

        """ This function stops all the drawn notes of the filtered sequence. """

        #print("Called stop_all_notes")

        if globals.NOTES_MOVING is True:
            #print("stop all notes")

            for event in self.drawn_notes_group:

                if event == ["META"]:
                    continue

                for note in event:
                    note.stop()

        globals.NOTES_MOVING = False

        return None

    def move_all_notes(self):

        """
        This function sets the speed of all the drawn notes in the filtered
        sequence.
        """

        print("move all notes called")
        print("Tick per Frame used: ", self.tick_per_frame)

        if globals.NOTES_MOVING is False:
            #print("move all notes")

            for event in self.drawn_notes_group:

                if event == ["META"]:
                    continue

                for note in event:
                    note.set_speed(self.tick_per_frame)

        globals.NOTES_MOVING = True

        return None

    def clean_note_labels(self):

        """
        This function removes any drawn note labels. This is typically an
        when a midi file is uploaded. If the user is pressing a note when the
        tutor is being set, a neutral note label remains permenantly. This
        functions removes any possible note label after the tutor has been set.
        """

        #print("Clean Note Labels")

        for state in self.note_labels.keys():
            for note_name in self.note_labels[state].keys():
                self.note_labels[state][note_name].setOpacity(globals.HIDDEN)

        for note_name in self.note_name_labels.keys():
            self.note_name_labels[note_name].setOpacity(globals.HIDDEN)

        return None

    #---------------------------------------------------------------------------
    # GUI Tutoring Functions

    def play_stop(self):

        """ This stops/continues any tutoring activity. """

        if self.tutor_enable is True:
            if globals.LIVE_SETTINGS['play'] is True:
                globals.LIVE_SETTINGS['play'] = False
                self.toolbutton_play.setText("Play")
                self.stop_all_notes()
                self.arduino_comm([1], 'stop')

            else:
                globals.LIVE_SETTINGS['play'] = True
                self.toolbutton_play.setText("Stop")
                self.move_all_notes()
                self.arduino_comm([1], 'play')
        else:
            print("Tutor not enabled")

        return None

    def restart(self):

        """ This restarts the song. """

        if self.tutor_enable is True:

            self.clean_tutor()
            self.set_tutor()

            if globals.LIVE_SETTINGS['play'] is True:
                globals.LIVE_SETTINGS['play'] = False
                self.toolbutton_play.setText("Play")
                self.stop_all_notes()
                self.arduino_comm([1], 'stop')

        else:
            print("Tutor not enabled")

        return None

    def mode_change(self):

        """
        This function performs all the necessary steps to change the tutoring
        mode of the application.
        """

        print("tutoring mode changed")
        globals.LIVE_SETTINGS['mode'] = self.combobox_tutoring_mode.currentText()

        if self.tutor_enable is True:

            complete_flag = False
            i = 1

            try:
                while True:

                    if self.tutor.sequence_pointer - i < 0:
                        break

                    for late_note in self.drawn_notes_group[self.tutor.sequence_pointer - i]:
                        if late_note == 'META':
                            i += 1
                            continue

                        late_note.played = True
                        complete_flag = True

                    if complete_flag is True:
                        #print('2')
                        break

            except AttributeError:
                print("AttributeError")

        print("Completed mode changed")

        return None

    def speed_change(self):

        """ This function changes the speed of the application. """

        if self.tutor_enable is True:
            globals.LIVE_SETTINGS['speed'] = self.spinbox_speed.value()
            print("Speed Changed")

            self.set_tick_per_frame()

            if globals.NOTES_MOVING is True:

                for event in self.drawn_notes_group:

                    if event == ["META"]:
                        continue

                    for note in event:
                        note.set_speed(self.tick_per_frame)

        return None

    def transpose_change(self):

        """
        This function performs all the necessary steps to transpose the drawn
        notes in the filtered sequence.
        """

        if self.tutor_enable is True:
            globals.LIVE_SETTINGS['transpose'] = self.spinbox_transpose.value()

            transpose_diff = globals.LIVE_SETTINGS['transpose'] - self.transpose_tracker
            self.transpose_tracker = globals.LIVE_SETTINGS['transpose']

            # Change all notes in Graphics
            for event in self.drawn_notes_group:
                if event == ['META']:
                    continue
                for note in event:
                    note.set_note_pitch(note.note_pitch + transpose_diff)

            # Change the filtered_sequence
            for i in range(len(self.filtered_sequence)):
                note_array = self.filtered_sequence[i][0]
                if note_array == 'META':
                    continue
                new_note_array = []
                for note in note_array:
                    new_note_array.append(note + transpose_diff)
                self.filtered_sequence[i][0] = new_note_array


            print("Post-transpose filtered_sequence")
            print(self.filtered_sequence)

            # Change the keyboard_state
            globals.KEYBOARD_STATE['TARGET'] = [note + transpose_diff for note in globals.KEYBOARD_STATE['TARGET']]
            globals.KEYBOARD_STATE['RIGHT'].clear()
            globals.KEYBOARD_STATE['WRONG'].clear()

            print("transpose_change !")
            self.arduino_comm('!')
            self.arduino_comm(globals.KEYBOARD_STATE['TARGET'], 'timing')

        else:
            print("Tutor disabled, transpose change discarted")

        return None

    def go_to_change(self):

        """
        This function performs all the necessary steps to shift the drawn notes
        in the filtered sequence to the points selected by the user.
        """

        if self.tutor_enable is True:

            if self.filtered_sequence == []:
                print("EMPTY FILTERED SEQUENCE ERROR")
                return None

            print("#######################GO TO#################################")
            go_to_value = self.spinbox_go_to.value()
            print("go to change: ", go_to_value)

            while self.filtered_sequence[go_to_value][0] == 'META' and go_to_value >= 0:

                if go_to_value == self.tutor.sequence_pointer:
                    print("No change needed")
                    return None

                go_to_value -= 1

            if self.filtered_sequence[go_to_value][0] == 'META':
                print("No previous note event")
                return None

            self.shift_song(go_to_value)

        return None

    def skip_event(self):

        """ This function performs the necessary steps to skip one event. """

        if self.tutor_enable is True:

            if self.filtered_sequence == []:
                print("EMPTY FILTERED SEQUENCE ERROR")
                return None

            print("#########################SKIP EVENT##########################")

            go_to_value = self.tutor.sequence_pointer + 1

            while self.filtered_sequence[go_to_value][0] == 'META' and go_to_value < len(self.filtered_sequence):

                go_to_value += 1

            if go_to_value == len(self.filtered_sequence):
                print("Skipping to End of Song")
                return None

            self.shift_song(go_to_value)

        return None

    def interval_state_change(self):

        """
        This function disables/enables the interval looping feature. Additionally,
        it sets the spinbox values to the global variables for record keeping.
        """

        new_state = self.checkbox_interval.checkState()

        if new_state == 0:
            print("Interval Looping Disabled")
            globals.LIVE_SETTINGS['interval_loop'] = False
        else:
            print("Interval Looping Enabled")
            globals.LIVE_SETTINGS['interval_loop'] = True

        current_value = self.spinbox_initial_location.value()
        globals.LIVE_SETTINGS['interval_initial'] = current_value

        current_value = self.spinbox_final_location.value()
        globals.LIVE_SETTINGS['interval_final'] = current_value

        return None

    def interval_initial_change(self):

        """
        This function accounts for all the necessary changes when the initial
        location value changes.
        """

        print("Initial Change")

        new_value = self.spinbox_initial_location.value()
        print("Previous Value: {0}\tNew Value: {1}".format(globals.LIVE_SETTINGS['interval_initial'], new_value))
        globals.LIVE_SETTINGS['interval_initial'] = new_value

        self.spinbox_final_location.setMinimum(new_value + 1)

        return None

    def interval_final_change(self):

        """
        This function accounts for all the necessary changes when the final location
        value changes.
        """

        print("Final Change")

        new_value = self.spinbox_final_location.value()
        print("Previous Value: {0}\tNew Value: {1}".format(globals.LIVE_SETTINGS['interval_final'], new_value))
        globals.LIVE_SETTINGS['interval_final'] = new_value

        self.spinbox_initial_location.setMaximum(new_value - 1)

        return None

    #---------------------------------------------------------------------------
    # Tutoring Manipulation Functions

    def setup_tutor(self):

        """
        This function setups up the tutor. This requires the midi file to be
        processed and for any previous tutor thread to be terminated. Then the new
        tutor is set in place.
        """

        self.midi_file_path = self.file_container.file_path['.mid']
        self.midi_setup()

        if self.tutor_enable is True:
            self.clean_tutor()

        # Normal tutor setup procedure
        self.set_tutor()

        return None

    def clean_tutor(self):

        """
        This function terminates the tutor thread and cleans the application
        to be ready for a new tutor thread.
        """

        self.tutor.terminate()
        globals.LIVE_SETTINGS['play'] = False
        self.toolbutton_play.setText("Play")

        for event in self.drawn_notes_group:
            if event == ['META']:
                continue
            for note in event:
                self.scene.removeItem(note)
                del note

        return None

    def set_tutor(self):

        """
        This function removes any neutral note labels, cleans the LED bar, stops
        all the notes in the graphics, draws the filtered sequence, and beginnings
        the tutor thread.
        """

        self.clean_note_labels()
        globals.KEYBOARD_STATE['ARDUINO']['RW'] = []

        print("set_tutor !")
        self.arduino_comm('!')

        globals.NOTES_MOVING = False
        self.arduino_comm([1], 'stop')

        self.drawn_notes_group.clear()
        self.draw_filtered_sequence()

        self.enable_live_settings()
        #PUT CODE HERE

        self.tutor = Tutor(self)
        self.tutor.start()
        self.tutor.finished.connect(self.end_of_song)

        return None

    def end_of_song(self):

        """
        This functions stops the graphics, informs the user of song completion,
        sets the UI for a upcoming restart or upload of a new file.
        """

        print("End of Song")

        globals.KEYBOARD_STATE['TARGET'] = []
        self.stop_all_notes()
        self.arduino_comm('!')
        self.arduino_comm([1],'stop')

        globals.LIVE_SETTINGS['play'] = False
        self.toolbutton_play.setText("Play")

        self.spinbox_go_to.setEnabled(False)
        self.toolbutton_skip_event.setEnabled(False)

        return None

    def shift_song(self, go_to_value):

        """
        This function, given the desired index of the filtered sequence, will
        shift all the drawn notes of the filtered sequence and account for the
        tempo changes along the way to the indicated index.
        """

        print("&&&&&&&&&&&&&&&&&&&&&&&&&SHIFT SONG&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

        while self.drawn_notes_group[go_to_value][0] == 'META' and go_to_value > 0:
            go_to_value = go_to_value - 1

        while self.drawn_notes_group[go_to_value][0] == 'META' and go_to_value < globals.TOTAL_EVENTS:
            go_to_value = go_to_value + 1

        print("Go To Value (after accounting for META and bounds): ", go_to_value)

        shift = self.drawn_notes_group[go_to_value][0].x - globals.LEFT_TICK_SHIFT * globals.S_W_R

        if shift != 0:
            print("Shift Needed")
            self.tutor.sequence_pointer = go_to_value

            for i in range(len(self.drawn_notes_group)):

                if self.drawn_notes_group[i][0] == 'META':
                    if self.filtered_sequence[i][1] == 'set_tempo':
                        new_tempo = self.filtered_sequence[i][2].tempo
                        print("tempo change: Previous: {0} - Now: {1}".format(self.tempo, new_tempo))
                        self.tempo = new_tempo

                    continue

                for note in self.drawn_notes_group[i]:
                    note.x -= shift

                    if note.x >= globals.LEFT_TICK_SHIFT * globals.S_W_R:
                        note.played = False

            globals.KEYBOARD_STATE['TARGET'] = self.filtered_sequence[self.tutor.sequence_pointer][0]
            print("! go to")
            self.arduino_comm('!')
            self.arduino_comm(globals.KEYBOARD_STATE['TARGET'], 'timing')
            self.speed_change()

            self.label_current_event_value.setText("{0}/{1}".format(self.tutor.sequence_pointer, globals.TOTAL_EVENTS))

        else:
            print("Shift not needed")

        return None

    #---------------------------------------------------------------------------
    # File Input

    def upload_file(self):

        """
        This function allows the user to upload a file. Then perform an action
        according to the uploaded file.
        """

        upload_file_path = self.open_filename_dialog_user_input("Select Audio File", "All Supported Files (*.mid *.mp3 *.pdf);;All Files (*.*);;MIDI Files(*.mid);;MP3 Files(*.mp3);;PDF Files (*.pdf)")

        if upload_file_path:

            print("UPLOAD FILE LOCATION: {0}".format(upload_file_path))

            self.file_container.remove_all()
            self.file_container.original_file = upload_file_path
            self.file_container.add_file_type(upload_file_path)

            if is_mid(upload_file_path):

                self.spinbox_speed.setValue(100)
                self.spinbox_transpose.setValue(0)
                self.spinbox_go_to.setValue(0)
                self.transpose_tracker = 0
                self.combobox_tutoring_mode.setCurrentText("Beginner")

                self.midi_file_path = upload_file_path
                self.setup_tutor()

            else:

                self.midi_file_path = None

        return None

    def open_filename_dialog_user_input(self, title, supported_files):

        """
        This file dialog is used to obtain the file location of the .mid, .mp3,
        and .pdf file.
        """

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, title, "", supported_files, options=options)

        if filename:
            file_dialog_output = str(filename)
        else:
            return ""

        file_dialog_output = file_dialog_output.replace('/' , '\\' )
        return file_dialog_output

    def open_directory_dialog_user_input(self):

        """
        This file dialog is used to obtain the folder directory of the desired
        save location for the generated files.
        """

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ShowDirsOnly
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, caption = 'Open a folder', options = options)

        if directory:
            file_dialog_output = str(directory)
        else:
            return ""

        file_dialog_output = file_dialog_output.replace('/' , '\\' )
        return file_dialog_output

    def save_filename_dialog_user_input(self, title, supported_files):

        """
        This file is used to obtain the file location of the save file, typically
        .mid and .pdf files.
        """

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, title, "", supported_files, options = options)

        if filename:
            file_dialog_output = str(filename)
        else:
            return ""

        file_dialog_output = file_dialog_output.replace('/','\\')

        if file_dialog_output.endswith('.mid') is False and supported_files.find('.mid') != -1:
            file_dialog_output += '.mid'
        if file_dialog_output.endswith('.pdf') is False and supported_files.find('.pdf') != -1:
            file_dialog_output += '.pdf'

        return file_dialog_output

    def save_generated_files(self):

        """
        This functions saves all the files generated by the user. Effectively
        it relocates all the files found temp to the user's choice of directory.
        """

        if len(self.file_container.file_path) >= 2:
            filename = os.path.splitext(os.path.basename(self.file_container.original_file))[0]
            user_given_filename, okPressed = QtWidgets.QInputDialog.getText(self, "Save Files","Files Group Name:", QtWidgets.QLineEdit.Normal, filename)

            if okPressed:
                save_folder_path = self.open_directory_dialog_user_input()
                print("SAVE FOLDER LOCATION: {0}".format(save_folder_path))

                if user_given_filename == '' or save_folder_path == '':
                    QtWidgets.QMessageBox.about(self, "Invalid Information",  "Please enter a valid filename or/and save folder path")
                    return None

                # Obtaining mid file location
                self.file_container.temp_to_folder(save_folder_path, user_given_filename)

        else:
            QtWidgets.QMessageBox.about(self, "No Conversion Present", "Please upload and convert a file before saving it.")

        return None

    #---------------------------------------------------------------------------
    # File Conversion

    def exe_validity_check(self, output_file_type):

        print("Checking Validity")

        cfg = read_config()

        if output_file_type == '.mid':

            if self.file_container.has_mp3_file():
                if cfg['app_path']['open_close_source'] == 'open_source': # AmazingMidi
                    exe_file = pathlib.Path(cfg['app_path']['amazing_midi'])
                    return exe_file.is_file()

                else: # AnthemScore
                    exe_file = pathlib.Path(cfg['app_path']['anthemscore'])
                    return exe_file.is_file()
            else:
                exe_file = pathlib.Path(cfg['app_path']['audiveris'])
                if exe_file.is_file() is False:
                    return False

                exe_file = pathlib.Path(cfg['app_path']['muse_score'])
                return exe_file.is_file()

        elif output_file_type == '.pdf':
            exe_file = pathlib.Path(cfg['app_path']['muse_score'])
            return exe_file.is_file()

        return None

    def append_gradle_to_path(self):

        """
        This function appends the path of gradle to the current path.
        This function might not be necessary, keep just in case needed in the
        future.
        """

        cfg = read_config()

        path = os.environ["PATH"]
        gradle_path = cfg['app_path']['gradle']
        gradle_base_dir = r"C:\Gradle"

        gradle_path_object = pathlib.Path(gradle_path)
        gradle_base_dir_object = pathlib.Path(gradle_base_dir)

        if gradle_path in path:
            print("GRADLE ALREADY IN PATH")
            return True

        elif gradle_path_object.is_dir():
            print("GRADLE IMPORT (using gradle_path)")
            os.environ["PATH"] += os.pathsep + gradle_path
            return True

        elif gradle_base_dir_object.is_dir():
            dirs = [f for f in os.listdir(gradle_base_dir) if os.path.isdir(os.path.join(gradle_base_dir, f))]

            for dir in dirs:
                if dir.find('gradle') != -1:
                    print("Found gradle directory")
                    gradle_path = gradle_base_dir + '\\' + dir + '\\bin'

                    print("GRADLE IMPORT (General Gradle Dir)")
                    os.environ["PATH"] += os.pathsep + gradle_path
                    return True

            print(r"GRADLE IMPORT FAILED (bin folder not found in C:\Gradle)")
            return False

        else:
            print(r"GRADLE IMPORT FAILED (C:\Gradle not found)")

        return False

    def get_output_information(self, title, supported_files):

        """
        This function obtains the output file path and determines the directory
        and filename for later use in the file conversion processes.
        """

        globals.OUTPUT_FILE_PATH = self.save_filename_dialog_user_input(title, supported_files)
        destination_path_object = pathlib.Path(globals.OUTPUT_FILE_PATH)
        globals.OUTPUT_FILE_DIR = str(destination_path_object.parent)
        file_object = ntpath.basename(globals.OUTPUT_FILE_PATH)
        globals.OUTPUT_FILENAME = file_object.split(".")[0]

        #print("Output File Path: ", globals.OUTPUT_FILE_PATH)
        #print("Output File Dir: ", globals.OUTPUT_FILE_DIR)

        return None

    def generate_midi_file(self):

        """
        This function converts the file uploaded to .mid. It checkes if the
        user has actually uploaded a file and if the conversion is valid.
        """

        if self.file_container.is_empty() is True:
            QtWidgets.QMessageBox.about(self, "File Needed", "Please upload a file before taking an action")
            return None

        if self.file_container.has_midi_file() is True:
            QtWidgets.QMessageBox.about(self, "Invalid/Unnecessary Conversion", "Cannot convert .mid to .mid or already present .mid file in output directory.")
            return None

        if self.exe_validity_check('.mid') is False:
            QtWidgets.QMessageBox.about(self, "Invalid/Missing EXE Paths", "Cannot convert input file to .mid file because .exe path(s) of external applications are invalid/missing.")
            return None

        self.get_output_information('Save MIDI File', 'MIDI Files (*.mid)')

        if globals.OUTPUT_FILE_PATH == '':
            print('Invalid Save File')
            return None
        else:
            print("Valid Save file")

        self.loading_animation_dialog = LoadingAnimationDialog()
        self.loading_animation_dialog.setModal(True)
        self.loading_animation_dialog.show()

        self.file_conversion_output = '.mid'
        self.file_converter = FileConverter(self, '.mid')
        self.file_converter.start()
        self.file_converter.finished.connect(self.file_conversion_completion)

        return None

    def generate_pdf_file(self):

        """
        This function converts the uploaded file into a .pdf. It checks if the
        user has uploaded file to beging with and if the conversion is valid.
        """

        if self.file_container.is_empty() is True:
            QtWidgets.QMessageBox.about(self, "File Needed", "Please upload a file before taking an action.")
            return None

        if self.file_container.has_pdf_file() is True:
            QtWidgets.QMessageBox.about(self, "Invalid/Unnecessary Conversion", "Cannot convert .pdf to .pdf or already present .pdf file in output directory")
            return None

        if self.exe_validity_check('.pdf') is False:
            QtWidgets.QMessageBox.about(self, "Invalid/Missing EXE Paths", "Cannot convert input file to .pdf file because .exe path(s) of external applications are invalid/missing.")
            return None

        self.get_output_information('Save PDF File', 'PDF Files (*.pdf)')

        if globals.OUTPUT_FILE_PATH == '':
            print('Invalid Save File')
            return None
        else:
            print("Valid Save file")

        self.loading_animation_dialog = LoadingAnimationDialog()
        self.loading_animation_dialog.setModal(True)
        self.loading_animation_dialog.show()

        self.file_conversion_output = '.pdf'
        self.file_converter = FileConverter(self, '.pdf')
        self.file_converter.start()
        self.file_converter.finished.connect(self.file_conversion_completion)

        return None

    def file_conversion_completion(self):

        """
        This function stops the loading animation and if necessary setups up the
        tutor thread.
        """

        print("Completed File Conversion")
        self.loading_animation_dialog.close()

        if self.file_conversion_output == '.mid':
            self.setup_tutor()

        return None

    #--------------------------------------------------------------------------
    # Midi Handling

    def midi_setup(self):

        """
        This fuction deletes pre-existing MIDI files and places the new desired MIDI
        file into the cwd of tutor.py . Then it converts the midi information
        of that file into a sequence of note events.
        """

        # Mido Method
        self.tracks_selected_labels = None
        self.midi_file = mido.MidiFile(self.midi_file_path)
        self.midi_file.tick_divider = 1

        print("Ticks per beat: ", self.midi_file.ticks_per_beat)

        self.track_translation()

        return True

    def track_translation(self):

        """
        This function does the complete process of converting a track into
        a filtered sequence.
        """

        self.original_sequence = []
        self.filtered_sequence = []

        # Now obtaining the pattern of the midi file found.
        self.track_identification()
        self.track_selection()
        self.calculate_tick_divider()
        self.stage_track_to_sequence()
        self.sequence_filtering()
        self.midi_report()

        # Setting default tempo
        self.tempo = 500000
        self.set_tick_per_frame()
        self.set_total_events()

        return None

    def track_identification(self):

        """
        This function identifies and labels the tracks found in the midi file.
        Majority of midi files contain a setup track with META events and then
        have the actual song tracks. This identification process account for both
        types of tracks.
        """

        #print("Looking into the midi file's tracks")
        #print("Quantity of Tracks: ", len(self.midi_file.tracks))

        self.tracks_information = []
        self.setup_tracks = []
        self.note_tracks = []

        for i in range(len(self.midi_file.tracks)):
            meta_counter = 0
            note_counter = 0
            track_name = "Track " + str(i)
            self.midi_file.tracks[i].name = track_name

            for msg in self.midi_file.tracks[i]:
                if msg.is_meta:
                    meta_counter += 1
                    if msg.type == 'track_name':

                        if msg.name == '':
                            continue

                        self.midi_file.tracks[i].name = msg.name
                if msg.type == 'note_on':
                    note_counter += 1

            if note_counter == 0:
                # setup tracks
                self.midi_file.tracks[i].track_type = "setup_track"
                self.setup_tracks.append(self.midi_file.tracks[i])
            else:
                self.midi_file.tracks[i].track_type = 'note_track'
                self.midi_file.tracks[i].played = False
                self.note_tracks.append(self.midi_file.tracks[i])

        return None

    def track_selection(self):

        """
        This function allows the selection of particular tracks by their track
        names. With the selected tracks, a new 'staged_track' is generated, that
        includes all the selected tracks. Having the entire selected song in one
        track makes the process of making the filtered sequence much easier.
        """

        #print("Note tracks: ", self.note_tracks)

        if self.tracks_selected_labels is None:
            # Setup and first note event track for original setup
            self.staged_track = mido.merge_tracks([self.note_tracks[0]] + self.setup_tracks)
            self.note_tracks[0].played = True

        else:
            self.tracks_selected = []

            for track in self.note_tracks:
                track.played = self.tracks_selected_labels[track.name]
                if track.played is True:
                    self.tracks_selected.append(track)

            self.staged_track = mido.merge_tracks(self.tracks_selected + self.setup_tracks)

        #print("Staged Track", self.staged_track)

        return None

    def calculate_tick_divider(self):

        """
        This function calculates the tick divider to normalize the midi file
        into a standard midi file [that its PPQN is 98]. This helps make midi
        files more predictable and typically resolves many spacing errors in
        the graphics side of the midi file.
        """

        cfg = read_config()

        if cfg['options']['normalize ppqn'] is True:

            if self.midi_file.ticks_per_beat != globals.PPQN_STANDARD:
                print("TICKS PER BEAT TOO HIGH -> SET TO DEFAULT 98")
                self.midi_file.tick_divider = self.midi_file.ticks_per_beat / globals.PPQN_STANDARD
                self.midi_file.ticks_per_beat = globals.PPQN_STANDARD

        else:
            print("PPQN not normalized to 98")

        #print("self.midi_file.tick_divider: ", self.midi_file.tick_divider)

        return None

    def stage_track_to_sequence(self):

        """
        This function converts the staged track, which includes all the selected
        tracks in to sequence of turn on, turn off, and set tempo events. These
        events are the information that we are concern in the song.
        """

        cfg = read_config()
        piano_size = cfg['port']['piano_size']

        if piano_size == '88':
            lowest_note = 21
            highest_note = 108

        elif piano_size == '76':
            lowest_note = 29
            highest_note = 104

        #print("Tracked used: ", self.staged_track)

        for msg in self.staged_track:

            #print(msg)

            if msg.type == 'note_on':

                if msg.note > highest_note or msg.note < lowest_note:
                    continue

                if msg.velocity == 0:
                    # Note Off
                    self.original_sequence.append(SkoreMidiEvent(None, round(msg.time / self.midi_file.tick_divider)))
                    self.original_sequence.append(SkoreMidiEvent(False, msg.note))
                    continue

                # Note On
                self.original_sequence.append(SkoreMidiEvent(None, round(msg.time / self.midi_file.tick_divider)))
                self.original_sequence.append(SkoreMidiEvent(True, msg.note))

            elif msg.type == 'note_off':

                if msg.note > highest_note or msg.note < lowest_note:
                    continue

                # Note Off
                self.original_sequence.append(SkoreMidiEvent(None, round(msg.time / self.midi_file.tick_divider)))
                self.original_sequence.append(SkoreMidiEvent(False, msg.note))

            if msg.is_meta:
                self.original_sequence.append(SkoreMetaEvent(msg.type, msg))

        return None

    def sequence_filtering(self):

        """
        This function performs the digital filtering of the sequence to convert
        a string of close notes into a chord. Basically, chord detection happens
        within this function.
        """

        #print("CHORD TICK TOLERANCE USED: ", globals.CHORD_TICK_TOLERANCE)

        final_index = -1

        for i in range(len(self.original_sequence)):

            #-------------------------------------------------------------------
            # Meta Event Detection

            if isinstance(self.original_sequence[i], SkoreMetaEvent):
                #print("Meta Event Added to self.filtered_sequence at {} index", i)
                self.filtered_sequence.append(["META", self.original_sequence[i].event_type, self.original_sequence[i].data])
                continue

            if final_index >= i:
                continue

            if self.original_sequence[i].event_type is None or self.original_sequence[i].event_type is False:
                continue

            #-------------------------------------------------------------------
            # Determing Pre-Note/Chord Delay

            delta_time = 0

            for event in reversed(self.original_sequence[:i]):

                if event.event_type is None:
                    delta_time += event.data

                elif event.event_type is True:
                    break

            #-------------------------------------------------------------------
            # Chord Detection

            chord_delta_time = 0
            note_array = []
            final_index = i

            for index_tracker, event in enumerate(self.original_sequence[i:]):

                if event.event_type is None:
                    if event.data >= globals.CHORD_TICK_TOLERANCE:
                        final_index += index_tracker - 1
                        break
                    else:
                        if chord_delta_time + event.data >= globals.CHORD_SUM_TOLERANCE:
                            final_index += index_tracker - 1
                            break
                        else:
                            chord_delta_time += event.data

                elif event.event_type is True:
                    note_array.append(event.data)

            self.filtered_sequence.append([note_array, delta_time])

        return None

    def midi_report(self):

        """
        This function informs the user about the specs of the inputted midi file.
        """

        print("""
---------------------------Tutor Midi Setup-----------------------------
MIDI FILE LOCATION:
{0}

STAGED TRACK:
{1}

ORIGINAL MIDI SEQUENCE LENGTH:
{2}

FILTERED MIDI SEQUENCE LENGTH:
{3}

        """.format(self.midi_file_path, self.staged_track, len(self.original_sequence), len(self.filtered_sequence)))#.format(self.midi_file_path, len(self.original_sequence), len(self.filtered_sequence)))

        return None

    def set_total_events(self):

        """
        This function sets the total events number. This number is utlized in the
        go to feature.
        """

        globals.TOTAL_EVENTS = len(self.filtered_sequence) - 1
        self.label_current_event_value.setText("0/{0}".format(globals.TOTAL_EVENTS))
        self.spinbox_go_to.setRange(0, globals.TOTAL_EVENTS)

        self.spinbox_final_location.setRange(1, globals.TOTAL_EVENTS)
        self.spinbox_initial_location.setRange(0, globals.TOTAL_EVENTS - 1)
        self.spinbox_final_location.setValue(globals.TOTAL_EVENTS)
        self.spinbox_initial_location.setValue(0)

        return None

    def set_tick_per_frame(self):

        """
        This function is responsbile for determing the speed of the notes
        depending on many aspects of the song, its spacing, the frame rate of the
        SKORE application.
        """

        print("#@@@@@@@@@@@@@@@@@@@@@@SET TICK PER FRAME@@@@@@@@@@@@@@@@@@@@@@@@")

        # 60 fps = 16ms, 1fps = a number of ticks
        """
        try:
            difference = time.time() - self.initial_time
        except AttributeError:
            pass

        self.initial_time = time.time()

        try:
            print("Difference: ", difference)
            frame_per_sec = 1000/(difference*1000)
            print("frame_per_sec: ", frame_per_sec)
        except NameError:
            frame_per_sec = 1000/(globals.CLOCK_DELAY)
        """

        frame_per_sec = 1000/(globals.CLOCK_DELAY)

        sec_per_tick = mido.tick2second(1, self.midi_file.ticks_per_beat, self.tempo) / (self.midi_file.tick_divider * 2)
        sec_per_tick = sec_per_tick * 100/globals.LIVE_SETTINGS['speed']

        self.tick_per_frame = (1/sec_per_tick) * (1/frame_per_sec)

        print("Calculated tick_per_frame: ", self.tick_per_frame)

        # Too high tick_per_frame safety. Can cause tutoring to miss events.

        if self.tick_per_frame > globals.MAX_TICK_PER_FRAME * globals.LIVE_SETTINGS['speed']/100:
            print("tick_per_frame value is too high, setting it to max value.")
            self.tick_per_frame = globals.MAX_TICK_PER_FRAME * globals.LIVE_SETTINGS['speed']/100
            print("New tick_per_frame value = {0}".format(globals.MAX_TICK_PER_FRAME * globals.LIVE_SETTINGS['speed']/100))

        return None

    #---------------------------------------------------------------------------
    # Track Management

    def open_track_manager_dialog(self):

        """
        This function opens the track manager dialog for the user to change
        the tracks utlized at the moment.
        """

        if self.tutor_enable is True:
            print("Open track_manager")
            self.track_manager = TrackManagerDialog(self.note_tracks)
            self.track_manager.finished_and_transmit_data_signal.connect(self.end_track_manager_dialog)
            self.track_manager.setModal(True)
            self.track_manager.show()
        else:
            QtWidgets.QMessageBox.about(self, "No MIDI File", "Please first upload or generate a MIDI file.")

        return None

    @QtCore.pyqtSlot('QString')
    def end_track_manager_dialog(self, tracks_selected_labels):

        """
        This function determines the tracks selected by the user while using the
        track manager dialog. Then it performs the necessary task to update the
        staged track to then redraw the new filtered sequence.
        """

        print("Accepted")
        print("tracks_selected_labels: ", tracks_selected_labels)

        self.tracks_selected_labels = ast.literal_eval(tracks_selected_labels)

        self.clean_tutor()
        self.track_translation()
        self.set_tutor()

        return None

    #---------------------------------------------------------------------------
    # Settings Functions

    def open_settings_dialog(self):

        """ This function opens the ConfigDialog to change the apps settings. """

        self.config_dialog = ConfigDialog()
        self.config_dialog.finish_apply_signal.connect(self.settings_dialog_change)
        self.config_dialog.setModal(True)
        self.config_dialog.show()

        return None

    def settings_dialog_change(self):

        """
        This function performs the necessary steps to implement the changes the
        user desires, that were indicated in the ConfigDialog.
        """

        cfg = read_config()

        print("SETTINGS UPDATE: CHANGES APPLIED")
        self.update_globals()

        if self.piano_status is False:
            self.piano_port_setup()

        elif self.arduino_status is False or self.arduino_color_palet != cfg['color']:
            self.arduino_setup()

        self.comm_status_report()

        if self.midi_file_path is not None:
            self.setup_tutor()

        return None

    #---------------------------------------------------------------------------

    def skore_recorder(self):

        """
        This function changes the MIDI port handler to the skore recorder and
        opens the skore_recorder dialog.
        """

        try:
            self.recorder_handler = RecorderMidiHandler(self)
            self.midi_in.set_callback(self.recorder_handler)
        except AttributeError:
            QtWidgets.QMessageBox.about(self, "No MIDI device paired to SKORE", "Please first connect a MIDI device before recording.")
            return None

        self.recorder_dialog = RecorderDialog(self)
        self.recorder_dialog.finished.connect(self.end_skore_recorder)
        self.recorder_dialog.setModal(True)
        self.recorder_dialog.show()

        return None

    def end_skore_recorder(self):

        """
        This function returns the MIDI port handler back to tutoring after the
        user closes the skore_recorder dialog.
        """

        try:
            self.midi_in.set_callback(self.tutor_midi_handler)
        except AttributeError:
            print("Returning TutorMidiHandler to midi_in.set_callback failed!")

        print("Return from recorder_dialog")
        del self.recorder_dialog

        return None

    #---------------------------------------------------------------------------
    # Misc Functions

    def open_skore_website(self):

        """ This function simply opens the SKORE website. """

        webbrowser.open('https://mrcodingrobot.github.io/SKORE/')

        return None

    def open_about_dialog(self):

        """
        This function opens the AboutDialog, informing the user about the
        SKORE application.
        """

        print("About Message")
        self.about_dialog = AboutDialog()
        self.about_dialog.setModal(True)
        self.about_dialog.show()

        return None

    def update_globals(self):

        """
        This function updates some global variables that are subject to change
        by the user-controlled settings.
        """

        cfg = read_config()
        globals.CHORD_SUM_TOLERANCE = cfg['timing']['chord sum tolerance']
        globals.CHORD_TICK_TOLERANCE = cfg['timing']['chord tick tolerance']
        globals.COUNT_TIMEOUT = cfg['timing']['count timeout']
        globals.RECORD_CHORD_TOLERANCE = cfg['timing']['record chord tolerance']
        globals.ARDUINO_BAUD_RATE = cfg['port']['arduino baud rate']

        return None

    def closeEvent(self, event):

        """
        This function creates a nice rainbow effect to turn off all the lights
        in the LED Bar and to indicate the user that the application has been
        closed appropriately.
        """

        self.close()

        if self.arduino_status is True:

            # Night Rider effect
            """
            for i in range(90):
                send_string = '<u,{0},>'.format(i)
                self.arduino_write_and_handshake(send_string)

            for i in range(90):
                send_string = '<f,{0},>'.format(i)
                self.arduino_write_and_handshake(send_string)
            """
            pass

        return None

    def retranslate_ui(self):

        """
        This function handles with filling in the text content in the majority
        of the widgets in the SKORE application.
        """

        _translate = QtCore.QCoreApplication.translate

        self.toolbutton_restart.setText(_translate("MainWindow", "Restart"))
        self.toolbutton_play.setText(_translate("MainWindow", "Play"))
        self.toolbutton_track_manager.setText(_translate("MainWindow", "Track Manager"))
        self.toolbutton_skip_event.setText(_translate("MainWindow", "Skip Event"))

        self.label_speed.setText(_translate("MainWindow", "Speed:"))
        self.label_transpose.setText(_translate("MainWindow", "Transpose:"))
        self.label_tutoring_mode.setText(_translate("MainWindow", "Tutoring Mode:"))
        self.label_current_event.setText(_translate("MainWindow", "Current Event / Total Events :"))
        self.label_current_event_value.setText(_translate("MainWindow", "0/0"))
        self.label_go_to_event.setText(_translate("MainWindow", "Go To:"))
        self.label_interval_enable.setText(_translate("MainWindow", "Repetition Enabled: "))
        self.label_interval.setText(_translate("MainWindow", "Repetition Interval: "))

        self.menu_file.setTitle(_translate("MainWindow", "File"))
        self.menu_settings.setTitle(_translate("MainWindow", "Settings"))
        self.menu_help.setTitle(_translate("MainWindow", "Help"))
        self.action_open_file.setText(_translate("MainWindow", "Upload File..."))
        self.action_record.setText(_translate("MainWindow", "Record "))
        self.action_create_midi.setText(_translate("MainWindow", "Create MIDI"))
        self.action_create_pdf.setText(_translate("MainWindow", "Create PDF"))
        self.action_exit.setText(_translate("MainWindow", "Exit"))
        self.action_config.setText(_translate("MainWindow", "Config..."))
        self.action_website.setText(_translate("MainWindow", "Website"))
        self.action_about.setText(_translate("MainWindow", "About"))

        #-----------------------------------------------------------------------
        # Text Scaling

        font = self.label_speed.font()

        font.setPixelSize(13)
        #print("Prescaling Font Pixel Size: ", font.pixelSize())
        font.setPixelSize(font.pixelSize() * globals.S_W_R)
        #print("Postscaling Font Pixel Size: ", font.pixelSize())

        text_group = [self.toolbutton_restart, self.toolbutton_play, self.toolbutton_track_manager,
                      self.toolbutton_skip_event, self.label_speed, self.label_transpose, self.label_tutoring_mode,
                      self.label_current_event, self.label_current_event_value, self.label_go_to_event,
                      self.menu_file, self.menu_settings, self.menu_help, self.action_open_file,
                      self.action_record, self.action_create_midi, self.action_create_pdf,
                      self.action_exit, self.action_config, self.action_website,
                      self.action_about, self.spinbox_speed, self.spinbox_transpose,
                      self.combobox_tutoring_mode, self.spinbox_go_to, self.menubar,
                      self.label_interval_enable, self.checkbox_interval, self.label_interval,
                      self.spinbox_initial_location, self.spinbox_final_location]

        for element in text_group:
            element.setFont(font)

#-------------------------------------------------------------------------------
# Main Code

if __name__ == "__main__":

    #os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r'C:\Qt\5.11.2\winrt_x64_msvc2017\plugins'

    app = QtWidgets.QApplication(sys.argv)
    theme_list = QtWidgets.QStyleFactory.keys()
    app.setStyle(QtWidgets.QStyleFactory.create(theme_list[2])) #Fusion

    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    sizeObject = QtWidgets.QDesktopWidget().screenGeometry(-1)
    #print("Screen size : "  + str(sizeObject.height()) + "x"  + str(sizeObject.width()))

    globals.A_S_W = sizeObject.width()
    globals.A_S_H = sizeObject.height()
    globals.S_W_R = globals.A_S_W / globals.D_S_W
    globals.S_H_R = globals.A_S_H / globals.D_S_H

    app.addLibraryPath("./")
    QT_DEBUG_PLUGINS = True

    window = SkoreWindow()
    window.show()
    sys.exit(app.exec_())
