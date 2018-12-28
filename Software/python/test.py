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
import warnings
import difflib

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

# SKORE Library
from skore_lib import FileContainer, GuiManipulator, setting_read, setting_write, is_mid, rect_to_int

#-------------------------------------------------------------------------------
# Constants

APP_CLOSE_DELAY = 2
COMM_THREAD_DELAY = 0.001
TUTOR_THREAD_DELAY = 0.01

KEYBOARD_SHIFT = 36
COMM_TIMEOUT = 30
HANDSHAKE_DELAY = 0.1

CHORD_TICK_TOLERANCE = int(setting_read('chord_tick_tolerance'))
CHORD_SUM_TOLERANCE = 25
DELAY_EARLY_TOLERANCE = int(setting_read('delay_early_tolerance')) #35 # < 40, > 25, > 30, > 35, < 37, < 36
DELAY_LATE_TOLERANCE = int(setting_read('delay_late_tolerance'))

#-------------------------------------------------------------------------------
# Useful Function

def current_milli_time():
    return int(round(time.time() * 1000))

#-------------------------------------------------------------------------------
# Support Classes

class MidiEvent:

    def __init__(self, event_type, event_data):
        self.event_type = event_type
        self.data = event_data

        return None

    def __repr__(self):
        return "({0}, {1})".format(self.event_type, self.data)

class TransparentButton(QPushButton):
    # This class is custom version of QPushButton that is transparent

    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        self.button_state = 'enabled'

        op=QGraphicsOpacityEffect(self)
        op.setOpacity(0.01)
        self.setGraphicsEffect(op)
        self.setAutoFillBackground(True)

        return None

class DisabledButton(QPushButton):
    # This class is custom version of QPushButton that is not transparent, and not
    # enabled for the user's usability

    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        self.button_state = 'disabled'
        self.setStyleSheet("""
            background-color: rgb(240,240,240);
            border: none;""")
        list = QStyleFactory.keys()
        self.setStyle(QStyleFactory.create(list[0]))

class CoordinateButton(QPushButton):
    # This class is custom version of QPushButton that is set by calculated
    # coordinates rather than button-to-button matching

    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        self.button_state = 'enabled'

        op=QGraphicsOpacityEffect(self)
        op.setOpacity(0.01)
        self.setGraphicsEffect(op)
        self.setAutoFillBackground(True)

class DataBridge:

    def __init__(self):

        self.comm_data = {}
        self.tutor_data = {}
        self.gui_data = {}

        return None

#-------------------------------------------------------------------------------
# Main Classes

class AppOpenThread(QThread):
    # This thread deals with closure of the PianoBooster Application. Once the
    # application is closed, it will emit a signal to inform the SKORE Companion
    # application to close.

    app_close_signal = QtCore.pyqtSignal()

    def __init__(self, data_bridge):
        QThread.__init__(self)

        self.data_bridge = data_bridge

    def run(self):

        print("Piano Booster App State Thread Enabled")

        while(True):
            time.sleep(APP_CLOSE_DELAY)

            if self.data_bridge.gui_data['pia_app'].is_process_running() == False:
                print("PianoBooster Application Closure Detection")
                self.app_close_signal.emit()

                break

