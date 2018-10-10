import time
import rtmidi
from midi_processing import *
import os
import glob

midi_in = []
keys_pressed = []
keys_need_to_be_pressed = []
delay_sequence = []
chord_timing_tolerance = 10
sequence = []
time_per_tick = 0.0001
setup_time_delay = 2

#Determining where SKORE application is located.
complete_path = os.path.dirname(os.path.abspath(__file__))
skore_index = complete_path.find('SKORE') + len('SKORE')
skore_path = complete_path[0:skore_index+1]

#Importing SKORE functions and additional windows.
skore_program_controller_extension_path = r'user_interface\app_control'
sys.path.append(skore_path + skore_program_controller_extension_path)
from skore_program_controller import is_mid

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

def safe_change_keys_need_to_be_pressed(pitch, state):
    # This function safely removes or adds the pitch to the
    # keys_need_to_be_pressed variable

    if state == 1:
        if pitch in keys_need_to_be_pressed:
            return
        keys_need_to_be_pressed.append(pitch)

    elif state == 0:
        if pitch not in keys_need_to_be_pressed:
            return
        keys_need_to_be_pressed.remove(pitch)

    return

def safe_change_keys_pressed(pitch, state):
    # This function safely removes or adds the pitch to the
    # keys_pressed variable

    if state == 1:
        if pitch in keys_pressed:
            return
        keys_pressed.append(pitch)

    elif state == 0:
        if pitch not in keys_pressed:
            return
        keys_pressed.remove(pitch)

    return


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

    #print("for_counter: " + str(for_counter))
    final_delay_location += for_counter
    #final_delay_location_data = sequence[final_delay_location]
    #print("final_delay_location_data: " + str(final_delay_location_data))

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

def piano_port_setup():
    # This function sets up the communication between Python and the MIDI device
    # For now it will select the first listed device.
    # THIS NEEDS TO BE AJUSTABLE FROM THE GUI SETTINGS LATER

    global midi_in

    midi_in = rtmidi.MidiIn()

    print("Avaliable Ports")
    for port_name in midi_in.get_ports():
        print(port_name)

    try:
        midi_in.open_port(0)
        time.sleep(setup_time_delay)
        return 1

    except RuntimeError:
        print("No Piano Port Detected")
        midi_in = []
        return 0


def piano_get_message(keyboard):
    # This functions obtains the message send from the piano and appends the
    # note played to a list of currently played notes. It also removes if the
    # note is registered as off, from the list.

    if midi_in == []:
        print("Piano Setup is Required")
        return 0

    try:
        while(True):
            message = midi_in.get_message()

            if keyboard_equal(keys_need_to_be_pressed,keys_pressed):
                #print("Keyboard Match")
                return 1

            if message:
                note_properties = message[0]
                delay = message[1]

                if note_properties[0] == 144:

                    safe_change_keys_pressed(note_properties[1],1)

                if note_properties[0] != 144:

                    safe_change_keys_pressed(note_properties[1], 0)

    except AttributeError:
        print("Piano Setup is Required")
        return 0

def note_tracking():
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
            #print(chord_event_skip)
            #print(sequence[event_counter:])
            #print()

            continue


        if event[0] == '1':
            safe_change_keys_need_to_be_pressed(int(event[2:]), 1)

        if event[0] == '0':
            safe_change_keys_need_to_be_pressed(int(event[2:]), 0)

        if event[0] == 'D':

            note_delay = int(event[2:])

            final_delay_location = chord_detection(event_counter)

            if final_delay_location != event_counter:
                print("Chord Detected")
                notes, note_delay = get_chord_notes(event_counter, final_delay_location)

                for note in notes:
                    if note[0] == '1':
                        safe_change_keys_need_to_be_pressed(int(note[2:]),1)
                    else:
                        safe_change_keys_need_to_be_pressed(int(note[2:]),0)

                chord_event_skip = final_delay_location - event_counter


            print("Need " + str(keys_need_to_be_pressed))
            #print("Actual " + str(keys_pressed))

            # Here would go Bosker's code for Arduino Light Up

            while(counter < note_delay):
                if piano_get_message(keyboard = keys_need_to_be_pressed):
                    counter += 1
                    time.sleep(time_per_tick)


################################################################################

#Obtaining the file name of the mid file within the current working directory.
cwd_path = os.path.dirname(os.path.abspath(__file__))
files = glob.glob(cwd_path + '\*')

for file in files:
    if(is_mid(file)):
        mid_file = file

#Obtaining the note event info for the mid file
note_event_info = midi_to_note_event_info(mid_file)
print(note_event_info)
sequence = note_event_info


#Setting up piano
piano_port_setup()

#Creating delay sequence
#delay_sequence = sequence2delay_sequence(sequence)
#print(delay_sequence)

#Beginning tutoring
note_tracking()
