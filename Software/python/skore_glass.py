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
from skore_lib import setting_read, click_center_try, setting_write, rect_to_int, is_mid, output_address

warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2

# General Delay Values
comm_thread_delay = 0.001
tutor_thread_delay = 0.01
app_close_delay = 2

# Setup Variables
pia_app = []
all_qwidgets = []
all_qwidgets_names = []

message_box_active = 0

# SKORE Companion
timing_lineedit = ['time_per_tick','increment_counter','chord_timing_tolerance','manual_final_chord_sustain_timing']
timing_values = ['','','','']

# CommThread Variables
midi_in = []
midi_out = []
piano_size = []

# TutorThread Variables
current_keyboard_state = []
target_keyboard_state = []
wrong_notes = []
right_notes = []

sequence = []

chord_timing_tolerance = float(setting_read('chord_timing_tolerance'))
time_per_tick = float(setting_read('time_per_tick'))
increment_counter = int(setting_read("increment_counter"))

timeBeginPeriod = windll.winmm.timeBeginPeriod
timeBeginPeriod(1)

# Arduino Variables (within TutorThread)
arduino_keyboard = []
arduino = []
keyboard_shift = 0

# Timing Variables:
micro_per_beat_tempo = 0
PPQN = 0

############################LIVE TUTORING VARIABLES#############################
skill ='follow_you_button'
current_mode = 'beginner'
reset_flag = 0
hands = []
speed = []
transpose = []
start_bar_value = []
playing_state = False
restart = False
mode = []
live_setting_change = False
end_of_song_flag = 0

##################################GENERAL FUNCTIONS#############################

current_milli_time = lambda: int(round(time.time() * 1000))

#####################################PYQT5######################################

class AppOpenThread(QThread):
    # This thread deals with closure of the PianoBooster Application. Once the
    # application is closed, it will emit a signal to inform the SKORE Companion
    # application to close.

    app_close_signal = QtCore.pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def run(self):

        print("Piano Booster App State Thread Enabled")

        while(True):
            time.sleep(app_close_delay)

            if pia_app.is_process_running() == False:
                print("PianoBooster Application Closure Detection")
                self.app_close_signal.emit()

                break

################################################################################

class MidiEvent():
    # This class makes the midi event easier to understand and to obtain its
    # properties

    def __init__(self, _event_type, _data):
        self.event_type = _event_type
            # None -> delay
            # True -> TurnOnEvent
            # False -> TurnOffEvent
        if self.event_type == None:
            self.ticks = _data

        elif self.event_type == True or self.event_type == False:
            self.pitch = _data

    def __str__(self):
        if self.event_type == None:
            return '(' + str(self.event_type) + ',' + str(self.ticks) + ')'
        elif self.event_type == True or self.event_type == False:
            return '(' + str(self.event_type) + ',' + str(self.pitch) + ')'

    def __repr__(self):
        if self.event_type == None:
            return '(' + str(self.event_type) + ',' + str(self.ticks) + ')'
        elif self.event_type == True or self.event_type == False:
            return '(' + str(self.event_type) + ',' + str(self.pitch) + ')'

