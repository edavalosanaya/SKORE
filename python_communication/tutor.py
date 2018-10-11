import time
import rtmidi
from midi_processing import *
import os
import glob
import serial
from shutil import copyfile

#Determining where SKORE application is located.
complete_path = os.path.dirname(os.path.abspath(__file__))
skore_index = complete_path.find('SKORE') + len('SKORE')
skore_path = complete_path[0:skore_index+1]

#Importing SKORE functions and additional windows.
skore_program_controller_extension_path = r'user_interface\app_control'
sys.path.append(skore_path + skore_program_controller_extension_path)
from skore_program_controller import is_mid,setting_read,output_address

###############################VARIABLES########################################

#Piano Variables (For Setup)
midi_in = []
setup_time_delay = 2

#Tutoring Variables
current_keyboard_state = []
target_keyboard_state = []
chord_timing_tolerance = 10
sequence = []
time_per_tick = 0.00001

#Arduino Variables
arduino_keyboard = []
arduino = []

################################################################################
def arduino_setup():
    # This functions sets up the communication between Python and the Arduino.
    # For now the Arduino is assumed to be connected to COM3.
    # THIS NEEDS TO BE AJUSTABLE FROM THE GUI SETTINGS LATER

    global arduino

    try:
        #com_port = setting_read("arduino_com_port",default_or_temp)
        com_port = setting_read("arduino_com_port")
        print("COM Port Selected: " + str(com_port))

        #arduino = serial.Serial("COM3", 9600)
        arduino = serial.Serial(com_port, 9600)
        print("Arduino Connected")

        time.sleep(5)
        arduino.write(b'S')
        time.sleep(1)
        arduino.write(b'255,-1,-1')
        time.sleep(1)
        arduino.write(b'-1,255,-1')
        time.sleep(10)
        print("Arduino Setup Complete")
        return 1

    except serial.serialutil.SerialException:
        print("Arduino Not Found")
        return 0

def piano_port_setup():
    # This function sets up the communication between Python and the MIDI device
    # For now Python will connect the first listed device.
    # THIS NEEDS TO BE AJUSTABLE FROM THE GUI SETTINGS LATER

    global midi_in

    midi_in = rtmidi.MidiIn()

    avaliable_ports = midi_in.get_ports()
    print("Avaliable Ports:")

    for port_name in avaliable_ports:
        print(port_name)

    #selected_port = setting_read("piano_port",default_or_temp)
    selected_port = setting_read("piano_port")
    print("Selected Piano Port: " + str(selected_port))

    try:
        midi_in.open_port(avaliable_ports.index(selected_port))
        return 1

    except ValueError:
        print("No Piano Port Detected")
        midi_in = []
        return 0

def copy_midi_file(midi_file_location, destination_folder):

    new_midi_file_location, trash = output_address(midi_file_location, destination_folder, '.mid')
    copyfile(midi_file_location, new_midi_file_location)

    return

def delete_midi_in_cwd():

    cwd_path = os.path.dirname(os.path.abspath(__file__))
    files = glob.glob(cwd_path + '\*')

    for file in files:
        if(is_mid(file)):
            print("Deleted: " + str(file))
            os.remove(file)

    return

def midi2sequence():
    # This functions converts the midi file into a useful sequence. More can be
    # found of this function in the midi_processing.py file

    global sequence
    mid_file = []

    #Obtaining the file name of the mid file within the current working directory.
    cwd_path = os.path.dirname(os.path.abspath(__file__))
    files = glob.glob(cwd_path + '\*')

    for file in files:
        if(is_mid(file)):
            mid_file = file

    if mid_file == []:
        print("No midi file within \python_communication folder")
        return 0

    #Obtaining the note event info for the mid file
    note_event_info = midi_to_note_event_info(mid_file)
    print(note_event_info)
    sequence = note_event_info

    return 1

################################################################################

def keyboard_equal(list1,list2):
    # Checks if all the elements in list1 are at least found in list2
    # returns 1 if yes, 0 for no.

    if list1 == [] and list2 != []:
        return 0

    for element in list1:
        if element in list2:
            continue
        else:
            return 0
    return 1

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

################################################################################

def piano_comm(keyboard):
    # This functions obtains the message send from the piano and appends the
    # note played to a list of currently played notes. It also removes if the
    # note is registered as off, from the list.

    if midi_in == []:
        print("Piano Setup is Required")
        return 0

    try:
        while(True):
            message = midi_in.get_message()

            if keyboard_equal(target_keyboard_state,current_keyboard_state):
                #print("Keyboard Match")
                return 1

            if message:
                note_properties = message[0]
                delay = message[1]

                if note_properties[0] == 144:

                    safe_change_current_keyboard_state(note_properties[1],1)

                if note_properties[0] != 144:

                    safe_change_current_keyboard_state(note_properties[1], 0)

    except AttributeError:
        print("Piano Setup is Required")
        return 0

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

    # Change this section to be more efficient
    between_note_delay = 0.02
    transmitted_string = ''
    notes_to_send = notes_to_add + notes_to_remove

    for note in notes_to_send:
        transmitted_string += str(note) + ','

    #transmitted_string = transmitted_string[:-1] # to remove last note's comma
    #print("transmitted_string:" + transmitted_string)

    b = transmitted_string.encode('utf-8')
    b2 = bytes(transmitted_string, 'utf-8')
    arduino.write(b)
    time.sleep(between_note_delay)


    return


################################################################################

def chord_detection(inital_delay_location):
    # This function returns the final delay location, meaning the next delay that
    # does not include the chord. If the function returns inital_delay_location,
    # it means that the inital delay is not a chord.

    #print(inital_delay_location)
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
        chord_delay = 50

    #print(notes)
    #print(chord_delay)
    return notes, chord_delay

################################################################################

def tutor_beginner():
    # This is practically the tutoring code for Beginner Mode

    event_counter = -1
    final_delay_location = 0
    chord_event_skip = 0

    for event in sequence:
        event_counter += 1
        counter = 0
        #print(event)

        if chord_event_skip != 0:
            # This ensures that the sequence is taken all the way to the sustain
            # of the chord rather than duplicating the chords' data processing.

            chord_event_skip -= 1
            continue

        if event[0] == '1':
            safe_change_target_keyboard_state(int(event[2:]), 1)

        if event[0] == '0':
            safe_change_target_keyboard_state(int(event[2:]), 0)

        if event[0] == 'D':

            note_delay = int(event[2:])
            final_delay_location = chord_detection(event_counter)

            if final_delay_location != event_counter:
                #print("Chord Detected")
                notes, note_delay = get_chord_notes(event_counter, final_delay_location)

                for note in notes:
                    if note[0] == '1':
                        safe_change_target_keyboard_state(int(note[2:]),1)
                    else:
                        safe_change_target_keyboard_state(int(note[2:]),0)

                chord_event_skip = final_delay_location - event_counter

            print("Need " + str(target_keyboard_state))
            arduino_comm(target_keyboard_state)

            while(counter < note_delay):
                if piano_comm(keyboard = target_keyboard_state):
                    counter += 1
                    time.sleep(time_per_tick)

    # Turn off all notes once done with song
    arduino_comm([])

################################################################################
#delete_midi_in_cwd()

#Obtaining the MIDI sequence
midi_status = midi2sequence()

#Setting up piano
piano_status = piano_port_setup()
arduino_status = arduino_setup()

if arduino_status == 1 and piano_status == 1 and midi_status == 1:

    #Beginning tutoring
    tutor_beginner()
