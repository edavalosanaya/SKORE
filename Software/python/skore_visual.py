# General Utility
import win32api
import win32con
import psutil
import time
import inspect
import pywinauto
import sys
from pywinauto.controls.win32_controls import ButtonWrapper
from time import sleep
import os
import difflib
import math

# PYQT5, GUI Library
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Tutor Application
from midi import read_midifile, NoteEvent, NoteOffEvent, MetaEvent
from mido import tick2second
import serial
import serial.tools.list_ports
import glob
from ctypes import windll
import rtmidi
from shutil import copyfile

# This is to prevent an error caused when importing skore_lib
import warnings
warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2

# SKORE Library
from skore_lib import FileContainer, GuiManipulator, setting_read, is_mid, is_mp3, is_pdf, rect_to_int
from settings_dialog import SettingsDialog

#-------------------------------------------------------------------------------
# Constants

TUTOR_THREAD_DELAY = 0.1

KEYBOARD_SHIFT = 28 # 48, 36
COMM_TIMEOUT = 30
HANDSHAKE_DELAY = 0.001

CHORD_TICK_TOLERANCE = int(setting_read('chord_tick_tolerance'))
DELAY_EARLY_TOLERANCE = int(setting_read('delay_early_tolerance')) #35 # < 40, > 25, > 30, > 35, < 37, < 36
DELAY_LATE_TOLERANCE = int(setting_read('delay_late_tolerance'))
CHORD_SUM_TOLERANCE = 25

CLOCK_DELAY = 16

MIDDLE_C = 60

NOTE_NAME_TO_Y_LOCATION = {
    # Bass Clef
    "A0":330, "B0":320, "C1":310, "D1":300, "E1":290, "F1":280, "G1":270,
    "A1":260, "B1":250, "C2":240, "D2":230, "E2":220, "F2":210, "G2":200,
    "A2":190, "B2":180, "C3":170, "D3":160, "E3":150, "F3":140, "G3":130,
    "A3":120, "B3":110,
    # Treble Clef
    "C4":-180, "D4":-190, "E4":-200, "F4":-210, "G4": -220,
    "A4":-230, "B4":-240, "C5":-250, "D5":-260, "E5":-270, "F5":-280, "G5":-290,
    "A5":-300, "B5":-310, "C6":-320, "D6":-330, "E6":-340, "F6":-350, "G6":-360,
    "A6":-370, "B6":-380, "C7":-390, "D7":-400, "E7":-410, "F7":-420, "G7":-430,
    "A7":-440, "B7":-450, "C8":-460
}
# The highest note in 88 keyboard is C8

NOTE_PITCH_TO_NOTE_NAME = {
    21:"A0",22:"A0,B0",23:"B0",24:"C1",25:"C1,D1",26:"D1",27:"C1,D1",28:"E1",29:"F1",30:"F1,G1",31:"G1",32:"G1,A1",
    33:"A1",34:"A1,B1",35:"B1",36:"C2",37:"C2,D2",38:"D2",39:"D2,E2",40:"E2",41:"F2",42:"F2,G2",43:"G2",44:"G2,A2",
    45:"A2",46:"A2,B2",47:"B2",48:"C3",49:"C3,D3",50:"D3",51:"D3,E3",52:"E3",53:"F3",54:"F3,G3",55:"G3",56:"G3,A3",
    57:"A3",58:"A3,B3",59:"B3",60:"C4",61:"C4,D4",62:"D4",63:"D4,E4",64:"E4",65:"F4",66:"F4,G4",67:"G4",68:"G4,A4",
    69:"A4",70:"A4,B4",71:"B4",72:"C5",73:"C5,D5",74:"D5",75:"D5,E5",76:"E5",77:"F5",78:"F5,G5",79:"G5",80:"G5,A5",
    81:"A5",82:"A5,B5",83:"B5",84:"C6",85:"C6,D6",86:"D6",87:"D6,E6",88:"E6",89:"F6",90:"F6,G6",91:"G6",92:"G6,A6",
    93:"A6",94:"A6,B6",95:"B6",96:"D6",97:"C7,C7",98:"D7",99:"D7,E7",100:'E7',101:'F7',102:'F7,G7',103:'G7',104:"G7,A7",
    105:"A7",106:"A7,B7",107:"B7",108:"C8"
}

LEFT_TICK_SHIFT = -400
TIMING_NOTE_BOX = None
TIMING_NOTE_LINE = None
TIMING_NOTE_LINE_CATCH = None
VISIBLE_NOTE_BOX = None
GRAPHICS_CONTROLLER = None

BOTTOM_STAFF_LINE_Y_LOCATION = NOTE_NAME_TO_Y_LOCATION["G2"]
TOP_STAFF_LINE_Y_LOCATION = NOTE_NAME_TO_Y_LOCATION["F5"]

HIDDEN = 0.01
VISIBLE = 1

#keyboard_state index
NEUTRAL = 0
RIGHT = 1
WRONG = 2
TARGET = 4
ARDUINO = 5
#RIGHT_VISIBLE = 6
PREV_TARGET = 6

PIXMAPS = [[],[],[]]
GREEN = 0
YELLOW = 1
CYAN = 2

NOTE = 0
SHARP = 1
FLAT = 2
NATURAL = 3

# for only GraphicsNote
LIVE_SETTINGS = None


#-------------------------------------------------------------------------------
# Useful Function

#-------------------------------------------------------------------------------
# Classes

class MidiEvent:

    def __init__(self, event_type, event_data):
        self.event_type = event_type
        self.data = event_data

        return None

    def __repr__(self):
        return "({0}, {1})".format(self.event_type, self.data)