class TutorThread(QThread):
    # This thread performs the algorithm to control the LED lights with the
    # information of the other threads, such as the live tutoring variables.
    # The thread will include the code for the beginner, intermediate, and
    # expert mode.

    def __init__(self):
        QThread.__init__(self)

    def run(self):

        ################################MIDI FUNCTIONS##########################

        def midi_setup():
            # This fuction deletes pre-existing MIDI files and places the new desired MIDI
            # file into the cwd of tutor.py . Then it converts the midi information
            # of that file into a sequence of note events.

            global sequence
            mid_file = []

            cwd_path = os.path.dirname(os.path.abspath(__file__))
            if cwd_path == '' or cwd_path.find('SKORE') == -1:
                cwd_path = os.path.dirname(sys.argv[0])

            files = glob.glob(cwd_path + '\*')

            for file in files:
                if(is_mid(file)):
                    print("Deleted: " + str(file))
                    try:
                        os.remove(file)
                        break
                    except PermissionError:
                        raise RuntimeError("PianoBooster is restricting the removable of previous midi files")

            midi_file_location = setting_read('midi_file_location')

            new_midi_file_location, trash = output_address(midi_file_location, cwd_path, '.mid')
            copyfile(midi_file_location, new_midi_file_location)

            files = glob.glob(cwd_path + '\*')

            for file in files:
                if(is_mid(file)):
                    mid_file = file

            if mid_file == []:
                print("No midi file within the cwd: " + str(cwd_path))
                return 0

            # Obtaining the note event info for the mid file
            sequence = midi_to_note_event_info(mid_file)

            if sequence[0].event_type != None:
                sequence.insert(0,MidiEvent(None,0))

            #print(sequence)
            #print()
            return 1

        def midi_to_note_event_info(mid_file):
            # Now obtaining the pattern of the midi file found.
            global bpm, PPQN, micro_per_beat_tempo

            mid_file_name = os.path.basename(mid_file)
            pattern = read_midifile(mid_file)

            PPQN = pattern.resolution
            #print('PPQN: ', PPQN)

            note_event_matrix = []

            #print(pattern)

            for track in pattern:
                for event in track:
                    if isinstance(event, MetaEvent):
                        try:
                            tempo_info = event.data
                            #print(tempo_info)

                            if tempo_info != []:
                                for index, element in enumerate(tempo_info):
                                    micro_per_beat_tempo += element * 256 ** (2 - index)

                            print('micro_per_beat_tempo:', micro_per_beat_tempo)
                        except:
                            pass

                    if isinstance(event, NoteEvent):
                        if event.tick > 0:
                            #note_event_matrix.append('D,'+str(event.tick))
                            note_event_matrix.append(MidiEvent(None,event.tick))
                        if isinstance(event, NoteOffEvent):
                            #note_event_matrix.append('0,'+str(event.pitch))
                            note_event_matrix.append(MidiEvent(False, event.pitch))
                        else:
                            note_event_matrix.append(MidiEvent(True, event.pitch))
                            #note_event_matrix.append('1,'+str(event.pitch))

            return note_event_matrix

        ##############################UTILITY FUNCTIONS#########################

        def keyboard_valid():
            # This functions follows the confirmation system of PianoBooster
            # which determines if the keys pressed are acceptable compared to the
            # target keyboard configuration

            global right_notes
            acceptable = 1

            for note in target_keyboard_state:
                if note not in right_notes:
                    acceptable = 0
                    break

            if acceptable and len(wrong_notes) <= 1:
                right_notes = []
                #print("acceptable")
                return 1

            return 0

        #############################TUTORING UTILITY FUNCTIONS#################

        def determine_delay(index):

            #print("determine_delay_sequence:")
            #print(sequence[:index])
            #print()
            delay = 0

            for event in reversed(sequence[:index]):

                if event.event_type == None:
                    delay += event.ticks

                elif event.event_type == True:
                    return delay

            return delay

        def chord_detection(index):

            #print('index: ', index)
            #print("chord_detection:")
            #print(sequence[index:])
            #print()

            chord_delay = 0
            note_array = []
            is_chord = False
            final_index = index

            for index_tracker, event in enumerate(sequence[index:]):

                if event.event_type == None:
                    if event.ticks >= chord_timing_tolerance:
                        final_index += index_tracker - 1
                        break
                    else:
                        if chord_delay + event.ticks >= 25:
                            final_index += index_tracker - 1
                            break
                        else:
                            chord_delay += event.ticks

                elif event.event_type == True:
                    note_array.append(event.pitch)

            if len(note_array) > 1:
                is_chord = True

            return note_array, chord_delay, is_chord, final_index

        ##############################COMMUNICATION FUNCTIONS###################

        def arduino_comm(notes):
            # This function sends the information about which notes need to be added and
            # removed from the LED Rod.

            global arduino_keyboard, keyboard_shift

            #print("Arduino Comm Notes: " + str(notes))

            notes_to_add = []
            notes_to_remove = []

            #time.sleep(0.001)
            #print("Arduino Keyboard Pre-Communication: " + str(arduino_keyboard))

            if notes == []:
                notes_to_send = arduino_keyboard
                arduino_keyboard = []
                #print('sending *')
                arduino.write(b',*,#,')
                #time.sleep(0.05)

            else:
                for note in notes: # For Turning on a note
                    if note not in arduino_keyboard:
                        #print("Note Added: " + str(note))
                        notes_to_add.append(note)
                        arduino_keyboard.append(note)

                for note in arduino_keyboard: # for turning off a note
                    if note not in notes:
                        #print("Note Remove: " + str(note))
                        notes_to_remove.append(note)

                for note in notes_to_remove:
                    arduino_keyboard.remove(note)

                #print("notes_to_add: " + str(notes_to_add))
                #print("notes_to_remove: " + str(notes_to_remove))

                notes_to_send = notes_to_add + notes_to_remove
                notes_to_send.sort()

                # All transmitted notes are contain within the same string
                transmitted_string = ''
                non_shifted_string = ''

                for note in notes_to_send:
                    shifted_note = note - keyboard_shift + 1
                    transmitted_string += str(shifted_note) + ','
                    non_shifted_string += str(note) + ','

                transmitted_string = ',' + transmitted_string + ',#,'
                non_shifted_string = ',' + non_shifted_string + ',#,'

                #transmitted_string = transmitted_string[:-1] # to remove last note's comma
                #print("transmitted_string to Arduino: " + transmitted_string)
                #print("non_shifted_string to Arduino: " + non_shifted_string)
                #print("shifted_string to Arduino: " + transmitted_string)

                encoded_transmitted_string = transmitted_string.encode('utf-8')
                arduino.write(encoded_transmitted_string)

                #print("Post-Communication: " + str(arduino_keyboard))

            while(True):
                read_data = arduino.read()
                #print(read_data)
                if read_data == b'#':
                    print("recieved confirmation from arduino")
                    break

            return

        #################################TUTOR FUNCTIONS########################

        def tutor_beginner(starting_index):
            # This is practically the tutoring code for Beginner Mode

            global target_keyboard_state, playing_state, right_notes
            global wrong_notes, restart, arduino_keyboard, live_setting_change, transpose

            local_transpose_variable = 0
            target_keyboard_state = []
            right_notes = []
            wrong_notes = []
            arduino_keyboard = []

            delay_early_tolerance = 35 # < 40, > 25, > 30, > 35, < 37, < 36

            final_index = 0
            is_chord = False
            previous_turnon_event_index = 0

            for current_index, event in enumerate(sequence):

                #print(current_index,':',event)

                if starting_index > current_index:
                    continue

                if is_chord == True:
                    if current_index <= final_index:
                        # This is to account for the index shift if a chord is
                        # registered
                        continue
                    else:
                        is_chord = False

                # If Turn On Event
                if event.event_type == True:
                    print('##############################################################')
                    print('current_index:', current_index)

                    # Determine if chord and details
                    note_array, chord_delay, is_chord, final_index = chord_detection(current_index)
                    #print('Note/Chord Characteristics: ',note_array, chord_delay, is_chord, final_index)

                    for index, note in enumerate(note_array):
                        note_array[index] = transpose + note

                    target_keyboard_state = note_array

                    # Determine previous delay
                    delay = determine_delay(current_index)
                    #print('Pre-Note/Chord delay: ', delay, '  Millisecond version: (with tolerance) ', delay * delay_multiplier)

                    print('Target', target_keyboard_state)
                    arduino_comm(target_keyboard_state)
                    #print()

                    inital_time = current_milli_time()
                    #print('inital_time: ', inital_time)
                    timer = 0

                    #print(delay, PPQN, micro_per_beat_tempo)
                    second_delay = tick2second(delay - delay_early_tolerance, PPQN, micro_per_beat_tempo)
                    second_delay = round(second_delay * 1000 * 100/speed)
                    #print('second_delay:', second_delay)

                    # Waiting while loop
                    while(True):
                        time.sleep(tutor_thread_delay)

                        if live_setting_change:
                            live_setting_change = False

                            if restart == True:
                                arduino_comm([])
                                playing_state = True
                                restart = False
                                return 0

                            if current_mode != 'beginner':
                                arduino_comm([])
                                playing_state = False
                                print("changing tutoring mode")
                                return final_index + 1
                                #return previous_turnon_event_index

                            if local_transpose_variable != transpose:
                                print("Transpose Detected")
                                diff = transpose - local_transpose_variable
                                local_transpose_variable = transpose
                                for index, note in enumerate(target_keyboard_state):
                                    target_keyboard_state[index] = note + diff
                                    arduino_comm([])
                                    arduino_comm(target_keyboard_state)

                        if playing_state:
                            timer = current_milli_time() - inital_time
                            #print(timer)

                            if timer >= second_delay:
                                #print('ready')
                                if keyboard_valid():
                                    target_keyboard_state = []
                                    #arduino_comm([])
                                    break
                            else:
                                right_notes = []

                        else:
                            inital_time = current_milli_time()

                            if timer != 0:
                                # if user paused, account for the passed time
                                # in the timer
                                second_delay -= timer
                                timer = 0

                    previous_turnon_event_index = current_index

            # Outside of large For Loop
            arduino_comm([])
            playing_state = False
            print("end of song")
            return 0

        def tutor_intermediate(starting_index):
            #print(starting_index)
            #print("intermediate")
            return starting_index

        def tutor_expert(starting_index):
            #print(starting_index)
            #print('expert')
            return starting_index

        ###############################MAIN RUN CODE############################

        global restart

        tutoring_index = 0

        midi_setup()

        while (True):
            if current_mode == 'beginner':
                tutoring_index = tutor_beginner(tutoring_index)
            elif current_mode == 'intermediate':
                tutoring_index = tutor_intermediate(tutoring_index)
            elif current_mode == 'expert':
                tutoring_index = tutor_expert(tutoring_index)

            while(not playing_state):
                #print("completion of tutoring mode")
                time.sleep(0.1)

        return

