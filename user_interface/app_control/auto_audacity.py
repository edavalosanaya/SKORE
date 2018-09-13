import pywinauto
import time
import ntpath
import os
import pathlib

from skore_function import output_address, clean_temp_folder, setting_read, create_setting_temp

#How to print the dictionary items!!!!!
#print(aud_app.__dict__.items())
#print(window.__dict__.items())

#############################FILE LOCATIONS#####################################
#user_input_address = r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\conversion_test\Original_MP3\SpiritedAway.mp3"
#destination_address = r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\temp"
user_input_address_auda = setting_read('user_input_address_auda','temp')
destination_address = setting_read('destination_address','temp')
[end_address, filename] = output_address(user_input_address_auda, destination_address, '.wav')
clean_temp_folder()
create_setting_temp()
################################MAIN CODE#######################################
aud_app = pywinauto.application.Application()
aud_app_exe_path = setting_read('aud_app_exe_path','temp')
aud_app.start(aud_app_exe_path)
#aud_app.start(r"c:\Program Files (x86)\Audacity\audacity.exe")

#Creating a window variable for Audacity
w_handle = pywinauto.findwindows.find_windows(title='Audacity')[0] #[461274]
window = aud_app.window(handle=w_handle) #pywinauto.application.WindowSpecification Object

#Clicking on file menu
window.menu_item(u'&File->&Open').click()

#Creating a window variable for File Browser
w_open_handle = pywinauto.findwindows.find_windows(title='Select one or more audio files...')[0]
w_open = aud_app.window(handle=w_open_handle)

#Entering the user's input file
w_open.type_keys(user_input_address_auda)
w_open.type_keys("{ENTER}")

#Wait until the file has been opened
time.sleep(1)
window.wait('enabled', timeout = 30)

#Export the file
window.menu_item('&File->Export Audio ...').click()
w_export_handle = pywinauto.findwindows.find_windows(title='Export Audio')[0]
w_export = aud_app.window(handle=w_export_handle)

#w_export.type_keys(filename)
w_export.type_keys(end_address)
w_export.type_keys("{ENTER}")

#Editing Metadata
time.sleep(0.5)
aud_app.EditMetadata.OK.click()
window.wait('enabled', timeout = 30)
time.sleep(0.1)

#############################Closing Audacity###################################
window.menu_item('&File->&Close').click()
time.sleep(0.1)
aud_app.SaveChanges.No.click()
aud_app.kill()
time.sleep(0.1)