class MidiInputHandler(object):

    def __init__(self, port, gui):
        self.port = port
        self.gui = gui
        self.notes_drawn = {}

    def __call__(self, event, data=None):
        #print("{0} - {1} - {2}".format(self.port, message, delta_time))
        message, delta_time = event
        note_pitch = message[1]

        if self.gui.tutor_enable is True:


            if message[0] == 0x90 and message[2] != 0: # Note ON Event
                if note_pitch in self.gui.keyboard_state[TARGET]:
                    if note_pitch not in self.gui.keyboard_state[RIGHT]:
                        self.gui.keyboard_state[RIGHT].append(note_pitch)

                        note_name = NOTE_PITCH_TO_NOTE_NAME[note_pitch][:2]
                        self.gui.note_labels[RIGHT][note_name].setOpacity(VISIBLE)
                        self.gui.note_name_labels[note_name].setOpacity(VISIBLE)

                else:
                    if note_pitch not in self.gui.keyboard_state[WRONG]:
                        self.gui.keyboard_state[WRONG].append(note_pitch)

                        note_name = NOTE_PITCH_TO_NOTE_NAME[note_pitch][:2]
                        self.gui.note_labels[WRONG][note_name].setOpacity(VISIBLE)
                        self.gui.note_name_labels[note_name].setOpacity(VISIBLE)


            else: # Note OFF Event
                if note_pitch in self.gui.keyboard_state[RIGHT]:
                    self.gui.keyboard_state[RIGHT].remove(note_pitch)

                    note_name = NOTE_PITCH_TO_NOTE_NAME[note_pitch][:2]
                    self.gui.note_labels[RIGHT][note_name].setOpacity(HIDDEN)
                    self.gui.note_name_labels[note_name].setOpacity(HIDDEN)


                elif note_pitch in self.gui.keyboard_state[WRONG]:
                    self.gui.keyboard_state[WRONG].remove(note_pitch)

                    note_name = NOTE_PITCH_TO_NOTE_NAME[note_pitch][:2]
                    self.gui.note_labels[WRONG][note_name].setOpacity(HIDDEN)
                    self.gui.note_name_labels[note_name].setOpacity(HIDDEN)


            """
            if message[0] == 0x90 and message[2] != 0: # Note ON Event
                if note_pitch in self.gui.keyboard_state[TARGET]:
                    if note_pitch not in self.gui.keyboard_state[RIGHT_VISIBLE]:
                        self.gui.keyboard_state[RIGHT_VISIBLE].append(note_pitch)
                        self.gui.keyboard_state[RIGHT].append(note_pitch)

                        note_name = NOTE_PITCH_TO_NOTE_NAME[note_pitch][:2]
                        self.gui.note_labels[RIGHT][note_name].setOpacity(VISIBLE)
                        self.gui.note_name_labels[note_name].setOpacity(VISIBLE)

                else:
                    if note_pitch not in self.gui.keyboard_state[WRONG]:
                        self.gui.keyboard_state[WRONG].append(note_pitch)

                        note_name = NOTE_PITCH_TO_NOTE_NAME[note_pitch][:2]
                        self.gui.note_labels[WRONG][note_name].setOpacity(VISIBLE)
                        self.gui.note_name_labels[note_name].setOpacity(VISIBLE)


            else: # Note OFF Event
                if note_pitch in self.gui.keyboard_state[RIGHT_VISIBLE]:
                    self.gui.keyboard_state[RIGHT_VISIBLE].remove(note_pitch)
                    if note_pitch in self.gui.keyboard_state[RIGHT]:
                        self.gui.keyboard_state[RIGHT].remove(note_pitch)

                    note_name = NOTE_PITCH_TO_NOTE_NAME[note_pitch][:2]
                    self.gui.note_labels[RIGHT][note_name].setOpacity(HIDDEN)
                    self.gui.note_name_labels[note_name].setOpacity(HIDDEN)

                elif note_pitch in self.gui.keyboard_state[WRONG]:
                    self.gui.keyboard_state[WRONG].remove(note_pitch)

                    note_name = NOTE_PITCH_TO_NOTE_NAME[note_pitch][:2]
                    self.gui.note_labels[WRONG][note_name].setOpacity(HIDDEN)
                    self.gui.note_name_labels[note_name].setOpacity(HIDDEN)

            """


        else:

            if message[0] == 0x90 and message[2] != 0: # Note ON Event
                if note_pitch not in self.gui.keyboard_state[NEUTRAL]:
                    self.gui.keyboard_state[NEUTRAL].append(note_pitch)

                    note_name = NOTE_PITCH_TO_NOTE_NAME[note_pitch][:2]
                    self.gui.note_labels[NEUTRAL][note_name].setOpacity(VISIBLE)
                    self.gui.note_name_labels[note_name].setOpacity(VISIBLE)

            else: # Note OFF Event
                if note_pitch in self.gui.keyboard_state[NEUTRAL]:
                    self.gui.keyboard_state[NEUTRAL].remove(note_pitch)

                    note_name = NOTE_PITCH_TO_NOTE_NAME[note_pitch][:2]
                    self.gui.note_labels[NEUTRAL][note_name].setOpacity(HIDDEN)
                    self.gui.note_name_labels[note_name].setOpacity(HIDDEN)

        #print("Current Keyboard State: {0}".format(self.gui.current_keyboard_state))

        return None

class GraphicsPlayedLabel(QGraphicsItem):

    def __init__(self, note, correct = None):
        super(GraphicsPlayedLabel, self).__init__()

        self.x = -510
        self.width = 20
        self.height = 5
        self.correct = correct

        if type(note) is int:
            note_name = NOTE_PITCH_TO_NOTE_NAME[note]

            if ',' in note_name:
                #print("flat/sharp note detected")
                #pritn("for now, always flats")
                note_name = note_name[:2]

            self.note_name = note_name
            self.y = NOTE_NAME_TO_Y_LOCATION[note_name]

        elif type(note) is str:

            self.note_name = note
            self.y = NOTE_NAME_TO_Y_LOCATION[note]

        return None

    def paint(self, painter, option, widget):

        if self.correct is True:
            painter.setBrush(QColor(0,255,255))
        elif self.correct is None:
            painter.setBrush(QColor(255,255,0))
        else:
            painter.setBrush(QColor(255,0,0))

        painter.drawRect(round(self.x - self.width/2), round(self.y - self.height/2), self.width, self.height)

        return None

    def boundingRect(self):
        return QRectF(self.x, self.y, self.width, self.height)

class GraphicsPlayedNameLabel(QGraphicsItem):

    def __init__(self, note):
        super(GraphicsPlayedNameLabel, self).__init__()

        self.x = -530
        self.width = 20
        self.height = 20

        if type(note) is int:
            note_name = NOTE_PITCH_TO_NOTE_NAME[note]

            if ',' in note_name:
                #print("flat/sharp note detected")
                #pritn("for now, always flats")
                note_name = note_name[:2]

            self.note_name = note_name
            self.y = NOTE_NAME_TO_Y_LOCATION[note_name]

        elif type(note) is str:

            self.note_name = note
            self.y = NOTE_NAME_TO_Y_LOCATION[note]

        return None

    def paint(self, painter, option, widget):

        painter.setPen(Qt.white)
        painter.drawText(round(self.x - self.width/2), round(self.y - self.height/2), self.width, self.height, 0, self.note_name)
        return None

    def boundingRect(self):
        return QRectF(self.x, self.y, self.width, self.height)

class GraphicsController(QGraphicsObject):

    stop_signal = QtCore.pyqtSignal()

    def __init__(self):
        super(GraphicsController, self).__init__()

