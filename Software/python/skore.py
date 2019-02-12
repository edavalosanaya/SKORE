# General Utility
import time
import sys
from time import sleep
import os
import difflib
import webbrowser
import ast

# PYQT5, GUI Library
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *

# Tutor Application
from midi import read_midifile, NoteEvent, NoteOffEvent, MetaEvent
from mido import tick2second, MidiFile, merge_tracks
import serial
import serial.tools.list_ports
import rtmidi

# This is to prevent an error caused when importing skore_lib
import warnings
warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2

# SKORE Library
import globals
from tutor_and_midi_classes import Tutor, TutorMidiHandler, SkoreMetaEvent, SkoreMidiEvent
from main_window_graphics import GraphicsSystemMessage, GraphicsPlayedLabel, GraphicsPlayedNameLabel
from main_window_graphics import GraphicsController, GraphicsNote
from lib_skore import FileContainer, GuiManipulator, read_config, is_mid, is_mp3, is_pdf, rect_to_int
from recorder_dialog import RecorderDialog, RecorderMidiHandler
from config_dialog import ConfigDialog
from track_manager_dialog import TrackManagerDialog

#-------------------------------------------------------------------------------
# Classes

class SkoreWindow(QMainWindow):

    def __init__(self):

        super(QMainWindow, self).__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle("SKORE")
        self.resize(1944, 984)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        #self.setStyleSheet("""
        #    background-color: rgb(0,0,0);
        #    color: white;
        #    """)

        # Variable Initialization
        self.midi_in = None
        self.arduino = None
        #globals.KEYBOARD_STATE = {'NEUTRAL':[],'RIGHT':[],'WRONG':[],'TARGET':[],'ARDUINO':[],'PREV_TARGET':[]}

        # Setup functions
        self.setup_ui()
        self.setup_graphics()
        self.setup_comm()
        self.setup_func()

        # File Handling
        self.file_container = FileContainer()
        self.file_container.clean_temp_folder()

        # Tutor setup
        self.tutor = None
        self.tutor_enable = False

        self.live_settings = {
            'play': False, 'restart': False, 'mode': 'Beginner', 'hand': 'Both',
            'speed': 100, 'transpose': 0
        }

        self.tracks_selected_labels = None

        # Timer Setup
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.clock)
        self.timer.start(globals.CLOCK_DELAY) # 60 FPS, 16ms, 30 FPS, 33ms

    def setup_ui(self):

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        #self.gridLayoutWidget.setGeometry(QtCore.QRect(-1, 0, 1922, 921))
        self.gridLayoutWidget.setGeometry(QtCore.QRect(-1, 0, 1922, 950))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")

        #-----------------------------------------------------------------------
        # gridLayout_central
        self.gridLayout_central = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_central.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_central.setObjectName("gridLayout_central")

        self.scene = QGraphicsScene()
        self.scene.setItemIndexMethod(-1)
        self.graphicsView_game = QtWidgets.QGraphicsView(self.scene, self.gridLayoutWidget)
        self.graphicsView_game.setObjectName("graphicsView_game")
        self.gridLayout_central.addWidget(self.graphicsView_game, 1, 0, 1, 1)

        #-----------------------------------------------------------------------
        # gridLayout_central -> horizontalLayout_live_settings
        self.horizontalLayout_live_settings = QtWidgets.QHBoxLayout()
        self.horizontalLayout_live_settings.setObjectName("horizontalLayout_live_settings")

        spacerItem = QtWidgets.QSpacerItem(10, 40, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.horizontalLayout_live_settings.addItem(spacerItem)

        self.toolButton_restart = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_restart.setObjectName("toolButton_restart")
        self.horizontalLayout_live_settings.addWidget(self.toolButton_restart)

        self.toolButton_play = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_play.setObjectName("toolButton_play")
        self.horizontalLayout_live_settings.addWidget(self.toolButton_play)

        self.toolButton_track_manager = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_track_manager.setObjectName("toolButton_track_manager")
        self.horizontalLayout_live_settings.addWidget(self.toolButton_track_manager)

        self.label_tutoring_mode = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_tutoring_mode.setObjectName("label_tutoring_mode")
        self.horizontalLayout_live_settings.addWidget(self.label_tutoring_mode)

        self.comboBox_tutoring_mode = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_tutoring_mode.setObjectName("comboBox_tutoring_mode")
        self.horizontalLayout_live_settings.addWidget(self.comboBox_tutoring_mode)

        self.label_hand_skill = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_hand_skill.setObjectName("label_hand_skill")
        self.horizontalLayout_live_settings.addWidget(self.label_hand_skill)

        self.comboBox_hand_skill = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_hand_skill.setObjectName("comboBox_hand_skill")
        self.horizontalLayout_live_settings.addWidget(self.comboBox_hand_skill)

        self.label_speed = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_speed.setObjectName("label_speed")
        self.horizontalLayout_live_settings.addWidget(self.label_speed)

        self.spinBox_speed = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox_speed.setObjectName("spinBox_speed")
        self.horizontalLayout_live_settings.addWidget(self.spinBox_speed)

        self.label_transpose = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_transpose.setObjectName("label_transpose")
        self.horizontalLayout_live_settings.addWidget(self.label_transpose)

        self.spinBox_transpose = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox_transpose.setObjectName("spinBox_transpose")
        self.horizontalLayout_live_settings.addWidget(self.spinBox_transpose)

        spacerItem2 = QtWidgets.QSpacerItem(40, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.horizontalLayout_live_settings.addItem(spacerItem2)

        self.gridLayout_central.addLayout(self.horizontalLayout_live_settings, 0, 0, 1, 1)

        #-----------------------------------------------------------------------
        # Menubar
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1944, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)


        self.actionOpenFile = QtWidgets.QAction(self)
        self.actionOpenFile.setObjectName("actionOpenFile")
        self.actionRecord = QtWidgets.QAction(self)
        self.actionRecord.setObjectName("actionRecord")
        self.actionPlay = QtWidgets.QAction(self)
        self.actionPlay.setObjectName("actionPlay")
        self.actionCreate_MIDI = QtWidgets.QAction(self)
        self.actionCreate_MIDI.setObjectName("actionCreate_MIDI")
        self.actionCreate_PDF = QtWidgets.QAction(self)
        self.actionCreate_PDF.setObjectName("actionCreate_PDF")

        self.actionSave_File = QtWidgets.QAction(self)
        self.actionSave_File.setObjectName("actionSave_File")
        self.actionExit = QtWidgets.QAction(self)
        self.actionExit.setObjectName("actionExit")

        self.actionConfig = QtWidgets.QAction(self)
        self.actionConfig.setObjectName("actionConfig")
        #self.actionTrackManager = QtWidgets.QAction(self)
        #self.actionTrackManager.setObjectName("actionTrackManager")

        self.actionWebsite = QtWidgets.QAction(self)
        self.actionWebsite.setObjectName("actionWebsite")
        self.actionAbout = QtWidgets.QAction(self)
        self.actionAbout.setObjectName("actionAbout")

        #-----------------------------------------------------------------------
        # MenuFile

        self.menuFile.addAction(self.actionOpenFile)
        self.menuFile.addAction(self.actionRecord)
        self.menuFile.addSeparator()

        # Troubleshooting for now
        self.menuFile.addAction(self.actionPlay)

        self.menuFile.addAction(self.actionCreate_MIDI)
        self.menuFile.addAction(self.actionCreate_PDF)
        self.menuFile.addAction(self.actionSave_File)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)

        #self.menuSettings.addAction(self.actionTrackManager)
        self.menuSettings.addAction(self.actionConfig)

        self.menuHelp.addAction(self.actionWebsite)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())


        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setTabOrder(self.toolButton_restart, self.toolButton_play)
        self.setTabOrder(self.toolButton_play, self.spinBox_transpose)
        self.setTabOrder(self.spinBox_transpose, self.graphicsView_game)
        self.setTabOrder(self.graphicsView_game, self.spinBox_speed)

        return None

    def setup_func(self):

        """
        QActions that still need assignment
        self.actionAbout = QtWidgets.QAction(self)
        self.actionAbout.setObjectName("actionAbout")
        """
        #-----------------------------------------------------------------------
        # MenuBar Actions
        self.actionOpenFile.setShortcut('Ctrl+O')
        self.actionOpenFile.triggered.connect(self.upload_file)

        self.actionRecord.setShortcut("Ctrl+Shift+R")
        self.actionRecord.triggered.connect(self.skore_recorder)

        # Troubleshooting
        self.actionPlay.setShortcut("Ctrl+Shift+P")
        self.actionPlay.triggered.connect(self.play_midi_file)

        self.actionCreate_MIDI.setShortcut("Ctrl+M")
        self.actionCreate_MIDI.triggered.connect(self.generate_midi_file)

        self.actionCreate_PDF.setShortcut("Ctrl+P")
        self.actionCreate_PDF.triggered.connect(self.generate_pdf_file)

        self.actionSave_File.setShortcut("Ctrl+S")
        self.actionSave_File.triggered.connect(self.save_generated_files)

        self.actionExit.triggered.connect(self.close)

        self.actionConfig.triggered.connect(self.open_settings_dialog)

        #self.actionTrackManager.setShortcut("Ctrl+Shift+T")
        #self.actionTrackManager.triggered.connect(self.open_track_manager_dialog)

        self.actionWebsite.triggered.connect(self.open_skore_website)

        #-----------------------------------------------------------------------
        # Live Settings
        self.toolButton_play.clicked.connect(self.play_stop)
        self.toolButton_restart.clicked.connect(self.restart)
        self.toolButton_track_manager.clicked.connect(self.open_track_manager_dialog)

        self.spinBox_speed.setRange(globals.MIN_SPEED, globals.MAX_SPEED)
        self.spinBox_speed.setSingleStep(1)
        self.spinBox_speed.setValue(100)
        self.spinBox_speed.valueChanged.connect(self.speed_change)

        self.spinBox_transpose.setRange(-12, 12)
        self.spinBox_transpose.setSingleStep(1)
        self.spinBox_transpose.setValue(0)
        self.spinBox_transpose.valueChanged.connect(self.transpose_change)

        #-----------------------------------------------------------------------
        # ComboBox Settings

        self.comboBox_tutoring_mode.addItem("Beginner")
        self.comboBox_tutoring_mode.addItem("Intermediate")
        self.comboBox_tutoring_mode.addItem("Expert")

        self.comboBox_hand_skill.addItem("Both")
        self.comboBox_hand_skill.addItem("Left Hand")
        self.comboBox_hand_skill.addItem("Right Hand")

        self.comboBox_tutoring_mode.currentIndexChanged.connect(self.mode_change)
        self.comboBox_hand_skill.currentIndexChanged.connect(self.hand_change)

        return None

    #---------------------------------------------------------------------------
    # Communications

    def setup_comm(self):

        self.arduino_status = self.arduino_setup()
        self.piano_status = self.piano_port_setup()

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

        return False

    def arduino_setup(self):
        # This functions sets up the communication between Python and the Arduino.
        # For now the Arduino is assumed to be connected to COM3.
        cfg = read_config()

        # Closing, if applicable, the arduino port
        if self.arduino:
            self.arduino.close()
            self.arduino = []

        com_port = cfg['port']['arduino']

        try:
            self.arduino = serial.Serial(com_port, globals.ARDUINO_BAUD_RATE, writeTimeout = globals.COMM_TIMEOUT)
        except serial.serialutil.SerialException:
            print("ARDUINO AT {0} NOT FOUND".format(com_port))
            return False

        transmitted_string = {}

        for key, values in cfg['color'].items():
            transmitted_string[key] = cfg['color'][key]

        # Color Setup Order: White/Black/Right/Wrong/Upcoming
        setup_transmitted_string = transmitted_string['white'] + ',' + transmitted_string['black']
        setup_transmitted_string = setup_transmitted_string + ',' + transmitted_string['wrong'] + ',' + transmitted_string['upcoming'] + ','

        time.sleep(2)
        self.arduino.write(setup_transmitted_string.encode('utf-8'))

        print("""
--------------------------Arduino Configuration-------------------------
COM PORT: {0}
SETUP STRING: {1}

        """.format(com_port, setup_transmitted_string))

        if self.arduino_handshake() is not True:
            print("Arduino Handshake failed")

        return True

    def piano_port_setup(self):
        # This function sets up the communication between Python and the MIDI device
        # For now Python will connect the first listed device.

        # Rtmidi method
        if not self.midi_in:
            try:
                self.midi_in.close_port()
            except:
                self.midi_in = None

        #-----------------------------------------------------------------------
        # Midi In

        self.midi_in = rtmidi.MidiIn()
        in_avaliable_ports = self.midi_in.get_ports()
        cfg = read_config()
        selected_port = cfg['port']['piano']

        try:
            self.closes_match_in_port = difflib.get_close_matches(selected_port, in_avaliable_ports)[0]
        except IndexError:
            print("{0} NOT FOUND".format(selected_port))
            self.midi_in = None
            return False


        try:
            self.midi_in.open_port(in_avaliable_ports.index(self.closes_match_in_port))
        except:
            print("Piano Port Setup Failure")
            self.midi_in = None
            return False

        globals.WRONG_NOTE_READY = True
        self.tutor_midi_handler = TutorMidiHandler(self)
        self.midi_in.set_callback(self.tutor_midi_handler)
        #self.midi_in.set_callback(TutorMidiHandler(self))

        #-----------------------------------------------------------------------
        # Midi Out

        self.midi_out = rtmidi.MidiOut()
        out_avaliable_ports = self.midi_out.get_ports()
        try:
            self.closes_match_out_port = difflib.get_close_matches(selected_port, out_avaliable_ports)[0]
        except IndexError:
            print("OUTPUT PORT TO {0} NOT FOUND".format(selected_port))
            self.midi_in = None
            self.midi_out = None
            return False

        try:
            self.midi_out.open_port(out_avaliable_ports.index(self.closes_match_out_port))
        except:
            print("Piano MIDI OUT Port Setup Failure")
            self.midi_out = None
            return False

        print("""
----------------------------Piano Configuration-------------------------
MIDI IN & OUT
PIANO PORT: {0} (SUCCESSFUL)
PIANO PORT HANDLER SETUP (SUCCESSFUL)

        """.format(self.closes_match_in_port))

        return True

    def white_keys_string(self, notes):
        white_keys_string_value = ','.join(str(note - globals.KEYBOARD_SHIFT) for note in notes if note in globals.NOTE_PITCH_WHITE_KEYS)
        return white_keys_string_value

    def black_keys_string(self, notes):
        black_keys_string_value = ','.join(str(note - globals.KEYBOARD_SHIFT) for note in notes if note in globals.NOTE_PITCH_BLACK_KEYS)
        return black_keys_string_value

    def black_white_send_string(self, notes):
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

        print("STRING SENT:", send_string)
        self.arduino.write(send_string.encode('utf-8'))

        if self.arduino_handshake() is not True:
            raise RuntimeError("Communication Desync with Arduino")
            #print("Continue eventhough Arduino Handshake Failed")

        return None

    def arduino_handshake(self):

        count = 0

        while True:
            time.sleep(globals.HANDSHAKE_DELAY)
            read_data = self.arduino.read()

            if read_data == b'+':
                print("HANDSHAKE COMPLETED")
                return True

            #print(count)
            if count > globals.COUNT_TIMEOUT:
                break
            else:
                count += 1


        print("HANDSHAKE FAILED!")
        return False

    def arduino_comm(self, notes, operation = 'set'):
        # This function sends the information about which notes need to be added and
        # removed from the LED Rod.
        # <,w,1,>

        #print("Arduino Comm - Notes: {0}\tOperation: {1}".format(notes, operation))

        if self.arduino_status is False:
            return None

        #-----------------------------------------------------------------------
        # Handling right/wrong notification option

        if operation[0] == 'i': # Incorrect
            globals.WRONG_NOTE_READY = False
            #print("wrong_note_ready is False")
            notes_to_send = [notes]

            if operation.endswith('on'):
                if notes not in globals.KEYBOARD_STATE['ARDUINO']['RW'] and notes not in globals.KEYBOARD_STATE['TARGET']:
                    send_string = '<i' + ',' + ','.join(str(note - globals.KEYBOARD_SHIFT) for note in notes_to_send) + ',>'
                    self.arduino_write_and_handshake(send_string)
                    globals.KEYBOARD_STATE['ARDUINO']['RW'] += notes_to_send
            else: # off
                if notes in globals.KEYBOARD_STATE['TARGET']:
                    try:
                        globals.KEYBOARD_STATE['ARDUINO']['RW'].remove(notes)
                    except ValueError:
                        print("Attempted removal of note not in KEYBOARD_STATE['ARDUINO']['RW']")

                elif notes in globals.KEYBOARD_STATE['ARDUINO']['RW']:
                    send_string = '<f,' + ','.join(str(note - globals.KEYBOARD_SHIFT) for note in notes_to_send) + ',>'
                    self.arduino_write_and_handshake(send_string)
                    globals.KEYBOARD_STATE['ARDUINO']['RW'].remove(notes)

            globals.WRONG_NOTE_READY = True
            #print("wrong_note_ready is True")
            return None


        #-----------------------------------------------------------------------
        # Handling timing notification option
        count = 0

        while globals.WRONG_NOTE_READY is False:
            time.sleep(globals.HANDSHAKE_DELAY)
            #print("handling timing notification & globals.WRONG_NOTE_READY")

            if count > globals.COUNT_TIMEOUT:
                print("PANIC!")
                globals.HANDLER_ENABLE = False
                globals.WRONG_NOTE_READY = True
                globals.KEYBOARD_STATE['ARDUINO']['RW'] = []

                print("Cleaning LED")
                temp_target = globals.KEYBOARD_STATE['TARGET']
                self.arduino_comm([], 'set')
                print("Placing Back the Target")
                globals.KEYBOARD_STATE['TARGET'] = temp_target
                self.arduino_comm(globals.KEYBOARD_STATE['TARGET'])

                #globals.WRONG_NOTE_READY = False
                globals.HANDLER_ENABLE = True
                break
            else:
                count += 1


        globals.HANDLER_ENABLE = False

        #-----------------------------------------------------------------------
        # Clear All

        if notes == []:
            #print("Clear all except Right/Wrong Notes")
            globals.HANDLER_ENABLE = False

            right_wrong_notes = globals.KEYBOARD_STATE['ARDUINO']['RW']
            send_string = '<!,>'

            self.arduino_write_and_handshake(send_string)
            globals.KEYBOARD_STATE['ARDUINO']['TARGET'] = []
            globals.KEYBOARD_STATE['ARDUINO']['RW'] = []

            if right_wrong_notes != []:
                send_string = '<i,' + ','.join(str(note - globals.KEYBOARD_SHIFT) for note in right_wrong_notes) + ',>'
                self.arduino_write_and_handshake(send_string)
                globals.KEYBOARD_STATE['ARDUINO']['RW'] = right_wrong_notes

            globals.HANDLER_ENABLE = True

            return None

        #-----------------------------------------------------------------------
        # Notes

        if self.tutor.options['timing notification'] is False:
            if operation != 'correct' and operation != 'incorrect':
                send_string = self.black_white_send_string(notes)

        else:
            if operation == 'timing':
                send_string = self.black_white_send_string(notes)
            elif operation == 'set':
                notes_to_send = list(set(notes).symmetric_difference(globals.KEYBOARD_STATE['ARDUINO']['TARGET']))
                send_string = '<u,' + ','.join(str(note - globals.KEYBOARD_SHIFT) for note in notes_to_send) + ',>'

        self.arduino_write_and_handshake(send_string)
        globals.KEYBOARD_STATE['ARDUINO']['TARGET'] = notes

        globals.HANDLER_ENABLE = True

        return None

    #---------------------------------------------------------------------------
    # Graphics Functions

    def clock(self):
        self.scene.update()
        return None

    def setup_graphics(self):

        self.graphicsView_game.setBackgroundBrush(QBrush(Qt.black))

        #-----------------------------------------------------------------------
        # Setting up the Staff
        greenPen = QPen(Qt.green)
        w = 1500
        x = round(w/2) * -1
        y = 200
        group = []

        for i in range(5):
            group.append(self.scene.addLine(x, y, x+w, y, greenPen))
            y -= 20

        y = -200

        for i in range(5):
            group.append(self.scene.addLine(x, y, x+w, y, greenPen))
            y -= 20

        #-----------------------------------------------------------------------
        # Setting up Visible note box
        #w = 1350
        w = 1210
        #x = round(w/2) * -1 + round(w/20) + 20
        x = round(w/2) * -1 + round(w/20) + 80
        h = 810
        y = round(h/2) * -1 - round(h/10) + 15

        #print("X1: {0} Y1: {1}\tX2: {2} Y2: {3}".format(x,y,x+w,y+h))

        redPen = QPen(Qt.red)
        redBrush = QBrush(Qt.red)

        self.visible_note_box = self.scene.addRect(x,y,w,h, redPen, redBrush)
        self.visible_note_box.setOpacity(globals.HIDDEN)

        #-----------------------------------------------------------------------
        # Setting up timing note bar
        w = 50 # tolerances of 25 on each side
        x = globals.LEFT_TICK_SHIFT - round(w/2)
        h = 810
        y = -470

        magentaBrush = QBrush(QColor(153, 0, 153))
        magentaPen = QPen(QColor(153, 0, 153))

        self.timing_note_box = self.scene.addRect(x, y, w , h, magentaPen, magentaBrush)
        self.timing_note_box.setOpacity(0.5)

        self.timing_note_line = self.scene.addLine(globals.LEFT_TICK_SHIFT, y, globals.LEFT_TICK_SHIFT, h + y, magentaPen)

        #-----------------------------------------------------------------------
        # Setting up timing note line catch
        w = 25
        x = globals.LEFT_TICK_SHIFT - round(w/2) - round(25/2) - 1
        h = 810
        y = -470

        whiteBrush = QBrush(Qt.white)
        whitePen = QPen(Qt.white)

        self.timing_note_line_catch = self.scene.addRect(x, y, w, h, whitePen, whiteBrush)
        self.timing_note_line_catch.setOpacity(globals.HIDDEN)

        #-----------------------------------------------------------------------
        # Placing Treble and Bass Clef
        treble_clef = QPixmap(r".\images\graphics_assets\green_treble_clef.png")
        treble_clef = treble_clef.scaledToHeight(180)

        treble_clef_pointer = self.scene.addPixmap(treble_clef)
        treble_clef_pointer.setOffset(-750, -331)

        bass_clef = QPixmap(r".\images\graphics_assets\green_bass_clef.png")
        bass_clef = bass_clef.scaledToHeight(70)

        bass_clef_pointer = self.scene.addPixmap(bass_clef)
        bass_clef_pointer.setOffset(-720, 120)

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

        #-----------------------------------------------------------------------

        globals.VISIBLE_NOTE_BOX = self.visible_note_box
        globals.TIMING_NOTE_BOX = self.timing_note_box
        globals.TIMING_NOTE_LINE = self.timing_note_line
        globals.TIMING_NOTE_LINE_CATCH = self.timing_note_line_catch

        # Note
        globals.PIXMAPS['GREEN'].append(QPixmap(r".\images\graphics_assets\green_music_note_head.png").scaled(19,19))
        globals.PIXMAPS['YELLOW'].append(QPixmap(r".\images\graphics_assets\yellow_music_note_head.png").scaled(19,19))
        globals.PIXMAPS['CYAN'].append(QPixmap(r".\images\graphics_assets\cyan_music_note_head.png").scaled(19,19))

        # Sharp
        globals.PIXMAPS['GREEN'].append(QPixmap(r".\images\graphics_assets\green_sharp.png").scaled(20,45))
        globals.PIXMAPS['YELLOW'].append(QPixmap(r".\images\graphics_assets\yellow_sharp.png").scaled(20,45))
        globals.PIXMAPS['CYAN'].append(QPixmap(r".\images\graphics_assets\cyan_sharp.png").scaled(20,45))

        # Flat
        globals.PIXMAPS['GREEN'].append(QPixmap(r".\images\graphics_assets\green_flat.png").scaled(13,35))
        globals.PIXMAPS['YELLOW'].append(QPixmap(r".\images\graphics_assets\yellow_flat.png").scaled(13,35))
        globals.PIXMAPS['CYAN'].append(QPixmap(r".\images\graphics_assets\cyan_flat.png").scaled(13,35))

        # Natural
        globals.PIXMAPS['GREEN'].append(QPixmap(r".\images\graphics_assets\green_natural.png").scaled(40,48))
        globals.PIXMAPS['YELLOW'].append(QPixmap(r".\images\graphics_assets\yellow_natural.png").scaled(40,48))
        globals.PIXMAPS['CYAN'].append(QPixmap(r".\images\graphics_assets\cyan_natural.png").scaled(40,48))

        return None

    def draw_filtered_sequence(self):

        tick_count = globals.LEFT_TICK_SHIFT
        #print("Drawing the following filtered_sequence")
        #print(self.filtered_sequence)

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
                    #print("Top note: ", drawn_note)
                    drawn_note.top_note = True

            self.drawn_notes_group.append(temp_list)

        return True

    def stop_all_notes(self):
        for event in self.drawn_notes_group:

            if event == ["META"]:
                continue

            for note in event:
                note.stop()
        return None

    def move_all_notes(self):

        for event in self.drawn_notes_group:

            if event == ["META"]:
                continue

            for note in event:
                note.set_speed(self.tick_per_frame)

        return None

    #---------------------------------------------------------------------------
    # GUI Tutoring Functions

    def play_stop(self):

        if self.tutor_enable is True:
            if self.live_settings['play'] is True:
                self.live_settings['play'] = False
                self.toolButton_play.setText("Play")
                self.stop_all_notes()
            else:
                self.live_settings['play'] = True
                self.toolButton_play.setText("Stop")
                self.move_all_notes()
        else:
            print("Tutor not enabled")

        return None

    def restart(self):

        if self.tutor_enable is True:

            #self.tutor.exit()
            self.tutor.terminate()
            self.live_settings['play'] = False
            self.toolButton_play.setText("Play")

            for event in self.drawn_notes_group:
                if event == ['META']:
                    continue
                for note in event:
                    self.scene.removeItem(note)
                    del note

            globals.KEYBOARD_STATE['ARDUINO']['RW'] = []
            self.arduino_comm([], 'set')

            self.drawn_notes_group.clear()
            self.draw_filtered_sequence()
            self.tutor = Tutor(self)
            self.tutor.start()
            self.tutor.finished.connect(self.end_of_song)

        else:
            print("Tutor not enabled")

        return None

    def mode_change(self):

        print("tutoring mode changed")
        self.live_settings['mode'] = self.comboBox_tutoring_mode.currentText()

        return None

    def hand_change(self):

        if self.tutor_enable is True:

            print("hand skill changed")
            self.live_settings['hand'] = self.comboBox_hand_skill.currentText()

            if self.live_settings['hand'] == "Both":
                for event in self.drawn_notes_group:
                    if event == ['META']:
                        continue
                    for note in event:
                        note.shaded = False

            elif self.live_settings['hand'] == "Right Hand":
                for event in self.drawn_notes_group:
                    if event == ['META']:
                        continue
                    for note in event:
                        if note.note_pitch >= globals.MIDDLE_C:
                            note.shaded = False
                        else:
                            note.shaded = True

            elif self.live_settings['hand'] == "Left Hand":
                for event in self.drawn_notes_group:
                    if event == ['META']:
                        continue
                    for note in event:
                        if note.note_pitch >= globals.MIDDLE_C:
                            note.shaded = True
                        else:
                            note.shaded = False
        else:
            print("Tutor not enabled")

        return None

    def speed_change(self):

        self.live_settings['speed'] = self.spinBox_speed.value()
        print("Speed Changed")

        if self.tutor_enable is True:
            self.set_tick_per_frame()

        return None

    def transpose_change(self):

        if self.tutor_enable is True:
            self.live_settings['transpose'] = self.spinBox_transpose.value()

            transpose_diff = self.live_settings['transpose'] - self.transpose_tracker
            self.transpose_tracker = self.live_settings['transpose']

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

        else:
            print("Tutor disabled, transpose change discarted")

        return None

    #---------------------------------------------------------------------------
    # Tutoring Manipulation Functions

    def setup_tutor(self):

        #print("CURRENT TASK: TUTOR SETUP")

        if self.tutor_enable:

            #self.tutor.exit()
            self.tutor.terminate()
            self.live_settings['play'] = False
            self.toolButton_play.setText("Play")

            for event in self.drawn_notes_group:
                if event == ['META']:
                    continue
                for note in event:
                    self.scene.removeItem(note)
                    del note

            self.drawn_notes_group.clear()

        # Normal tutor setup procedure
        self.tutor_enable = True

        self.original_sequence = []
        self.filtered_sequence = []

        # Graphics
        self.drawn_notes_group = []

        self.tracks_selected_labels = None

        self.midi_setup()
        self.draw_filtered_sequence()

        self.tutor = Tutor(self)
        self.tutor.start()
        self.tutor.finished.connect(self.end_of_song)

        return None

    def end_of_song(self):

        self.live_settings['play'] = False
        self.toolButton_play.setText("Play")

        return None

    #---------------------------------------------------------------------------
    # File Input

    def upload_file(self):
        # This function allows the user to upload a file for file conversions

        upload_file_path = self.open_filename_dialog_user_input("Select Audio File", "All Supported Files (*.mid *.mp3 *.pdf);;All Files (*.*);;MIDI Files(*.mid);;MP3 Files(*.mp3);;PDF Files (*.pdf)")

        if upload_file_path:

            print("UPLOAD FILE LOCATION: {0}".format(upload_file_path))

            self.file_container.clean_temp_folder()
            self.file_container.remove_all()
            self.file_container.original_file = upload_file_path
            self.file_container.add_file_type(upload_file_path)

            if is_mid(upload_file_path):

                self.spinBox_speed.setValue(100)
                self.spinBox_transpose.setValue(0)
                self.transpose_tracker = 0
                self.comboBox_tutoring_mode.setCurrentText("Beginner")
                self.comboBox_hand_skill.setCurrentText("Both")

                self.midi_file_path = upload_file_path
                #self.midi_setup()
                self.setup_tutor()

        return None

    def open_filename_dialog_user_input(self, title, supported_files):
        # This file dialog is used to obtain the file location of the .mid, .mp3,
        # and .pdf file.


        #fileName, _ = QFileDialog.getOpenFileName(caption = "Select Audio File", filter = "All Supported Files (*.mid *.mp3 *.pdf);;All Files (*.*);;MIDI Files(*.mid);;MP3 Files(*.mp3);;PDF Files (*.pdf)")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, title, "", supported_files, options=options)

        if fileName:
            file_dialog_output = str(fileName)
        else:
            return ""

        file_dialog_output = file_dialog_output.replace('/' , '\\' )
        return file_dialog_output

    def open_directory_dialog_user_input(self):
        # This file dialog is used to obtain the folder directory of the desired
        # save location for the generated files

        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        options |= QFileDialog.DontUseNativeDialog
        #directory = QFileDialog.getExistingDirectory(self, caption = 'Open a folder', directory = skore_path, options = options)
        directory = QFileDialog.getExistingDirectory(self, caption = 'Open a folder', options = options)

        if directory:
            file_dialog_output = str(directory)
        else:
            return ""

        file_dialog_output = file_dialog_output.replace('/' , '\\' )
        return file_dialog_output

    def save_generated_files(self):
        # This functions saves all the files generated by the user. Effectively
        # it relocates all the files found temp to the user's choice of directory

        if len(self.file_container.file_path) >= 2:
            filename = os.path.splitext(os.path.basename(self.file_container.original_file))[0]
            user_given_filename, okPressed = QInputDialog.getText(self, "Save Files","Files Group Name:", QLineEdit.Normal, filename)

            if okPressed:
                save_folder_path = self.open_directory_dialog_user_input()
                print("SAVE FOLDER LOCATION: {0}".format(save_folder_path))

                if user_given_filename == '' or save_folder_path == '':
                    QMessageBox.about(self, "Invalid Information",  "Please enter a valid filename or/and save folder path")
                    return None

                # Obtaining mid file location
                self.file_container.temp_to_folder(save_folder_path, user_given_filename)

        else:
            QMessageBox.about(self, "No Conversion Present", "Please upload and convert a file before saving it.")

        return None

    #--------------------------------------------------------------------------
    # Midi Handling

    def midi_setup(self):
        # This fuction deletes pre-existing MIDI files and places the new desired MIDI
        # file into the cwd of tutor.py . Then it converts the midi information
        # of that file into a sequence of note events.

        # Mido Method
        self.original_sequence = []
        self.filtered_sequence = []
        self.midi_file = MidiFile(self.midi_file_path)
        self.midi_file.tick_divider = 1

        #print("Ticks per beat: ", self.midi_file.ticks_per_beat)
        #print("CURRENT TASK: MIDI SETUP")

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

        return True

    def track_identification(self):

        #self.midi_file.tempo = None

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
                # setup track
                self.midi_file.tracks[i].track_type = "setup_track"
                self.setup_tracks.append(self.midi_file.tracks[i])
            else:
                self.midi_file.tracks[i].track_type = 'note_track'
                self.midi_file.tracks[i].played = False
                self.note_tracks.append(self.midi_file.tracks[i])

        return None

    def track_selection(self):

        #print("Note tracks: ", self.note_tracks)

        if self.tracks_selected_labels is None:
            # Setup and first note event track for original setup
            #print("Setup track: ", self.note_tracks[0])
            self.staged_track = merge_tracks([self.note_tracks[0]] + self.setup_tracks)
            self.note_tracks[0].played = True

        else:
            self.tracks_selected = []

            for track in self.note_tracks:
                track.played = self.tracks_selected_labels[track.name]
                if track.played is True:
                    self.tracks_selected.append(track)

            self.staged_track = merge_tracks(self.tracks_selected + self.setup_tracks)

        #print("Staged Track", self.staged_track)

        return None

    def calculate_tick_divider(self):

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

            if msg.type == 'note_on':
                if msg.note > highest_note or msg.note < lowest_note:
                    continue
                self.original_sequence.append(SkoreMidiEvent(None, round(msg.time / self.midi_file.tick_divider)))
                self.original_sequence.append(SkoreMidiEvent(True, msg.note))
            elif msg.type == 'note_off':
                if msg.note > highest_note or msg.note < lowest_note:
                    continue
                self.original_sequence.append(SkoreMidiEvent(None, round(msg.time / self.midi_file.tick_divider)))
                self.original_sequence.append(SkoreMidiEvent(False, msg.note))

            if msg.is_meta:
                self.original_sequence.append(SkoreMetaEvent(msg.type, msg))

        return None

    def sequence_filtering(self):

        final_index = -1

        for i in range(len(self.original_sequence)):

            #-------------------------------------------------------------------
            # Meta Event Detection
            #print(self.original_sequence[i])

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

            #self.filtered_sequence.append([note_array, sec_delay])
            self.filtered_sequence.append([note_array, delta_time])

        return None

    def midi_report(self):

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

    def set_tick_per_frame(self):

        # 60 fps = 16ms, 1fps = a number of ticks
        frame_per_sec = 1000/(globals.CLOCK_DELAY)

        sec_per_tick = tick2second(1, self.midi_file.ticks_per_beat, self.tempo) / (self.midi_file.tick_divider * 2)
        sec_per_tick = sec_per_tick * 100/self.live_settings['speed']

        self.tick_per_frame = (1/sec_per_tick) * (1/frame_per_sec)
        #print("sec_per_tick: {0}\nframe_per_sec: {1}\ntick_per_frame: {2}".format(sec_per_tick, frame_per_sec, tick_per_frame))

        return None

    def play_midi_file(self):

        if self.tutor_enable is True:
            print("play midi file")

            for msg in self.midi_file.play():
                print(msg)
                self.midi_out.send_message(msg.bytes())

                #if msg.type == 'note_on' or msg.type == 'note_off':
                    #self.arduino_comm(msg.note, 'toggle')

            print("Finished")

        else:
            print("No midi file found")

        return None

    #---------------------------------------------------------------------------
    # Track Management

    def open_track_manager_dialog(self):

        if self.tutor_enable is True:
            print("Open track_manager")
            self.track_manager = TrackManagerDialog(self.note_tracks)
            self.track_manager.finished_and_transmit_data_signal.connect(self.end_track_manager_dialog)
            self.track_manager.setModal(True)
            self.track_manager.show()

        return None

    @pyqtSlot('QString')
    def end_track_manager_dialog(self, tracks_selected_labels):

        print("Accepted")
        print("tracks_selected_labels: ", tracks_selected_labels)

        self.tracks_selected_labels = ast.literal_eval(tracks_selected_labels)

        self.tutor.terminate()
        self.live_settings['play'] = False
        self.toolButton_play.setText("Play")

        for event in self.drawn_notes_group:
            if event == ['META']:
                continue
            for note in event:
                self.scene.removeItem(note)
                del note

        self.original_sequence = []
        self.filtered_sequence = []

        # Graphics
        self.drawn_notes_group = []

        self.track_selection()
        self.calculate_tick_divider()
        self.stage_track_to_sequence()
        self.sequence_filtering()
        self.midi_report()

        # Setting default tempo
        self.tempo = 500000
        self.set_tick_per_frame()

        self.draw_filtered_sequence()

        self.tutor = Tutor(self)
        self.tutor.start()
        self.tutor.finished.connect(self.end_of_song)

        return None

    #---------------------------------------------------------------------------
    # File Conversion

    def generate_midi_file(self):
        # This functions converts the file uploaded to .mid. It checkes if the
        # user has actually uploaded a file and if the conversion is valid.

        if self.file_container.is_empty() is not True:
            if self.file_container.has_midi_file() is True:
                QMessageBox.about(self, "Invalid/Unnecessary Conversion", "Cannot convert .mid to .mid or already present .mid file in output directory")
                return

            # Obtaining mid file location
            self.file_container.input_to_mid()
            self.midi_file_path = self.file_container.file_path['.mid']
            self.setup_tutor()

        else:
            #QMessageBox.about(MainWindow, "File Needed", "Please upload a file before taking an action")
            QMessageBox.about(self, "File Needed", "Please upload a file before taking an action")

        return None

    def generate_pdf_file(self):

        if self.file_container.is_empty() is not True:
            if self.file_container.has_pdf_file() is True:
                QMessageBox.about(self, "Invalid/Unnecessary Conversion", "Cannot convert .pdf to .pdf or already present .pdf file in output directory")
                return

            else:
                # Obtaining mid file location
                self.file_container.input_to_pdf()

        else:
            print("No file uploaded")
            QMessageBox.about(self, "File Needed", "Please upload a file before taking an action.")
        return

    #---------------------------------------------------------------------------
    # Settings Functions

    def open_settings_dialog(self):

        self.config_dialog = ConfigDialog()
        self.config_dialog.finish_apply_signal.connect(self.settings_dialog_change)
        self.config_dialog.setModal(True)
        self.config_dialog.show()

        return None

    def settings_dialog_change(self):

        print("SETTINGS UPDATE: CHANGES APPLIED")
        self.setup_comm()
        self.restart()

        return None

    #---------------------------------------------------------------------------

    def skore_recorder(self):

        try:
            self.recorder_handler = RecorderMidiHandler(self)
            self.midi_in.set_callback(self.recorder_handler)
        except AttributeError:
            QMessageBox.about(self, "No MIDI device paired to SKORE", "Please connect a MIDI device and update the settings before recording.")
            return None

        self.recorder_dialog = RecorderDialog(self)
        self.recorder_dialog.finished.connect(self.end_skore_recorder)
        self.recorder_dialog.setModal(True)
        self.recorder_dialog.show()

        return None

    def end_skore_recorder(self):

        try:
            self.midi_in.set_callback(self.tutor_midi_handler)
            #self.midi_in.set_callback(TutorMidiHandler(self))
        except AttributeError:
            print("Returning TutorMidiHandler to midi_in.set_callback failed!")

        print("Return from recorder_dialog")
        del self.recorder_dialog

        return None

    #---------------------------------------------------------------------------
    # Misc Functions

    def open_skore_website(self):
        webbrowser.open('https://mrcodingrobot.github.io/SKORE/')
        return None

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.toolButton_restart.setText(_translate("MainWindow", "Restart"))
        self.toolButton_play.setText(_translate("MainWindow", "Play"))
        self.toolButton_track_manager.setText(_translate("MainWindow", "Track Manager"))
        self.label_speed.setText(_translate("MainWindow", "Speed:"))
        self.label_transpose.setText(_translate("MainWindow", "Transpose:"))
        self.label_tutoring_mode.setText(_translate("MainWindow", "Tutoring Mode:"))
        self.label_hand_skill.setText(_translate("MainWindow", "Hand Skill:"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionOpenFile.setText(_translate("MainWindow", "Open File..."))
        self.actionRecord.setText(_translate("MainWindow", "Record "))

        # Troubleshooting
        self.actionPlay.setText(_translate("MainWindow", "Play MIDI"))

        self.actionCreate_MIDI.setText(_translate("MainWindow", "Create MIDI"))
        self.actionCreate_PDF.setText(_translate("MainWindow", "Create PDF"))
        self.actionSave_File.setText(_translate("MainWindow", "Save Files..."))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionConfig.setText(_translate("MainWindow", "Config..."))
        #self.actionTrackManager.setText(_translate("MainWindow", "Track Manager"))
        self.actionWebsite.setText(_translate("MainWindow", "Website"))
        self.actionAbout.setText(_translate("MainWindow", "About"))

#-------------------------------------------------------------------------------
# Main Code

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    theme_list = QStyleFactory.keys()
    app.setStyle(QStyleFactory.create(theme_list[2])) #Fusion

    window = SkoreWindow()
    window.show()
    sys.exit(app.exec_())