class Comm(QThread):
    # This thread initializes the communication between the piano, virtual midi,
    # and arduino. Additionally, it continuously keeping tracking of the current
    # state of the piano and relays the information recieved from the piano to
    # the virtual port. Look to the communication diagram for further explanation.

    comm_setup_signal = QtCore.pyqtSignal()

    def __init__(self, data_bridge):
        QThread.__init__(self)

        self.arduino = None
        self.midi_in = None
        self.midi_out = None
        self.current_keyboard_state = []

        self.data_bridge = data_bridge
        self.data_bridge.comm_data['current_keyboard_state'] = self.current_keyboard_state
        self.data_bridge.comm_data['comm'] = self

    def arduino_handshake(self):

        print("waiting for arduino handshake")
        timeout = time.time() + COMM_TIMEOUT
        while time.time() < timeout:
            time.sleep(HANDSHAKE_DELAY)
            read_data = self.arduino.read()
            if read_data == b'#':
                print("finished handshake")
                return True

        raise RuntimeError("Communication Desync with Arduino")
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
            raise RuntimeError("Piano Size Selection not found.")

        # Closing, if applicable, the arduino port
        if self.arduino:
            self.arduino.close()
            self.arduino = []

        try:
            com_port = setting_read("arduino_port")
            print("COM Port Selected: " + str(com_port))

            self.arduino = serial.Serial(com_port, 230400, writeTimeout = COMM_TIMEOUT)
            self.data_bridge.comm_data['arduino'] = self.arduino
            print("Arduino Connected")

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


            print("\nData Transmitted to the Arduino for Setup:")
            print("Piano Size: " + str(piano_size))
            print("WhiteKey Colors: " + str(whitekey_transmitted_string))
            print("BlackKey Colors: " + str(blackkey_transmitted_string))

            setup_transmitted_string = size_message + whitekey_transmitted_string + blackkey_transmitted_string
            setup_transmitted_string += ',#,'

            time.sleep(2)
            print("Setup String:" + setup_transmitted_string)
            self.arduino.write(setup_transmitted_string.encode('utf-8'))
            #time.sleep(2)
            if self.arduino_handshake() is True:
                return True

        except serial.serialutil.SerialException:
            print("Arduino Not Found")
            return False

    def piano_port_setup(self):
        # This function sets up the communication between Python and the MIDI device
        # For now Python will connect the first listed device.

        if not self.midi_in and not self.midi_out:
            try:
                self.midi_in.close_port()
                self.midi_out.close_port()
            except:
                self.midi_in = None
                self.midi_out = None

        self.midi_in = rtmidi.MidiIn()
        self.data_bridge.comm_data['midi_in'] = self.midi_in
        in_avaliable_ports = self.midi_in.get_ports()
        selected_port = setting_read("piano_port")
        closes_match_in_port = difflib.get_close_matches(selected_port, in_avaliable_ports)[0]
        print("Piano Port: " + str(closes_match_in_port))

        try:
            self.midi_in.open_port(in_avaliable_ports.index(closes_match_in_port))
        except:
            print("Piano Port Setup Failure")
            self.midi_in = []
            self.midi_out = []
            return None

        self.midi_out = rtmidi.MidiOut()
        self.data_bridge.comm_data['midi_out'] = self.midi_out
        out_avaliable_ports = self.midi_out.get_ports()
        closes_match_out_port = difflib.get_close_matches('LoopBe Internal MIDI',out_avaliable_ports)[0]
        print("LoopBe Internal Port: " + str(closes_match_out_port))

        try:
            self.midi_out.open_port(out_avaliable_ports.index(closes_match_out_port))
            return True
        except:
            print("LoopBe Internal Port Setup Failure")
            self.midi_in = None
            self.midi_out = None

        return None

    def safe_change_current_keyboard_state(self, pitch, state):
        # This function safely removes or adds the pitch to the
        # current_keyboard_state variable

        if state is True:
            if pitch in self.current_keyboard_state:
                return None
            self.current_keyboard_state.append(pitch)

        elif state is False:
            if pitch not in self.current_keyboard_state:
                return None
            self.current_keyboard_state.remove(pitch)

        return None

    #---------------------------------------------------------------------------

    def run(self):

        print("Piano and Arduino Communication Thread Enabled")

        arduino_status = self.arduino_setup()
        piano_status = self.piano_port_setup()

        if arduino_status is True and piano_status is True:
            print("Piano and Arduino Communication Setup Successful")
            self.comm_setup_signal.emit()

            #try:
            while True:
                time.sleep(COMM_THREAD_DELAY)
                message = self.midi_in.get_message()

                if message:
                    note_info, delay = message
                    ####
                    self.midi_out.send_message(note_info)
                    ####

                    if note_info[0] == 144 and note_info[2] != 0: # Note ON event
                        self.safe_change_current_keyboard_state(note_info[1], True)

                        if note_info[1] in self.data_bridge.tutor_data['target_keyboard_state']:
                            if note_info[1] not in self.data_bridge.tutor_data['right_notes']:
                                self.data_bridge.tutor_data['right_notes'].append(note_info[1])
                        else:
                            if note_info[1] not in self.data_bridge.tutor_data['wrong_notes']:
                                self.data_bridge.tutor_data['wrong_notes'].append(note_info[1])

                    else: # Note OFF event
                        self.safe_change_current_keyboard_state(note_info[1], False)

                        if note_info[1] in self.data_bridge.tutor_data['right_notes']:
                            self.data_bridge.tutor_data['right_notes'].remove(note_info[1])
                        elif note_info[1] in self.data_bridge.tutor_data['wrong_notes']:
                            self.data_bridge.tutor_data['wrong_notes'].remove(note_info[1])

                    print(self.current_keyboard_state)

            #except AttributeError:
            #    print("Lost Piano Communication")
            #except RuntimeError:
            #    print("Python-side Error ***bug***")

        return

