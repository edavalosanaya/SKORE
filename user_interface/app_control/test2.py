import ntpath
import pathlib
import time
import cv2
import numpy as np
import pyautogui
import os
import pywinauto
import glob
from pathlib import Path
from shutil import copyfile, move
import shutil
import sys

templates_address = []
destination_address = []

#Determining where SKORE application is located
complete_path = os.path.dirname(os.path.abspath(__file__))
skore_index = complete_path.find('SKORE') + len('SKORE')
skore_path = complete_path[0:skore_index+1]

#Importing SKORE functions and additional windows
skore_program_controller_extension_path = r'user_interface\app_control'
sys.path.append(skore_path + skore_program_controller_extension_path)
from skore_program_controller import output_address

skore_program_controller_extension_path = r"user_interface\app_control"
temp_folder_extension_path = r"user_interface\app_control\temp"
templates_folder_extension_path = r"user_interface\app_control\templates"
conversion_test_folder_extension_path = r"user_interface\app_control\conversion_test"
misc_folder_extension_path = r"user_interface\app_control\misc"
output_folder_extension_path = r"user_interface\app_control\output"

# Determing the address of the temp and templates folders
temp_folder_path = skore_path + temp_folder_extension_path
templates_folder_path = skore_path + templates_folder_extension_path
conversion_test_folder_path = skore_path + conversion_test_folder_extension_path
misc_folder_path = skore_path + misc_folder_extension_path
output_folder_path = skore_path + output_folder_extension_path
skore_program_controller_path = skore_path + skore_program_controller_extension_path

int_dimensions = []

def auto_xenoplay(user_input_address_xeno, destination_address):
    # This function does the automation of the xenoplay application
    # This is the highest-possibility of failure function. THIS WORKS SOMETIMES

    global int_dimensions

    [end_address, filename] = output_address(user_input_address_xeno, destination_address, '.mid')
    os.system("start \"\" cmd /c \"cd " + skore_program_controller_path +" & start_xenoplay.py \"")

    # Trying to handle Xenoage Player, waiting until the window is available
    while(True):
        try:
            xeno_app = pywinauto.application.Application().connect(title = 'Xenoage Player 0.4')
            #print()
            break
        except pywinauto.findwindows.ElementNotFoundError:
            #print('.', end = '')
            time.sleep(0.1)

    # Once the window is available, obtain control of the application
    xeno_app = pywinauto.application.Application().connect(title = 'Xenoage Player 0.4')
    w_handle = pywinauto.findwindows.find_windows(title='Xenoage Player 0.4')[0]
    window = xeno_app.window(handle=w_handle) #pywinauto.application.WindowSpecification Object

    delay = 0.4

    # Opening the .mxl file onto Xenoage Player
    original_rect_dimensions = window.rectangle()
    int_dimensions = rect_to_int(original_rect_dimensions)

    time.sleep(delay)
    click_center_try('file_button_xeno')
    time.sleep(delay)
    click_center_try('open_button_xeno_menu')
    time.sleep(delay)

    # Entering the address of the mxl file and opening the file
    #time.sleep(2)
    o_handle = pywinauto.findwindows.find_windows(title='Open')[0]
    o_window = xeno_app.window(handle=o_handle)
    original_rect_dimensions = o_window.rectangle()
    int_dimensions = rect_to_int(original_rect_dimensions)

    o_window.type_keys(user_input_address_xeno)
    time.sleep(delay)
    click_center_try('open_button_xeno')
    time.sleep(delay)

    # Attempting to save the .mxl as a .mid file, while also stoping the app
    # from playing music
    original_rect_dimensions = window.rectangle()
    int_dimensions = rect_to_int(original_rect_dimensions)

    click_center_try('stop_button_xeno')
    time.sleep(delay)
    click_center_try('file_button_xeno')
    time.sleep(delay)
    click_center_try('save_as_button_xeno')
    time.sleep(delay)

    # Entering the new name and address of the .mid file
    s_handle = pywinauto.findwindows.find_windows(title='Save')[0]
    s_window = xeno_app.window(handle=s_handle)
    original_rect_dimensions = s_window.rectangle()
    int_dimensions = rect_to_int(original_rect_dimensions)

    time.sleep(delay)
    s_window.type_keys(end_address)
    time.sleep(delay)
    click_center_try('save_button_xeno')
    time.sleep(delay)

    # Closing Xenoplay
    xeno_app.kill()
    print(".mxl -> .mid complete")
    return end_address

def click_center_try(button):
    # This functions does the same as click_center, but allows the function to wait
    # Until the image is found.


    while(True):
        try:
            click_center(button)
            break
        except AttributeError:
            #print('.', end='')
            time.sleep(0.5)
    return

def click_center(button):
    # This function utilizes screen shoots and determines the location of certain
    # buttons within the screenshot.

    if int_dimensions == []:
        image = pyautogui.screenshot()
    else:
        image = pyautogui.screenshot(region=int_dimensions)
        #image = pyautogui.screenshot(region = (722,425,381,132))

    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite('gui_screenshot.png', image)
    img = cv2.imread('gui_screenshot.png', 0)
    #location = find_image_path(button)
    template = cv2.imread(templates_folder_path + '\\' + button + '.png', 0)

    w, h = template.shape[::-1]

    method = eval('cv2.TM_CCOEFF')
    res = cv2.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    if int_dimensions != []:
        # Shifting values to lay ontop of the region correctly
        top_left = [top_left[0] + int_dimensions[0], top_left[1] + int_dimensions[1]]
        bottom_right = (top_left[0] + w, top_left[1] + h)

    #print(top_left)
    #print(bottom_right)

    file_button_center_coords = [ int((top_left[0]+bottom_right[0])/2) , int((top_left[1]+bottom_right[1])/2) ]
    pywinauto.mouse.click(button="left",coords=(file_button_center_coords[0],file_button_center_coords[1]))
    os.remove('gui_screenshot.png')
    time.sleep(0.1)
    return

def rect_to_int(rect_dimensions):

    int_dimensions = [0,0,0,0]

    dimensions = str(rect_dimensions)
    dimensions = dimensions[1:-1]
    dimensions = dimensions.split(',')

    for dimension in dimensions:

        int_dimension = dimension.replace("L","")
        int_dimension = int_dimension.replace("T","")
        int_dimension = int_dimension.replace("R","")
        int_dimension = int_dimension.replace("B","")
        int_dimension = int(int_dimension)
        int_dimensions[dimensions.index(dimension)] = int_dimension

    tolerance = 10

    int_dimensions[2] = int_dimensions[2] - int_dimensions[0] + tolerance
    int_dimensions[3] = int_dimensions[3] - int_dimensions[1] + tolerance

    #print(int_dimensions)

    return int_dimensions

################################################################################

temp_folder_extension_path = r"user_interface\app_control\temp"
temp_folder_path = skore_path + temp_folder_extension_path

input = r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\conversion_test\audiverius_samples\SpiritedAway.mxl"
auto_xenoplay(input,temp_folder_path)