class GraphicsNote(QGraphicsItem):

    def __init__(self, note, x = 0):
        super(GraphicsNote, self).__init__()

        self.xr = 8
        self.yr = 8
        self.x = x
        self.h_speed = 0
        self.played = False
        self.should_be_played_now = False
        self.top_note = False
        self.shaded = False

        self.set_note_pitch(note)

        return None

    def __repr__(self):

        return str(self.note_name)

    def set_speed(self, h_speed = None):
        if h_speed is not None:
            self.h_speed = h_speed

    def set_note_pitch(self, note):

        #-----------------------------------------------------------------------
        # Determining the note's y value
        self.sharp_flat = False

        if type(note) is int:
            self.note_pitch = note
            note_name = NOTE_PITCH_TO_NOTE_NAME[note]

            if ',' in note_name:
                #print("Sharp/Flat detected!")
                #print("Original note name: ", note_name)
                self.sharp_flat = True
                note_name = note_name[:2]

            self.note_name = note_name
            self.y = NOTE_NAME_TO_Y_LOCATION[note_name]

        elif type(note) is str:

            self.note_name = note
            self.y = NOTE_NAME_TO_Y_LOCATION[note]

        #print("Pitch: {2}\tNote: {0}\t Y: {1}".format(self.note_name, self.y, self.note_pitch))

        return None

    def stop(self):
        self.h_speed = 0

    def painter_move(self):
        self.x = round(self.x - self.h_speed)
        return None

    def paint(self, painter, option, widget):

        # Beginner Mode Halting
        if LIVE_SETTINGS['mode'] == 'Beginner' and TIMING_NOTE_LINE_CATCH.contains(QPointF(self.x, self.y)) and self.h_speed != 0 and self.played is False:
            #print("Stop signal emit")
            GRAPHICS_CONTROLLER.stop_signal.emit()

        #-----------------------------------------------------------------------
        # Hiding the note if not withing the visible notes box

        #should_be_visible = VISIBLE_NOTE_BOX.contains(QPointF(self.x, self.y))
        #if should_be_visible is True:
        if VISIBLE_NOTE_BOX.contains(QPointF(self.x, self.y)) is True:
            self.setOpacity(1)
            self.visible = True
        else:
            self.setOpacity(HIDDEN)
            self.visible = False

        #-----------------------------------------------------------------------
        # Hand Skill Effects

        if self.shaded is True:
            self.setOpacity(0.4)

        #-----------------------------------------------------------------------
        # Changing color the notes if within the timing notes box

        should_change_color = TIMING_NOTE_BOX.contains(QPointF(self.x, self.y))

        if self.played is True:
            color = CYAN
            ledger_pen_color = QColor(0,255,255)

        elif should_change_color is True:
            color = YELLOW
            self.should_be_played_now = True
            ledger_pen_color = Qt.yellow
        else:
            color = GREEN
            self.should_be_played_now = False
            ledger_pen_color = Qt.green

        self.painter_move()
        painter.drawPixmap(self.x - 7, self.y - 9, PIXMAPS[color][NOTE])

        if self.sharp_flat is True:
            # Flat
            #painter.drawPixmap(self.x - 25, self.y - 25, PIXMAPS[color][FLAT])
            # Sharp
            painter.drawPixmap(self.x - 30, self.y - 23, PIXMAPS[color][SHARP])
            # Natural
            #painter.drawPixmap(self.x - 37, self.y - 23, PIXMAPS[color][NATURAL])

        #-----------------------------------------------------------------------
        # Ledger lines
        painter.setPen(ledger_pen_color)

        # Top Ledger lines
        if self.y < TOP_STAFF_LINE_Y_LOCATION - 20:
            temp_y = TOP_STAFF_LINE_Y_LOCATION - 20
            while temp_y >= self.y:
                painter.drawLine(self.x - 20, temp_y, self.x + 20, temp_y)
                temp_y -= 20

        # Bottom Ledger Lines
        elif self.y > BOTTOM_STAFF_LINE_Y_LOCATION + 20:
            temp_y = BOTTOM_STAFF_LINE_Y_LOCATION + 20
            while temp_y <= self.y:
                painter.drawLine(self.x - 20, temp_y, self.x + 20, temp_y)
                temp_y += 20

        elif self.note_name == "C4":
            painter.drawLine(self.x - 20, self.y, self.x + 20, self.y)

        #-----------------------------------------------------------------------
        # Note label

        if self.top_note is True:
            painter.setPen(Qt.white)
            w = 20
            h = 20
            painter.drawText(self.x - 5, self.y - 25, w, h, 0, self.note_name)

        return None

    def boundingRect(self):
        return QRectF(-self.xr, -self.xr, 2*self.xr, 2*self.xr)

class RedDotThread(QThread):
    # This thread checks and determines the address given for the midi file
    # recorded by Red Dot Forever. It successfully changes the upload_file
    # variable and other necessary changes to account for any changes.

    red_dot_signal = QtCore.pyqtSignal('QString','QString')

    def __init__(self):
        QThread.__init__(self)

    def run(self):

        address_list = []
        filename_list = []
        s_handle = []

        red_app = pywinauto.application.Application()
        red_app_exe_path = setting_read('red_app_exe_path')
        red_app.start(red_app_exe_path)
        print("Initialized Red Dot Forever")

        while(True):
            try:
                w_handle = pywinauto.findwindows.find_windows(title="Red Dot Forever")[0]
                window = red_app.window(handle=w_handle)
                break
            except IndexError:
                time.sleep(0.2)


        while(True):
            try:
                s_handle = pywinauto.findwindows.find_windows(parent=w_handle)[0]
                s_window = red_app.window(handle=s_handle)
            except IndexError:
                s_handle = []

            if s_handle != []:
                toolbarwindow = s_window.Toolbar4
                edit = s_window.Edit
                while(True):
                    try:
                        address_list = toolbarwindow.texts()
                        filename_list = edit.texts()
                    except:
                        break

            # Checking if the Red Dot Forever application is running
            processes = [p.name() for p in psutil.process_iter()]

            for process in processes:
                if process == 'reddot.exe':
                    # Red Dot Forever is running
                    break

            if process != 'reddot.exe':
                print("Red Dot Forever Closed")
                break

        if address_list == [] or filename_list == []:
            return

        print("Final Data")
        print("Address: " + str(address_list))
        print("File Name: " + str(filename_list))

        address_string = ''
        filename_string = ''

        for item in address_list:
            address_string += item + ';'

        address_string = address_string[:-1]

        for item in filename_list:
            filename_string += item + ';'

        filename_string = filename_string[:-1]
        self.red_dot_signal.emit(address_string,filename_string)

        return None