class Tutor(QThread):
    # This thread performs the algorithm to control the LED lights with the
    # information of the other threads, such as the live tutoring variables.
    # The thread will include the code for the beginner, intermediate, and
    # expert mode.

    def __init__(self, file_container, data_bridge):
        QThread.__init__(self)

        self.file_container = file_container

        self.sequence = []
        self.PPQN = None
        self.micro_per_beat_tempo = 0
        self.tutoring_index = 0

        self.right_notes = []
        self.wrong_notes = []
        self.target_keyboard_state = []
        self.arduino_keyboard = []

        self.data_bridge = data_bridge
        self.data_bridge.tutor_data['right_notes'] = self.right_notes
        self.data_bridge.tutor_data['wrong_notes'] = self.wrong_notes
        self.data_bridge.tutor_data['target_keyboard_state'] = self.target_keyboard_state
        self.data_bridge.tutor_data['arduino_keyboard'] = self.arduino_keyboard

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
                print("Deleted: " + str(file))
                try:
                    os.remove(file)
                    break
                except PermissionError:
                    #raise RuntimeError("PianoBooster is restricting the removable of previous midi files")
                    print("PianoBooster is restricting the removable of previous midi files")
                    continue

        #self.file_container.stringify_container()

        if self.file_container.has_midi_file() is True:
            midi_file = self.file_container.file_path['.mid']
        else:
            raise RuntimeError("Midi file not found.")

        filename = os.path.basename(midi_file)
        new_midi_file = cwd_path + '\\' + filename

        try:
            copyfile(midi_file, new_midi_file)
        except SameFileError:
            print("Noting that midi file already exist")

        # Obtaining the note event info for the mid file
        self.midi_to_note_event_info(new_midi_file)

        if self.sequence[0].event_type != None:
            self.sequence.insert(0,MidiEvent(None,0))

        #print(sequence)
        #print()
        return True

    def midi_to_note_event_info(self, mid_file):
        # Now obtaining the pattern of the midi file found.

        print(mid_file)

        mid_file_name = os.path.basename(mid_file)
        pattern = read_midifile(mid_file)

        self.PPQN = pattern.resolution
        #print('PPQN: ', PPQN)
        #print(pattern)

        for track in pattern:
            for event in track:
                if isinstance(event, MetaEvent):
                    try:
                        tempo_info = event.data
                        #print(tempo_info)

                        if tempo_info != []:
                            for index, element in enumerate(tempo_info):
                                self.micro_per_beat_tempo += element * 256 ** (2 - index)

                        print('micro_per_beat_tempo:', self.micro_per_beat_tempo)
                    except:
                        pass

                if isinstance(event, NoteEvent):
                    if event.tick > 0:
                        self.sequence.append(MidiEvent(None, event.tick))
                    if isinstance(event, NoteOffEvent):
                        self.sequence.append(MidiEvent(False, event.pitch))
                    else:
                        self.sequence.append(MidiEvent(True, event.pitch))

        return None

    ##############################UTILITY FUNCTIONS#########################

    def keyboard_valid(self):
        # This functions follows the confirmation system of PianoBooster
        # which determines if the keys pressed are acceptable compared to the
        # target keyboard configuration

        for note in self.target_keyboard_state:
            if note not in self.right_notes:
                return False

        if len(self.wrong_notes) <= 1:
            self.right_notes.clear()
            return True

        return None

    #############################TUTORING UTILITY FUNCTIONS#################

    def determine_delay(self, index):

        delay = 0

        for event in reversed(self.sequence[:index]):

            if event.event_type is None:
                delay += event.data

            elif event.event_type is True:
                return delay

        return delay

    def chord_detection(self, index):

        #print('index: ', index)
        #print("chord_detection:")
        #print(sequence[index:])
        #print()

        chord_delay = 0
        note_array = []
        is_chord = False
        final_index = index

        for index_tracker, event in enumerate(self.sequence[index:]):

            print(event)

            if event.event_type is None:
                if event.data >= CHORD_TICK_TOLERANCE:
                    final_index += index_tracker - 1
                    break
                else:
                    if chord_delay + event.data >= CHORD_SUM_TOLERANCE:
                        final_index += index_tracker - 1
                        break
                    else:
                        chord_delay += event.data

            elif event.event_type is True:
                note_array.append(event.data)

        if len(note_array) > 1:
            is_chord = True

        return note_array, chord_delay, is_chord, final_index

    ##############################COMMUNICATION FUNCTIONS###################

    def arduino_comm(self, notes):
        # This function sends the information about which notes need to be added and
        # removed from the LED Rod.

        #print("Arduino Comm Notes: " + str(notes))

        #notes_to_add = []
        #notes_to_remove = []
        notes_to_send = []

        #time.sleep(0.001)
        #print("Arduino Keyboard Pre-Communication: " + str(arduino_keyboard))

        if notes:
            notes_to_send = self.arduino_keyboard
            self.arduino_keyboard.clear()
            #print('sending *')
            self.data_bridge.comm_data['arduino'].write(b',*,#,')
            #time.sleep(0.05)

        else:

            notes_to_send = list(set(self.target_keyboard_state).symmetric_difference(self.arduino_keyboard))
            #notes_to_send.sort()

            # All transmitted notes are contain within the same string
            transmitted_string = ''
            non_shifted_string = ''

            for note in notes_to_send:
                shifted_note = note - KEYBOARD_SHIFT + 1
                transmitted_string += str(shifted_note) + ','
                non_shifted_string += str(note) + ','

            transmitted_string = ',' + transmitted_string + ',#,'
            non_shifted_string = ',' + non_shifted_string + ',#,'

            #transmitted_string = transmitted_string[:-1] # to remove last note's comma
            #print("transmitted_string to Arduino: " + transmitted_string)
            #print("non_shifted_string to Arduino: " + non_shifted_string)
            #print("shifted_string to Arduino: " + transmitted_string)

            encoded_transmitted_string = transmitted_string.encode('utf-8')
            self.data_bridge.comm_data['arduino'].write(encoded_transmitted_string)

            #print("Post-Communication: " + str(arduino_keyboard))

            self.data_bridge.comm_data['comm'].arduino_handshake()

        return None

    #################################TUTOR FUNCTIONS########################

    def tutor_beginner(self, starting_index):
        # This is practically the tutoring code for Beginner Mode

        self.local_transpose_variable = 0
        self.target_keyboard_state = []
        self.right_notes = []
        self.wrong_notes = []
        self.arduino_keyboard = []

        final_index = 0
        is_chord = False

        for current_index, event in enumerate(self.sequence):

            if starting_index > current_index:
                continue

            if is_chord is True:
                if current_index <= final_index:
                    # This is to account for the index shift if a chord is
                    # registered
                    continue
                else:
                    is_chord = False

            # If Turn On Event
            if event.event_type == True:
                print('\n##############################################################')
                print('current_index:', current_index)

                # Determine if chord and details
                note_array, chord_delay, is_chord, final_index = self.chord_detection(current_index)
                print('Note/Chord Characteristics: ',note_array, chord_delay, is_chord, final_index)

                for index, note in enumerate(note_array):
                    note_array[index] = self.data_bridge.gui_data['live_settings']['transpose'] + note

                self.target_keyboard_state.clear()
                self.target_keyboard_state.extend(note_array)

                # Determine previous delay
                delay = self.determine_delay(current_index)
                #print('Pre-Note/Chord delay: ', delay, '  Millisecond version: (with tolerance) ', delay * delay_multiplier)

                print('Target', self.target_keyboard_state)
                self.arduino_comm(self.target_keyboard_state)
                #print()

                inital_time = current_milli_time()
                #print('inital_time: ', inital_time)
                timer = 0

                #print(delay, PPQN, micro_per_beat_tempo)
                second_delay = tick2second(delay - DELAY_EARLY_TOLERANCE, self.PPQN, self.micro_per_beat_tempo)
                second_delay = round(second_delay * 1000 * 100/self.data_bridge.gui_data['live_settings']['speed'])
                #print('second_delay:', second_delay)

                # Waiting while loop
                while(True):
                    time.sleep(TUTOR_THREAD_DELAY)

                    if self.data_bridge.gui_data['live_settings']['live_settings_change'] is True:
                        self.data_bridge.gui_data['live_settings']['live_settings_change'] = False

                        if self.data_bridge.gui_data['live_settings']['restart'] is True:
                            self.arduino_comm([])
                            self.data_bridge.gui_data['live_settings']['playing_state'] = True
                            self.data_bridge.gui_data['live_settings']['restart'] = False
                            return 0

                        if self.data_bridge.gui_data['live_settings']['current_mode'] != 'beginner':
                            self.arduino_comm([])
                            self.data_bridge.gui_data['live_settings']['playing_state'] = False
                            print("changing tutoring mode")
                            return final_index + 1
                            #return previous_turnon_event_index

                        if local_transpose_variable != self.data_bridge.gui_data['live_settings']['transpose']:
                            print("Transpose Detected")
                            diff = self.data_bridge.gui_data['live_settings']['transpose'] - local_transpose_variable
                            local_transpose_variable = self.data_bridge.gui_data['live_settings']['transpose']
                            self.target_keyboard_state = [note + diff for note in self.target_keyboard_state]
                            self.arduino_comm([])
                            self.arduino_comm(self.target_keyboard_state)

                    if self.data_bridge.gui_data['live_settings']['playing_state'] is True:

                        if timer >= second_delay:

                            if self.keyboard_valid():
                                self.target_keyboard_state.clear()
                                #arduino_comm([])
                                break

                            continue

                        else:
                            self.right_notes.clear()

                        timer = current_milli_time() - inital_time
                        print(timer)

                    else:
                        inital_time = current_milli_time()

                        if timer != 0:
                            # if user paused, account for the passed time
                            # in the timer
                            second_delay -= timer
                            timer = 0

        # Outside of large For Loop
        #self.arduino_comm([])
        self.data_bridge.gui_data['live_settings']['playing_state'] = False
        print("end of song")
        return 0

    def tutor_intermediate(self, starting_index):
        #print(starting_index)
        #print("intermediate")
        return starting_index

    def tutor_expert(self, starting_index):
        #print(starting_index)
        #print('expert')
        return starting_index

    def run(self):

        ###############################MAIN RUN CODE############################

        midi_status = self.midi_setup()

        if midi_status is True:

            while True:
                if self.data_bridge.gui_data['live_settings']['current_mode'] == 'beginner':
                    self.tutoring_index = self.tutor_beginner(self.tutoring_index)
                elif self.data_bridge.gui_data['live_settings']['current_mode'] == 'intermediate':
                    self.tutoring_index = self.tutor_intermediate(self.tutoring_index)
                elif self.data_bridge.gui_data['live_settings']['current_mode'] == 'expert':
                    self.tutoring_index = self.tutor_expert(self.tutoring_index)

                while self.data_bridge.gui_data['live_settings']['playing_state']:
                    #print("completion of tutoring mode")
                    time.sleep(0.1)
        else:
            return None

