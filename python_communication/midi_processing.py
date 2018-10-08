from midi import read_midifile, NoteEvent, NoteOffEvent
import sys
import os
import glob

"""
#Determining where SKORE application is located.
complete_path = os.path.dirname(os.path.abspath(__file__))
skore_index = complete_path.find('SKORE') + len('SKORE')
skore_path = complete_path[0:skore_index+1]

#Importing SKORE functions and additional windows.
skore_program_controller_extension_path = r'user_interface\app_control'
sys.path.append(skore_path + skore_program_controller_extension_path)
from skore_program_controller import is_mid
"""

####################################FUNCTIONS###################################

def midi_to_note_event_info(mid_file):
    #Now obtaining the pattern of the midi file found.

    mid_file_name = os.path.basename(mid_file)
    pattern = read_midifile(mid_file_name)

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

###################################MAIN CODE####################################

"""
#Obtaining the file name of the mid file within the current working directory.
cwd_path = os.path.dirname(os.path.abspath(__file__))
files = glob.glob(cwd_path + '\*')

for file in files:
    if(is_mid(file)):
        mid_file = file

note_event_info = midi_to_note_event_info(mid_file)
print(note_event_info)
"""
