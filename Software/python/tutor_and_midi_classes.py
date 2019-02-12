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

import globals
from lib_skore import read_config

#-------------------------------------------------------------------------------

class SkoreMidiEvent:

    def __init__(self, event_type, event_data):
        self.event_type = event_type
        self.data = event_data

        return None

    def __repr__(self):
        return "({0}, {1})".format(self.event_type, self.data)

class SkoreMetaEvent:

    def __init__(self, event_type, event_data):
        self.event_type = event_type
        self.data = event_data

        return None

    def __repr__(self):

        return "(Meta: {0}, {1})".format(self.event_type, self.data)

class TutorMidiHandler(object):

    def __init__(self, gui):
        self.gui = gui
        self.notes_drawn = {}

    def __call__(self, event, data=None):
        message, delta_time = event
        note_pitch = message[1]
        #print("{0} - {1}".format(message, delta_time))

        if self.gui.tutor_enable is True:

            if message[0] == 0x90 and message[2] != 0: # Note ON Event
                if note_pitch in globals.KEYBOARD_STATE['TARGET']:
                    if note_pitch not in globals.KEYBOARD_STATE['RIGHT']:
                        globals.KEYBOARD_STATE['RIGHT'].append(note_pitch)

                        note_name = globals.NOTE_PITCH_TO_NOTE_NAME[note_pitch][:2]
                        self.gui.note_labels['RIGHT'][note_name].setOpacity(globals.VISIBLE)
                        self.gui.note_name_labels[note_name].setOpacity(globals.VISIBLE)
                        #self.wrong_note_arduino_comm('right', note_pitch)

                else:
                    if note_pitch not in globals.KEYBOARD_STATE['WRONG']:
                        globals.KEYBOARD_STATE['WRONG'].append(note_pitch)

                        note_name = globals.NOTE_PITCH_TO_NOTE_NAME[note_pitch][:2]
                        self.gui.note_labels['WRONG'][note_name].setOpacity(globals.VISIBLE)
                        self.gui.note_name_labels[note_name].setOpacity(globals.VISIBLE)
                        self.wrong_note_arduino_comm('wrong', note_pitch, 'on')

            else: # Note OFF Event
                if note_pitch in globals.KEYBOARD_STATE['RIGHT']:
                    globals.KEYBOARD_STATE['RIGHT'].remove(note_pitch)

                    note_name = globals.NOTE_PITCH_TO_NOTE_NAME[note_pitch][:2]
                    self.gui.note_labels['RIGHT'][note_name].setOpacity(globals.HIDDEN)
                    self.gui.note_name_labels[note_name].setOpacity(globals.HIDDEN)
                    #self.wrong_note_arduino_comm('right', note_pitch)


                elif note_pitch in globals.KEYBOARD_STATE['WRONG']:
                    globals.KEYBOARD_STATE['WRONG'].remove(note_pitch)

                    note_name = globals.NOTE_PITCH_TO_NOTE_NAME[note_pitch][:2]
                    self.gui.note_labels['WRONG'][note_name].setOpacity(globals.HIDDEN)
                    self.gui.note_name_labels[note_name].setOpacity(globals.HIDDEN)
                    self.wrong_note_arduino_comm('wrong', note_pitch, 'off')

        else:

            if message[0] == 0x90 and message[2] != 0: # Note ON Event
                if note_pitch not in globals.KEYBOARD_STATE['NEUTRAL']:
                    globals.KEYBOARD_STATE['NEUTRAL'].append(note_pitch)

                    note_name = globals.NOTE_PITCH_TO_NOTE_NAME[note_pitch][:2]
                    self.gui.note_labels['NEUTRAL'][note_name].setOpacity(globals.VISIBLE)
                    self.gui.note_name_labels[note_name].setOpacity(globals.VISIBLE)

            else: # Note OFF Event
                if note_pitch in globals.KEYBOARD_STATE['NEUTRAL']:
                    globals.KEYBOARD_STATE['NEUTRAL'].remove(note_pitch)

                    note_name = globals.NOTE_PITCH_TO_NOTE_NAME[note_pitch][:2]
                    self.gui.note_labels['NEUTRAL'][note_name].setOpacity(globals.HIDDEN)
                    self.gui.note_name_labels[note_name].setOpacity(globals.HIDDEN)

        #print("Current Keyboard State: {0}".format(self.gui.current_keyboard_state))

        return None

    def wrong_note_arduino_comm(self, right_wrong, pitch, on_off):

        if globals.HANDLER_ENABLE is False:
            return None

        if self.gui.tutor.options['right/wrong notification'] is False:
            return None

        if globals.WRONG_NOTE_READY is True:
            self.gui.arduino_comm(pitch, 'incorrect-{0}'.format(on_off)) # wrong
            return None

        if self.gui.arduino_handshake is False:

            print("WRONG NOTE ERROR!!!!!")
            print("RESET")

            globals.KEYBOARD_STATE['ARDUINO']['RW'] = []
            self.gui.arduino_comm([], 'set')
            self.gui.arduino_comm(globals.KEYBOARD_STATE['TARGET'])

        return None