class SkoreGlassGui(QMainWindow):
    # This class creates the transparent GUI overlay that rests ontop of PianoBooster.
    # It initalizises PianoBooster, the communication systems, and buttons that
    # manipulate PianoBooster

    button_signal = QtCore.pyqtSignal('QString')

    def __init__(self, file_container):
        super(QMainWindow, self).__init__()
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        #self.setWindowOpacity(0.5) # 0 does not work
        #self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint )
        #self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        self.file_container = file_container
        self.live_settings = {'skill': 'follow_you_button', 'current_mode': 'beginner',
                              'reset_flag': False, 'hands': 'boths', 'speed': 100, 'transpose': 0,
                              'start_bar_value': 0, 'playing_state': False, 'restart': False, 'mode': 'follow_you',
                              'live_settings_change': False}

        self.skore_gui_buttons = {}
        self.pianobooster_buttons = {}
        self.message_box_active = False

        self.data_bridge = DataBridge()
        self.data_bridge.gui_data['live_settings'] = self.live_settings
        self.data_bridge.gui_data['pia_app'] = None

        self.setup_pianobooster()
        self.setup_transparent_ui()
        self.setup_menu_bar()
        self.setup_visible_ui()
        self.setup_thread()

    def setup_pianobooster(self):
            # This function performs the task of opening PianoBooster and appropriately
            # clicking on the majority of the qwidgets to make them addressable. When
            # PianoBooster is opened, the qwidgets are still not addressible via
            # pywinauto. For some weird reason, clicked on them enables them. The code
            # utilizes template matching to click on specific regions of the PianoBooster
            # GUI

            # Initilizing the PianoBooster Application
            pia_app = pywinauto.application.Application()
            pia_app_exe_path = setting_read('pia_app_exe_path')
            pia_app.start(pia_app_exe_path)
            print("Initialized PianoBooser")

            # Getting a handle of the application, the application's title changes depending
            # on the .mid file opened by the application.
            possible_handles = pywinauto.findwindows.find_elements()

            # Getting the title of the PianoBooster application, might to try multiple times
            time.sleep(0.5)
            while True:
                try:
                    for i in range(len(possible_handles)):
                        key = str(possible_handles[i])
                        if key.find('Piano Booster') != -1:
                            wanted_key = key
                            #print('Found it ' + key)

                    first_index = wanted_key.find("'")
                    last_index = wanted_key.find(',')
                    pia_app_title = wanted_key[first_index + 1 :last_index - 1]
                    break

                except UnboundLocalError:
                    time.sleep(0.1)

            # Once with the handle, control over the window is achieved.
            while True:
                try:
                    w_handle = pywinauto.findwindows.find_windows(title=pia_app_title)[0]
                    window = pia_app.window(handle=w_handle)
                    break
                except IndexError:
                    time.sleep(0.1)

            # Initializion of the Qwidget within the application

            window.maximize()
            time.sleep(0.5)

            rect_object = window.rectangle()
            dimensions = rect_to_int(rect_object)

            self.pianobooster_image_gui_manipulator = GuiManipulator()
            self.pianobooster_image_gui_manipulator.click_center_try('skill_groupBox_pia', dimensions)
            self.pianobooster_image_gui_manipulator.click_center_try('hands_groupBox_pia', dimensions)
            self.pianobooster_image_gui_manipulator.click_center_try('book_song_buttons_pia', dimensions)
            self.pianobooster_image_gui_manipulator.click_center_try('flag_button_pia', dimensions)
            self.pianobooster_image_gui_manipulator.click_center_try('part_button_pia', dimensions)



            # Aquiring the qwigets from the application
            main_qwidget = pia_app.QWidget
            main_qwidget.wait('ready')

            # Skill Group Box
            listen_button = main_qwidget.Skill3
            follow_you_button = main_qwidget.Skill2
            play_along_button = main_qwidget.Skill

            # Hands Group Box
            right_hand_button = main_qwidget.Hands4
            both_hands_button = main_qwidget.Hands3
            left_hand_button = main_qwidget.Hands2
            slider_hand = main_qwidget.Hands

            # Parts Group Box
            parts_mute_button = main_qwidget.Parts
            parts_slider_button = main_qwidget.Parts2
            parts_selection_button = main_qwidget.Parts3

            # Song and Book Button
            song_combo_button = main_qwidget.songCombo
            book_combo_button = main_qwidget.bookCombo

            # GuiTopBar
            key_combo_button = main_qwidget.keyCombo
            play_button = main_qwidget.playButton
            restart_button = main_qwidget.playFromStartButton
            save_bar_button = main_qwidget.savebarButton
            speed_spin_button = main_qwidget.speedSpin
            start_bar_spin_button = main_qwidget.startBarSpin
            transpose_spin_button = main_qwidget.transposeSpin
            looping_bars_popup_button = main_qwidget.loopingBarsPopupButton
            major_button = main_qwidget.majorCombo

            try:
                menubar_button = main_qwidget[u'3']
            except:
                try:
                    menubar_button = main_qwidget.QWidget34
                except:
                    raise RuntimeError("Main Menu QWidget Missed")

            self.pianobooster_buttons = {'book_combo_button': book_combo_button, 'song_combo_button': song_combo_button, 'listen_button': listen_button,
                                'follow_you_button': follow_you_button, 'play_along_button': play_along_button, 'restart_button': restart_button,
                                'play_button': play_button, 'speed_spin_button': speed_spin_button, 'transpose_spin_button': transpose_spin_button,
                                'looping_bars_popup_button': looping_bars_popup_button, 'start_bar_spin_button': start_bar_spin_button,
                                'menubar_button': menubar_button, 'parts_selection_button': parts_selection_button, 'parts_mute_button': parts_mute_button,
                                'parts_slider_button': parts_slider_button, 'right_hand_button': right_hand_button, 'both_hands_button': both_hands_button,
                                'left_hand_button': left_hand_button, 'slider_hand': slider_hand, 'key_combo_button': key_combo_button,
                                'major_button': major_button, 'save_bar_button': save_bar_button}

            delay = 0.4
            #listen_button.click()
            self.pianobooster_buttons['follow_you_button'].click()
            self.pianobooster_buttons['both_hands_button'].click()

            # Opening the .mid file
            time.sleep(delay)
            self.pianobooster_image_gui_manipulator.click_center_try('file_button_xeno', dimensions)
            time.sleep(delay)
            self.pianobooster_image_gui_manipulator.click_center_try('open_button_pianobooster_menu', dimensions)
            time.sleep(delay)


            while True:
                try:
                    o_handle = pywinauto.findwindows.find_windows(title='Open Midi File')[0]
                    o_window = pia_app.window(handle = o_handle)
                    break
                except IndexError:
                    time.sleep(0.1)

            #self.file_container.stringify_container()
            mid_file_path = self.file_container.file_path['.mid']
            #mid_file_path = r"C:\Users\daval\Documents\GitHub\SKORE\Software\python\conversion_test\aa.mid"
            o_window.type_keys(mid_file_path)
            o_window.type_keys('{ENTER}')

            self.pianobooster_image_gui_manipulator.click_center_try('skill_groupBox_pia', dimensions)
            self.pianobooster_buttons['speed_spin_button'].click_input()
            self.pianobooster_buttons['speed_spin_button'].type_keys('^a {DEL}100{ENTER}')
            self.live_settings['speed'] = 100
            self.live_settings['transpose'] = 0
            self.pianobooster_image_gui_manipulator.click_center_try('skill_groupBox_pia', dimensions)

            print("Finished Initialization")
            self.data_bridge.gui_data['pia_app'] = pia_app

            return None

    def setup_transparent_ui(self):
        # This functions sets up all the transparent GUI

        self.book_combo_button = DisabledButton(self)
        self.song_combo_button = DisabledButton(self)
        self.listen_button = DisabledButton(self)
        self.follow_you_button = DisabledButton(self)
        self.play_along_button = DisabledButton(self)
        self.restart_button = TransparentButton(self)
        self.play_button = TransparentButton(self)
        self.speed_spin_button = TransparentButton(self)
        self.transpose_spin_button = TransparentButton(self)
        self.looping_bars_popup_button = DisabledButton(self)
        self.start_bar_spin_button = DisabledButton(self)
        self.menubar_button = TransparentButton(self)
        self.parts_selection_button = DisabledButton(self)
        self.parts_mute_button = DisabledButton(self)
        self.parts_slider_button = DisabledButton(self)
        self.right_hand_button = TransparentButton(self)
        self.both_hands_button = TransparentButton(self)
        self.left_hand_button = TransparentButton(self)
        self.slider_hand = DisabledButton(self)
        self.key_combo_button = TransparentButton(self)
        self.major_button = TransparentButton(self)
        self.save_bar_button = DisabledButton(self)

        self.skore_gui_buttonGroup = QButtonGroup()
        self.skore_gui_buttonGroup.setExclusive(True)
        self.skore_gui_buttonGroup.addButton(self.book_combo_button)
        self.skore_gui_buttonGroup.addButton(self.song_combo_button)
        self.skore_gui_buttonGroup.addButton(self.listen_button)
        self.skore_gui_buttonGroup.addButton(self.follow_you_button)
        self.skore_gui_buttonGroup.addButton(self.play_along_button)
        self.skore_gui_buttonGroup.addButton(self.restart_button)
        self.skore_gui_buttonGroup.addButton(self.play_button)
        self.skore_gui_buttonGroup.addButton(self.speed_spin_button)
        self.skore_gui_buttonGroup.addButton(self.transpose_spin_button)
        self.skore_gui_buttonGroup.addButton(self.looping_bars_popup_button)
        self.skore_gui_buttonGroup.addButton(self.start_bar_spin_button)
        #self.skore_gui_buttonGroup.addButton(self.menubar_button)
        self.skore_gui_buttonGroup.addButton(self.parts_selection_button)
        self.skore_gui_buttonGroup.addButton(self.parts_mute_button)
        self.skore_gui_buttonGroup.addButton(self.parts_slider_button)
        self.skore_gui_buttonGroup.addButton(self.right_hand_button)
        self.skore_gui_buttonGroup.addButton(self.both_hands_button)
        self.skore_gui_buttonGroup.addButton(self.left_hand_button)
        self.skore_gui_buttonGroup.addButton(self.slider_hand)
        self.skore_gui_buttonGroup.addButton(self.key_combo_button)
        self.skore_gui_buttonGroup.addButton(self.major_button)
        self.skore_gui_buttonGroup.addButton(self.save_bar_button)


        self.skore_gui_buttons = {'book_combo_button': self.book_combo_button, 'song_combo_button': self.song_combo_button, 'listen_button': self.listen_button,
                            'follow_you_button': self.follow_you_button, 'play_along_button': self.play_along_button, 'restart_button': self.restart_button,
                            'play_button': self.play_button, 'speed_spin_button': self.speed_spin_button, 'transpose_spin_button': self.transpose_spin_button,
                            'looping_bars_popup_button': self.looping_bars_popup_button, 'start_bar_spin_button': self.start_bar_spin_button,
                            'menubar_button': self.menubar_button, 'parts_selection_button': self.parts_selection_button, 'parts_mute_button': self.parts_mute_button,
                            'parts_slider_button': self.parts_slider_button, 'right_hand_button': self.right_hand_button, 'both_hands_button': self.both_hands_button,
                            'left_hand_button': self.left_hand_button, 'slider_hand': self.slider_hand, 'key_combo_button': self.key_combo_button,
                            'major_button': self.major_button, 'save_bar_button': self.save_bar_button}


        self.skore_gui_buttons_geometry()

        self.skore_gui_buttonGroup.buttonClicked.connect(self.transparent_button_click)
        self.button_signal.connect(self.create_message_box)

    def setup_menu_bar(self):
        # This function assigns the coordinates to the CoordinateButton class, which
        # have to be calculated. This is because the menubar buttons QRect object
        # was not obtainable with pywinauto.

        self.view_menubar_button = CoordinateButton(self)
        self.song_menubar_button = CoordinateButton(self)
        self.setup_menubar_button = CoordinateButton(self)
        self.help_menubar_button = CoordinateButton(self)

        self.view_menubar_button.setObjectName('view_menubar_button')
        self.song_menubar_button.setObjectName('song_menubar_button')
        self.setup_menubar_button.setObjectName('setup_menubar_button')
        self.help_menubar_button.setObjectName('help_menubar_button')

        self.menubar_buttonGroup = QButtonGroup()
        self.menubar_buttonGroup.setExclusive(True)
        self.menubar_buttonGroup.addButton(self.view_menubar_button)
        self.menubar_buttonGroup.addButton(self.song_menubar_button)
        self.menubar_buttonGroup.addButton(self.setup_menubar_button)
        self.menubar_buttonGroup.addButton(self.help_menubar_button)
        self.menubar_buttonGroup.addButton(self.menubar_button)

        #menubar_button_list = [self.view_menubar_button, self.song_menubar_button,
        #                        self.setup_menubar_button, self.help_menubar_button]

        self.menubar_button_set_geometry()
        self.menubar_buttonGroup.buttonClicked.connect(self.menubar_click)

        return

    def setup_visible_ui(self):
        # This functions sets up all the visible GUI

        #self.setStyleSheet("""
        #    background-color: rgb(50,50,50);
        #    color: white;
        #    """)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setGeometry(QtCore.QRect(5, 650, 400, 300))

        # Tutoring Mode
        self.listen_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.listen_pushButton.setGeometry(QtCore.QRect(5, 30, 310, 51))
        self.listen_pushButton.setObjectName("listen_pushButton")
        self.listen_pushButton.setText("Listen Mode")

        self.beginner_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.beginner_pushButton.setGeometry(QtCore.QRect(5, 85, 310, 51))
        self.beginner_pushButton.setObjectName("beginner_pushButton")
        self.beginner_pushButton.setText("Beginner Mode")

        self.intermediate_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.intermediate_pushButton.setGeometry(QtCore.QRect(5, 140, 310, 51))
        self.intermediate_pushButton.setObjectName("intermediate_pushButton")
        self.intermediate_pushButton.setText("Intermediate Mode")

        self.expert_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.expert_pushButton.setGeometry(QtCore.QRect(5, 195, 310, 51))
        self.expert_pushButton.setObjectName("expert_pushButton")
        self.expert_pushButton.setText("Expert Mode")

        self.visible_buttonGroup = QButtonGroup()
        self.visible_buttonGroup.setExclusive(True)
        self.visible_buttonGroup.addButton(self.listen_pushButton)
        self.visible_buttonGroup.addButton(self.beginner_pushButton)
        self.visible_buttonGroup.addButton(self.intermediate_pushButton)
        self.visible_buttonGroup.addButton(self.expert_pushButton)

        self.visible_buttonGroup.buttonClicked.connect(self.visible_button_click)

        return None

    def setup_thread(self):
        # This functions initalizes the communication threads between PianoBooster,
        # the piano, and the arduino.

        # Initializing PianoBooster App Open Check MultiThreading
        self.check_open_app_thread = AppOpenThread(self.data_bridge)
        self.check_open_app_thread.app_close_signal.connect(self.close_all_thread)
        self.check_open_app_thread.start()

        # Initializing Piano and Arduino Communication
        # Testing Here
        self.comm = Comm(self.data_bridge)
        self.comm.comm_setup_signal.connect(self.start_tutor_thread)
        self.comm.start()

        return

    #---------------------------------------------------------------------------

    def skore_gui_buttons_geometry(self):
        # This function assigns the corresponding transparent buttons to the
        # visible pianobooster buttons that are intended to be keep enabled.

        for key in self.skore_gui_buttons.keys():
            if key == 'menubar_button':
                dimensions = self.pianobooster_buttons[key].rectangle()
                width = int((dimensions.right - dimensions.left)*0.02)
                self.skore_gui_buttons[key].setGeometry(QRect(dimensions.left, dimensions.top, width, dimensions.bottom - dimensions.top))
                continue

            dimensions = self.pianobooster_buttons[key].rectangle()
            self.skore_gui_buttons[key].setGeometry(QRect(dimensions.left, dimensions.top, dimensions.right - dimensions.left, dimensions.bottom - dimensions.top))

        return None

    def menubar_button_set_geometry(self):
        # This funciton calculates and set the geometry of the menubar buttons,
        # which have a subclass decided for them, called CoordinateButton

        dimensions = self.menubar_button.geometry()
        self.view_menubar_button.setGeometry(dimensions.right() + 1, dimensions.top(), dimensions.width() + 7, dimensions.height())
        dimensions = self.view_menubar_button.geometry()
        self.song_menubar_button.setGeometry(dimensions.right() + 1, dimensions.top(), dimensions.width() + 4, dimensions.height())
        dimensions = self.song_menubar_button.geometry()
        self.setup_menubar_button.setGeometry(dimensions.right() + 1, dimensions.top(), dimensions.width() + 4, dimensions.height())
        dimensions = self.setup_menubar_button.geometry()
        self.help_menubar_button.setGeometry(dimensions.right() + 1, dimensions.top(), dimensions.width() + 4, dimensions.height())

        return None

    def visible_button_click(self, button):
        # This function selects the tutoring mode to beginner

        changing_mode = ''

        if button == self.listen_pushButton:
            changing_mode = 'listen'
        elif button == self.beginner_pushButton:
            chaning_mode = 'beginner'
        elif button == self.intermediate_pushButton:
            changing_mode = 'intermediate'
        elif button == self.expert_pushButton:
            changing_mode = 'expert'
        else:
            raise RuntimeError("Invalid button.")


        if self.live_settings['current_mode'] == changing_mode:
            return None

        self.live_settings['current_mode'] = changing_mode
        self.live_settings['live_settings_change'] = True

        if self.live_settings['playing_state'] is True:
            self.pianobooster_buttons['play_button'].click() # play_button
            self.live_settings['playing_state'] = False

        self.pianobooster_buttons['follow_you_button'].click() # follow_you_button

        return None

    def transparent_button_click(self, button):
        # This function clicks on the corresponding PianoBooster button once
        # a transparent and enabled button

        if button.button_state == 'disabled':
            return

        if button == self.play_button:
            self.pianobooster_buttons['play_button'].click()
            self.live_settings['playing_state'] = not self.live_settings['playing_state']
            print("Playing State: {0}".format(self.live_settings['playing_state']))

        elif button == self.restart_button:
            self.pianobooster_buttons['restart_button'].click()
            self.live_settings['playing_state'] = True
            self.live_settings['restart'] = True
            self.live_settings['live_settings_change'] = True
            print("Restart Pressed")

        elif button == self.speed_spin_button or button == self.transpose_spin_button: #or button_name == 'start_bar_spin_button':
            if self.message_box_active is False:
                if button == self.speed_spin_button:
                    button_name = 'speed_spin_button'
                else:
                    button_name = 'transpose_spin_button'
                self.button_signal.emit(button_name)
            else:
                print("QInputDialog in use")

        elif button == self.right_hand_button:
            self.pianobooster_buttons['right_hand_button'].click()
        elif button == self.both_hands_button:
            self.pianobooster_buttons['both_hands_button'].click()
        elif button == self.left_hand_button:
            self.pianobooster_buttons['left_hand_button'].click()

        return None

    def menubar_click(self, button):
        # This function clicks on the assigned buttons that are the coordinate
        # buttons.

        #button_name = str(button.objectName())
        x_coord, y_coord = win32api.GetCursorPos()
        print(x_coord,',',y_coord)

        self.hide()
        self.click(x_coord,y_coord)
        #self.click(x_coord,y_coord)
        time.sleep(0.1)
        self.show()

        return

    def click(self,x,y):
        # This function manually clicks on a set of x and y coordinates

        win32api.SetCursorPos((x,y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
        return None

    @pyqtSlot('QString')
    def create_message_box(self, item):
        # This function creates a QInputDialog box for the user to input
        # multivalue information, such as speed and transpose

        was_playing = False
        setting_change = False

        # Stopping the application
        if self.live_settings['playing_state'] is True:
            was_playing = True
            print("Stoping app")
            self.pianobooster_buttons['play_button'].click()
            self.live_settings['playing_state'] = False
            self.live_settings['live_settings_change'] = True

        # Asking user for value of spin button
        self.message_box_active = True

        if item == 'speed_spin_button':
            num, ok = QInputDialog.getInt(self, item + "Pressed", "Enter the value [20 - 200] for " + item)

            if num <= 200 or num >= 20:
                original_speed = self.live_settings['speed']
                if original_speed != num:
                    self.live_settings['speed'] = num
                    setting_change = True
                else:
                    print("Same speed value, no change.")

        elif item == 'transpose_spin_button':
            num, ok = QInputDialog.getInt(self, item + "Pressed", "Enter the value [-12 - 12] for " + item)

            if num <= 12 or num >= -12:
                original_transpose = self.live_settings['transpose']
                if original_transpose != num:
                    self.live_settings['transpose'] = num
                    setting_change = True
                else:
                    print("Same transpose value, no change.")

        else:
            raise RuntimeError("Invalid button selected for messagebox")

        # manually pressed the spin button and places the value
        if setting_change is True:
            self.hide()
            self.pianobooster_buttons[item].click_input()
            self.pianobooster_buttons[item].type_keys('^a {DEL}' + str(num) + '{ENTER}')
            time.sleep(0.2)
            self.show()

        print("End of Message Box Usage")
        self.message_box_active = False

        if was_playing is True:
            print("Continuing the app")
            self.pianobooster_buttons['play_button'].click() # play button
            self.live_settings['playing_state'] = True
            self.live_settings['live_settings_change'] = True

        return None

    @pyqtSlot()
    def start_tutor_thread(self):
        # This function starts the tutoring thread. This is done after a signal,
        # which is the communication setup successful signal, to ensure that
        # the arduino and piano are ready for tutoring

        self.tutor = Tutor(self.file_container, self.data_bridge)
        self.tutor.start()

    def close_all_thread(self):
        # This functions account for if skore.py attempts to close skore_companion.py
        # This function terminates appropriately all the threads and then closes
        # the SKORE Companion Application

        print("SKORE application closes SKORE companion detected")

        print("Terminating all threads")
        try:
            self.comm.terminate()
        except AttributeError:
            print("Failure in Comm Termination")

        try:
            self.tutor.terminate()
        except AttributeError:
            print("Failure in Comms is acknowledge")

        # Closing communication ports
        print("Closing all Communication Ports")

        try:
            self.data_bridge.comm_data['midi_in'].close_port()
            self.data_bridge.comm_data['midi_out'].close_port()
            print("midi ports closed")
        except KeyError:
            print("Comm Thread not Initialized")
        except AttributeError:
            print("Failure in Comms is acknowledge")

        try:
            self.data_bridge.comm_data['arduino'].close()
            print("arduino port closed")
        except KeyError:
            print("Comm Thread not Initialized")
        except AttributeError:
            print("Failure in arduino.close()")

        self.close()
        return

#-------------------------------------------------------------------------------
# Main Code
"""
app = QApplication(sys.argv)
list = QStyleFactory.keys()
app.setStyle(QStyleFactory.create(list[2])) #Fusion
temp_file_container = FileContainer()
window = SkoreGlassGui(temp_file_container)
window.show()
sys.exit(app.exec_())
"""
