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
#coord_thread_delay = 0.05
#coord_thread_delay = 0.01
#click_thread_delay = 0.5
#button_thread_delay = 0.2
tutor_thread_delay = 0.1
app_close_delay = 7

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

############################LIVE TUTORING VARIABLES#############################
skill ='follow_you_button'
current_mode = 'beginner'
reset_flag = 0
hands = []
speed = []
tranpose = []
start_bar_value = []
playing_state = False
restart = False
mode = []
live_setting_change = False
end_of_song_flag = 0

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

            # Checking if the pianobooster application is running
            processes = [p.name() for p in psutil.process_iter()]

            for process in processes:
                if process == 'pianobooster.exe':
                    # PianoBooster is running
                    break

            if process != 'pianobooster.exe':
                # if the PianoBooster is not running, end mouse tracking
                print("PianoBooster Application Closure Detection")
                time.sleep(1)
                self.app_close_signal.emit()
                break

################################################################################

class TutorThread(QThread):
    # This thread performs the algorithm to control the LED lights with the
    # information of the other threads, such as the live tutoring variables.
    # The thread will include the code for the beginner, intermediate, and
    # expert mode.

    def __init__(self):
        QThread.__init__(self)

    def run(self):

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

            global right_notes
            acceptable = 1

            for note in target_keyboard_state:
                if note not in right_notes:
                    acceptable = 0
                    break

            if acceptable and len(wrong_notes) <= 1:
                right_notes = []
                print("acceptable")
                return 1

            return 0

        #############################TUTORING UTILITY FUNCTIONS#################

        def chord_detection(inital_delay_location):
            # This function returns the final delay location, meaning the next delay that
            # does not include the chord. If the function returns inital_delay_location,
            # it means that the inital delay is not a chord.

            final_delay_location = inital_delay_location
            for_counter = 0
        #    print(inital_delay_location)
        #    print(chord_timing_tolerance)

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
            global arduino_keyboard

            print("Arduino Comm Notes: " + str(notes))

            notes_to_add = []
            notes_to_remove = []

            time.sleep(0.001)
            print("Arduino Keyboard Pre-Communication: " + str(arduino_keyboard))

            if notes == []:
                notes_to_send = arduino_keyboard
                arduino_keyboard = []
            else:
                for note in notes: # For Turning on a note
                    if note not in arduino_keyboard:
                        notes_to_add.append(note)
                        arduino_keyboard.append(note)

                for note in arduino_keyboard: # for turning off a note
                    if note not in notes:
                        notes_to_remove.append(note)
                        arduino_keyboard.remove(note)

                notes_to_send = notes_to_add + notes_to_remove

            # All transmitted notes are contain within the same string
            transmitted_string = ''
            print('notes_to_send: ' + str(notes_to_send))

            for note in notes_to_send:
                transmitted_string += str(note) + ','

            #transmitted_string = transmitted_string[:-1] # to remove last note's comma
            print("transmitted_string to Arduino: " + transmitted_string)

            b = transmitted_string.encode('utf-8')
            #print(b)
            #b2 = bytes(transmitted_string, 'utf-8')
            arduino.write(b)

            print("Post-Communication: " + str(arduino_keyboard))

            return

        #################################TUTOR FUNCTIONS########################

        def resetting_tutor():
            #Resetting all variables for song to restart
            global restart,temp_keyboard,notes,current_keyboard_state,right_notes,wrong_notes,sequence,for_counter
            global playing_state,event_counter,final_delay_location,chord_event_skip,live_setting_change,target_keyboard_state
            global end_of_song_flag

            restart = False

            if end_of_song_flag != 1:
                arduino_comm([])
                end_of_song_flag = 0
                print('end of song flag'+ str(end_of_song_flag))


            #sequence = []
            #temp_keyboard = []
            #notes = []
            #current_keyboard_state = []
            target_keyboard_state = []
            ###
            right_notes = []
            wrong_notes = []
            event_counter = -1
            ###
            #for_counter = 0
            #final_delay_location = 0
            #chord_event_skip = 0
            ###
            playing_state = True # resetting acts as play button as well
            live_setting_change = False
            #reset_flag = 0


            return

        def tutor_beginner():
            # This is practically the tutoring code for Beginner Mode

            global target_keyboard_state, playing_state, end_of_song_flag, right_notes
            global wrong_notes, restart, arduino_keyboard

            target_keyboard_state = []
            right_notes = []
            wrong_notes = []
            arduino_keyboard = []

            event_counter = -1
            final_delay_location = 0
            chord_event_skip = 0
            end_of_song_flag = 0

            for event in sequence:
                event_counter += 1
                #counter = 0

                if chord_event_skip != 0:
                    # This ensures that the sequence is taken all the way to the sustain
                    # of the chord rather than duplicating the chords' data processing.
                    chord_event_skip -= 1
                    continue

                if event[0] == '1':
                    safe_change_target_keyboard_state(int(event[2:]), 1)

                if event[0] == 'D':

                    note_delay = int(event[2:])
                    final_delay_location = chord_detection(event_counter)

                    if final_delay_location != event_counter:
                        #print("Chord Detected")
                        notes, note_delay = get_chord_notes(event_counter, final_delay_location)
