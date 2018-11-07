# General Utility
import win32api
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
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QAction, QMainWindow, QInputDialog, QLineEdit, QFileDialog, QMessageBox, QLabel, QButtonGroup, QDialogButtonBox, QColorDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread

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

import threading

# General Delay Values
comm_thread_delay = 0.001
#coord_thread_delay = 0.05
coord_thread_delay = 0.01
click_thread_delay = 0.5
button_thread_delay = 0.5
tutor_thread_delay = 0.1

# CommThread Variables
midi_in = []
midi_out = []
piano_size = []

# TutorThread Variables
current_keyboard_state = []
target_keyboard_state = []
desired_notes_pressed = []
sequence = []

#chord_timing_tolerance = 10
#time_per_tick = 0.00001
chord_timing_tolerance = float(setting_read('chord_timing_tolerance'))
time_per_tick = float(setting_read('time_per_tick'))
increment_counter = int(setting_read("increment_counter"))

timeBeginPeriod = windll.winmm.timeBeginPeriod
timeBeginPeriod(1)

# Arduino Variables (within TutorThread)
arduino_keyboard = []
arduino = []

################################MIDI FIlE SETUP#########################

def piano_port_setup():
    # This function sets up the communication between Python and the MIDI device
    # For now Python will connect the first listed device.

    import difflib
    global midi_in, midi_out

    if midi_in != [] and midi_out != []:
        #midi_in.close()
        #midi_out.close()
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

def piano_comm():

    print("Piano and Arduino Communication Thread Enabled")

    #arduino_status = arduino_setup()
    piano_status = piano_port_setup()

    #if arduino_status and piano_status:
    if piano_status:
        print("Piano and Arduino Communication Setup Successful")
        #self.comm_setup_signal.emit()

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
                            if note_info[1] not in desired_notes_pressed:
                                desired_notes_pressed.append(note_info[1])
                    else: # Note OFF event
                        #current_keyboard_state.remove(note_info[1])
                        safe_change_current_keyboard_state(note_info[1],0)
                        if note_info[1] in target_keyboard_state:
                            if note_info[1] in desired_notes_pressed:
                                desired_notes_pressed.remove(note_info[1])

                    print('current_keyboard_state: ' + str(current_keyboard_state))

        except AttributeError:
            print("Lost Piano Communication")

def midi_setup():
    # This fuction deletes pre-existing MIDI files and places the new desired MIDI
    # file into the cwd of tutor.py . Then it converts the midi information
    # of that file into a sequence of note events.

    global sequence
    mid_file = []

    cwd_path = os.path.dirname(os.path.abspath(__file__))
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

    #Obtaining the note event info for the mid file
    sequence = midi_to_note_event_info(mid_file)
    print(sequence)
    return 1

def midi_to_note_event_info(mid_file):
    # Now obtaining the pattern of the midi file found.

    mid_file_name = os.path.basename(mid_file)
    pattern = read_midifile(mid_file)

    note_event_matrix = []

    for track in pattern:
        for event in track:
            if isinstance(event, NoteEvent):
                if event.tick > 0:
                    note_event_matrix.append('D,'+str(event.tick))
                if isinstance(event, NoteOffEvent):
                    note_event_matrix.append('0,'+str(event.pitch))
                else:
                    note_event_matrix.append('1,'+str(event.pitch))

    return note_event_matrix

##############################UTILITY FUNCTIONS#########################

def keyboard_valid():
    #current_keyboard_state = []
    #target_keyboard_state = []
    #desired_notes_pressed = []
    global desired_notes_pressed

    print(current_keyboard_state, end = '')
    print(target_keyboard_state, end = '')
    print(desired_notes_pressed)
    target_keyboard_state.sort()
    desired_notes_pressed.sort()

    if target_keyboard_state == desired_notes_pressed and len(current_keyboard_state) <= len(desired_notes_pressed) + 1:
        print("acceptable")
        desired_notes_pressed = []
        return 1

    else:
        return 0

#############################TUTORING UTILITY FUNCTIONS#################

