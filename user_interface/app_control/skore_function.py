import ntpath
import pathlib
import time
import cv2
import numpy as np
import pyautogui
import os
import pywinauto
import glob


##############################CONSTANTS#########################################
templates_address =r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\audiveris_automation\templates"

##############################FUNCTIONS#########################################
#This function obtains the input_address of a file, and uses the final address
#to create the address of the output of the file conversion, including extension
def output_address(input_address, final_address, end_file_extension):
    file = ntpath.basename(input_address)
    filename = file.split(".")[0]

    exist_path = pathlib.Path(input_address)
    file_path = exist_path.parent

    #input_address_new_extension = str(file_path) + '\\' + filename + end_file_extension
    end_address = final_address + '\\' + filename + end_file_extension
    return end_address, filename

#This function utilizes screen shoots and determines the location of certain
#buttons within the screenshot.
def click_center(button):
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite('audiveris_gui_screenshot.png', image)
    img = cv2.imread('audiveris_gui_screenshot.png', 0)

    template = cv2.imread(templates_address + '\\' + button + '.png', 0)
    w, h = template.shape[::-1]

    method = eval('cv2.TM_CCOEFF')
    res = cv2.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    file_button_center_coords = [ int((top_left[0]+bottom_right[0])/2) , int((top_left[1]+bottom_right[1])/2) ]
    pywinauto.mouse.click(button="left",coords=(file_button_center_coords[0],file_button_center_coords[1]))
    os.remove('audiveris_gui_screenshot.png')
    time.sleep(0.1)

def click_center_try(button):
    while(True):
        try:
            click_center(button)
            break
        except AttributeError:
            print('.', end='')
            time.sleep(0.5)

def clean_temp_folder():
    files = glob.glob(r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\temp\*")
    for file in files:
        os.remove(file)
