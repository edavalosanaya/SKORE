import time
import rtmidi
from midi_processing import *
import os
import glob
import serial
import serial.tools.list_ports
from shutil import copyfile
from threading import Thread, Event
from ctypes import windll

#Determining where SKORE application is located.
complete_path = os.path.dirname(os.path.abspath(__file__))
skore_index = complete_path.find('SKORE') + len('SKORE')
skore_path = complete_path[0:skore_index+1]

#Importing SKORE functions and additional windows.
skore_program_controller_extension_path = r'user_interface\app_control'
sys.path.append(skore_path + skore_program_controller_extension_path)
from skore_program_controller import is_mid,setting_read,output_address

#Obtaining tutor.py's working directory.
tutor_extension_path = r'python_communication'
tutor_path = skore_path + tutor_extension_path

###############################VARIABLES########################################

#Piano Variables (For Setup)
midi_in = []
piano_size = []

#Tutoring Variables
current_keyboard_state = []
target_keyboard_state = []
sequence = []
end_of_tutoring_event = Event()

#chord_timing_tolerance = 10
#time_per_tick = 0.00001
chord_timing_tolerance = float(setting_read('chord_timing_tolerance'))
time_per_tick = float(setting_read('time_per_tick'))
increment_counter = int(setting_read("increment_counter"))

timeBeginPeriod = windll.winmm.timeBeginPeriod
timeBeginPeriod(1)

between_note_delay = 0.02

#Arduino Variables
arduino_keyboard = []
arduino = []

################################################################################
def avaliable_arduino_com():
    # This fuction returns all the available COM ports in a list of strings.
    ports = serial.tools.list_ports.comports(include_links=False)
    results = []
    for port in ports:
        #print(port.device)
        results.append(str(port.device))
    return results

def avaliable_piano_port():
    # This function returns all the available MIDI ports in a list of string.
    temp_midi_in = []

    temp_midi_in = rtmidi.MidiIn()

    avaliable_ports = temp_midi_in.get_ports()
    #print("Avaliable Ports:")

    results = []
    for port_name in avaliable_ports:
        #print(port_name)
        results.append(str(port_name))
    return results

def arduino_setup():
    # This functions sets up the communication between Python and the Arduino.
    # For now the Arduino is assumed to be connected to COM3.

    global arduino
    global piano_size

    whitekey = []
    blackkey = []
    whitekey_transmitted_string = ''
    blackkey_transmitted_string = ''
    piano_size = setting_read('piano_size')

    # Closing, if applicable, the arduino port
    if arduino != []:
        arduino.close()
        arduino = []

    try:
        #com_port = setting_read("arduino_com_port",default_or_temp)
        com_port = setting_read("arduino_com_port")
        print("COM Port Selected: " + str(com_port))

        #arduino = serial.Serial("COM3", 9600)
        arduino = serial.Serial(com_port, 9600)
        print("Arduino Connected")

        whitekey.append(int(setting_read('whitekey_r')))
        whitekey.append(int(setting_read('whitekey_g')))
        whitekey.append(int(setting_read('whitekey_b')))

        blackkey.append(int(setting_read('blackkey_r')))
        blackkey.append(int(setting_read('blackkey_g')))
        blackkey.append(int(setting_read('blackkey_b')))

        for data in whitekey:
            whitekey_transmitted_string += str(data) + ','

        for data in blackkey:
            blackkey_transmitted_string += str(data) + ','


        #time.sleep(5)
        time.sleep(1)
        arduino.write(piano_size.encode('utf-8'))
        time.sleep(1)
        whitekey_message = whitekey_transmitted_string.encode('utf-8')
        arduino.write(whitekey_message)
        time.sleep(1)
        blackkey_message = blackkey_transmitted_string.encode('utf-8')
        arduino.write(blackkey_message)
        #time.sleep(10)
        time.sleep(1)
        print("Arduino Setup Complete")
        return 1

    except serial.serialutil.SerialException:
        print("Arduino Not Found")
        return 0