#for chord
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
                    arduino_comm(target_keyboard_state)

                    while(True):
                        time.sleep(tutor_thread_delay)
                        #if live_setting_change:
                        #    print("HEY THINGS CHANGED")

                        if restart == True or current_mode != 'beginner':
                            restart = False
                            arduino_comm([])
                            #resetting_tutor()
                            return

                        if playing_state == False:
                            #print("paused")
                            pass

                        elif keyboard_valid() and skill == 'follow_you_button':
                            target_keyboard_state = []
                            break

                    #    elif skill in ('listen_button','play_along_button'):
                    #        time.sleep(1) #time variable dependent on piano booster speed setting and delay of note
                    #        target_keyboard_state = []
                    #        break

            # Turn off all notes when song is over
            arduino_comm([])
            playing_state = False
            end_of_song_flag = 1
            print('end of song flag= ' + str(end_of_song_flag))

        def tutor_intermediate():
            #similar to beginner, expect while(true) loop
            global target_keyboard_state

            event_counter = -1
            final_delay_location = 0
            chord_event_skip = 0

            for event in sequence:
                event_counter += 1
                #counter = 0

                if chord_event_skip != 0:
                    # This ensures that the sequence is taken all the way to the sustain
                    # of the chord rather than duplicating the chords' data processing.

                    chord_event_skip -= 1
                    continue

                if event[0] == '1':
                    safe_change_target_keyboard_state(int(event[2:]), 1)
                    #target_keyboard_state.append(int(event[2:]))
                #if event[0] == '0':
                #    safe_change_target_keyboard_state(int(event[2:]), 0)
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


                    note_delay = note_delay*100/speed # relationship between speed and delay
                    if target_keyboard_state == []:
                        continue

                    print("Target " + str(target_keyboard_state))
                    arduino_comm(target_keyboard_state)


                    while(True):
                        time.sleep(tutor_thread_delay)
                        #if live_setting_change:
                        #    print("HEY THINGS CHANGED")

                        if restart == True or current_mode != 'intermediate':
                            resetting_tutor()
                            return

                        if playing_state == False:
                            print("paused")

                        elif skill == 'play_along_button':
                            time.sleep(note_delay)
                            target_keyboard_state = []
                            break

                    #    elif skill in ('listen_button','play_along_button'):
                    #        time.sleep(1) #time variable dependent on piano booster speed setting and delay of note
                    #        target_keyboard_state = []
                    #        break



        def tutor_expert():
            print('expert')

        ###############################MAIN RUN CODE############################
        #threading.Thread(target=piano_comm).start()
        global restart

        midi_setup()

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

        def arduino_setup():
            # This functions sets up the communication between Python and the Arduino.
            # For now the Arduino is assumed to be connected to COM3.

            global arduino
            global piano_size

            whitekey = []
            blackkey = []
            whitekey_transmitted_string = ''
            blackkey_transmitted_string = ''
            piano_size = setting_read('piano_size') + ','

            # Closing, if applicable, the arduino port
            if arduino != []:
                arduino.close()
                arduino = []

            try:
                com_port = setting_read("arduino_com_port")
                print("COM Port Selected: " + str(com_port))

                arduino = serial.Serial(com_port, 9600)
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

                #time.sleep(5)
                time.sleep(2)
                arduino.write(piano_size.encode('utf-8'))
                time.sleep(1)
                whitekey_message = whitekey_transmitted_string.encode('utf-8')
                arduino.write(whitekey_message)
                time.sleep(1)
                blackkey_message = blackkey_transmitted_string.encode('utf-8')
                arduino.write(blackkey_message)
                print("Arduino Setup Complete")
                # THIS IS AN ISSUE IN HOW LONG IT TAKES FOR THE ARDUINO TO BE READY
                time.sleep(5)
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

                        print('current_keyboard_state: ' + str(current_keyboard_state))

            except AttributeError:
                print("Lost Piano Communication")

        return

