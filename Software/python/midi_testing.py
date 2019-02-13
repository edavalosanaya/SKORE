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
import math

# PYQT5, GUI Library
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Tutor Application
from midi import read_midifile, NoteEvent, NoteOffEvent, MetaEvent, TimeSignatureEvent, SetTempoEvent
from mido import tick2second
import serial
import serial.tools.list_ports
import glob
from ctypes import windll
import rtmidi
from shutil import copyfile

from skore_lib import FileContainer, GuiManipulator, setting_read, setting_write, is_mid, rect_to_int

#-------------------------------------------------------------------------------
APP_CLOSE_DELAY = 2
COMM_THREAD_DELAY = 0.001
TUTOR_THREAD_DELAY = 0.01

KEYBOARD_SHIFT = 28 # 48, 36
COMM_TIMEOUT = 30
HANDSHAKE_DELAY = 0.001

CHORD_TICK_TOLERANCE = int(setting_read('chord_tick_tolerance'))
CHORD_SUM_TOLERANCE = 25
DELAY_EARLY_TOLERANCE = int(setting_read('delay_early_tolerance')) #35 # < 40, > 25, > 30, > 35, < 37, < 36
DELAY_LATE_TOLERANCE = int(setting_read('delay_late_tolerance'))
MIDDLE_C = 60


#-------------------------------------------------------------------------------

class MidiEvent:

    def __init__(self, event_type, event_data):
        self.event_type = event_type
        self.data = event_data

        return None

    def __repr__(self):
        return "({0}, {1})".format(self.event_type, self.data)

original_sequence = []
filtered_sequence = []

new_midi_file = r"C:\Users\ZBos\Documents\GitHub\SKORE\Software\python" + r"\simple2.mid"
micro_per_beat_tempo = 0

#-------------------------------------------------------------------------------

# Obtaining the note event info for the mid file
mid_file_name = os.path.basename(new_midi_file)
pattern = read_midifile(new_midi_file)

print("Pattern: ")
print(pattern)
print("\n")

PPQN = pattern.resolution # parameter
#self.PPQN = 96

for track in pattern:        # adding tracks issue
    for event in track:
        if isinstance(event, TimeSignatureEvent): # Time signature events need a speical calculation to determine secs.
            print("TimeSignatureEvent DETECTED")

            try:
                event_data = event.data
            except:
                print("TimeSignatureEvent ERROR")
                continue

            print(event_data)
            time_signature = event_data[0] / event_data[1]**2 # TimeSignatureEvent
            midi_ticks_per_metronome_click = event_data[2] # Midi ticks per metronome click
            notes_per_midi_quart_note = event_data[3] # 32nd notes per midi quarter note

            print("Time signature: {0}\nMidi ticks per metronome: {1}\n32nd Notes per midi quarter note: {2}"
            .format(time_signature,midi_ticks_per_metronome_click,notes_per_midi_quart_note))

            for index, element in enumerate(event_data):
                micro_per_beat_tempo += element * 256 ** (2 - index) #parameter

            #print('micro_per_beat_tempo:', self.micro_per_beat_tempo)

        if isinstance(event, SetTempoEvent):  # different calculation must be made to find micro_per_beat_tempo
            print("SetTempoEvent DETECTED")

            try:
                event_data = event.data
            except:
                print("SetTempoEvent ERROR")
                continue

            print(event_data)
            for index, element in enumerate(event_data):
                micro_per_beat_tempo += element * 256 ** (2 - index)

        if isinstance(event, NoteEvent): ##
            print(event)
            if event.tick > 0:
                original_sequence.append(MidiEvent(None, event.tick))
            if event.data[1] == 0 or isinstance(event, NoteOffEvent):
                original_sequence.append(MidiEvent(False, event.pitch))
            else:
                original_sequence.append(MidiEvent(True, event.pitch))


if original_sequence[0].event_type != None:
    original_sequence.insert(0,MidiEvent(None,0))


#-------------------------------------------------------------------------------

# Pre-Song Analysis
final_index = -1

print("PPQN: {0}\tMicro_per_beat_tempo: {1}".format(PPQN, micro_per_beat_tempo))

for i in range(len(original_sequence)):

    if final_index >= i:
        continue

    if original_sequence[i].event_type is None or original_sequence[i].event_type is False:
        continue

    #-------------------------------------------------------------------
    # Determing Pre-Note/Chord Delay

    delta_time = 0

    for event in reversed(original_sequence[:i]):

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

    for index_tracker, event in enumerate(original_sequence[i:]):

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


    sec_delay = tick2second(delta_time, PPQN, micro_per_beat_tempo)
    filtered_sequence.append([note_array, sec_delay])
    #filtered_sequence.append([note_array, delta_time])

print("""
---------------------------Tutor Midi Setup-----------------------------
MIDI FILE LOCATION: {0}

ORIGINAL MIDI SEQUENCE:
{1}

FILTERED MIDI SEQUENCE:
{2}

""".format(new_midi_file, original_sequence, filtered_sequence))
