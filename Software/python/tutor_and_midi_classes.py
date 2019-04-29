# General Utility LIbraries
import time
import sys
import os

# PyQt5, GUI Library
from PyQt5 import QtCore, QtGui, QtWidgets

# Serial and Midi Port Library
#import rtmidi

# SKORE Modules
import globals
from lib_skore import read_config

#-------------------------------------------------------------------------------

class SkoreMidiEvent:

    """
    This class is a helpful function for midi events, made specially for SKORE.
    """

    def __init__(self, event_type, event_data):

        """ Initilization for main class variables. """

        self.event_type = event_type
        self.data = event_data

        return None

    def __repr__(self):

        """ String representation of the class. """

        return "({0}, {1})".format(self.event_type, self.data)

class SkoreMetaEvent:

    """
    This class is a helpful function for midi meta events, made specially for SKORE.
    """

    def __init__(self, event_type, event_data):

        """ Initilization for main class variables. """

        self.event_type = event_type
        self.data = event_data

        return None

    def __repr__(self):

        """ String representation of the class. """

        return "(Meta: {0}, {1})".format(self.event_type, self.data)

class TutorMidiHandler:

    """
    This class is the callback handler of the Piano port. This handler is design
    to assist the tutoring thread.
    """

    def __init__(self, gui):

        """ Initilization for main class variables. """

        self.gui = gui
        self.notes_drawn = {}

        return None

    def __call__(self, event, data=None):

        """ Handling of the incoming piano message. """

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

        """
        This function request for the wrong note to be indicated in the LED Bar.
        Communication with the arduino is utlizes.
        """

        if self.gui.tutor.options['right/wrong notification'] is False:
            return None

        while globals.HANDLER_ENABLE is False:
            print("$", end = "")
            time.sleep(globals.TUTOR_THREAD_DELAY)

        self.gui.arduino_comm(pitch, 'incorrect-{0}'.format(on_off)) # wrong

        return None