################################################################################

class TransparentButton(QPushButton):

    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        op=QGraphicsOpacityEffect(self)
        op.setOpacity(0.01)
        self.setGraphicsEffect(op)
        self.setAutoFillBackground(True)

class TransparentGui(QMainWindow):

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
        self.setupVisibleUI()
        self.setupThread()

    def setupTransparentUI(self):

        global local_button_list

        #self.book_combo_button = QPushButton(self)
        self.book_combo_button = TransparentButton(self)
        self.song_combo_button = TransparentButton(self)
        self.listen_button = TransparentButton(self)
        self.follow_you_button = TransparentButton(self)
        self.play_along_button = TransparentButton(self)
        self.restart_button = TransparentButton(self)
        self.play_button = TransparentButton(self)
        self.speed_spin_button = TransparentButton(self)
        self.transpose_spin_button = TransparentButton(self)
        self.looping_bars_popup_button = TransparentButton(self)
        self.start_bar_spin_button = TransparentButton(self)
        self.menubar_button = TransparentButton(self)
        self.parts_selection_button = TransparentButton(self)
        self.parts_mute_button = TransparentButton(self)
        self.parts_slider_button = TransparentButton(self)
        self.right_hand_button = TransparentButton(self)
        self.both_hands_button = TransparentButton(self)
        self.left_hand_button = TransparentButton(self)
        self.slider_hand = TransparentButton(self)
        self.key_combo_button = TransparentButton(self)
        self.major_button = TransparentButton(self)
        self.save_bar_button = TransparentButton(self)

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

        # Initializing PianoBooster App Open Check MultiThreading
        self.check_open_app_thread = AppOpenThread()
        self.check_open_app_thread.app_close_signal.connect(self.close_all_thread)
        self.check_open_app_thread.start()

        # Initializing Piano and Arduino Communication
        self.comm_thread = CommThread()
        self.comm_thread.comm_setup_signal.connect(self.start_tutoring_thread)
        self.comm_thread.start()

        return

    def local_button_set_geometry(self):
        for i in range(len(local_button_list)):
            #print('i: ' + str(i))
            dimensions = all_qwidgets[i].rectangle()
            local_button_list[i].setGeometry(QRect(dimensions.left, dimensions.top, dimensions.right - dimensions.left, dimensions.bottom - dimensions.top))

        return

    def beginner_mode_setting(self):
        # This function selects the tutoring mode to beginner

        global current_mode, live_setting_change

        current_mode = 'beginner'
        live_setting_change = True
        return

    def intermediate_mode_setting(self):
        # This function selects the tutoring mode to intermediate

        global current_mode,live_setting_change

        current_mode = 'intermediate'
        live_setting_change = True
        return

    def expert_mode_setting(self):
        # This function selects the tutoring mode to expert

        global current_mode,live_setting_change

        current_mode = 'expert'
        live_setting_change = True
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

        global skill, hands, speed, tranpose, start_bar_value, playing_state
        global restart, live_setting_change

        button_name = str(button.objectName())
        button_attribute = getattr(self,button_name)

        for index,qwidget in enumerate(local_button_list):
            if qwidget == button_attribute:
                desired_index = index
                break

        if button_name == 'play_button':
            playing_state = not playing_state
            live_setting_change = True
            print("Playing State: " + str(playing_state))

        elif button_name == 'restart_button':
            #reset_flag = 1
            playing_state = True
            restart = True
            live_setting_change = True
            print("Restart Pressed")

        elif button_name == 'follow_you_button':
            skill = button_name
            live_setting_change = True
            print(button_name + " pressed")

        elif button_name == 'listen_button':
            skill = button_name
            live_setting_change = True
            print(button_name + " pressed")

        elif button_name == 'play_along_button':
            skill = button_name
            live_setting_change = True
            print(button_name + " pressed")


        if button_name == 'speed_spin_button' or button_name == 'transpose_spin_button' or button_name == 'start_bar_spin_button':
            if message_box_active == 0:
                self.button_signal.emit(button_name, desired_index)
            else:
                print("QInputDialog in use")
        else:
            all_qwidgets[desired_index].click()

    @pyqtSlot('QString', 'int')
    def create_message_box(self, item, desired_index):
        # This function creates a QInputDialog box for the user to input
        # multivalue information, such as speed and tranpose

        global speed, tranpose, message_box_active
        global playing_state, speed, tranpose, live_setting_change, start_bar_value

        flag = 0
        unacceptable_value_flag = 0

        # Stopping the application
        if playing_state == True:
            flag = 1
            print("Stoping app")
            #all_qwidgets[8].click()
            all_qwidgets[6].click()
            playing_state = False
            live_setting_change = True

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
                live_setting_change = True
            elif item == 'transpose_spin_button':
                tranpose = num
                live_setting_change = True
            elif item == 'start_bar_spin_button':
                start_bar_value = num
                live_setting_change = True


            self.hide()
            all_qwidgets[desired_index].click_input()
            all_qwidgets[desired_index].type_keys('^a {DEL}' + str(num))
            time.sleep(0.2)
            self.show()

        print("End of Message Box Usage")
        message_box_active = 0

        if flag == 1:
            print("Continuing the app")
            #all_qwidgets[8].click()
            all_qwidgets[6].click()
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
        #self.click_tracking_thread.terminate()
        #self.coord_tracking_thread.terminate()
        #self.user_tracking_thread.terminate()
        #self.check_open_app_thread.terminate()
        self.comm_thread.terminate()

        try:
            self.tutor_thread.terminate()
        except AttributeError:
            print("Failure in Comms is acknowledge")

        try:
        #pia_app.kill()
            midi_in.close_port()
            midi_out.close_port()
        except AttributeError:
            print("Failure in Comms is acknowledge")

        self.close()

        return

    def retrieve_name(self, var):
        callers_local_vars = inspect.currentframe().f_back.f_locals.items()
        return [var_name for var_name, var_val in callers_local_vars if var_val is var]

    def piano_booster_setup(self):
        # This function performs the task of opening PianoBooster and appropriately
        # clicking on the majority of the qwidgets to make them addressable. When
        # PianoBooster is opened, the qwidgets are still not addressible via
        # pywinauto. For some weird reason, clicked on them enables them. The code
        # utilizes template matching to click on specific regions of the PianoBooster
        # GUI

        global all_qwidgets, all_qwidgets_names, int_dimensions, pia_app

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
        #click_center_try('hands_groupBox_pia', unique_int_dimensions)
        #click_center_try('book_song_buttons_pia', unique_int_dimensions)
        #click_center_try('flag_button_pia', unique_int_dimensions)
        #click_center_try('part_button_pia', unique_int_dimensions)

        return

################################################################################

"""
app = QApplication(sys.argv)
list = QStyleFactory.keys()
app.setStyle(QStyleFactory.create(list[2])) #Fusion
window = TransparentGui()
window.show()
sys.exit(app.exec_())
"""
