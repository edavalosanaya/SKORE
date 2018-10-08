import time
import rtmidi
from midi_processing import *
import os
import glob

midi_in = []
keys_pressed = []
keys_need_to_be_pressed = []

#Determining where SKORE application is located.
complete_path = os.path.dirname(os.path.abspath(__file__))
skore_index = complete_path.find('SKORE') + len('SKORE')
skore_path = complete_path[0:skore_index+1]

#Importing SKORE functions and additional windows.
skore_program_controller_extension_path = r'user_interface\app_control'
sys.path.append(skore_path + skore_program_controller_extension_path)
from skore_program_controller import is_mid

################################################################################

def keyboard_check(list1,list2):
    if list1 == [] and list2 != []:
        return 0

    for element in list1:
        if element in list2:
            continue
        else:
            return 0
    return 1

def piano_port_setup():
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


def piano_get_message(**kwargs):

    #state = kwargs.get('state', None)
    pitch = kwargs.get('pitch', None)
    keyboard = kwargs.get('keyboard', None)

    if pitch == None and keyboard == None:
        print("Infinite Loop Warning")

    if midi_in == []:
        print("Piano Setup is Required")
        return 0

    try:
        while(True):
            message = midi_in.get_message()

            if pitch != None and pitch in keys_pressed:
                print(str(pitch) + " Pressed")
                return 1

            if keyboard_check(keys_need_to_be_pressed,keys_pressed):
                #print("Equal")
                return 1

            if message:
                note_properties = message[0]
                delay = message[1]

                if note_properties[0] == 144:
                    keys_pressed.append(note_properties[1])
                    #print("Key Added: " + str(note_properties[1]))

                if note_properties[0] != 144:
                    try:
                        keys_pressed.remove(note_properties[1])
                    except ValueError:
                        print("Error Noted")

                    #print("Key Remove: " + str(note_properties[1]))

                if pitch == None and keyboard == None:
                    print(str(note_properties) + ', ' + str(delay))


            #    print(message)
    except AttributeError:
        print("Piano Setup is Required")
        return 0

def note_tracking(sequence):
    time_per_tick = 0.01

    for event in sequence:
        counter = 0
        print(event)
        if event[0] == '1':
            keys_need_to_be_pressed.append(int(event[2:]))
            continue
        elif event[0] == '0':
            keys_need_to_be_pressed.remove(int(event[2:]))
            continue
        elif event[0] == 'D':

            #print("checking keyboard status")
            print("Need " + str(keys_need_to_be_pressed))
            print("Actual " + str(keys_pressed))
            #time.sleep(1)

            while(counter < int(event[2:])):
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

note_event_info = midi_to_note_event_info(mid_file)
print(note_event_info)
sequence = note_event_info

piano_port_setup()
#sequence = ['1,60','D,121','0,60','D,201','1,64','D,1','1,67','D,2','1,60','D,319','0,64','D,2','0,67','D,1','0,60']
note_tracking(sequence)
