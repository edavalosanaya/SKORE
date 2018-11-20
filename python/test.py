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
from midi import read_midifile, NoteEvent, NoteOffEvent
from skore_program_controller import is_mid,setting_read,output_address
import serial
import serial.tools.list_ports
import glob
from ctypes import windll
import rtmidi
from shutil import copyfile

# SKORE Library
from skore_program_controller import setting_read, click_center_try, setting_write, rect_to_int

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

############################LIVE TUTORING VARIABLES#############################
skill ='follow_you_button'
current_mode = 'beginner'
reset_flag = 0
hands = []
speed = []
tranpose = []
start_bar_value = []

#playing_state = False
playing_state = True

restart = False
mode = []
live_setting_change = False
end_of_song_flag = 0

################################################################################

current_milli_time = lambda: int(round(time.time() * 1000))

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

    print("Sequence (None = delay, True = TurnOnEvent, False = TurnOffEvent)")
    print(sequence)
    print()
    return 1

def midi_to_note_event_info(mid_file):
    # Now obtaining the pattern of the midi file found.

    mid_file_name = os.path.basename(mid_file)
    pattern = read_midifile(mid_file)

    note_event_matrix = []

    #print(pattern)

    for track in pattern:
        for event in track:
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

    #print(sequence[:index])
    delay = 0

    for event in reversed(sequence[:index]):

        if event.event_type == None:
            delay += event.ticks

        elif event.event_type == True:
            return delay

    return delay

def chord_detection(index):

    #print('index: ', index)
    #print(sequence[index:])

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

    print("Arduino Comm Notes: " + str(notes))

    notes_to_add = []
    notes_to_remove = []

    time.sleep(0.001)
    print("Arduino Keyboard Pre-Communication: " + str(arduino_keyboard))

    if notes == []:
        notes_to_send = arduino_keyboard
        arduino_keyboard = []
        arduino.write(b'*')
        return

    else:
        for note in notes: # For Turning on a note
            if note not in arduino_keyboard:
                print("Note Added: " + str(note))
                notes_to_add.append(note)
                arduino_keyboard.append(note)

        for note in arduino_keyboard: # for turning off a note
            if note not in notes:
                print("Note Remove: " + str(note))
                notes_to_remove.append(note)

        for note in notes_to_remove:
            arduino_keyboard.remove(note)

        print("notes_to_add: " + str(notes_to_add))
        print("notes_to_remove: " + str(notes_to_remove))

        notes_to_send = notes_to_add + notes_to_remove
        notes_to_send.sort()

    # All transmitted notes are contain within the same string
    transmitted_string = ''
    non_shifted_string = ''

    for note in notes_to_send:
        shifted_note = note - keyboard_shift + 1
        transmitted_string += str(shifted_note) + ','
        non_shifted_string += str(note) + ','

    transmitted_string = ',' + transmitted_string
    non_shifted_string = ',' + non_shifted_string

    #transmitted_string = transmitted_string[:-1] # to remove last note's comma
    #print("transmitted_string to Arduino: " + transmitted_string)
    print("non_shifted_string to Arduino: " + non_shifted_string)
    print("shifted_string to Arduino: " + transmitted_string)


    b = transmitted_string.encode('utf-8')
    #print(b)
    #b2 = bytes(transmitted_string, 'utf-8')
    arduino.write(b)

    print("Post-Communication: " + str(arduino_keyboard))

    return

#################################TUTOR FUNCTIONS########################

def tutor_beginner():
    # This is practically the tutoring code for Beginner Mode

    global target_keyboard_state, playing_state, right_notes
    global wrong_notes, restart, arduino_keyboard

    target_keyboard_state = []
    right_notes = []
    wrong_notes = []
    arduino_keyboard = []

    final_index = 0
    is_chord = False

    for current_index, event in enumerate(sequence):

        if is_chord == True:
            if current_index <= final_index:
                # This is to account for the index shift if a chord is
                # registered
                continue
            else:
                is_chord = False

        # If Turn On Event
        if event.event_type == True:
            print('current_index', current_index)

            # Determine if chord and details
            note_array, chord_delay, is_chord, final_index = chord_detection(current_index)
            print('Note/Chord Characteristics: ',note_array, chord_delay, is_chord, final_index)
            target_keyboard_state = note_array

            # Determine previous delay
            delay = determine_delay(current_index)
            print('Pre-Note/Chord delay: ', delay, '  Millisecond version: (with tolerance) ', delay*10 - 25)

            print('Target', target_keyboard_state)
            #arduino_comm(target_keyboard_state)
            print()

            inital_time = current_milli_time()
            #print('inital_time: ', inital_time)
            timer = 0

            # Waiting while loop
            while(True):
                time.sleep(tutor_thread_delay)

                if playing_state:
                    timer = current_milli_time() - inital_time
                    #print(timer)

                    if timer >= delay * 10 - 25:
                        #if keyboard_valid():
                        if True:
                            target_keyboard_state = []
                            #arduino_coom([])
                            break

                else:
                    inital_time = current_milli_time()

                    if timer != 0:
                        # if user paused, account for the passed time
                        # in the timer
                        delay -= timer
                        timer = 0

    # Outside of large For Loop
    #arduino_comm([])
    playing_state = False
    print("end of song")

def tutor_intermediate():
    print("intermediate")
    return

def tutor_expert():
    print('expert')

###############################MAIN RUN CODE############################

#global restart

midi_setup()

tutor_beginner()


"""
while (True):
    if current_mode == 'beginner':
        tutor_beginner()
    elif current_mode == 'intermediate':
        tutor_intermediate()
    elif current_mode == 'expert':
        tutor_expert()

    while(not playing_state):
        #print("completion of tutoring mode")
        time.sleep(0.2)

    restart = False
"""
