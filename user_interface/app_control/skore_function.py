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
from shutil import copyfile

##############################CONSTANTS#########################################
#templates_address =[r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\audiveris_automation\templates",
#                    r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\xenoplay_automation\templates"]
#Create variables
templates_address = []
destination_address = []

#Determing the address of the entire SKORE system
complete_path = os.path.dirname(os.path.abspath(__file__))
skore_index = complete_path.find('SKORE') + len('SKORE')
skore_path = complete_path[0:skore_index+1]
path_setting_extension = r"user_interface\app_control"
path_temp_folder_extension = r"user_interface\app_control\temp"
path_skore_function_extension = r"user_interface\app_control"
##############################FUNCTIONS#########################################
def setting_read(setting,temp):
    #Reading the value of the setting

    #Opening File
    global skore_path

    #If the settings should be obtain from the temp or default setting text
    if(temp == 'temp'):
        file = open(skore_path + path_temp_folder_extension + '\\' + 'settings_temp.txt', 'r')
    elif(temp == 'default'):
        file = open(skore_path + path_setting_extension + '\\' + 'settings.txt', 'r')
    else:
        raise RuntimeError("Invalid type of setting, should be either temp or default")

    #Reading the contents of the setting text
    contents = file.readlines()
    settings = []

    #Spliting the lines at point with = character
    for line in contents:
        if(line.find('=') == -1):
            continue
        settings.extend(line.split("="))

    #Finding setting's results
    try:
        elem = settings.index(setting)
        if(settings[elem + 1] == '\n'):
            return "None"

        #Optaining the information of the setting and spliting it from the title
        list = settings[elem + 1]

        if(list.find(',') > 0):
            #For multiple address settings
            #Spliting the multiple addresses
            list = list.split(',')

            #Removing the \n character at the end
            last_element = list[-1]
            last_element_cut = last_element[0:-1]
            list[list.index(last_element)] = last_element_cut

            #Converting String to raw literal string
            for element in list:
                eval_element = eval(element)
                list[list.index(element)] = eval_element
                #"%r"%eval_element
            return list

        else:
            #For single address settings
            #removing \n at the end of the string
            list = list[0:-1]
            #Cleaning the string
            list = eval(list)
            return list

    except ValueError:
        raise RuntimeError("Invalid Setting Title")
    return


def setting_temp_write(setting, write_data):
    #Writing the configuration settings

    #Opening File
    global skore_path
    file_read = open(skore_path + path_setting_extension + '\\' + 'settings.txt', 'r')
    contents_all = file_read.read()
    contents_line = file_read.readlines()
    file_read.close()

    #Finding the setting wanted to be changed
    setting_index = contents_all.find(setting)
    equal_sign_index = contents_all.find('=', setting_index)
    end_of_line_index = contents_all.find('\n', equal_sign_index)
    current_setting_value = contents_all[equal_sign_index + 1:end_of_line_index]
    contents_all = contents_all.replace(current_setting_value, write_data)

    #Writing the value of the setting onto the file
    file_write = open(skore_path + path_temp_folder_extension + '\\' + 'settings_temp.txt', 'w')
    file_write.write(contents_all)
    file_write.close()
    return

def create_setting_temp():
    #Create the setting temp file

    copyfile('settings.txt', skore_path + path_temp_folder_extension + '\\' + 'settings_temp.txt')
    return

def output_address(input_address, final_address, end_file_extension):
    #This function obtains the input_address of a file, and uses the final address
    #to create the address of the output of the file conversion, including extension

    file = ntpath.basename(input_address)
    filename = file.split(".")[0]

    exist_path = pathlib.Path(input_address)
    file_path = exist_path.parent

    #input_address_new_extension = str(file_path) + '\\' + filename + end_file_extension
    end_address = final_address + '\\' + filename + end_file_extension
    return end_address, filename

def find_image_path(button):
    #This function determines the location of the templates

    global templates_address
    templates_address = setting_read('templates_address','temp')

    for address in range(0, len(templates_address)):
        file = Path(templates_address[address] + '\\' + button + '.png')
        if(file.is_file()):
            return address
    raise RuntimeError("Desired Template was not found")
    return

def click_center(button):
    #This function utilizes screen shoots and determines the location of certain
    #buttons within the screenshot.

    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite('audiveris_gui_screenshot.png', image)
    img = cv2.imread('audiveris_gui_screenshot.png', 0)

    location = find_image_path(button)
    template = cv2.imread(templates_address[location] + '\\' + button + '.png', 0)

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
    return

def click_center_try(button):
    #This functions does the same as click_center, but allows the function to wait
    #Until the image is found.

    while(True):
        try:
            click_center(button)
            break
        except AttributeError:
            print('.', end='')
            time.sleep(0.5)
    return

def clean_temp_folder():
    #This function cleans the temp file within SKORE repository
    destination_address = setting_read('destination_address','temp')
    destination_address = destination_address + '\*'
    destination_address = '%r' %destination_address
    destination_address = destination_address[1:-1]
    files = glob.glob(destination_address)

    #files = glob.glob(r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\temp\*")
    for file in files:
        os.remove(file)
    return

#################################MAIN###########################################
create_setting_temp()