################################################################################

class CommThread(QThread):
    # This thread initializes the communication between the piano, virtual midi,
    # and arduino. Additionally, it continuously keeping tracking of the current
    # state of the piano and relays the information recieved from the piano to
    # the virtual port. Look to the communication diagram for further explanation.

    comm_setup_signal = QtCore.pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def run(self):

        ############################COMM SETUP FUNCTION#########################

        def arduino_setup():
            # This functions sets up the communication between Python and the Arduino.
            # For now the Arduino is assumed to be connected to COM3.

            global arduino
            global piano_size
            global keyboard_shift

            whitekey = []
            blackkey = []
            whitekey_transmitted_string = ''
            blackkey_transmitted_string = ''
            piano_size = setting_read('piano_size') + ','

            if piano_size == 'S,':
                keyboard_shift = 36
                size_message = '61,'
            elif piano_size == 'M,':
                keyboard_shift = 36
                size_message = '76,'
            elif piano_size == 'L,':
                keyboard_shift = 36
                size_message = '88,'

            # Closing, if applicable, the arduino port
            if arduino != []:
                arduino.close()
                arduino = []

            try:
                com_port = setting_read("arduino_com_port")
                print("COM Port Selected: " + str(com_port))

                arduino = serial.Serial(com_port, 230400, writeTimeout = 0)
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


                print("Data Transmitted to the Arduino for Setup:")
                print("Piano Size: " + str(piano_size))
                print("WhiteKey Colors: " + str(whitekey_transmitted_string))
                print("BlackKey Colors: " + str(blackkey_transmitted_string))

                setup_transmitted_string = size_message + whitekey_transmitted_string + blackkey_transmitted_string
                #setup_transmitted_string = setup_transmitted_string.replace(' ','')
                setup_transmitted_string = setup_transmitted_string + ',#,'

                time.sleep(2)
                print("Setup String:" + setup_transmitted_string)
                arduino.write(setup_transmitted_string.encode('utf-8'))
                time.sleep(2)

                while(True):
                    read_data = arduino.read()
                    #print(read_data)
                    if read_data == b'#':
                        print("recieved confirmation from arduino")
                        break

                return 1

            except serial.serialutil.SerialException:
                print("Arduino Not Found")
                return 0

        def piano_port_setup():
            # This function sets up the communication between Python and the MIDI device
            # For now Python will connect the first listed device.

            import difflib
            global midi_in, midi_out

            if midi_in != [] and midi_out != []:
                midi_in.close_port()
                midi_out.close_port()
                midi_in = []
                midi_out = []

            try:
                midi_in = rtmidi.MidiIn()
                in_avaliable_ports = midi_in.get_ports()
                selected_port = setting_read("piano_port")
                closes_match_in_port = difflib.get_close_matches(selected_port, in_avaliable_ports)[0]
                print("Piano Port: " + str(closes_match_in_port))
                midi_in.open_port(in_avaliable_ports.index(closes_match_in_port))
            except:
                print("Piano Port Setup Failure")
                midi_in = []
                midi_out = []
                return 0

            try:
                midi_out = rtmidi.MidiOut()
                out_avaliable_ports = midi_out.get_ports()
                closes_match_out_port = difflib.get_close_matches('LoopBe Internal MIDI',out_avaliable_ports)[0]
                print("LoopBe Internal Port: " + str(closes_match_out_port))
                midi_out.open_port(out_avaliable_ports.index(closes_match_out_port))
                return 1
            except:
                print("LoopBe Internal Port Setup Failure")
                midi_in = []
                midi_out = []

            return 0

        #############################UTILITY FUNCTIONS##########################

        def safe_change_current_keyboard_state(pitch, state):
            # This function safely removes or adds the pitch to the
            # current_keyboard_state variable

            if state == 1:
                if pitch in current_keyboard_state:
                    return
                current_keyboard_state.append(pitch)

            elif state == 0:
                if pitch not in current_keyboard_state:
                    return
                current_keyboard_state.remove(pitch)

            return

        #############################MAIN CODE##################################

        print("Piano and Arduino Communication Thread Enabled")

        arduino_status = arduino_setup()
        piano_status = piano_port_setup()

        if arduino_status and piano_status:
            print("Piano and Arduino Communication Setup Successful")
            self.comm_setup_signal.emit()

            try:
                while(True):
                    time.sleep(comm_thread_delay)
                    message = midi_in.get_message()

                    if message:
                        note_info, delay = message
                        #print(note_info)
                        midi_out.send_message(note_info)

                        if note_info[0] == 144: # Note ON event
                            #current_keyboard_state.append(note_info[1])
                            safe_change_current_keyboard_state(note_info[1],1)
                            if note_info[1] in target_keyboard_state:
                                if note_info[1] not in right_notes:
                                    right_notes.append(note_info[1])
                            else:
                                if note_info[1] not in wrong_notes:
                                    wrong_notes.append(note_info[1])

                        else: # Note OFF event
                            #current_keyboard_state.remove(note_info[1])
                            safe_change_current_keyboard_state(note_info[1],0)
                            if note_info[1] in right_notes:
                                right_notes.remove(note_info[1])
                            elif note_info[1] in wrong_notes:
                                wrong_notes.remove(note_info[1])

                        #print('current_keyboard_state: ' + str(current_keyboard_state))

            except AttributeError:
                print("Lost Piano Communication")

        return