def chord_detection(inital_delay_location):
    # This function returns the final delay location, meaning the next delay that
    # does not include the chord. If the function returns inital_delay_location,
    # it means that the inital delay is not a chord.

    final_delay_location = inital_delay_location
    for_counter = 0

    if int(sequence[inital_delay_location][2:]) <= chord_timing_tolerance:

        for event in sequence[inital_delay_location: ]:

            if event[0] == 'D':
                #print("Delay Detected")

                if int(event[2:]) >= chord_timing_tolerance:
                    #print("End of Chord Detected")
                    break

                else:
                    for_counter += 1
                    continue
            else:
                for_counter += 1
                continue
    else:
        #print("Not a chord")
        return inital_delay_location

    final_delay_location += for_counter
    return final_delay_location

def get_chord_notes(inital_delay_location,final_delay_location):
    # This functions obtains the notes within the inital and final delay locations
    # Additionally, the function obtains the duration of the chord.

    notes = []

    for event in sequence[inital_delay_location:final_delay_location]:
        if event[0] != 'D':
            notes.append(event)

    try:
        chord_delay = int(sequence[final_delay_location][2:])
    except IndexError:
        chord_delay = float(setting_read("manual_final_chord_sustain_timing"))

    return notes, chord_delay

def safe_change_target_keyboard_state(pitch, state):
    # This function safely removes or adds the pitch to the
    # target_keyboard_state variable

    if state == 1:
        if pitch in target_keyboard_state:
            return
        target_keyboard_state.append(pitch)

    elif state == 0:
        if pitch not in target_keyboard_state:
            return
        target_keyboard_state.remove(pitch)

    return

##############################COMMUNICATION FUNCTIONS###################

def arduino_comm(notes):
    # This function sends the information about which notes need to be added and
    # removed from the LED Rod.

    notes_to_add = []
    notes_to_remove = []

    time.sleep(0.001)

    for note in notes:
        if note not in arduino_keyboard:
            #print(note)
            notes_to_add.append(note)
            arduino_keyboard.append(note)

    if notes == []:
        temp_keyboard = []

        for note in arduino_keyboard:
            notes_to_remove.append(note)
            temp_keyboard.append(note)

        for note in temp_keyboard:
            arduino_keyboard.remove(note)
    else:
        for note in arduino_keyboard:
            if note not in notes:
                notes_to_remove.append(note)
                arduino_keyboard.remove(note)

    # All transmitted notes are contain within the same string
    transmitted_string = ''
    notes_to_send = notes_to_add + notes_to_remove

    for note in notes_to_send:
        transmitted_string += str(note) + ','

    #transmitted_string = transmitted_string[:-1] # to remove last note's comma
    print("transmitted_string to Arduino: " + transmitted_string)

    b = transmitted_string.encode('utf-8')
    #b2 = bytes(transmitted_string, 'utf-8')
    arduino.write(b)

    return

#################################TUTOR FUNCTIONS########################

def tutor_beginner():
    # This is practically the tutoring code for Beginner Mode

    event_counter = -1
    final_delay_location = 0
    chord_event_skip = 0

    for event in sequence:
        event_counter += 1
        counter = 0

        if chord_event_skip != 0:
            # This ensures that the sequence is taken all the way to the sustain
            # of the chord rather than duplicating the chords' data processing.

            chord_event_skip -= 1
            continue

        if event[0] == '1':
            safe_change_target_keyboard_state(int(event[2:]), 1)
            #target_keyboard_state.append(int(event[2:]))
        if event[0] == '0':
            safe_change_target_keyboard_state(int(event[2:]), 0)
            #target_keyboard_state.remove(int(event[2:]))

        if event[0] == 'D':

            note_delay = int(event[2:])
            final_delay_location = chord_detection(event_counter)

            if final_delay_location != event_counter:
                #print("Chord Detected")
                notes, note_delay = get_chord_notes(event_counter, final_delay_location)

                for note in notes:
                    if note[0] == '1':
                        safe_change_target_keyboard_state(int(note[2:]),1)
                        #target_keyboard_state.append(int(event[2:]))
                    else:
                        safe_change_target_keyboard_state(int(note[2:]),0)
                        #target_keyboard_state.remove(int(event[2:]))

                chord_event_skip = final_delay_location - event_counter

            if target_keyboard_state == []:
                continue

            print("Target " + str(target_keyboard_state))
            #arduino_comm(target_keyboard_state)


            while(True):
                time.sleep(tutor_thread_delay)
                if keyboard_valid():
                    break
    # Turn off all notes when song is over
    #arduino_comm([-1])

###############################MAIN RUN CODE############################
piano_port_setup()
#threading.Thread(target=piano_comm).start()

midi_setup()
tutor_beginner()
#threading.Thread(target=piano_comm).terminate()