class Tutor(QtCore.QThread):

    """
    This class is the thread that performs the tutoring of the SKORE application.
    It recieves commands from the main SKORE GUI, recieves information from the
    TutorMidiHanlder, and performs the necessary logic to teach ther user the song.
    """

    def __init__(self, gui):

        """
        This function initlizes the major configuration for the tutor thread.
        """

        QtCore.QThread.__init__(self)
        self.gui = gui
        self.gui.tutor_enable = True

        cfg = read_config()
        self.options = {'right/wrong notification': cfg['options']['right/wrong notification'],
                        'timing notification': cfg['options']['timing notification']}

        return None

    def interval_looping(self):

        if globals.LIVE_SETTINGS['interval_loop'] is True:
            print("{0} - {1} - {2}".format(globals.LIVE_SETTINGS['interval_initial'], self.sequence_pointer, globals.LIVE_SETTINGS['interval_final']))
            if globals.LIVE_SETTINGS['interval_initial'] > self.sequence_pointer or self.sequence_pointer > globals.LIVE_SETTINGS['interval_final'] - 1:
                print("Shift song")
                self.gui.shift_song(globals.LIVE_SETTINGS['interval_initial'])

        return None

    def keyboard_valid(self):

        """
        This function return the validity of the current keyboard compared to
        the target keyboard. The user mostly play all the notes in the target
        keyboard and can only have one wrong for the current keyboard to be
        consider valid.
        """

        if globals.KEYBOARD_STATE['TARGET'] == []:
            return True

        for note in globals.KEYBOARD_STATE['TARGET']:
            if note not in globals.KEYBOARD_STATE['RIGHT']:
                return False

        if len(globals.KEYBOARD_STATE['WRONG']) >= 2:
            return False

        return True

    def keyboard_change(self):

        """
        This function determines if the user's keystrokes are unique, meaning that
        the user pressed the target keyboard once it was indicated, not before.
        This prevents the tutoring to continue if the user simply sustains the
        target keyboard, they must actually pressed it when indicated.
        """

        if self.keyboard_change_value is True:
            return None

        current_keyboard_state = globals.KEYBOARD_STATE['RIGHT'] + globals.KEYBOARD_STATE['WRONG']

        if self.post_lighting_notes_pressed == [] or current_keyboard_state == []:
            self.keyboard_change_value = True

        if set(current_keyboard_state).intersection(set(globals.KEYBOARD_STATE['TARGET'])) == set():
            #print("CHANGE DETECTED!")
            self.keyboard_change_value = True

        return None

    def target_in_timing_box(self, event_graphic_notes):

        """ This function returns true if the target is within the timing box. """

        should_be_played_now_list = [note.should_be_played_now for note in event_graphic_notes]
        if True in should_be_played_now_list:
            return True

        return False

    def target_in_late_timing_box(self, event_graphic_notes):

        """
        This function returns true if the target is within the late timing box.
        """

        late_list = [note.is_late for note in event_graphic_notes]
        if True in late_list:
            return True

        return False

    def beginner(self):

        """
        This function is the beginner mode tutoring logic that accounts for the
        specific process need to be done soley for the beginner mode. These
        including informing the user of the upcoming, stopping the notes once
        they reach the timing box, and waiting for the entire target keyboard
        to be pressed.
        """

        run_once = True
        upcoming_once = True

        self.post_lighting_notes_pressed = globals.KEYBOARD_STATE['RIGHT'] + globals.KEYBOARD_STATE['WRONG']
        self.keyboard_change_value = False

        while True:
            if globals.LIVE_SETTINGS['mode'] != 'Beginner':
                return False

            self.interval_looping()
            self.keyboard_change()

            event_graphic_notes = self.gui.drawn_notes_group[self.sequence_pointer]
            if self.target_in_timing_box(event_graphic_notes) and globals.LIVE_SETTINGS['play'] is True:

                # Change color to inform timing
                if self.options['timing notification'] is True and run_once is True:
                    self.gui.arduino_comm(globals.KEYBOARD_STATE['TARGET'], 'timing')
                    run_once = False
                    upcoming_once = False

                self.keyboard_change()

                if self.keyboard_valid() is True and self.keyboard_change_value is True:

                    # Marking played notes
                    for note in event_graphic_notes:
                        note.played = True

                    self.gui.move_all_notes()
                    return True

            if upcoming_once is True:
                self.gui.arduino_comm(globals.KEYBOARD_STATE['TARGET'], 'upcoming')
                upcoming_once = False

            time.sleep(globals.TUTOR_THREAD_DELAY)

        return None

    def intermediate(self):

        """
        This function is the intermediate mode tutoring logic that accounts for
        the specific process need to be done soley for the intermediat mode.
        These including informing the user of the upcoming, and continuing with
        the song regardless of user input.
        """

        run_once = True
        upcoming_once = True

        self.post_lighting_notes_pressed = globals.KEYBOARD_STATE['RIGHT'] + globals.KEYBOARD_STATE['WRONG']
        self.keyboard_change_value = False

        if globals.LIVE_SETTINGS['play'] is True:
            self.gui.move_all_notes()

        while True:
            if globals.LIVE_SETTINGS['mode'] != 'Intermediate':
                return False

            self.interval_looping()
            self.keyboard_change()

            event_graphic_notes = self.gui.drawn_notes_group[self.sequence_pointer]
            if self.target_in_timing_box(event_graphic_notes) and globals.LIVE_SETTINGS['play'] is True:

                # Change color to inform timing
                if self.options['timing notification'] is True and run_once is True:
                    self.gui.arduino_comm(globals.KEYBOARD_STATE['TARGET'], 'timing')
                    run_once = False
                    upcoming_once = False

                # Marking played notes
                played_notes = [note for note in event_graphic_notes if note.note_pitch in globals.KEYBOARD_STATE['RIGHT']]
                for note in played_notes:
                    note.played = True

                # Note is late
                if self.target_in_late_timing_box(event_graphic_notes) is True:
                    return True

            if upcoming_once is True:
                self.gui.arduino_comm(globals.KEYBOARD_STATE['TARGET'], 'upcoming')
                upcoming_once = False

            time.sleep(globals.TUTOR_THREAD_DELAY)

        return None

    def expert(self):

        """
        This function is the expert mode tutoring logic that accounts for
        the specific process need to be done soley for the expert mode.
        These including continuing with the song regardless of user input.
        """

        run_once = True

        self.post_lighting_notes_pressed = globals.KEYBOARD_STATE['RIGHT'] + globals.KEYBOARD_STATE['WRONG']
        self.keyboard_change_value = False

        if globals.LIVE_SETTINGS['play'] is True:
            self.gui.move_all_notes()

        while True:
            if globals.LIVE_SETTINGS['mode'] != 'Expert':
                return False

            self.interval_looping()

            event_graphic_notes = self.gui.drawn_notes_group[self.sequence_pointer]
            if self.target_in_timing_box(event_graphic_notes) and globals.LIVE_SETTINGS['play'] is True:

                # Change color to inform timing
                if self.options['timing notification'] is True and run_once is True:
                    self.gui.arduino_comm(globals.KEYBOARD_STATE['TARGET'], 'timing')
                    run_once = False

                # Marking played notes
                played_notes = [note for note in event_graphic_notes if note.note_pitch in globals.KEYBOARD_STATE['RIGHT']]
                for note in played_notes:
                    note.played = True

                # Note is late
                if self.target_in_late_timing_box(event_graphic_notes) is True:
                    return True

            time.sleep(globals.TUTOR_THREAD_DELAY)

        return None

    def run(self):

        """
        This function performs the general tutoring process that is shared by all
        tutoring modes, such as setup, keeping a sequence pointer, and song
        conclusion.
        """

        globals.KEYBOARD_STATE['RIGHT'] = []
        globals.KEYBOARD_STATE['WRONG'] = []
        globals.KEYBOARD_STATE['ARDUINO']['TARGET'] = []
        globals.KEYBOARD_STATE['ARDUINO']['RW'] = []

        self.sequence_pointer = 0

        while self.sequence_pointer < len(self.gui.filtered_sequence):

            self.interval_looping()

            self.gui.label_current_event_value.setText("{0}/{1}".format(self.sequence_pointer, globals.TOTAL_EVENTS))

            #-------------------------------------------------------------------
            # Meta Event Effects
            if self.gui.filtered_sequence[self.sequence_pointer][0] == "META":
                print("Meta event detected")
                if self.gui.filtered_sequence[self.sequence_pointer][1] == "set_tempo":
                    new_tempo = self.gui.filtered_sequence[self.sequence_pointer][2].tempo
                    print("tempo change: Previous: {0} - Now: {1}".format(self.gui.tempo, new_tempo))
                    self.gui.tempo = new_tempo
                    self.gui.speed_change()

                self.sequence_pointer += 1
                continue

            #-------------------------------------------------------------------
            # Setting up keyboard_state[TARGET]
            print("#---------------------------------------------------------------")
            globals.KEYBOARD_STATE['TARGET'] = self.gui.filtered_sequence[self.sequence_pointer][0]
            print("Target: ", globals.KEYBOARD_STATE['TARGET'])

            if globals.KEYBOARD_STATE['TARGET'] == []:
                continue

            #-------------------------------------------------------------------
            # Tutoring Mode Change
            while True:
                if globals.LIVE_SETTINGS['mode'] == "Beginner":
                    go_to_next_note = self.beginner()
                elif globals.LIVE_SETTINGS['mode'] == "Intermediate":
                    go_to_next_note = self.intermediate()
                else:
                    go_to_next_note =  self.expert()

                if go_to_next_note is True:
                    self.gui.arduino_comm(globals.KEYBOARD_STATE['TARGET'], 'off')
                    break

            self.sequence_pointer += 1

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

        return None