class Tutor(QThread):

    def __init__(self, gui):
        QThread.__init__(self)
        self.gui = gui

        return None

    def keyboard_valid(self):
        # This functions follows the confirmation system of PianoBooster
        # which determines if the keys pressed are acceptable compared to the
        # target keyboard configuration
        if self.gui.keyboard_state[TARGET] == []:
            return True

        if len(set(self.gui.keyboard_state[TARGET]).symmetric_difference(self.gui.keyboard_state[RIGHT])) != 0:
            return False

        if len(self.gui.keyboard_state[WRONG]) >= 2:
            return False

        return True

    def target_keyboard_in_timing_box(self, event_graphic_notes):

        test_note = event_graphic_notes[0]
        if test_note.should_be_played_now is True:
            return True

        return False

    def tutor(self):

        self.gui.keyboard_state[RIGHT] = []
        self.gui.keyboard_state[WRONG] = []
        self.gui.keyboard_state[ARDUINO] = []
        #self.gui.keyboard_state[PREV_TARGET] = []

        for self.sequence_pointer in range(len(self.gui.filtered_sequence)):

            #print("Pointer: {0}\nFiltered_Sequence: {1}\n".format(self.sequence_pointer, self.gui.filtered_sequence))

            self.gui.keyboard_state[TARGET] = self.gui.filtered_sequence[self.sequence_pointer][0]
            self.gui.arduino_comm(self.gui.keyboard_state[TARGET])
            print("Target: ", self.gui.keyboard_state[TARGET])

            #-------------------------------------------------------------------
            # Hand Skill Effect
            if self.gui.live_settings['hand'] != "Both":
                if self.gui.live_settings['hand'] == 'Right Hand':
                    self.gui.keyboard_state[TARGET] = [pitch for pitch in self.gui.keyboard_state[TARGET] if pitch >= MIDDLE_C]
                else:
                    self.gui.keyboard_state[TARGET] = [pitch for pitch in self.gui.keyboard_state[TARGET] if pitch < MIDDLE_C]

            #-------------------------------------------------------------------
            # PREV_TARGET and TARGET Matching delay
            if set(self.gui.keyboard_state[TARGET]).symmetric_difference(set(self.gui.keyboard_state[PREV_TARGET])) == set():
                self.gui.keyboard_state[RIGHT].sort()
                temp_right = self.gui.keyboard_state[RIGHT]
                print("waiting for keyboard_state[RIGHT] to change")
                while self.gui.keyboard_state[RIGHT] == temp_right:
                    print("waiting for change") # Aren't we all
                    if temp_right == []:
                        break
                    time.sleep(TUTOR_THREAD_DELAY)
                print("keyboard_state[RIGHT] change detected")

            #-------------------------------------------------------------------
            # Tutoring Mode Change
            while True:
                if self.gui.live_settings['mode'] == "Beginner":
                    go_to_next_note = self.beginner()
                elif self.gui.live_settings['mode'] == "Intermediate":
                    go_to_next_note = self.intermediate()
                else:
                    go_to_next_note =  self.expert()
                if go_to_next_note is True:
                    break

            self.gui.keyboard_state[PREV_TARGET] = self.gui.keyboard_state[TARGET]

        #-----------------------------------------------------------------------
        # End of Song process
        drawn_note = [note for array in self.gui.drawn_notes_group for note in array]
        visible_notes = [note.visible for note in drawn_note]

        while True in visible_notes:
            time.sleep(TUTOR_THREAD_DELAY)
            visible_notes = [note.visible for note in drawn_note]

        print("End of Song")
        self.gui.stop_all_notes()

        return None

    def beginner(self):

        while True:
            if self.gui.live_settings['mode'] != 'Beginner':
                return False

            event_graphic_notes = self.gui.drawn_notes_group[self.sequence_pointer]
            if self.keyboard_valid() is True and self.target_keyboard_in_timing_box(event_graphic_notes):
                for note in event_graphic_notes:
                    note.played = True

                self.gui.move_all_notes()
                return True

            time.sleep(TUTOR_THREAD_DELAY)

        return None

    def intermediate(self):

        while True:
            if self.gui.live_settings['mode'] != 'Intermediate':
                return False

            event_graphic_notes = self.gui.drawn_notes_group[self.sequence_pointer]
            if self.target_keyboard_in_timing_box(event_graphic_notes):

                played_notes = [note for note in event_graphic_notes if note.note_pitch in self.gui.keyboard_state[RIGHT]]
                for note in played_notes:
                    note.played = True

                self.gui.move_all_notes()
                return True

            time.sleep(TUTOR_THREAD_DELAY)



        return None

    def expert(self):

        return None

    def run(self):

        while self.gui.live_settings['play'] == False:
            time.sleep(TUTOR_THREAD_DELAY)

        self.tutor()

        return None

