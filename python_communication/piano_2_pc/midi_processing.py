import midi
import sys
import os
import glob

#Determining where SKORE application is located.
complete_path = os.path.dirname(os.path.abspath(__file__))
skore_index = complete_path.find('SKORE') + len('SKORE')
skore_path = complete_path[0:skore_index+1]

#Importing SKORE functions and additional windows.
skore_program_controller_extension_path = r'user_interface\app_control'
sys.path.append(skore_path + skore_program_controller_extension_path)
from skore_program_controller import is_mid

#Obtaining the file name of the mid file within the current working directory.
cwd_path = os.path.dirname(os.path.abspath(__file__))
files = glob.glob(cwd_path + '\*')

for file in files:
    if(is_mid(file)):
        mid_file = file

#Now obtaining the pattern of the midi file found.
mid_file_name = os.path.basename(mid_file)
pattern = midi.read_midifile(mid_file_name)

print(pattern)
