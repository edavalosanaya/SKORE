import pywinauto
import time
import ntpath
import os
import pathlib

from skore_function import output_address, clean_temp_folder, setting_read

#This program, MidiMusicSheet, converts .wav to .mid files

#############################FILE LOCATIONS#####################################
#user_input_address = r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\conversion_test\WAV_files\SpiritedAway.wav"
#destination_address = r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\temp"
#tone_address = r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\amazingmidi_automation\piano0.wav"
user_input_address_amaz = setting_read('user_input_address_amaz','temp')
tone_address = setting_read('amazingmidi_tone_address','temp')
destination_address = setting_read('destination_address','temp')

[end_address, filename] = output_address(user_input_address_amaz, destination_address, '.mid')
clean_temp_folder()

################################MAIN CODE#######################################
delay = 1
ama_app = pywinauto.application.Application()
ama_app_exe_path = setting_read('ama_app_exe_path','temp')
#ama_app.start(r"C:\Program Files (x86)\AmazingMIDI\amazingmidi.exe")
ama_app.start(ama_app_exe_path)
print("Opening AmazingMIDI")

#Creating a window variable for AmazingMIDI
while(True):
    try:
        w_handle = pywinauto.findwindows.find_windows(title='AmazingMIDI ')[0]
        window = ama_app.window(handle=w_handle) #pywinauto.application.WindowSpecification Object
        print()
        break
    except IndexError:
        print('.', end = '')
        time.sleep(0.1)

#Clicking on file menu, selecting tone file
window.menu_item(u'&File->&Specify Tone File...').click()

#Entering the tone file's address
t_handle = pywinauto.findwindows.find_windows(title='Specify Tone File')[0]
t_window = ama_app.window(handle=t_handle)
t_window.type_keys(tone_address)
t_window.type_keys('{ENTER}')

#Clicking on file menu, selecting input file
window.menu_item(u'&File->&Specify Input File...').click()

#Entering the user input file's address
i_handle = pywinauto.findwindows.find_windows(title='Specify Input File')[0]
i_window = ama_app.window(handle=i_handle)
i_window.type_keys(user_input_address_amaz)
i_window.type_keys('{ENTER}')

#Clicking on file menu, selecting output files
window.menu_item(u'&File->&Specify Output File...').click()

#Entering the output file's end_address
o_handle = pywinauto.findwindows.find_windows(title='Specify Output File')[0]
o_window = ama_app.window(handle=o_handle)
o_window.type_keys(end_address)
o_window.type_keys('{ENTER}')

#Clicking on Transcribe menu, selecting Transcribe
window.menu_item(u'&Transcribe->&Transcribe...').click()

#Entering Transcribe Options
to_handle = pywinauto.findwindows.find_windows(title='Transcribe')[0]
to_window = ama_app.window(handle=to_handle)
to_window.type_keys('{ENTER}')

#Closing amazingmidi
time.sleep(1)
window.wait('enabled', timeout = 30)
window.menu_item(u'&File->Exit').click()