class SkoreWindow(QMainWindow):

    def __init__(self):

        global LIVE_SETTINGS

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
        self.keyboard_state = [[],[],[],[],[],[],[]]

        # Setup functions
        #self.setup_ui()
        self.setup_ui2()
        self.setup_graphics_background()
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

        LIVE_SETTINGS = self.live_settings

        # Timer Setup
        print("QTimer Initializing")
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.clock)
        self.timer.start(CLOCK_DELAY) # 60 FPS, 16ms, 30 FPS, 33ms

    def setup_ui(self):

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1901, 921))
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
        self.gridLayout_central.addWidget(self.graphicsView_game, 1, 1, 1, 1)

        #-----------------------------------------------------------------------
        # gridLayout_central -> horizontalLayout_live_settings
        self.horizontalLayout_live_settings = QtWidgets.QHBoxLayout()
        self.horizontalLayout_live_settings.setObjectName("horizontalLayout_live_settings")

        self.toolButton_restart = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_restart.setObjectName("toolButton_restart")
        self.horizontalLayout_live_settings.addWidget(self.toolButton_restart)

        self.toolButton_play = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_play.setObjectName("toolButton_play")
        self.horizontalLayout_live_settings.addWidget(self.toolButton_play)

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

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_live_settings.addItem(spacerItem)

        self.gridLayout_central.addLayout(self.horizontalLayout_live_settings, 0, 1, 1, 1)

        #-----------------------------------------------------------------------
        # gridLayout_central -> gridLayout_options
        self.gridLayout_options = QtWidgets.QGridLayout()
        self.gridLayout_options.setObjectName("gridLayout_options")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_options.addItem(spacerItem1, 1, 1, 1, 1)

        #-----------------------------------------------------------------------
        # gridLayout_central -> gridLayout_options -> verticalLayout_tutoring_mode
        self.verticalLayout_tutoring_mode = QtWidgets.QVBoxLayout()
        self.verticalLayout_tutoring_mode.setObjectName("verticalLayout_tutoring_mode")

        self.label_tutoring_mode = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_tutoring_mode.setObjectName("label_tutoring_mode")
        self.verticalLayout_tutoring_mode.addWidget(self.label_tutoring_mode)

        self.line_tutoring_mode = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line_tutoring_mode.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_tutoring_mode.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_tutoring_mode.setObjectName("line_tutoring_mode")
        self.verticalLayout_tutoring_mode.addWidget(self.line_tutoring_mode)

        self.radioButton_beginner = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.radioButton_beginner.setObjectName("radioButton_beginner")
        self.verticalLayout_tutoring_mode.addWidget(self.radioButton_beginner)

        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_tutoring_mode.addItem(spacerItem2)

        self.radioButton_intermediate = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.radioButton_intermediate.setObjectName("radioButton_intermediate")
        self.verticalLayout_tutoring_mode.addWidget(self.radioButton_intermediate)

        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_tutoring_mode.addItem(spacerItem3)

        self.radioButton_expert = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.radioButton_expert.setObjectName("radioButton_expert")
        self.verticalLayout_tutoring_mode.addWidget(self.radioButton_expert)

        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_tutoring_mode.addItem(spacerItem4)

        self.gridLayout_options.addLayout(self.verticalLayout_tutoring_mode, 0, 1, 1, 1)

        #-----------------------------------------------------------------------
        # gridLayout_central -> gridLayout_options -> verticalLayout_hand
        self.verticalLayout_hand = QtWidgets.QVBoxLayout()
        self.verticalLayout_hand.setObjectName("verticalLayout_hand")

        self.label_hand_skill = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_hand_skill.setObjectName("label_hand_skill")
        self.verticalLayout_hand.addWidget(self.label_hand_skill)

        self.line_hand_skill = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line_hand_skill.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_hand_skill.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_hand_skill.setObjectName("line_hand_skill")
        self.verticalLayout_hand.addWidget(self.line_hand_skill)

        self.radioButton_both = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.radioButton_both.setObjectName("radioButton_both")
        self.verticalLayout_hand.addWidget(self.radioButton_both)

        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_hand.addItem(spacerItem5)

        self.radioButton_left_hand = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.radioButton_left_hand.setObjectName("radioButton_left_hand")
        self.verticalLayout_hand.addWidget(self.radioButton_left_hand)

        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_hand.addItem(spacerItem6)

        self.radioButton_right_hand = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.radioButton_right_hand.setObjectName("radioButton_right_hand")
        self.verticalLayout_hand.addWidget(self.radioButton_right_hand)

        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_hand.addItem(spacerItem7)

        self.gridLayout_options.addLayout(self.verticalLayout_hand, 0, 2, 1, 1)
        self.gridLayout_central.addLayout(self.gridLayout_options, 1, 0, 1, 1)

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
        self.actionWebsite = QtWidgets.QAction(self)
        self.actionWebsite.setObjectName("actionWebsite")
        self.actionAbout = QtWidgets.QAction(self)
        self.actionAbout.setObjectName("actionAbout")

        #-----------------------------------------------------------------------
        # MenuFile

        self.menuFile.addAction(self.actionOpenFile)
        self.menuFile.addAction(self.actionRecord)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionCreate_MIDI)
        self.menuFile.addAction(self.actionCreate_PDF)
        self.menuFile.addAction(self.actionSave_File)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
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
        self.setTabOrder(self.spinBox_transpose, self.radioButton_beginner)
        self.setTabOrder(self.radioButton_beginner, self.radioButton_intermediate)
        self.setTabOrder(self.radioButton_intermediate, self.radioButton_expert)
        self.setTabOrder(self.radioButton_expert, self.radioButton_both)
        self.setTabOrder(self.radioButton_both, self.radioButton_left_hand)
        self.setTabOrder(self.radioButton_left_hand, self.radioButton_right_hand)
        self.setTabOrder(self.radioButton_right_hand, self.graphicsView_game)
        self.setTabOrder(self.graphicsView_game, self.spinBox_speed)

    def setup_ui2(self):

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

        self.toolButton_restart = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_restart.setObjectName("toolButton_restart")
        self.horizontalLayout_live_settings.addWidget(self.toolButton_restart)

        self.toolButton_play = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_play.setObjectName("toolButton_play")
        self.horizontalLayout_live_settings.addWidget(self.toolButton_play)

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

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_live_settings.addItem(spacerItem)

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
        self.actionWebsite = QtWidgets.QAction(self)
        self.actionWebsite.setObjectName("actionWebsite")
        self.actionAbout = QtWidgets.QAction(self)
        self.actionAbout.setObjectName("actionAbout")

        #-----------------------------------------------------------------------
        # MenuFile

        self.menuFile.addAction(self.actionOpenFile)
        self.menuFile.addAction(self.actionRecord)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionCreate_MIDI)
        self.menuFile.addAction(self.actionCreate_PDF)
        self.menuFile.addAction(self.actionSave_File)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
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
        self.actionWebsite = QtWidgets.QAction(self)
        self.actionWebsite.setObjectName("actionWebsite")
        self.actionAbout = QtWidgets.QAction(self)
        self.actionAbout.setObjectName("actionAbout")
        """
        #-----------------------------------------------------------------------
        # MenuBar Actions
        self.actionOpenFile.setShortcut('Ctrl+O')
        self.actionOpenFile.triggered.connect(self.upload_file)

        self.actionRecord.setShortcut("Ctrl+Shift+R")
        self.actionRecord.triggered.connect(self.open_red_dot_forever)

        self.actionCreate_MIDI.setShortcut("Ctrl+M")
        self.actionCreate_MIDI.triggered.connect(self.generate_midi_file)

        self.actionCreate_PDF.setShortcut("Ctrl+P")
        self.actionCreate_PDF.triggered.connect(self.generate_pdf_file)

        self.actionSave_File.setShortcut("Ctrl+S")
        self.actionSave_File.triggered.connect(self.save_generated_files)

        self.actionExit.triggered.connect(self.close)

        self.actionConfig.triggered.connect(self.open_settings_dialog)

        #-----------------------------------------------------------------------
        # Live Settings
        self.toolButton_play.clicked.connect(self.play_stop)
        self.toolButton_restart.clicked.connect(self.restart)

        self.spinBox_speed.setRange(10,400)
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

        """
        # setup_ui
        self.tutoring_mode_button_group = QButtonGroup()
        self.tutoring_mode_button_group.addButton(self.radioButton_beginner)
        self.tutoring_mode_button_group.addButton(self.radioButton_intermediate)
        self.tutoring_mode_button_group.addButton(self.radioButton_expert)
        self.tutoring_mode_button_group.setExclusive(True)
        self.radioButton_beginner.setChecked(True)

        self.hand_skill_button_group = QButtonGroup()
        self.hand_skill_button_group.addButton(self.radioButton_both)
        self.hand_skill_button_group.addButton(self.radioButton_right_hand)
        self.hand_skill_button_group.addButton(self.radioButton_left_hand)
        self.hand_skill_button_group.setExclusive(True)
        self.radioButton_both.setChecked(True)

        self.tutoring_mode_button_group.buttonClicked.connect(self.mode_change)
        self.hand_skill_button_group.buttonClicked.connect(self.hand_change)
        """
        return None

    #---------------------------------------------------------------------------
    # Communications

    def setup_comm(self):

        arduino_status = self.arduino_setup()
        piano_status = self.piano_port_setup()

        if arduino_status is True:
            print("ARDUINO COMMUNICATION SETUP SUCCESS")
        else:
            print("ARDUINO COMMUNICATION SETUP FAILURE")

        if piano_status is True:
            print("PIANO COMMUICATION SETUP SUCCESS")
        else:
            print("PIANO COMMUNICATION SETUP FAILURE")

        return False

    def arduino_handshake(self):

        return True
        #print("waiting for arduino handshake")
        timeout = time.time() + COMM_TIMEOUT
        while time.time() < timeout:
            time.sleep(HANDSHAKE_DELAY)
            read_data = self.arduino.read()
            #print(read_data)
            if read_data == b'#':
                #print("finished handshake")
                return True

        raise RuntimeError("Communication Desync with Arduino")
        return None

    def arduino_comm(self, notes):
        # This function sends the information about which notes need to be added and
        # removed from the LED Rod.

        if notes:

            notes_to_send = list(set(self.keyboard_state[TARGET]).symmetric_difference(self.keyboard_state[ARDUINO]))

        else:

            notes_to_send = self.keyboard_state[ARDUINO]

        send_string = ','.join(str(note) for note in notes_to_send) + ',#'
        print("ARDUINO MESSAGE:", send_string)
        self.arduino.write(send_string.encode('utf-8'))
        self.keyboard_state[ARDUINO] = self.keyboard_state[TARGET]

        return None

    def arduino_setup(self):
        # This functions sets up the communication between Python and the Arduino.
        # For now the Arduino is assumed to be connected to COM3.

        whitekey = []
        blackkey = []
        size_message = ''
        whitekey_transmitted_string = ''
        blackkey_transmitted_string = ''
        piano_size = setting_read('piano_size') + ','

        if piano_size == 'S,':
            size_message = '61,'
        elif piano_size == 'M,':
            size_message = '76,'
        elif piano_size == 'L,':
            size_message = '88,'
        else:
            raise RuntimeError("PIANO SIZE SELECTION NOT FOUND")

        # Closing, if applicable, the arduino port
        if self.arduino:
            self.arduino.close()
            self.arduino = []

        com_port = setting_read("arduino_port")

        try:
            self.arduino = serial.Serial(com_port, 230400, writeTimeout = COMM_TIMEOUT)
        except serial.serialutil.SerialException:
            print("ARDUINO AT {0} NOT FOUND".format(com_port))
            return False

        whitekey.append(int(setting_read('whitekey_r')))
        whitekey.append(int(setting_read('whitekey_g')))
        whitekey.append(int(setting_read('whitekey_b')))

        blackkey.append(int(setting_read('blackkey_r')))
        blackkey.append(int(setting_read('blackkey_g')))
        blackkey.append(int(setting_read('blackkey_b')))

        for data in whitekey:
            if data == 0:
                data = 1
            whitekey_transmitted_string += str(data) + ','

        for data in blackkey:
            if data == 0:
                data = 1
            blackkey_transmitted_string += str(data) + ','

        setup_transmitted_string = size_message + whitekey_transmitted_string + blackkey_transmitted_string
        setup_transmitted_string += ',#,'

        time.sleep(2)
        self.arduino.write(setup_transmitted_string.encode('utf-8'))

        print("""
