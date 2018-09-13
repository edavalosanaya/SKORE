import pywinauto
import time
import ntpath
import os
import pathlib

from skore_function import output_address, clean_temp_folder, setting_grab

#This program, MidiMusicSheet, converts .mid to .pdf files

#############################FILE LOCATIONS#####################################
#user_input_address = r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\conversion_test\Red_Dot_Forever\ChrisPlaying.mid"
#destination_address = r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\temp"
user_input_address_midi = setting_grab('user_input_address_midi')
destination_address = setting_grab('destination_address')
[end_address, filename] = output_address(user_input_address_midi, destination_address, '.pdf')
clean_temp_folder()

################################MAIN CODE#######################################
midi_app = pywinauto.application.Application()
midi_exe_path = setting_grab('midi_exe_path')
#midi_app.start(r"C:\Users\daval\Desktop\MidiSheetMusic-2.6.exe")
midi_app.start(midi_exe_path)
print("Opening MidiSheetMusic.")

#Creating a window variable for Midi Sheet Music
while(True):
    try:
        w_handle = pywinauto.findwindows.find_windows(title='Midi Sheet Music')[0]
        window = midi_app.window(handle=w_handle) #pywinauto.application.WindowSpecification Object
        print()
        break
    except IndexError:
        print('.', end = '')
        time.sleep(0.2)

#Clicking on file menu
window.menu_item(u'&File->&Open').click()

#Entering the input file's address
o_handle = pywinauto.findwindows.find_windows(title='Open')[0]
o_window = midi_app.window(handle=o_handle)
o_window.type_keys(user_input_address_midi)
o_window.type_keys('{ENTER}')

#Wait until the file has been opened
time.sleep(1)
window.wait('enabled', timeout = 30)

#Saving the .pdf file to final address
window.menu_item(u'&File->&Save as PDF...').click()
s_handle = pywinauto.findwindows.find_windows(title='Save As')[0]
s_window = midi_app.window(handle=s_handle)
s_window.type_keys(end_address)
s_window.type_keys('{ENTER}')

#Closing the application *HARD CODED*
time.sleep(3)
#window.wait('enabled', timeout = 30)
#window.menu_item(u'&File->&Exit')
midi_app.kill()