def piano_port_setup():
    # This function sets up the communication between Python and the MIDI device
    # For now Python will connect the first listed device.

    global midi_in

    # Closing piano port
    if midi_in != []:
        midi_in.close()
        midi_in = []

    midi_in = rtmidi.MidiIn()
    avaliable_ports = midi_in.get_ports()

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

################################################################################

def copy_midi_file(midi_file_location, destination_folder):
    # This function makes a copy of the MIDI file into the cwd of tutor.py

    new_midi_file_location, trash = output_address(midi_file_location, destination_folder, '.mid')
    copyfile(midi_file_location, new_midi_file_location)

    return

def delete_midi_in_cwd():
    # This function deletes all the MIDI files within the cwd of tutor.py

    cwd_path = os.path.dirname(os.path.abspath(__file__))
    files = glob.glob(cwd_path + '\*')

    for file in files:
        if(is_mid(file)):
            print("Deleted: " + str(file))
            os.remove(file)

    return

def midi_setup(midi_file_location, destination_folder):
    # This fuction deletes pre-existing MIDI files and places the new desired MIDI
    # file into the cwd of tutor.py

    delete_midi_in_cwd()
    copy_midi_file(midi_file_location, destination_folder)
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

    #start = time.time()
    if list1 == [] and list2 != []:
        return 0

    for element in list1:
        if element in list2:
            continue
        else:
            #end = time.time()
            #print("keyboard_equal: " + str(start - end))
            return 0

    #end = time.time()
    #print("keyboard_equal: " + str(start - end))
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

def piano_comm():
    # This functions obtains the message send from the piano and appends the
    # note played to a list of currently played notes. It also removes if the
    # note is registered as off, from the list.

    try:
        while(True):

            if end_of_tutoring_event.is_set():
                break

            message = midi_in.get_message()

            if message:
                note_properties = message[0]
                #delay = message[1]

                if note_properties[0] == 144:
                    safe_change_current_keyboard_state(note_properties[1], 1)

                if note_properties[0] != 144:
                    safe_change_current_keyboard_state(note_properties[1], 0)

    except AttributeError:
        print("Piano Setup is Required or Piano has been disconnected.")
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

    # All transmitted notes are contain within the same string
    transmitted_string = ''
    notes_to_send = notes_to_add + notes_to_remove

    for note in notes_to_send:
        transmitted_string += str(note) + ','

    #transmitted_string = transmitted_string[:-1] # to remove last note's comma
    #print("transmitted_string:" + transmitted_string)

    b = transmitted_string.encode('utf-8')
    #b2 = bytes(transmitted_string, 'utf-8')
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
        chord_delay = float(setting_read("manual_final_chord_sustain_timing"))

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

            print("Target " + str(target_keyboard_state))
            arduino_comm(target_keyboard_state)

            #counter = note_delay

            while(counter < note_delay):
            #while(counter):
                if keyboard_equal(target_keyboard_state,current_keyboard_state):
                    #print("Same")
                    counter += increment_counter
                    #counter -= increment_counter
                    time.sleep(time_per_tick)
                    continue
                #print("Not Same")

    # Turn off all notes when song is over
    arduino_comm([])

################################################################################

def complete_tutor():

    delete_midi_in_cwd()
    file = r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\conversion_test\ashkan_sonata.mid"
    copy_midi_file(file,tutor_path)

    # Obtaining the MIDI sequence
    midi_status = midi2sequence()

    # Setting up piano
    piano_status = piano_port_setup()
    arduino_status = arduino_setup()

    if arduino_status == 1 and piano_status == 1 and midi_status == 1:

        # This begins the piano_comm keyboard tracking
        piano_comm_thread = Thread(target=piano_comm)
        piano_comm_thread.start()

        # Beginning tutoring
        tutor_beginner()

        # Closes the piano_comm keyboard tracking after tutoring is complete
        end_of_tutoring_event.set()


    return

################################################################################
#complete_tutor()
#print(avaliable_piano_port())
