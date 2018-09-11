import pywinauto
import time
import ntpath
import pathlib
from pathlib import Path
import os
import sys
import numpy as np
import pyautogui
import cv2

#importing skore functions
sys.path.append(r'C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control')
from skore_function import click_center, output_address, clean_temp_folder, click_center_try

#############################FILE LOCATIONS#####################################
test_sample_address = r"C:\Users\daval\Desktop\COLLEGE\Senior_Year\Fall_Semester\Senior_Design\Smart_Tutor_Piano_Idea\Conversion_Test\AnthemScore\SpiritedAway.pdf"
aud_output_file_path = r"C:\Users\daval\AppData\Roaming\AudiverisLtd\audiveris\data\output"
destination_address = r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\temp"

[final_address,filename] = output_address(test_sample_address,destination_address, '.mxl')
clean_temp_folder()
#################################MAIN###########################################
#Opening audiveris in a separate cmd
os.system("start cmd /c start_audiveris.py")

time.sleep(1)
print('Audiveris is loading please wait.', end = '')

#Trying to handle Audiveris, waiting until the window is available
while(True):
    try:
        audi_app = pywinauto.application.Application().connect(title = 'Audiveris')
        break
    except pywinauto.findwindows.ElementNotFoundError:
        print('.', end = '')
        time.sleep(0.5)

#Once the window is available, obtain control of the application
audi_app = pywinauto.application.Application().connect(title = 'Audiveris')
w_handle = pywinauto.findwindows.find_windows(title='Audiveris')[0]
window = audi_app.window(handle=w_handle) #pywinauto.application.WindowSpecification Object

#Place the Audiveris window above all and maximize
window.type_keys("{TAB}")
window.maximize()
time.sleep(0.1)

#Image processing to obtain file button location
click_center_try('file_button')

#Image processing to obtain input button location
click_center_try('input_button')

#Inputting the .pdf file address to load into audiveris
while(True):
    try:
        window.type_keys(test_sample_address)
        time.sleep(0.5)
        break
    except pywinauto.base_wrapper.ElementNotEnabled:
        print(".", end = '')
        time.sleep(0.1)

#Image processing to click on open button
click_center_try('open_button')

#Image processing to click on book button
click_center_try('book_button')

#Image processing to select "Export Book as..." book_button
time.sleep(1)
click_center_try('export_book_as_button')

#Entering final address to export book as button
while(True):
    try:
        window.type_keys(final_address)
        time.sleep(0.5)
        break
    except pywinauto.base_wrapper.ElementNotEnabled:
        print(".", end = '')
        time.sleep(0.1)

time.sleep(1)
#Image porcessing to select "Save" button
click_center_try('save_button')

#Waiting for the completion of the transcribing of the book
output_file = Path(final_address)
while(True):
    if(output_file.is_file()):
        time.sleep(0.1)
        break
    else:
        time.sleep(0.5)

#Closing Audiveris
audi_app.kill()