################################################################################

class TransparentButton(QPushButton):
    # This class is custom version of QPushButton that is transparent

    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        self.button_state = 'enabled'

        op=QGraphicsOpacityEffect(self)
        op.setOpacity(0.01)
        self.setGraphicsEffect(op)
        self.setAutoFillBackground(True)

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

class SkoreGlassGui(QMainWindow):
    # This class creates the transparent GUI overlay that rests ontop of PianoBooster.
    # It initalizises PianoBooster, the communication systems, and buttons that
    # manipulate PianoBooster

    button_signal = QtCore.pyqtSignal('QString', 'int')
    local_button_list = []

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        #self.setWindowOpacity(0.5) # 0 does not work
        #self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint )
        #self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        self.piano_booster_setup()
        self.setupTransparentUI()
        self.setupMenuBar()
        self.setupVisibleUI()
        self.setupThread()

    def setupTransparentUI(self):
        # This functions sets up all the transparent GUI

        global local_button_list

        #self.book_combo_button = QPushButton(self)
        #self.book_combo_button = TransparentButton(self)
        #self.song_combo_button = TransparentButton(self)
        self.book_combo_button = DisabledButton(self)
        self.song_combo_button = DisabledButton(self)

        self.listen_button = TransparentButton(self)

        #self.follow_you_button = TransparentButton(self)
        #self.play_along_button = TransparentButton(self)

        self.follow_you_button = DisabledButton(self)
        self.play_along_button = DisabledButton(self)

        self.restart_button = TransparentButton(self)
        self.play_button = TransparentButton(self)
        self.speed_spin_button = TransparentButton(self)
        self.transpose_spin_button = TransparentButton(self)

        #self.looping_bars_popup_button = TransparentButton(self)
        #self.start_bar_spin_button = TransparentButton(self)

        self.looping_bars_popup_button = DisabledButton(self)
        self.start_bar_spin_button = DisabledButton(self)


        self.menubar_button = TransparentButton(self)

        #self.parts_selection_button = TransparentButton(self)
        #self.parts_mute_button = TransparentButton(self)
        #self.parts_slider_button = TransparentButton(self)

        self.parts_selection_button = DisabledButton(self)
        self.parts_mute_button = DisabledButton(self)
        self.parts_slider_button = DisabledButton(self)

        self.right_hand_button = TransparentButton(self)
        self.both_hands_button = TransparentButton(self)
        self.left_hand_button = TransparentButton(self)

        #self.slider_hand = TransparentButton(self)

        self.slider_hand = DisabledButton(self)

        self.key_combo_button = TransparentButton(self)
        self.major_button = TransparentButton(self)
        #self.save_bar_button = TransparentButton(self)

        self.save_bar_button = DisabledButton(self)

        self.book_combo_button.setObjectName('book_combo_button')
        self.song_combo_button.setObjectName('song_combo_button')
        self.listen_button.setObjectName('listen_button')
        self.follow_you_button.setObjectName('follow_you_button')
        self.play_along_button.setObjectName('play_along_button')
        self.restart_button.setObjectName('restart_button')
        self.play_button.setObjectName('play_button')
        self.speed_spin_button.setObjectName('speed_spin_button')
        self.transpose_spin_button.setObjectName('transpose_spin_button')
        self.looping_bars_popup_button.setObjectName('looping_bars_popup_button')
        self.start_bar_spin_button.setObjectName('start_bar_spin_button')
        self.menubar_button.setObjectName('menubar_button')
        self.parts_selection_button.setObjectName('parts_selection_button')
        self.parts_mute_button.setObjectName('parts_mute_button')
        self.parts_slider_button.setObjectName('parts_slider_button')
        self.right_hand_button.setObjectName('right_hand_button')
        self.both_hands_button.setObjectName('both_hands_button')
        self.left_hand_button.setObjectName('left_hand_button')
        self.slider_hand.setObjectName('slider_hand')
        self.key_combo_button.setObjectName('key_combo_button')
        self.major_button.setObjectName('major_button')
        self.save_bar_button.setObjectName('save_bar_button')

        self.local_buttonGroup = QButtonGroup()
        self.local_buttonGroup.setExclusive(True)
        self.local_buttonGroup.addButton(self.book_combo_button)
        self.local_buttonGroup.addButton(self.song_combo_button)
        self.local_buttonGroup.addButton(self.listen_button)
        self.local_buttonGroup.addButton(self.follow_you_button)
        self.local_buttonGroup.addButton(self.play_along_button)
        self.local_buttonGroup.addButton(self.restart_button)
        self.local_buttonGroup.addButton(self.play_button)
        self.local_buttonGroup.addButton(self.speed_spin_button)
        self.local_buttonGroup.addButton(self.transpose_spin_button)
        self.local_buttonGroup.addButton(self.looping_bars_popup_button)
        self.local_buttonGroup.addButton(self.start_bar_spin_button)
        self.local_buttonGroup.addButton(self.menubar_button)
        self.local_buttonGroup.addButton(self.parts_selection_button)
        self.local_buttonGroup.addButton(self.parts_mute_button)
        self.local_buttonGroup.addButton(self.parts_slider_button)
        self.local_buttonGroup.addButton(self.right_hand_button)
        self.local_buttonGroup.addButton(self.both_hands_button)
        self.local_buttonGroup.addButton(self.left_hand_button)
        self.local_buttonGroup.addButton(self.slider_hand)
        self.local_buttonGroup.addButton(self.key_combo_button)
        self.local_buttonGroup.addButton(self.major_button)
        self.local_buttonGroup.addButton(self.save_bar_button)


        local_button_list = [self.book_combo_button, self.song_combo_button, self.listen_button,
                            self.follow_you_button, self.play_along_button, self.restart_button,
                            self.play_button, self.speed_spin_button, self.transpose_spin_button,
                            self.looping_bars_popup_button, self.start_bar_spin_button,
                            self.menubar_button, self.parts_selection_button, self.parts_mute_button,
                            self.parts_slider_button, self.right_hand_button, self.both_hands_button,
                            self.left_hand_button, self.slider_hand, self.key_combo_button,
                            self.major_button, self.save_bar_button]


        self.local_button_set_geometry()

        self.local_buttonGroup.buttonClicked.connect(self.button_click)
        self.button_signal.connect(self.create_message_box)

    def setupVisibleUI(self):
        # This functions sets up all the visible GUI

        self.setStyleSheet("""
            background-color: rgb(50,50,50);
            color: white;
            """)

        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(1400,700,400,230))
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setObjectName("tabWidget")

        self.tabWidget.setStyleSheet("""
                QTabBar::tab {background: rgb(50,50,50);}
                QTabBar::tab:!selected {background: rgb(40,40,40);}
                QTabWidget>QWidget>QWidget{background: rgb(50,50,50);}""")

        self.tabWidget.setAutoFillBackground(True)

        self.tutor_mode_tab = QtWidgets.QWidget()
        self.tutor_mode_tab.setObjectName("tutor_mode_tab")
        self.tabWidget.addTab(self.tutor_mode_tab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tutor_mode_tab), "Tutor Mode")

        # Tutor Mode Tab
        self.tutor_label = QtWidgets.QLabel(self.tutor_mode_tab)
        self.tutor_label.setGeometry(QtCore.QRect(10,5,381,20))
        self.tutor_label.setObjectName("tutor_label")
        self.tutor_label.setText("Select or change Tutoring Mode")

        # Tutoring Mode
        self.beginner_companion_pushButton = QtWidgets.QPushButton(self.tutor_mode_tab)
        self.beginner_companion_pushButton.setGeometry(QtCore.QRect(10,30,381,51))
        self.beginner_companion_pushButton.setObjectName("beginner_companion_pushButton")
        self.beginner_companion_pushButton.setText("Beginner Mode")

        self.intermediate_companion_pushButton = QtWidgets.QPushButton(self.tutor_mode_tab)
        self.intermediate_companion_pushButton.setGeometry(QtCore.QRect(10,85,381,51))
        self.intermediate_companion_pushButton.setObjectName("intermediate_companion_pushButton")
        self.intermediate_companion_pushButton.setText("Intermediate Mode")

        self.expert_companion_pushButton = QtWidgets.QPushButton(self.tutor_mode_tab)
        self.expert_companion_pushButton.setGeometry(QtCore.QRect(10,140,381,51))
        self.expert_companion_pushButton.setObjectName("expert_companion_pushButton")
        self.expert_companion_pushButton.setText("Expert Mode")

        # Timing Mode Tab
        self.timing_tab = QtWidgets.QWidget()
        self.timing_tab.setObjectName("timing_mode_tab")
        self.tabWidget.addTab(self.timing_tab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.timing_tab), "Timing Settings")

        time_per_tick_y_value = 10
        increment_counter_y_value = time_per_tick_y_value + 40
        chord_timing_tolerance_y_value = increment_counter_y_value + 40
        manual_final_chord_sustain_y_value = chord_timing_tolerance_y_value + 40
        lineEdit_length = 120

        self.time_per_tick_label = QtWidgets.QLabel(self.timing_tab)
        self.time_per_tick_label.setGeometry(QtCore.QRect(20, time_per_tick_y_value, 91, 16))
        self.time_per_tick_label.setObjectName("time_per_tick_label")
        self.time_per_tick_label.setText("Time per Tick:")
        self.time_per_tick_lineEdit = QtWidgets.QLineEdit(self.timing_tab)
        self.time_per_tick_lineEdit.setGeometry(QtCore.QRect(250, time_per_tick_y_value, lineEdit_length, 22))
        self.time_per_tick_lineEdit.setObjectName("time_per_tick_lineEdit")

        self.increment_counter_label = QtWidgets.QLabel(self.timing_tab)
        self.increment_counter_label.setGeometry(QtCore.QRect(20, increment_counter_y_value, 151 , 16))
        self.increment_counter_label.setObjectName("increment_counter_label")
        self.increment_counter_label.setText("Increment Counter Value:")

        self.increment_counter_lineEdit = QtWidgets.QLineEdit(self.timing_tab)
        self.increment_counter_lineEdit.setGeometry(QtCore.QRect(250, increment_counter_y_value, lineEdit_length, 22))
        self.increment_counter_lineEdit.setObjectName("increment_counter_lineEdit")

        self.chord_timing_tolerance_label = QtWidgets.QLabel(self.timing_tab)
        self.chord_timing_tolerance_label.setGeometry(QtCore.QRect(20, chord_timing_tolerance_y_value, 151, 16))
        self.chord_timing_tolerance_label.setObjectName("chord_timing_tolerance_label")
        self.chord_timing_tolerance_label.setText("Chord Timing Tolerance:")
        self.chord_timing_tolerance_lineEdit = QtWidgets.QLineEdit(self.timing_tab)
        self.chord_timing_tolerance_lineEdit.setGeometry(QtCore.QRect(250, chord_timing_tolerance_y_value, lineEdit_length, 22))
        self.chord_timing_tolerance_lineEdit.setObjectName("chord_timing_tolerance_lineEdit")

        self.manual_final_chord_sustain_timing_label = QtWidgets.QLabel(self.timing_tab)
        self.manual_final_chord_sustain_timing_label.setGeometry(QtCore.QRect(20, manual_final_chord_sustain_y_value, 211, 16))
        self.manual_final_chord_sustain_timing_label.setObjectName("manual_final_chord_sustain_timing_label")
        self.manual_final_chord_sustain_timing_label.setText("Manual Final Chord Sustain Timing Value:")
        self.manual_final_chord_sustain_timing_lineEdit = QtWidgets.QLineEdit(self.timing_tab)
        self.manual_final_chord_sustain_timing_lineEdit.setGeometry(QtCore.QRect(250, manual_final_chord_sustain_y_value, lineEdit_length, 22))
        self.manual_final_chord_sustain_timing_lineEdit.setObjectName("manual_final_chord_sustain_timing_lineEdit")

        self.apply_pushButton = QtWidgets.QPushButton(self.timing_tab)
        self.apply_pushButton.setGeometry(QtCore.QRect(250, 170, lineEdit_length, 25))
        self.apply_pushButton.setObjectName("apply_pushButton")
        self.apply_pushButton.setText("Apply")
        self.apply_pushButton.clicked.connect(self.apply_timing_values)

        # Tutoring Mode Function Assignment
        self.beginner_companion_pushButton.clicked.connect(self.beginner_mode_setting)
        self.intermediate_companion_pushButton.clicked.connect(self.intermediate_mode_setting)
        self.expert_companion_pushButton.clicked.connect(self.expert_mode_setting)

        # Timing Tab Initialization
        self.settings_timing_read()
        self.update_timing_values()

        return

    def setupThread(self):
        # This functions initalizes the communication threads between PianoBooster,
        # the piano, and the arduino.

        # Initializing PianoBooster App Open Check MultiThreading
        self.check_open_app_thread = AppOpenThread()
        self.check_open_app_thread.app_close_signal.connect(self.close_all_thread)
        self.check_open_app_thread.start()

        # Initializing Piano and Arduino Communication
        self.comm_thread = CommThread()
        self.comm_thread.comm_setup_signal.connect(self.start_tutoring_thread)
        self.comm_thread.start()

        return

    def setupMenuBar(self):
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

        menubar_button_list = [self.view_menubar_button, self.song_menubar_button,
                                self.setup_menubar_button, self.help_menubar_button]

        self.menubar_button_set_geometry()
        self.menubar_buttonGroup.buttonClicked.connect(self.menubar_click)

        return

    def local_button_set_geometry(self):
        # This function assigns the corresponding transparent buttons to the
        # visible pianobooster buttons that are intended to be keep enabled.

        for i in range(len(local_button_list)):
            if str(local_button_list[i].objectName()) == 'menubar_button':
                dimensions = all_qwidgets[i].rectangle()
                width = int((dimensions.right - dimensions.left)*0.02)
                local_button_list[i].setGeometry(QRect(dimensions.left, dimensions.top, width, dimensions.bottom - dimensions.top))
                continue

            dimensions = all_qwidgets[i].rectangle()
            local_button_list[i].setGeometry(QRect(dimensions.left, dimensions.top, dimensions.right - dimensions.left, dimensions.bottom - dimensions.top))

        return

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
        return

    def beginner_mode_setting(self):
        # This function selects the tutoring mode to beginner

        global current_mode, live_setting_change, playing_state

        if current_mode == 'beginner':
            return

        current_mode = 'beginner'
        live_setting_change = True

        #all_qwidgets[5].click()
        if playing_state:
            all_qwidgets[6].click() # play_button
            playing_state = False
        all_qwidgets[3].click() # follow_you_button

        return

    def intermediate_mode_setting(self):
        # This function selects the tutoring mode to intermediate

        global current_mode, live_setting_change, playing_state

        if current_mode == 'intermediate':
            return

        current_mode = 'intermediate'
        live_setting_change = True

        #all_qwidgets[5].click()
        if playing_state:
            all_qwidgets[6].click() # play_button
            playing_state = False
        all_qwidgets[4].click() # play_along_button

        return

    def expert_mode_setting(self):
        # This function selects the tutoring mode to expert

        global current_mode, live_setting_change, playing_state

        if current_mode == 'expert':
            return

        current_mode = 'expert'
        live_setting_change = True

        #all_qwidgets[5].click()
        if playing_state:
            all_qwidgets[6].click() # play_button
            playing_state = False
        all_qwidgets[4].click() # play_along_button

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

        global live_setting_change

        self.settings_timing_read()

        for i in range(len(timing_lineedit)):
            lineEdit_attribute = getattr(self, timing_lineedit[i] + '_lineEdit')
            text = lineEdit_attribute.text()
            if timing_values[i] != text:
                timing_values[i] = text
                current_setting = setting_read(timing_lineedit[i])
                if current_setting != text:
                    setting_write(timing_lineedit[i], timing_values[i])
                    live_setting_change = True
        return

    def button_click(self, button):
        # This function clicks on the corresponding PianoBooster button once
        # a transparent and enabled button

        global skill, hands, speed, transpose, start_bar_value, playing_state
        global restart, live_setting_change, current_mode

        button_name = str(button.objectName())
        button_attribute = getattr(self,button_name)

        if button_attribute.button_state == 'disabled':
            return

        #for index,qwidget in enumerate(local_button_list):
        #    if qwidget == button_attribute:
        #        desired_index = index
        #        break

        if button_name == 'play_button':
            all_qwidgets[6].click() # play_button
            playing_state = not playing_state
            #live_setting_change = True
            print("Playing State: " + str(playing_state))

        elif button_name == 'restart_button':
            all_qwidgets[5].click() # restart_button
            playing_state = True
            restart = True
            live_setting_change = True
            print("Restart Pressed")

        elif button_name == 'listen_button':
            all_qwidgets[2].click() # follow_you_button
            #skill = button_name
            current_mode = 'intermediate'
            live_setting_change = True
            print(button_name + " pressed")

        elif button_name == 'speed_spin_button' or button_name == 'transpose_spin_button': #or button_name == 'start_bar_spin_button':
            if message_box_active == 0:
                if button_name == 'speed_spin_button':
                    desired_index = 7
                else:
                    desired_index = 8
                self.button_signal.emit(button_name, desired_index)
            else:
                print("QInputDialog in use")
        #else:
        #    all_qwidgets[desired_index].click()

    def menubar_click(self, button):
        # This function clicks on the assigned buttons that are the coordinate
        # buttons.

        button_name = str(button.objectName())
        x_coord, y_coord = win32api.GetCursorPos()
        print(x_coord,',',y_coord)

        self.hide()
        self.click(x_coord,y_coord)
        self.click(x_coord,y_coord)
        time.sleep(0.01)
        self.show()

        return

    def click(self,x,y):
        # This function manually clicks on a set of x and y coordinates

        win32api.SetCursorPos((x,y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
        return

    @pyqtSlot('QString', 'int')
    def create_message_box(self, item, desired_index):
        # This function creates a QInputDialog box for the user to input
        # multivalue information, such as speed and transpose

        global speed, transpose, message_box_active, playing_state, speed, transpose
        global live_setting_change, start_bar_value

        flag = 0
        unacceptable_value_flag = 0

        # Stopping the application
        if playing_state == True:
            flag = 1
            print("Stoping app")
            all_qwidgets[6].click() # play button
            playing_state = False
            #live_setting_change = True

        # Asking user for value of spin button
        message_box_active = 1

        if item == 'speed_spin_button':
            num, ok = QInputDialog.getInt(self, item + "Pressed", "Enter the value [20 - 200] for " + item)
            if num > 200 or num < 20:
                unacceptable_value_flag = 1
        elif item == 'transpose_spin_button':
            num, ok = QInputDialog.getInt(self, item + "Pressed", "Enter the value [-12 - 12] for " + item)
            if num > 12 or num < -12:
                unacceptable_value_flag = 1
        else:
            num, ok = QInputDialog.getDouble(self, item + "Pressed", "Enter the value [0 - 999.9] for " + item)
            if num > 999.9 or num < 0:
                unacceptable_value_flag = 1

        # Processing data entered from QInputDialog
        if ok and not unacceptable_value_flag:
            if item == 'speed_spin_button':
                speed = num
                #live_setting_change = True
            elif item == 'transpose_spin_button':
                transpose = num
                print("Transpose: ", transpose)
                live_setting_change = True
            elif item == 'start_bar_spin_button':
                start_bar_value = num
                #live_setting_change = True

            # manually pressed the spin button and places the value
            self.hide()
            all_qwidgets[desired_index].click_input()
            all_qwidgets[desired_index].type_keys('^a {DEL}' + str(num) + '{ENTER}')
            time.sleep(0.2)
            self.show()

        print("End of Message Box Usage")
        message_box_active = 0

        if flag == 1:
            print("Continuing the app")
            #all_qwidgets[8].click()
            all_qwidgets[6].click() # play button
            playing_state = True
            live_setting_change = True

        return

    @pyqtSlot()
    def start_tutoring_thread(self):
        # This function starts the tutoring thread. This is done after a signal,
        # which is the communication setup successful signal, to ensure that
        # the arduino and piano are ready for tutoring

        self.tutor_thread = TutorThread()
        self.tutor_thread.start()

    def close_all_thread(self):
        # This functions account for if skore.py attempts to close skore_companion.py
        # This function terminates appropriately all the threads and then closes
        # the SKORE Companion Application

        print("SKORE application closes SKORE companion detected")

        print("Terminating all threads")
        self.comm_thread.terminate()

        try:
            self.tutor_thread.terminate()
        except AttributeError:
            print("Failure in Comms is acknowledge")

        # Closing communication ports
        print("Closing all Communication Ports")
        try:
            midi_in.close_port()
            midi_out.close_port()
            print("midi ports closed")
        except AttributeError:
            print("Failure in Comms is acknowledge")

        try:
            arduino.close()
            print("arduino port closed")
        except:
            print("Failure in arduino.close()")

        self.close()
        return

    def retrieve_name(self, var):
        # This function returns the actual name of the variable called var

        callers_local_vars = inspect.currentframe().f_back.f_locals.items()
        return [var_name for var_name, var_val in callers_local_vars if var_val is var]

    def piano_booster_setup(self):
        # This function performs the task of opening PianoBooster and appropriately
        # clicking on the majority of the qwidgets to make them addressable. When
        # PianoBooster is opened, the qwidgets are still not addressible via
        # pywinauto. For some weird reason, clicked on them enables them. The code
        # utilizes template matching to click on specific regions of the PianoBooster
        # GUI

        global all_qwidgets, all_qwidgets_names, int_dimensions, pia_app, speed, transpose

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
        while(True):
            try:
                for i in range(len(possible_handles)):
                    key = str(possible_handles[i])
                    if(key.find('Piano Booster') != -1):
                        wanted_key = key
                        #print('Found it ' + key)

                first_index = wanted_key.find("'")
                last_index = wanted_key.find(',')
                pia_app_title = wanted_key[first_index + 1 :last_index - 1]
                break

            except UnboundLocalError:
                time.sleep(0.1)


        # Once with the handle, control over the window is achieved.
        while(True):
            try:
                w_handle = pywinauto.findwindows.find_windows(title=pia_app_title)[0]
                window = pia_app.window(handle=w_handle)
                break
            except IndexError:
                time.sleep(0.1)

        # Initializion of the Qwidget within the application
        window.maximize()
        time.sleep(0.5)

        rect_dimensions = window.rectangle()
        unique_int_dimensions = rect_to_int(rect_dimensions)

        click_center_try('skill_groupBox_pia', unique_int_dimensions)
        click_center_try('hands_groupBox_pia', unique_int_dimensions)
        click_center_try('book_song_buttons_pia', unique_int_dimensions)
        click_center_try('flag_button_pia', unique_int_dimensions)
        click_center_try('part_button_pia', unique_int_dimensions)

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
        try:
            menubar_button = main_qwidget[u'3']
        except:
            try:
                menubar_button = main_qwidget.QWidget34
            except:
                raise RuntimeError("Main Menu QWidget Missed")

        key_combo_button = main_qwidget.keyCombo
        play_button = main_qwidget.playButton
        restart_button = main_qwidget.playFromStartButton
        save_bar_button = main_qwidget.savebarButton
        speed_spin_button = main_qwidget.speedSpin
        start_bar_spin_button = main_qwidget.startBarSpin
        transpose_spin_button = main_qwidget.transposeSpin
        looping_bars_popup_button = main_qwidget.loopingBarsPopupButton
        major_button = main_qwidget.majorCombo

        # Creating list easily address each qwidget
        all_qwidgets = [book_combo_button, song_combo_button, listen_button,
                            follow_you_button, play_along_button, restart_button,
                            play_button, speed_spin_button, transpose_spin_button,
                            looping_bars_popup_button, start_bar_spin_button,
                            menubar_button, parts_selection_button, parts_mute_button,
                            parts_slider_button, right_hand_button, both_hands_button,
                            left_hand_button, slider_hand, key_combo_button,
                            major_button, save_bar_button]

        all_qwidgets_names = []

        for i in range(len(all_qwidgets)):
            all_qwidgets_names.append(self.retrieve_name(all_qwidgets[i])[0])

        delay = 0.4
        #listen_button.click()
        follow_you_button.click()
        both_hands_button.click()

        # Opening the .mid file
        time.sleep(delay)
        click_center_try('file_button_xeno', unique_int_dimensions)
        time.sleep(delay)
        click_center_try('open_button_pianobooster_menu', unique_int_dimensions)
        time.sleep(delay)

        while(True):
            try:
                o_handle = pywinauto.findwindows.find_windows(title='Open Midi File')[0]
                o_window = pia_app.window(handle = o_handle)
                break
            except IndexError:
                time.sleep(0.1)

        mid_file_path = setting_read('midi_file_location')
        o_window.type_keys(mid_file_path)
        o_window.type_keys('{ENTER}')

        click_center_try('skill_groupBox_pia', unique_int_dimensions)
        speed_spin_button.click_input()
        speed_spin_button.type_keys('^a {DEL}100{ENTER}')
        speed = 100
        transpose = 0
        click_center_try('skill_groupBox_pia', unique_int_dimensions)
        return

################################################################################

"""
app = QApplication(sys.argv)
list = QStyleFactory.keys()
app.setStyle(QStyleFactory.create(list[2])) #Fusion
window = SkoreGlassGui()
window.show()
sys.exit(app.exec_())
"""