--------------------------Arduino Configuration-------------------------
COM PORT: {0}
PIANO SIZE: {1}
WHITEKEY COLORS: {2}
BLACKKEY COLORS: {3}
SETUP STRING: {4}

        """.format(com_port, piano_size, whitekey_transmitted_string, blackkey_transmitted_string, setup_transmitted_string))

        if self.arduino_handshake() is True:
            return True

        else:
            print("INITIAL ARDUINO HANDSHAKE FAILED")
            return False

    def piano_port_setup(self):
        # This function sets up the communication between Python and the MIDI device
        # For now Python will connect the first listed device.

        if not self.midi_in:
            try:
                self.midi_in.close_port()
            except:
                self.midi_in = None

        #-----------------------------------------------------------------------
        # Midi In

        self.midi_in = rtmidi.MidiIn()
        in_avaliable_ports = self.midi_in.get_ports()
        selected_port = setting_read("piano_port")
        try:
            closes_match_in_port = difflib.get_close_matches(selected_port, in_avaliable_ports)[0]
        except IndexError:
            print("{0} NOT FOUND".format(selected_port))
            self.midi_in = None
            return False


        try:
            self.midi_in.open_port(in_avaliable_ports.index(closes_match_in_port))
        except:
            print("Piano Port Setup Failure")
            self.midi_in = None
            return False

        self.midi_in.set_callback(MidiInputHandler(closes_match_in_port, self))

        print("""