class Tutor(QThread):

    def __init__(self, gui):
        QThread.__init__(self)
        self.gui = gui

        cfg = read_config()
        self.options = {'right/wrong notification': cfg['options']['right/wrong notification'],
                        'timing notification': cfg['options']['timing notification']}

        return None

    def keyboard_valid(self):
        # This functions follows the confirmation system of PianoBooster
        # which determines if the keys pressed are acceptable compared to the
        # target keyboard configuration
        if globals.KEYBOARD_STATE['TARGET'] == []:
            return True

        """
        if len(set(globals.KEYBOARD_STATE['TARGET']).intersection(set(globals.KEYBOARD_STATE['RIGHT']))) != len(globals.KEYBOARD_STATE['TARGET']):
            return False
        """
        for note in globals.KEYBOARD_STATE['TARGET']:
            if note not in globals.KEYBOARD_STATE['RIGHT']:
                return False

        if len(globals.KEYBOARD_STATE['WRONG']) >= 2:
            return False

        return True

    def keyboard_change(self):

        if self.keyboard_change_value is True:
            #print("It's true")
            return None

        current_keyboard_state = globals.KEYBOARD_STATE['RIGHT'] + globals.KEYBOARD_STATE['WRONG']

        #print("post_lighting_notes_pressed: {0} \tcurrent_keyboard_state: {1} \tTARGET: {2}".format(self.post_lighting_notes_pressed, current_keyboard_state, globals.KEYBOARD_STATE['TARGET']))

        if self.post_lighting_notes_pressed == [] or current_keyboard_state == []:
            #print("wow")
            self.keyboard_change_value = True


        if set(current_keyboard_state).intersection(set(globals.KEYBOARD_STATE['TARGET'])) == set():
            #print("CHANGE DETECTED!")
            self.keyboard_change_value = True


        return None

    def target_keyboard_in_timing_box(self, event_graphic_notes):

        """
        test_note = event_graphic_notes[0]
        if test_note.should_be_played_now is True:
            return True
        """
        should_be_played_now_list = [note.should_be_played_now for note in event_graphic_notes]
        if True in should_be_played_now_list:
            return True

        return False

    def tutor(self):

        globals.KEYBOARD_STATE['RIGHT'] = []
        globals.KEYBOARD_STATE['WRONG'] = []
        globals.KEYBOARD_STATE['ARDUINO']['TARGET'] = []
        globals.KEYBOARD_STATE['ARDUINO']['RW'] = []
        #globals.KEYBOARD_STATE[PREV_TARGET] = []

        for self.sequence_pointer in range(len(self.gui.filtered_sequence)):

            #print("Pointer: ", self.sequence_pointer)
            #-------------------------------------------------------------------
            # Meta Event Effects
            if self.gui.filtered_sequence[self.sequence_pointer][0] == "META":
                print("Meta event detected")
                if self.gui.filtered_sequence[self.sequence_pointer][1] == "set_tempo":
                    new_tempo = self.gui.filtered_sequence[self.sequence_pointer][2].tempo
                    print("tempo change: Previous: {0} - Now: {1}".format(self.gui.tempo, new_tempo))
                    self.gui.tempo = new_tempo
                continue

            #-------------------------------------------------------------------
            # Setting up keyboard_state[TARGET]
            print("#---------------------------------------------------------------")
            globals.KEYBOARD_STATE['TARGET'] = self.gui.filtered_sequence[self.sequence_pointer][0]
            print("Target: ", globals.KEYBOARD_STATE['TARGET'])

            #-------------------------------------------------------------------
            # Hand Skill Effect
            if self.gui.live_settings['hand'] != "Both":
                if self.gui.live_settings['hand'] == 'Right Hand':
                    globals.KEYBOARD_STATE['TARGET'] = [pitch for pitch in globals.KEYBOARD_STATE['TARGET'] if pitch >= globals.MIDDLE_C]
                else:
                    globals.KEYBOARD_STATE['TARGET'] = [pitch for pitch in globals.KEYBOARD_STATE['TARGET'] if pitch < globals.MIDDLE_C]

            #-------------------------------------------------------------------
            # Arduino Comm (dependent on tutoring mode)
            if self.gui.live_settings['mode'] != 'Expert':
                self.gui.arduino_comm(globals.KEYBOARD_STATE['TARGET'])

            self.post_lighting_notes_pressed = globals.KEYBOARD_STATE['RIGHT'] + globals.KEYBOARD_STATE['WRONG']
            #print("post_lighting_notes_pressed: ", self.post_lighting_notes_pressed)
            self.keyboard_change_value = False

            self.keyboard_change()

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

            self.gui.arduino_comm([])
            globals.KEYBOARD_STATE['PREV_TARGET'] = globals.KEYBOARD_STATE['TARGET']

        #-----------------------------------------------------------------------
        # End of Song process
        drawn_notes = []

        for event in self.gui.drawn_notes_group:
            if event == ["META"]:
                continue
            for note in event:
                drawn_notes.append(note)

        visible_notes = [note.visible for note in drawn_notes]

        while True in visible_notes:
            time.sleep(globals.TUTOR_THREAD_DELAY)
            visible_notes = [note.visible for note in drawn_notes]

        print("End of Song")
        self.gui.stop_all_notes()
        self.gui.arduino_comm([])

        return None

    def beginner(self):

        run_once = True

        while True:
            if self.gui.live_settings['mode'] != 'Beginner':
                return False

            self.keyboard_change()

            event_graphic_notes = self.gui.drawn_notes_group[self.sequence_pointer]
            if self.target_keyboard_in_timing_box(event_graphic_notes) and self.gui.live_settings['play'] is True:

                # Change color to inform timing
                if self.options['timing notification'] is True and run_once is True:
                    self.gui.arduino_comm(globals.KEYBOARD_STATE['TARGET'], 'timing')
                    run_once = False

                self.keyboard_change()

                if self.keyboard_valid() is True and self.keyboard_change_value is True:
                    for note in event_graphic_notes:
                        note.played = True

                    self.gui.move_all_notes()
                    return True

            time.sleep(globals.TUTOR_THREAD_DELAY)

        return None

    def intermediate(self):

        run_once = True

        while True:
            if self.gui.live_settings['mode'] != 'Intermediate':
                return False

            event_graphic_notes = self.gui.drawn_notes_group[self.sequence_pointer]
            if self.target_keyboard_in_timing_box(event_graphic_notes) and self.gui.live_settings['play'] is True:

                # Change color to inform timing
                if self.options['timing notification'] is True and run_once is True:
                    self.gui.arduino_comm(globals.KEYBOARD_STATE['TARGET'], 'timing')
                    run_once = False

                played_notes = [note for note in event_graphic_notes if note.note_pitch in globals.KEYBOARD_STATE['RIGHT']]
                for note in played_notes:
                    note.played = True

                self.gui.move_all_notes()
                return True

            time.sleep(globals.TUTOR_THREAD_DELAY)

        return None

    def expert(self):

        run_once = True

        while True:
            if self.gui.live_settings['mode'] != 'Expert':
                return False

            event_graphic_notes = self.gui.drawn_notes_group[self.sequence_pointer]
            if self.target_keyboard_in_timing_box(event_graphic_notes) is True and self.gui.live_settings['play'] is True:

                if run_once is True:
                    self.gui.arduino_comm(globals.KEYBOARD_STATE['TARGET'], 'timing')
                    run_once = False
                # Now turn LEDs to inform when to play (at all)

                played_notes = [note for note in event_graphic_notes if note.note_pitch in globals.KEYBOARD_STATE['RIGHT']]
                for note in played_notes:
                    note.played = True

                self.gui.move_all_notes()
                return True

            time.sleep(globals.TUTOR_THREAD_DELAY)

        return None

    def run(self):

        while self.gui.live_settings['play'] == False:
            time.sleep(globals.TUTOR_THREAD_DELAY)

        self.tutor()

        return None
