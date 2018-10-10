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

def sequence2delay_sequence(sequence):
    # Creates a sequence purely made out of delay values

    delay_sequence = []

    for event in sequence:

        if event[0] == 'D': # If event is Delay, the append value to delay sequence
            delay_sequence.append(int(event[2:]))

    return delay_sequence

def chord_detection(delay_location):
    # Determines if a chord is present and returns the value "chord_note_counter"
    # this value is corresponding to the number of notes in a chord - 1.

    chord_note_counter = 0

    # Shifting the delay location value to work with the delay sequence list
    delay_location = int((delay_location - 1)/2)
    after_event_delay_sequence = delay_sequence[delay_location:]
    #print(after_event_delay_sequence)

    # If the first delay of a note is smaller than a chord timing tolerance, chord has been detected
    try:
        if after_event_delay_sequence[0] <= chord_timing_tolerance:
            print("Chord Beginning or End")
    except IndexError:
        #print("End of Song")
        return 0

        # For loop checks for addtional notes in the chord with the same chord timing tolerance
        for event in after_event_delay_sequence:
            if event <= chord_timing_tolerance:
                chord_note_counter += 1
            else:
                break
        print("Additional Notes in Chord: " + str(chord_note_counter))

    # returning the quantity of notes in the chord - 1
    return chord_note_counter

def get_chord_notes(event_counter,chord_note_counter,sequence):
    # This function returns the notes and duration of the chord.

    notes = []
    print(sequence[event_counter])

    # Appending the state, ['1' or '0'], and pitch of a notes in the chord to a
    # list called notes.
    for i in range(0, chord_note_counter):
        notes.append(sequence[event_counter + 2*i + 1])

    # Try statement is here just incase the last notes are a chord.
    #
    try:
        chord_delay = int(sequence[event_counter + 2*chord_note_counter][2:])
    except IndexError:
        print("End of Song Chord")
        chord_delay = 50

    print(notes)
    print(chord_delay)
    return notes, chord_delay


def piano_port_setup():
    # This function sets up the communication between Python and the MIDI device
    # It will select the first listed device.
    # THIS NEEDS TO BE AJUSTABLE FROM THE GUI SETTINGS LATER

    global midi_in

    midi_in = rtmidi.MidiIn()

    print("Avaliable Ports")
    for port_name in midi_in.get_ports():
        print(port_name)

    try:
        midi_in.open_port(0)
        return 1

    except RuntimeError:
        print("No Piano Port Detected")
        midi_in = []
        return 0


def piano_get_message(keyboard):
    # This functions obtains the message send from the piano and appends the
    # note played to a list of currently played notes. It also removes if the
    # note is registered as off, from the playlist.

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

                    if note_properties[1] in keys_pressed:
                        continue

                    keys_pressed.append(note_properties[1])

                if note_properties[0] != 144:

                    if note_properties[1] not in keys_pressed:
                        continue

                    keys_pressed.remove(note_properties[1])

    except AttributeError:
        print("Piano Setup is Required")
        return 0

def note_tracking(sequence):
    # This is practically the tutoring code for Beginner Mode

    time_per_tick = 0.001
    event_counter = -1
    chord_note_counter = 0
    chord_event_skip = 0

    for event in sequence:
        event_counter += 1
        counter = 0
        #print(event)

        if chord_event_skip != 0:
            #print(chord_event_skip)
            chord_event_skip -= 1
            #print(chord_event_skip)

            #delay_location = int((event_counter - 1)/2)
            #after_event_delay_sequence = delay_sequence[delay_location:]
            #print(after_event_delay_sequence)

            continue

        if event[0] == '1':

            if int(event[2:]) not in keys_need_to_be_pressed:
                keys_need_to_be_pressed.append(int(event[2:]))
            continue

        elif event[0] == '0':

            if int(event[2:]) in keys_need_to_be_pressed:
                keys_need_to_be_pressed.remove(int(event[2:]))
            continue

        elif event[0] == 'D':

            note_delay = int(event[2:])

            chord_note_counter = chord_detection(event_counter)

            if chord_note_counter:
                print("Chord Detected")
                notes, note_delay = get_chord_notes(event_counter,chord_note_counter,sequence)

                for note in notes:
                    if note[0] == '1':
                        keys_need_to_be_pressed.append(int(note[2:]))
                    else:
                        keys_need_to_be_pressed.remove(int(note[2:]))

                chord_event_skip = chord_note_counter * 2


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
delay_sequence = sequence2delay_sequence(sequence)
print(delay_sequence)

#Beginning tutoring
note_tracking(sequence)