----------------------------Piano Configuration-------------------------
PIANO PORT: {0} (SUCCESSFUL)
PIANO PORT HANDLER SETUP (SUCCESSFUL)

        """.format(closes_match_in_port))

        return True

    #---------------------------------------------------------------------------
    # Graphics Functions

    def clock(self):
        self.scene.update()
        return None

    def setup_graphics_background(self):

        global VISIBLE_NOTE_BOX, TIMING_NOTE_BOX, TIMING_NOTE_LINE, TIMING_NOTE_LINE_CATCH
        global PIXMAPS, GRAPHICS_CONTROLLER

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
        self.visible_note_box.setOpacity(HIDDEN)

        #-----------------------------------------------------------------------
        # Setting up timing note bar
        w = 50 # tolerances of 25 on each side
        x = LEFT_TICK_SHIFT - round(w/2)
        h = 810
        y = -470

        magentaBrush = QBrush(QColor(153, 0, 153))
        magentaPen = QPen(QColor(153, 0, 153))

        self.timing_note_box = self.scene.addRect(x, y, w , h, magentaPen, magentaBrush)
        self.timing_note_box.setOpacity(0.5)

        self.timing_note_line = self.scene.addLine(LEFT_TICK_SHIFT, y, LEFT_TICK_SHIFT, h + y, magentaPen)

        #-----------------------------------------------------------------------
        # Setting up timing note line catch
        w = 25
        x = LEFT_TICK_SHIFT - round(w/2) - round(25/2) - 1
        h = 810
        y = -470

        whiteBrush = QBrush(Qt.white)
        whitePen = QPen(Qt.white)

        self.timing_note_line_catch = self.scene.addRect(x, y, w, h, whitePen, whiteBrush)
        self.timing_note_line_catch.setOpacity(HIDDEN)

        #-----------------------------------------------------------------------
        # Placing Treble and Bass Clef
        treble_clef = QPixmap(r".\images\green_treble_clef.png")
        treble_clef = treble_clef.scaledToHeight(180)

        treble_clef_pointer = self.scene.addPixmap(treble_clef)
        treble_clef_pointer.setOffset(-750, -331)

        bass_clef = QPixmap(r".\images\green_bass_clef.png")
        bass_clef = bass_clef.scaledToHeight(70)

        bass_clef_pointer = self.scene.addPixmap(bass_clef)
        bass_clef_pointer.setOffset(-720, 120)

        #-----------------------------------------------------------------------
        # Placing Note Labels
        self.note_labels = [{},{},{}]

        for note in NOTE_NAME_TO_Y_LOCATION.keys():

            self.note_labels[NEUTRAL][note] = GraphicsPlayedLabel(note, None)
            self.note_labels[NEUTRAL][note].setOpacity(HIDDEN)
            self.scene.addItem(self.note_labels[NEUTRAL][note])

            self.note_labels[RIGHT][note] = GraphicsPlayedLabel(note, True)
            self.note_labels[RIGHT][note].setOpacity(HIDDEN)
            self.scene.addItem(self.note_labels[RIGHT][note])

            self.note_labels[WRONG][note] = GraphicsPlayedLabel(note, False)
            self.note_labels[WRONG][note].setOpacity(HIDDEN)
            self.scene.addItem(self.note_labels[WRONG][note])

        #-----------------------------------------------------------------------
        # Placing Note Label Names
        self.note_name_labels = {}

        for note in NOTE_NAME_TO_Y_LOCATION.keys():

            self.note_name_labels[note] = GraphicsPlayedNameLabel(note)
            self.note_name_labels[note].setOpacity(HIDDEN)
            self.scene.addItem(self.note_name_labels[note])

        #-----------------------------------------------------------------------
        # Setup Graphics Controller

        GRAPHICS_CONTROLLER = GraphicsController()
        GRAPHICS_CONTROLLER.stop_signal.connect(self.stop_all_notes)

        # Graphics Test
        #note = GraphicsNote(70)
        #self.scene.addItem(note)

        #-----------------------------------------------------------------------

        VISIBLE_NOTE_BOX = self.visible_note_box
        TIMING_NOTE_BOX = self.timing_note_box
        TIMING_NOTE_LINE = self.timing_note_line
        TIMING_NOTE_LINE_CATCH = self.timing_note_line_catch

        # Note
        PIXMAPS[GREEN].append(QPixmap(r".\images\green_music_note_head.png").scaled(19,19))
        PIXMAPS[YELLOW].append(QPixmap(r".\images\yellow_music_note_head.png").scaled(19,19))
        PIXMAPS[CYAN].append(QPixmap(r".\images\cyan_music_note_head.png").scaled(19,19))

        # Sharp
        PIXMAPS[GREEN].append(QPixmap(r".\images\green_sharp.png").scaled(20,45))
        PIXMAPS[YELLOW].append(QPixmap(r".\images\yellow_sharp.png").scaled(20,45))
        PIXMAPS[CYAN].append(QPixmap(r".\images\cyan_sharp.png").scaled(20,45))

        # Flat
        PIXMAPS[GREEN].append(QPixmap(r".\images\green_flat.png").scaled(13,35))
        PIXMAPS[YELLOW].append(QPixmap(r".\images\yellow_flat.png").scaled(13,35))
        PIXMAPS[CYAN].append(QPixmap(r".\images\cyan_flat.png").scaled(13,35))

        # Natural
        PIXMAPS[GREEN].append(QPixmap(r".\images\green_natural.png").scaled(40,48))
        PIXMAPS[YELLOW].append(QPixmap(r".\images\yellow_natural.png").scaled(40,48))
        PIXMAPS[CYAN].append(QPixmap(r".\images\cyan_natural.png").scaled(40,48))

        return None

    def draw_filtered_sequence(self):

        tick_count = LEFT_TICK_SHIFT
        print("Drawing the following filtered_sequence")
        print(self.filtered_sequence)

        for event in self.filtered_sequence:
            note_array = event[0]
            tick = event[1]
            tick_count += tick
            temp_list = []

            if note_array == []:
                continue

            top_note = max(note_array)
            for note in note_array:
                drawn_note = GraphicsNote(note, tick_count)
                self.scene.addItem(drawn_note)
                temp_list.append(drawn_note)

                if note == top_note:
                    #print("Top note: ", drawn_note)
                    drawn_note.top_note = True

            self.drawn_notes_group.append(temp_list)

        return True

    def stop_all_notes(self):
        for event in self.drawn_notes_group:
            for note in event:
                note.stop()
        return None

    def move_all_notes(self):

        # 60 fps = 16ms, 1fps = a number of ticks
        frame_per_sec = 1000/(CLOCK_DELAY)

        sec_per_tick = tick2second(1, self.PPQN, self.micro_per_beat_tempo)
        sec_per_tick = sec_per_tick * 100/self.live_settings['speed']

        tick_per_frame = (1/sec_per_tick) * (1/frame_per_sec)
        #print("sec_per_tick: {0}\nframe_per_sec: {1}\ntick_per_frame: {2}".format(sec_per_tick, frame_per_sec, tick_per_frame))

        for event in self.drawn_notes_group:
            for note in event:
                note.set_speed(tick_per_frame)

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
                for note in event:
                    self.scene.removeItem(note)
                    del note

            self.drawn_notes_group.clear()
            self.draw_filtered_sequence()
            self.tutor = Tutor(self)
            self.tutor.start()

        else:
            print("Tutor not enabled")

        return None

    def mode_change(self):

        print("tutoring mode changed")
        self.live_settings['mode'] = self.comboBox_tutoring_mode.currentText()

        return None

    def hand_change(self):

        print("hand skill changed")
        self.live_settings['hand'] = self.comboBox_hand_skill.currentText()

        if self.live_settings['hand'] == "Both":
            for event in self.drawn_notes_group:
                for note in event:
                    note.shaded = False

        elif self.live_settings['hand'] == "Right Hand":
            for event in self.drawn_notes_group:
                for note in event:
                    if note.note_pitch >= MIDDLE_C:
                        note.shaded = False
                    else:
                        note.shaded = True

        elif self.live_settings['hand'] == "Left Hand":
            for event in self.drawn_notes_group:
                for note in event:
                    if note.note_pitch >= MIDDLE_C:
                        note.shaded = True
                    else:
                        note.shaded = False

        return None

    def speed_change(self):

        self.live_settings['speed'] = self.spinBox_speed.value()
        print("Speed Changed")

        return None

    def transpose_change(self):

        if self.tutor_enable is True:
            self.live_settings['transpose'] = self.spinBox_transpose.value()

            transpose_diff = self.live_settings['transpose'] - self.transpose_tracker
            self.transpose_tracker = self.live_settings['transpose']

            # Change all notes in Graphics
            for event in self.drawn_notes_group:
                for note in event:
                    note.set_note_pitch(note.note_pitch + transpose_diff)

            # Change the filtered_sequence
            for i in range(len(self.filtered_sequence)):
                note_array = self.filtered_sequence[i][0]
                new_note_array = []
                for note in note_array:
                    new_note_array.append(note + transpose_diff)
                self.filtered_sequence[i][0] = new_note_array


            print("Post-transpose filtered_sequence")
            print(self.filtered_sequence)

            # Change the keyboard_state
            self.keyboard_state[TARGET] = [note + transpose_diff for note in self.keyboard_state[TARGET]]
            self.keyboard_state[RIGHT].clear()
            self.keyboard_state[WRONG].clear()

        else:
            print("Tutor disabled, transpose change discarted")

        return None

    #---------------------------------------------------------------------------
    # Tutoring Manipulation Functions

    def setup_tutor(self):

        if self.tutor_enable:

            self.tutor.exit()
            self.live_settings['play'] = False
            self.toolButton_play.setText("Play")

            for event in self.drawn_notes_group:
                for note in event:
                    self.scene.removeItem(note)
                    del note

            self.drawn_notes_group.clear()

        # Normal tutor setup procedure
        self.tutor_enable = True

        self.original_sequence = []
        self.filtered_sequence = []
        self.PPQN = None
        self.micro_per_beat_tempo = 0

        # Graphics
        self.drawn_notes_group = []

        midi_setup_status = self.midi_setup()
        draw_setup_status = self.draw_filtered_sequence()

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

        upload_file_path = self.open_filename_dialog_user_input()

        if upload_file_path:

            print("UPLOAD FILE LOCATION: {0}".format(upload_file_path))

            self.file_container.clean_temp_folder()
            self.file_container.remove_all()
            self.file_container.original_file = upload_file_path
            self.file_container.add_file_type(upload_file_path)

            if is_mid(upload_file_path):
                print("Begin Tutoring")

                self.spinBox_speed.setValue(100)
                self.spinBox_transpose.setValue(0)
                self.transpose_tracker = 0
                self.comboBox_tutoring_mode.setCurrentText("Beginner")
                self.comboBox_hand_skill.setCurrentText("Both")

                self.remote_midi_file = upload_file_path
                self.setup_tutor()

        return None

    def open_filename_dialog_user_input(self):
        # This file dialog is used to obtain the file location of the .mid, .mp3,
        # and .pdf file.


        #fileName, _ = QFileDialog.getOpenFileName(caption = "Select Audio File", filter = "All Supported Files (*.mid *.mp3 *.pdf);;All Files (*.*);;MIDI Files(*.mid);;MP3 Files(*.mp3);;PDF Files (*.pdf)")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Select Audio File", "", "All Supported Files (*.mid *.mp3 *.pdf);;All Files (*.*);;MIDI Files(*.mid);;MP3 Files(*.mp3);;PDF Files (*.pdf)", options=options)

        if fileName:
            file_dialog_output = str(fileName)
        else:
            return ""

        file_dialog_output = file_dialog_output.replace('/' , '\\' )
        file_upload_event = 1
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

    def open_red_dot_forever(self):
        # This function start red dot forever thread
        self.red_dot_thread = RedDotThread()
        self.red_dot_thread.start()
        self.red_dot_thread.red_dot_signal.connect(self.red_dot_forever_translate)

        return

    @pyqtSlot('QString','QString')
    def red_dot_forever_translate(self, address_string, filename_string):

        # MIDI File Recorded!
        self.file_container.clean_temp_folder()
        self.file_container.remove_all()
        self.file_container.red_dot_address_conversion(address_string, filename_string)

        return

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

        cwd_path = os.path.dirname(os.path.abspath(__file__))
        if cwd_path == '' or cwd_path.find('SKORE') == -1:
            cwd_path = os.path.dirname(sys.argv[0])

        files = glob.glob(cwd_path + '\*')

        for file in files:
            if is_mid(file):
                os.remove(file)

        filename = os.path.basename(self.remote_midi_file)
        self.local_midi_file = cwd_path + '\\' + filename

        try:
            copyfile(self.remote_midi_file, self.local_midi_file)
        except SameFileError:
            print("Noting that midi file already exist")

        # Obtaining the note event info for the mid file
        self.midi_to_note_event_info()

        if self.original_sequence[0].event_type != None:
            self.original_sequence.insert(0,MidiEvent(None,0))

        # Pre-Song Analysis
        self.sequence_filtering()

        print("""
