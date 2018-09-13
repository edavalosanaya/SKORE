import pywinauto
import time
import ntpath
import os
import pathlib
import sys

#Determing the address of the entire SKORE system
complete_path = os.path.dirname(os.path.abspath(__file__))
skore_index = complete_path.find('SKORE') + len('SKORE')
skore_path = complete_path[0:skore_index+1]
path_skore_function_extension = r"user_interface\app_control"

#sys.path.append(r'C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control')
sys.path.append(skore_path + path_skore_function_extension)
from skore_function import output_address, clean_temp_folder, click_center_try, setting_grab

#############################FILE LOCATIONS#####################################
#user_input_address = r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\conversion_test\audiverius_samples\SpiritedAway.mxl"
#destination_address = r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\temp"
user_input_address_xeno = setting_grab('user_input_address_xeno')
destination_address = setting_grab('destination_address')

[end_address, filename] = output_address(user_input_address_xeno, destination_address, '.mid')
clean_temp_folder()

###############################MAIN#############################################
os.system("start cmd /c start_xenoplay.py")

#Trying to handle Xenoage Player, waiting until the window is available
while(True):
    try:
        xeno_app = pywinauto.application.Application().connect(title = 'Xenoage Player 0.4')
        print()
        break
    except pywinauto.findwindows.ElementNotFoundError:
        print('.', end = '')
        time.sleep(0.1)

#Once the window is available, obtain control of the application
xeno_app = pywinauto.application.Application().connect(title = 'Xenoage Player 0.4')
w_handle = pywinauto.findwindows.find_windows(title='Xenoage Player 0.4')[0]
window = xeno_app.window(handle=w_handle) #pywinauto.application.WindowSpecification Object

delay = 0.4

#Opening the .mxl file onto Xenoage Player
time.sleep(delay)
click_center_try('file_button_xeno')
time.sleep(delay)
click_center_try('open_button_xeno_menu')
time.sleep(delay)

#Entering the address of the mxl file and opening the file
window.type_keys(user_input_address_xeno)
time.sleep(delay)
click_center_try('open_button_xeno')
time.sleep(delay)

#Attempting to save the .mxl as a .mid file
click_center_try('file_button_xeno')
time.sleep(delay)
click_center_try('save_as_button_xeno')
time.sleep(delay)

#Entering the new name and address of the .mid file
s_handle = pywinauto.findwindows.find_windows(title='Save')[0]
s_window = xeno_app.window(handle=s_handle)
time.sleep(delay)
s_window.type_keys(end_address)
time.sleep(delay)
click_center_try('save_button_xeno')
time.sleep(delay)

#Closing Xenoplay
xeno_app.kill()