---------------------------Tutor Midi Setup-----------------------------
MIDI FILE LOCATION: {0}

ORIGINAL MIDI SEQUENCE:
{1}

FILTERED MIDI SEQUENCE:
{2}

        """.format(self.local_midi_file, self.original_sequence, self.filtered_sequence))

        return True

    def midi_to_note_event_info(self):
        # Now obtaining the pattern of the midi file found.

        midi_file_name = os.path.basename(self.local_midi_file)
        pattern = read_midifile(self.local_midi_file)

        self.PPQN = pattern.resolution

        for track in pattern:
            for event in track:
                if isinstance(event, MetaEvent):
                    try:
                        tempo_info = event.data

                        if tempo_info != []:
                            for index, element in enumerate(tempo_info):
                                self.micro_per_beat_tempo += element * 256 ** (2 - index)

                        #print('micro_per_beat_tempo:', self.micro_per_beat_tempo)
                    except:
                        pass

                if isinstance(event, NoteEvent):
                    if event.tick > 0:
                        self.original_sequence.append(MidiEvent(None, event.tick))
                    if event.data[1] == 0 or isinstance(event, NoteOffEvent):
                        self.original_sequence.append(MidiEvent(False, event.pitch))
                    else:
                        self.original_sequence.append(MidiEvent(True, event.pitch))
        return None

    def sequence_filtering(self):

        final_index = -1

        for i in range(len(self.original_sequence)):

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

            #sec_delay = tick2second(delta_time - DELAY_EARLY_TOLERANCE, self.PPQN, self.micro_per_beat_tempo)
            #sec_delay = round(sec_delay * 1000 * 100/self.data_bridge.gui_data['gui'].live_settings['speed'])

            #-------------------------------------------------------------------
            # Chord Detection

            chord_delta_time = 0
            note_array = []
            final_index = i

            for index_tracker, event in enumerate(self.original_sequence[i:]):

                if event.event_type is None:
                    if event.data >= CHORD_TICK_TOLERANCE:
                        final_index += index_tracker - 1
                        break
                    else:
                        if chord_delta_time + event.data >= CHORD_SUM_TOLERANCE:
                            final_index += index_tracker - 1
                            break
                        else:
                            chord_delta_time += event.data

                elif event.event_type is True:
                    note_array.append(event.data)

            #self.filtered_sequence.append([note_array, sec_delay])
            self.filtered_sequence.append([note_array, delta_time])

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
            if self.tutor is None:
                self.tutor = Tutor(self, self.file_container.file_path['.mid'])
            else:
                self.tutor.terminate()
                self.tutor = Tutor(self, self.file_container.file_path['.mid'])
            self.tutor.start()
            self.tutor_enable = True

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

        self.settings_dialog = SettingsDialog()
        self.settings_dialog.show()
        self.settings_dialog.finish_apply_signal.connect(self.settings_dialog_change)

        return None

    def settings_dialog_change(self):

        global CHORD_TICK_TOLERANCE, DELAY_EARLY_TOLERANCE, DELAY_LATE_TOLERANCE

        print("SETTINGS UPDATE: CHANGES APPLIED")
        self.setup_comm()
        CHORD_TICK_TOLERANCE = int(setting_read('chord_tick_tolerance'))
        DELAY_EARLY_TOLERANCE = int(setting_read('delay_early_tolerance')) #35 # < 40, > 25, > 30, > 35, < 37, < 36
        DELAY_LATE_TOLERANCE = int(setting_read('delay_late_tolerance'))

        return None

    #---------------------------------------------------------------------------
    # Misc Functions

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.toolButton_restart.setText(_translate("MainWindow", "Restart"))
        self.toolButton_play.setText(_translate("MainWindow", "Play"))
        self.label_speed.setText(_translate("MainWindow", "Speed:"))
        self.label_transpose.setText(_translate("MainWindow", "Transpose:"))
        self.label_tutoring_mode.setText(_translate("MainWindow", "   Tutoring Mode:"))
        #self.radioButton_beginner.setText(_translate("MainWindow", "Beginner"))
        #self.radioButton_intermediate.setText(_translate("MainWindow", "Intermediate"))
        #self.radioButton_expert.setText(_translate("MainWindow", "Expert"))
        self.label_hand_skill.setText(_translate("MainWindow", "Hand Skill:"))
        #self.radioButton_both.setText(_translate("MainWindow", "Both"))
        #self.radioButton_left_hand.setText(_translate("MainWindow", "Left"))
        #self.radioButton_right_hand.setText(_translate("MainWindow", "Right"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionOpenFile.setText(_translate("MainWindow", "Open File..."))
        self.actionCreate_MIDI.setText(_translate("MainWindow", "Create MIDI"))
        self.actionCreate_PDF.setText(_translate("MainWindow", "Create PDF"))
        self.actionSave_File.setText(_translate("MainWindow", "Save Files..."))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionRecord.setText(_translate("MainWindow", "Record "))
        self.actionConfig.setText(_translate("MainWindow", "Config..."))
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
