# General Utility Libraries
import sys
import time
import os

# File, Folder, and Directory Manipulation Library
import ntpath
import pathlib
import glob
from pathlib import Path
from shutil import copyfile, move
import shutil

# Image Procressing Library
import cv2
import numpy as np
import pyautogui

# GUI Automation Library
import pywinauto

# PyQt5, GUI LIbrary
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

##############################CONSTANTS#########################################

templates_address = []
destination_address = []
progress_bar = []
conversion_identifier = []

# Determing the address of the entire SKORE system
complete_path = os.path.dirname(os.path.abspath(__file__))
skore_index = complete_path.find('SKORE') + len('SKORE')
skore_path = complete_path[0:skore_index+1]

skore_program_controller_extension_path = r"python"
temp_folder_extension_path = r"python\temp"
templates_folder_extension_path = r"python\templates"
conversion_test_folder_extension_path = r"python\conversion_test"
misc_folder_extension_path = r"python\misc"
output_folder_extension_path = r"python\output"

# Determing the address of the temp and templates folders
temp_folder_path = skore_path + temp_folder_extension_path
templates_folder_path = skore_path + templates_folder_extension_path
conversion_test_folder_path = skore_path + conversion_test_folder_extension_path
misc_folder_path = skore_path + misc_folder_extension_path
output_folder_path = skore_path + output_folder_extension_path
skore_program_controller_path = skore_path + skore_program_controller_extension_path

# Purely Testing Purposes
amazing_midi_tune = misc_folder_path + '\\' + 'piano0.wav'

################################FUNCTIONS#######################################

def red_dot_address_conversion(address,file_name):

    complete_path = os.path.dirname(os.path.abspath(__file__))
    print(complete_path)
    complete_path_list = complete_path.split('\\')
    print(complete_path_list)
    this_pc_address = complete_path_list[0] + '\\' + complete_path_list[1] + '\\' + complete_path_list[2] + '\\'
    print(this_pc_address)

    root_path = str(address[0])
    root_file_name = str(file_name[0])
    root_path = root_path.split(' ')[1]
    root_path = root_path.replace(" ", "")

    print("Root Data")
    print(root_path)
    print(root_file_name)

    if root_file_name.find('.') == -1:
        root_file_name = root_file_name + '.mid'

    if root_path[0] != 'C':
        print("This PC address detected")
        root_path = this_pc_address + root_path

    complete_address = root_path + '\\' + root_file_name
    print("Complete Address: ", end = '')
    print(complete_address)

    return complete_address

def output_address(input_address, final_address, end_file_extension):
    # This function obtains the input_address of a file, and uses the final address
    # to create the address of the output of the file conversion, including extension

    file = ntpath.basename(input_address)
    filename = file.split(".")[0]

    exist_path = pathlib.Path(input_address)
    file_path = exist_path.parent

    #input_address_new_extension = str(file_path) + '\\' + filename + end_file_extension
    end_address = final_address + '\\' + filename + end_file_extension
    return end_address, filename

def rect_to_int(rect_dimensions):
    # This function is catered to help click_center by converting the RECT object
    # to a list of integers that is compatible with the cropping feature of the
    # click_center_try function

    int_dimensions = [0,0,0,0]

    dimensions = rect_dimensions

    tolerance = 10

    int_dimensions[0] = dimensions.left
    int_dimensions[1] = dimensions.top
    int_dimensions[2] = dimensions.right - dimensions.left + tolerance
    int_dimensions[3] = dimensions.bottom - dimensions.top + tolerance

    #int_dimensions[2] = int_dimensions[2] - int_dimensions[0] + tolerance
    #int_dimensions[3] = int_dimensions[3] - int_dimensions[1] + tolerance

    #print(int_dimensions)

    return int_dimensions

def click_center(button, dimensions):
    # This function utilizes screen shoots and determines the location of certain
    # buttons within the screenshot. The screenshot will then be cropped to only
    # include the application that is being clicked

    image = pyautogui.screenshot(region=dimensions)

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

    top_left = [top_left[0] + dimensions[0], top_left[1] + dimensions[1]]
    bottom_right = (top_left[0] + w, top_left[1] + h)

    file_button_center_coords = [ int((top_left[0]+bottom_right[0])/2) , int((top_left[1]+bottom_right[1])/2) ]
    pywinauto.mouse.click(button="left",coords=(file_button_center_coords[0],file_button_center_coords[1]))
    os.remove('gui_screenshot.png')
    time.sleep(0.1)
    return

def click_center_try(button, dimensions):
    # This functions does the same as click_center, but allows the function to wait
    # Until the image is found.

    while(True):
        try:
            click_center(button, dimensions)
            break
        except AttributeError:
            #print('.', end='')
            time.sleep(0.5)
    return

def clean_temp_folder():
    # This function cleans the temp file within SKORE repository

    #global temp_folder_path

    files = glob.glob(temp_folder_path + '\*')

    for file in files:
        os.remove(file)
    return

def temp_to_folder(**kwargs):
    # This functions transfer all the files found within temp folder into
    # "destination_folder" with the "filename" given.

    mid_path = []
    filename = kwargs.get('filename', None)
    destination_folder = kwargs.get('destination_folder', None)
    print("Transfering files with name: " + filename + "\t To directory: " + destination_folder)
    #print(filename)
    #print(destination_folder)

    files = glob.glob(temp_folder_path + '\*')

    for file in files:
        old_file = os.path.basename(file)
        file_type = os.path.splitext(old_file)[1]

        #print(file_type)

        if(filename):
            if(destination_folder):
                if(file_type == '.mid'):
                    print("MIDI file detected, 1")
                    mid_path = destination_folder + '\\' + filename + file_type
                shutil.move(file, destination_folder + '\\' + filename + file_type)
            else:
                if(file_type == '.mid'):
                    print("MIDI file detected, 2")
                    mid_path = output_folder_path + '\\' + filename + file_type
                shutil.move(file, output_folder_path + '\\' + filename + file_type)
        else:
            if(destination_folder):
                if(file_type == '.mid'):
                    print("MIDI file detected, 3")
                    mid_path = destination_folder + '\\' + old_file
                shutil.move(file, destination_folder + '\\' + old_file)
            else:
                if(file_type == '.mid'):
                    print("MIDI file detected, 4")
                    mid_path = output_folder_path + '\\' + old_file
                shutil.move(file, output_folder_path + '\\' + old_file)

    return mid_path

def setting_read(setting):
    # Reading the value of the setting

    import sys

    # Opening File
    file = open('settings.txt','r')

    # Reading the contents of the setting text
    contents = file.readlines()
    settings = []

    # Spliting the lines at point with = character
    for line in contents:
        if(line.find('=') == -1):
            continue
        settings.extend(line.split("="))

    # Finding setting's results
    try:
        elem = settings.index(setting)
        if(settings[elem + 1] == '\n'):
            return "None"

        # Optaining the information of the setting and spliting it from the title
        list = settings[elem + 1]

        if(list.find(',') > 0):
            # For multiple address settings
            # Spliting the multiple addresses
            list = list.split(',')

            # Removing the \n character at the end
            last_element = list[-1]
            last_element_cut = last_element[0:-1]
            list[list.index(last_element)] = last_element_cut

            # Converting String to raw literal string
            for element in list:
                eval_element = eval(element)
                list[list.index(element)] = eval_element
                #"%r"%eval_element
            return list

        else:
            # For single address settings removing \n at the end of the string
            list = list[0:-1]
            # Cleaning the string
            list = eval(list)
            return list

    except ValueError:
        raise RuntimeError("Invalid Setting Title")
    return

def setting_write(setting, write_data):
    # Writing the configuration settings of the settings_temp.txt file

    if write_data == []:
        write_data = ''

    # Opening File
    file_read = open('settings.txt','r')
    contents_all = file_read.read()
    contents_line = file_read.readlines()
    file_read.close()

    # Finding the setting wanted to be changed
    setting_index = contents_all.find(setting)
    equal_sign_index = contents_all.find('=', setting_index)
    end_of_line_index = contents_all.find('\n', equal_sign_index)
    current_setting_value = contents_all[equal_sign_index + 1:end_of_line_index]
    write_data = 'r"' + write_data + '"'

    #contents_all = contents_all.replace(current_setting_value, write_data, 1)
    before_equal_string = contents_all[0:equal_sign_index]
    after_equal_string = contents_all[equal_sign_index:-1]
    modified_after_equal_string = after_equal_string.replace(current_setting_value, write_data, 1)
    contents_all = before_equal_string + modified_after_equal_string + '\n'

    # Writing the value of the setting onto the file
    file_write = open('settings.txt', 'w')
    file_write.write(contents_all)
    file_write.close()
    print("Settings for " + setting + " have been modified to " + write_data)
    return

def is_mid(file_path):
    # Test if the input file is .mid

    file_name = os.path.basename(file_path)
    file_type = os.path.splitext(file_name)[1]

    if(file_type == '.mid'):
        return True

    return False

def is_mp3(file_path):
    # Test if the input file is .mp3

    file_name = os.path.basename(file_path)
    file_type = os.path.splitext(file_name)[1]

    if(file_type == '.mp3'):
        return True

    return False

def is_pdf(file_path):
    # Test if the input file is .pdf

    file_name = os.path.basename(file_path)
    file_type = os.path.splitext(file_name)[1]

    if(file_type == '.pdf'):
        return True

    return False

#################################AUTO FUNCTIONS#################################

def auto_amazing_midi(user_input_address_amaz, destination_address, tone_address, file_conversion_user_control):
    # This function does the .wav to .mid file conversions

    if conversion_identifier == 'mp3_to_pdf':
        progress_bar_values = [40,45,50,55,60,66]
    elif conversion_identifier == 'mp3_to_mid':
        progress_bar_values = [60,68,75,83,91,100]

    [end_address, filename] = output_address(user_input_address_amaz, destination_address, '.mid')

    delay = 1
    ama_app = pywinauto.application.Application()
    ama_app_exe_path = setting_read('ama_app_exe_path')
    ama_app.start(ama_app_exe_path)
    print("Initialized AmazingMIDI")
    progress_bar.current_action_label.setText("Initializing AmazingMIDI")
    progress_bar.progress.setValue(progress_bar_values[0])

    # Creating a window variable for AmazingMIDI
    while(True):
        try:
            w_handle = pywinauto.findwindows.find_windows(title='AmazingMIDI ')[0]
            window = ama_app.window(handle=w_handle) #pywinauto.application.WindowSpecification Object
            break
        except IndexError:
            time.sleep(0.1)

    # Clicking on file menu, selecting tone file
    window.menu_item(u'&File->&Specify Tone File...').click()

    # Entering the tone file's address
    #t_handle = pywinauto.findwindows.find_windows(title='Specify Tone File')[0]
    t_handle = pywinauto.findwindows.find_windows(parent=w_handle)[0]
    t_window = ama_app.window(handle=t_handle)

    t_window.type_keys(tone_address)
    t_window.type_keys('{ENTER}')
    progress_bar.current_action_label.setText("Opening tune WAV file")
    progress_bar.progress.setValue(progress_bar_values[1])

    # Clicking on file menu, selecting input file
    window.menu_item(u'&File->&Specify Input File...').click()

    # Entering the user input file's address
    #i_handle = pywinauto.findwindows.find_windows(title='Specify Input File')[0]
    i_handle = pywinauto.findwindows.find_windows(parent=w_handle)[0]
    i_window = ama_app.window(handle=i_handle)

    i_window.type_keys(user_input_address_amaz)
    i_window.type_keys('{ENTER}')
    progress_bar.current_action_label.setText("Opening input WAV file")
    progress_bar.progress.setValue(progress_bar_values[2])

    # Clicking on file menu, selecting output files
    window.menu_item(u'&File->&Specify Output File...').click()

    # Entering the output file's end_address
    #o_handle = pywinauto.findwindows.find_windows(title='Specify Output File')[0]
    o_handle = pywinauto.findwindows.find_windows(parent=w_handle)[0]
    o_window = ama_app.window(handle=o_handle)

    o_window.type_keys(end_address)
    o_window.type_keys('{ENTER}')
    progress_bar.current_action_label.setText("Selecting output WAV file location")
    progress_bar.progress.setValue(progress_bar_values[3])

    # Clicking on Transcribe menu, selecting Transcribe
    time.sleep(1)
    window.wait('enabled',timeout = 30)
    window.menu_item(u'&Transcribe->&Transcribe...').click()

    # Entering Transcribe Options
    #to_handle = pywinauto.findwindows.find_windows(title='Transcribe')[0]
    to_handle = pywinauto.findwindows.find_windows(parent=w_handle)[0]
    to_window = ama_app.window(handle=to_handle)

    # Need to ask the user if they wish to manually change the features of the
    # conversion here
    if file_conversion_user_control == True:
        progress_bar.current_action_label.setText("Waiting for User's Filter Selection")
        user_notification_mgbox = QMessageBox()
        user_notification_mgbox.setParent(None)
        user_notification_mgbox.setWindowTitle("Filter Control")
        user_notification_mgbox.setText("Please select the desired filtering and continue. Close this before pressing start.")
        user_notification_mgbox.setWindowFlag(Qt.WindowStaysOnTopHint)
        user_notification_mgbox.exec_()
        time.sleep(0.3)

        while(True):
            try:
                to_handle = pywinauto.findwindows.find_windows(title='Transcribe')[0]
                #to_handle = pywinauto.findwindows.find_window(parent=w_handle)[0]
                time.sleep(0.4)
            except:
                break

        print("Transcribe Window Closed")

    else:
        to_window.type_keys('{ENTER}')

    progress_bar.current_action_label.setText("Transcribing WAV files into MIDI")
    progress_bar.progress.setValue(progress_bar_values[4])

    # Closing amazingmidi
    time.sleep(1)
    window.wait('enabled', timeout = 30)
    window.menu_item(u'&File->Exit').click()

    print(".wav -> .mid complete")
    progress_bar.current_action_label.setText(".wav -> .mid complete")
    progress_bar.progress.setValue(progress_bar_values[5])
    return end_address

###############################################################################

def auto_audacity(user_input_address_auda,destination_address):
    # This function does the automation of the audacity application

    if conversion_identifier == 'mp3_to_pdf':
        progress_bar_values = [0,10,20,33]

    elif conversion_identifier == 'mp3_to_mid':
        progress_bar_values = [0,20,30,50]

    [end_address, filename] = output_address(user_input_address_auda, destination_address, '.wav')
    aud_app = pywinauto.application.Application()
    aud_app_exe_path = setting_read('aud_app_exe_path')
    aud_app.start(aud_app_exe_path)
    progress_bar.current_action_label.setText("Initializing Audacity")
    progress_bar.progress.setValue(progress_bar_values[0])

    # Creating a window variable for Audacity
    while(True):
        try:
            w_handle = pywinauto.findwindows.find_windows(title='Audacity')[0] #[461274]
            window = aud_app.window(handle=w_handle) #pywinauto.application.WindowSpecification Object
            break
        except IndexError:
            time.sleep(0.2)

    # Clicking on file menu
    window.menu_item(u'&File->&Open').click()

    # Creating a window variable for File Browser
    while(True):
        try:
            #w_open_handle = pywinauto.findwindows.find_windows(title='Select one or more audio files...')[0]
            w_open_handle = pywinauto.findwindows.find_windows(parent = w_handle)[0]
            w_open = aud_app.window(handle=w_open_handle)
            break
        except IndexError:
            time.sleep(0.2)

    # Entering the user's input file
    w_open.type_keys(user_input_address_auda)
    w_open.type_keys("{ENTER}")
    progress_bar.current_action_label.setText("Opening MP3 file")
    progress_bar.progress.setValue(progress_bar_values[1])

    # Wait until the file has been opened
    time.sleep(1)
    window.wait('enabled', timeout = 30)

    # Export the file
    window.menu_item('&File->Export Audio ...').click()

    while(True):
        try:
            #w_export_handle = pywinauto.findwindows.find_windows(title='Export Audio')[0]
            w_export_handle = pywinauto.findwindows.find_windows(parent = w_handle)[0]
            w_export = aud_app.window(handle=w_export_handle)
            break
        except IndexError:
            time.sleep(0.2)

    #w_export.type_keys(filename)
    w_export.type_keys(end_address)
    w_export.type_keys("{ENTER}")
    progress_bar.current_action_label.setText("Exporting MP3 file as WAV file")
    progress_bar.progress.setValue(progress_bar_values[2])

    # Editing Metadata
    time.sleep(0.5)
    aud_app.EditMetadata.OK.click()
    time.sleep(1)
    window.wait('enabled', timeout = 30)
    time.sleep(0.1)

    # Closing Audacity
    window.menu_item('&File->&Close').click()
    time.sleep(0.1)
    aud_app.SaveChanges.No.click()
    aud_app.kill()
    time.sleep(0.1)

    print(".mp3 -> .wav complete")
    progress_bar.current_action_label.setText(".mp3 -> .wav complete")
    progress_bar.progress.setValue(progress_bar_values[3])
    return end_address

################################################################################

def auto_midi_music_sheet(user_input_address_midi,destination_address):
    # This functions does the automation of the midi_music_sheet application.

    if conversion_identifier == 'mp3_to_pdf':
        progress_bar_values = [70,80,90,100]
    elif conversion_identifier == 'mid_to_pdf':
        progress_bar_values = [0,40,80,100]

    [end_address, filename] = output_address(user_input_address_midi, destination_address, '.pdf')
    midi_app = pywinauto.application.Application()
    midi_app_exe_path = setting_read('midi_app_exe_path')
    midi_app.start(midi_app_exe_path)
    print("Initialized MidiSheetMusic")
    progress_bar.current_action_label.setText("Initializing MidiSheetMusic")
    progress_bar.progress.setValue(progress_bar_values[0])

    # Creating a window variable for Midi Sheet Music
    while(True):
        try:
            w_handle = pywinauto.findwindows.find_windows(title='Midi Sheet Music')[0]
            window = midi_app.window(handle=w_handle)
            break
        except IndexError:
            time.sleep(0.2)

    # Clicking on file menu
    window.menu_item(u'&File->&Open').click()

    # Entering the input file's address
    while(True):
        try:
            #o_handle = pywinauto.findwindows.find_windows(title='Open')[0]
            o_handle = pywinauto.findwindows.find_windows(parent=w_handle)[0]
            o_window = midi_app.window(handle=o_handle)
            break
        except IndexError:
            time.sleep(0.2)

    o_window.type_keys(user_input_address_midi)
    o_window.type_keys('{ENTER}')

    progress_bar.current_action_label.setText("Opening MIDI file")
    progress_bar.progress.setValue(progress_bar_values[1])

    # Wait until the file has been opened
    time.sleep(1)
    window.wait('enabled', timeout = 30)

    # Saving the .pdf file to final address
    window.menu_item(u'&File->&Save as PDF...').click()

    while(True):
        try:
            #s_handle = pywinauto.findwindows.find_windows(title='Save As')[0]
            s_handle = pywinauto.findwindows.find_windows(parent=w_handle)[0]
            s_window = midi_app.window(handle=s_handle)
            break
        except IndexError:
            time.sleep(0.2)

    s_window.type_keys(end_address)
    s_window.type_keys('{ENTER}')

    progress_bar.current_action_label.setText("Saving PDF file")
    progress_bar.progress.setValue(progress_bar_values[2])

    # Closing the application *HARD CODED*
    #time.sleep(0.5)
    #while(True):
    #    try:
    #        c_handle = pywinauto.findwindows.find_windows(title='Generating PDF Document...')[0]
    #        c_window = midi_app.window(handle=c_handle)
    #        break
    #    except IndexError:
    #        print('.', end = '')

    #c_window.wait('not visible', timeout = 30)

    #window.wait('visible', timeout = 30)

    #I cannot create a fool proof method to wait for the pdf file generation.
    #The best I could come up with is creating a time delay using the size of
    #the file.

    # Creating file_size_dependent_delay_time
    file_size = os.path.getsize(user_input_address_midi)
    file_size_dependent_delay_time = file_size/2000 + 1
    time.sleep(file_size_dependent_delay_time)
    #window.menu_item(u'&File->&Exit')
    midi_app.kill()

    print(".mid -> .pdf complete")
    progress_bar.current_action_label.setText(".mid -> .pdf complete")
    progress_bar.progress.setValue(progress_bar_values[3])
    return end_address

################################################################################

def auto_audiveris(user_input_address_audi, destination_address):
    # This function automates the program audiveris.

    if conversion_identifier == 'pdf_to_mid':
        progress_bar_values = [0,20,30,50]

    [end_address,filename] = output_address(user_input_address_audi,destination_address, '.mxl')
    os.system("start \"\" cmd /c \"cd " + skore_program_controller_path +" & start_audiveris.py \"")

    time.sleep(1)
    print('Initialized Audiveris.', end = '')
    progress_bar.current_action_label.setText("Initializing Audiveris")
    progress_bar.progress.setValue(progress_bar_values[0])

    # Trying to handle Audiveris, waiting until the window is available
    while(True):
        try:
            audi_app = pywinauto.application.Application().connect(title = 'Audiveris')
            break
        except pywinauto.findwindows.ElementNotFoundError:
            print('.', end = '')
            time.sleep(0.5)

    # Once the window is available, obtain control of the application
    while(True):
        try:
            w_handle = pywinauto.findwindows.find_windows(title='Audiveris')[0]
            window = audi_app.window(handle=w_handle) #pywinauto.application.WindowSpecification Object
            break
        except IndexError:
            time.sleep(0.1)

    # Place the Audiveris window above all and maximize
    window.type_keys("{TAB}")
    window.maximize()
    time.sleep(0.1)

    original_rect_dimensions = window.rectangle()
    audi_dimensions = rect_to_int(original_rect_dimensions)

    # Accessing the input menu
    click_center_try('file_button', audi_dimensions)
    click_center_try('input_button', audi_dimensions)
    progress_bar.current_action_label.setText("Opening PDF File")
    progress_bar.progress.setValue(progress_bar_values[1])

    # Inputting the .pdf file address to load into audiveris
    while(True):
        try:
            window.type_keys(user_input_address_audi)
            time.sleep(0.5)
            break
        except pywinauto.base_wrapper.ElementNotEnabled:
            print(".", end = '')
            time.sleep(0.1)

    # Entering the export menu
    click_center_try('open_button', audi_dimensions)
    click_center_try('book_button', audi_dimensions)
    #time.sleep(5) HARD CODED

    # Creating file_size_dependent_delay_time
    file_size = os.path.getsize(user_input_address_audi)
    file_size_dependent_delay_time = int(file_size/1000000 + 5)
    print(file_size_dependent_delay_time)
    time.sleep(file_size_dependent_delay_time)

    click_center_try('export_book_as_button', audi_dimensions)

    # Entering final address to export book as button
    while(True):
        try:
            window.type_keys(end_address)
            progress_bar.current_action_label.setText("Exporting the MXL file")
            progress_bar.progress.setValue(progress_bar_values[2])
            time.sleep(0.5)
            break
        except pywinauto.base_wrapper.ElementNotEnabled:
            print(".", end = '')
            time.sleep(0.1)

    time.sleep(1)

    # Image porcessing to select "Save" button
    click_center_try('save_button', audi_dimensions)

    # Waiting for the completion of the transcribing of the book
    output_file = Path(end_address)
    progress_bar.current_action_label.setText("Waiting for MXL file generation. Takes a while")
    progress_bar.progress.setValue(progress_bar_values[3])
    while(True):
        if(output_file.is_file()):
            time.sleep(0.1)
            break
        else:
            time.sleep(0.5)

    # Closing Audiveris
    audi_app.kill()
    print(".pdf -> .mxl complete")
    progress_bar.current_action_label.setText(".pdf -> .mxl complete")
    progress_bar.progress.setValue(progress_bar_values[3])
    return end_address

################################################################################

def auto_xenoplay(user_input_address_xeno, destination_address):
    # This function does the automation of the xenoplay application
    # This is the highest-possibility of failure function. THIS WORKS SOMETIMES

    if conversion_identifier == 'pdf_to_mid':
        progress_bar_values = [60,70,80,100]

    [end_address, filename] = output_address(user_input_address_xeno, destination_address, '.mid')
    os.system("start \"\" cmd /c \"cd " + skore_program_controller_path +" & start_xenoplay.py \"")
    print("Initializing Xenoplayer")
    progress_bar.current_action_label.setText("Initializing Xenoplayer")
    progress_bar.progress.setValue(progress_bar_values[0])

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
    #xeno_app = pywinauto.application.Application().connect(title = 'Xenoage Player 0.4')
    while(True):
        try:
            w_handle = pywinauto.findwindows.find_windows(title='Xenoage Player 0.4')[0]
            window = xeno_app.window(handle=w_handle) #pywinauto.application.WindowSpecification Object
            break
        except IndexError:
            time.sleep(0.1)

    delay = 0.4

    # Opening the .mxl file onto Xenoage Player
    original_rect_dimensions = window.rectangle()
    xeno_dimensions = rect_to_int(original_rect_dimensions)

    time.sleep(delay)
    click_center_try('file_button_xeno', xeno_dimensions)
    time.sleep(delay)
    click_center_try('open_button_xeno_menu', xeno_dimensions)
    time.sleep(delay)
    progress_bar.current_action_label.setText("Opening MXL File")
    progress_bar.progress.setValue(progress_bar_values[1])

    # Entering the address of the mxl file and opening the file
    #time.sleep(1)
    while(True):
        try:
            #o_handle = pywinauto.findwindows.find_windows(title='Open')[0]
            o_handle = pywinauto.findwindows.find_windows(parent=w_handle)[0]
            o_window = xeno_app.window(handle=o_handle)
            break
        except IndexError:
            time.sleep(0.1)

    original_rect_dimensions = o_window.rectangle()
    xeno_open_dimensions = rect_to_int(original_rect_dimensions)

    o_window.type_keys(user_input_address_xeno)
    time.sleep(delay)
    click_center_try('open_button_xeno', xeno_open_dimensions)
    time.sleep(delay)

    # Attempting to save the .mxl as a .mid file, while also stoping the app
    # from playing music
    #original_rect_dimensions = window.rectangle()
    #int_dimensions = rect_to_int(original_rect_dimensions)

    click_center_try('stop_button_xeno', xeno_dimensions)
    time.sleep(delay)
    click_center_try('file_button_xeno', xeno_dimensions)
    time.sleep(delay)
    click_center_try('save_as_button_xeno', xeno_dimensions)
    time.sleep(delay)
    progress_bar.current_action_label.setText("Saving MIDI File")
    progress_bar.progress.setValue(progress_bar_values[2])

    # Entering the new name and address of the .mid file
    #time.sleep(1)
    while(True):
        try:
            #s_handle = pywinauto.findwindows.find_windows(title='Save')[0]
            s_handle = pywinauto.findwindows.find_windows(parent=w_handle)[0]
            s_window = xeno_app.window(handle=s_handle)
            break
        except IndexError:
            time.sleep(0.1)

    original_rect_dimensions = s_window.rectangle()
    xeno_save_dimensions = rect_to_int(original_rect_dimensions)

    time.sleep(delay)
    s_window.type_keys(end_address)
    time.sleep(delay)
    click_center_try('save_button_xeno', xeno_save_dimensions)
    time.sleep(delay)

    # Closing Xenoplay
    xeno_app.kill()
    print(".mxl -> .mid complete")
    progress_bar.current_action_label.setText(".mxl -> .mid complete")
    progress_bar.progress.setValue(progress_bar_values[3])
    return end_address

################################################################################

def auto_anthemscore(user_input_address_anth, destination_address, file_type, file_conversion_user_control):

    progress_bar_values = [0,15,30,45,60,75,90,100]

    # Obtaining the end address name
    [end_address, filename] = output_address(user_input_address_anth, destination_address, file_type)

    end_address_xml, trash = output_address(user_input_address_anth, destination_address, '.xml')

    # Obtaining the resulting midi file location
    if file_type == '.pdf':
        end_address_mid, trash = output_address(user_input_address_anth, destination_address, '.mid')
    else:
        end_address_mid = end_address

    # Determing the right path of conversion
    if file_conversion_user_control == False and file_type != '.pdf':
        progress_bar.current_action_label.setText("Initializing AnthemScore headless")
        progress_bar.progress.setValue(progress_bar_values[0])
        print("Easy")
        #os.system(r'AnthemScore -a ' + user_input_address_anth + ' -m ' + end_address)
        os.system("start \"\" cmd /c \"AnthemScore -a " + user_input_address_anth + " -m " + end_address + "\"")
        # Waiting for the completion of the file conversion
        output_file = Path(end_address)
        progress_bar.current_action_label.setText("Waiting for output file conversion.")
        counter = 0
        while(True):
            if(output_file.is_file()):
                time.sleep(0.1)
                break
            else:
                time.sleep(0.5)
                counter += 0.5
                if counter == 100:
                    counter = 80
                progress_bar.progress.setValue(counter)
    else:
        print("Difficult")
        ant_app_exe_path = setting_read('ant_app_exe_path')
        ant_app = pywinauto.application.Application()
        ant_app.start(ant_app_exe_path)
        print("Initializing AnthemScore")
        progress_bar.current_action_label.setText("Initializing AnthemScore GUI")
        progress_bar.progress.setValue(progress_bar_values[0])

        while(True):
            try:
                w_handle = pywinauto.findwindows.find_windows(title='AnthemScore')[0]
                window = ant_app.window(handle=w_handle)
                break
            except IndexError:
                time.sleep(0.2)

        # Clicking on file menu
        window.wait('enabled')
        time.sleep(0.5)
        window.maximize()
        original_rect_dimensions = window.rectangle()
        ant_dimensions = rect_to_int(original_rect_dimensions)
        progress_bar.current_action_label.setText("Opening File Menu")
        progress_bar.progress.setValue(progress_bar_values[1])
        click_center_try('file_button_anthem', ant_dimensions)
        click_center_try('open_button_anthem', ant_dimensions)

        # Creating a window variable for File Browser Dialog
        while(True):
            try:
                #w_open_handle = pywinauto.findwindows.find_windows(title="Select File")[0]
                w_open_handle = pywinauto.findwindows.find_windows(parent=w_handle)[0]
                w_open_window = ant_app.window(handle=w_open_handle)
                break
            except IndexError:
                time.sleep(0.2)

        # Entering the user's input file
        progress_bar.current_action_label.setText("Entering Input File")
        progress_bar.progress.setValue(progress_bar_values[2])
        w_open_window.type_keys(user_input_address_anth)
        w_open_window.type_keys("{ENTER}")

        # Wait until the file has been processed
        time.sleep(1)

        # Creating a window variable for Select File Dialog
        while(True):
            try:
                #s_open_handle = pywinauto.findwindows.find_windows(title=u'Select File')[0]
                s_open_handle = pywinauto.findwindows.find_windows(parent=w_handle)[0]
                s_open_window = ant_app.window(handle=s_open_handle)
                break
            except:
                try:
                    s_open_handle = pywinauto.findwindows.find_windows(parent=w_open_handle)[0]
                    s_open_window = ant_app.window(handle=s_open_handle)
                    break
                except:
                    try:
                        s_open_handle = pywinauto.findwindows.find_windows(title=u'Select File')[0]
                        s_open_window = ant_app.window(handle=s_open_handle)
                        break
                    except:
                        time.sleep(0.2)


            #except IndexError:
                #time.sleep(0.2)

        # Selecting Save As option
        original_rect_dimensions = s_open_window.rectangle()
        ant_open_dimensions = rect_to_int(original_rect_dimensions)
        click_center_try('save_as_button_anthem', ant_open_dimensions)

        # Creating a window variable for Save As Dialog
        while(True):
            try:
                #s_handle = pywinauto.findwindows.find_windows(title=u'Save As')[0]
                s_handle = pywinauto.findwindows.find_windows(parent=w_handle)[0]
                s_window = ant_app.window(handle=s_handle)
                break
            except:
                try:
                    s_handle = pywinauto.findwindows.find_windows(parent=w_handle)[0]
                    s_window = ant_app.window(handle=s_handle)
                    break
                except:
                    try:
                        s_handle = pywinauto.findwindows.find_windows(title=u'Save As')[0]
                        s_window = ant_app.window(handle=s_handle)
                        break
                    except:
                        time.sleep(0.2)

        progress_bar.current_action_label.setText("Selecting Destination Location")
        progress_bar.progress.setValue(progress_bar_values[3])
        #s_window.type_keys(end_address)
        s_window.type_keys(end_address_xml)
        s_window.type_keys("{ENTER}")
        time.sleep(2.5)

        click_center_try('ok_button_anthem', ant_open_dimensions)
        progress_bar.current_action_label.setText("Transcribing input file")
        progress_bar.progress.setValue(progress_bar_values[4])

        # Creating a window variable for Viewer Dialog
        while(True):
            try:
                #v_handle = pywinauto.findwindows.find_windows(title=u'Viewer')[0]
                v_handle = pywinauto.findwindows.find_windows(parent=w_handle)[0]
                v_window = ant_app.window(handle=v_handle)
                break
            except IndexError:
                time.sleep(1)

        print("File Processing Done")
        v_window.close()

        # Need to ask the user if they wish to manually change the features of the
        # conversion here
        if file_conversion_user_control == True:
            progress_bar.current_action_label.setText("Waiting for User Control Completion")
            user_notification_mgbox = QMessageBox()
            user_notification_mgbox.setParent(None)
            user_notification_mgbox.setWindowTitle("Filter Control")
            user_notification_mgbox.setText("Once finish utilizing AnthemScore, press [Ok]")
            user_notification_mgbox.setWindowFlag(Qt.WindowStaysOnTopHint)
            user_notification_mgbox.exec_()
            time.sleep(0.3)

        if user_input_address_anth[-4:] != '.mid':

            # Now actually saving the transformed files
            progress_bar.current_action_label.setText("Saving other useful file types")
            progress_bar.progress.setValue(progress_bar_values[5])
            click_center_try('file_button_anthem', ant_dimensions)
            click_center_try('save_as_button2_anthem', ant_dimensions)

            # Creating a window variable for Save As Dialog
            while(True):
                try:
                    #s2_handle = pywinauto.findwindows.find_windows(title=u'Save As')[0]
                    s2_handle = pywinauto.findwindows.find_windows(parent=w_handle)[0]
                    s2_window = ant_app.window(handle=s2_handle)
                    break
                except:
                    try:
                        s2_handle = pywinauto.findwindows.find_windows(title=u'Save As')[0]
                        s2_window = ant_app.window(handle=s2_handle)
                        break
                    except:
                        time.sleep(0.2)

            original_rect_dimensions = s2_window.rectangle()
            ant_save_dimensions = rect_to_int(original_rect_dimensions)

            # Selecting file type and saving the file
            click_center_try('format_button_anthem', ant_save_dimensions)

            """
            if file_type == '.mid':
                print("Clicked on pdf")
                click_center_try('format_pdf_button_anthem', ant_save_dimensions)
            elif file_type == '.pdf':
                click_center_try('format_mid_button_anthem', ant_save_dimensions)
                print("Clicked on mid")

            click_center_try('ok_button_anthem', ant_save_dimensions)
            """

            click_center_try('format_pdf_button_anthem', ant_save_dimensions)
            click_center_try('ok_button_anthem', ant_save_dimensions)

            time.sleep(0.5)
            click_center_try('file_button_anthem', ant_dimensions)
            click_center_try('save_as_button2_anthem', ant_dimensions)

            # Creating a window variable for Save As Dialog
            while(True):
                try:
                    #s2_handle = pywinauto.findwindows.find_windows(title=u'Save As')[0]
                    s2_handle = pywinauto.findwindows.find_windows(parent=w_handle)[0]
                    s2_window = ant_app.window(handle=s2_handle)
                    break
                except:
                    try:
                        s2_handle = pywinauto.findwindows.find_windows(title=u'Save As')[0]
                        s2_window = ant_app.window(handle=s2_handle)
                        break
                    except:
                        time.sleep(0.2)

            original_rect_dimensions = s2_window.rectangle()
            ant_save_dimensions = rect_to_int(original_rect_dimensions)
            click_center_try('format_button_anthem', ant_save_dimensions)
            click_center_try('format_mid_button_anthem', ant_save_dimensions)
            click_center_try('ok_button_anthem', ant_save_dimensions)



        progress_bar.current_action_label.setText("Closing AnthemScore")
        progress_bar.progress.setValue(progress_bar_values[6])
        time.sleep(5)
        ant_app.kill()

    progress_bar.current_action_label.setText("File Conversion Complete")
    progress_bar.progress.setValue(progress_bar_values[7])
    return end_address, end_address_mid

################################################################################

def start_red_dot_forever():
    # This function simply starts the red dot forever application

    red_app = pywinauto.application.Application()
    red_app_exe_path = setting_read('red_app_exe_path')
    red_app.start(red_app_exe_path)
    print("Initialized Red Dot Forever")
    return

################################################################################

def start_piano_booster():
    # This function starts the piano booster application

    pia_app = pywinauto.application.Application()
    pia_app_exe_path = setting_read('pia_app_exe_path')
    pia_app.start(pia_app_exe_path)
    print("Initialized PianoBooser")
    return

########################MAJOR FILE CONVERSIONS FUNCTIONS########################

def mp3_to_pdf(mp3_input):
    # This function converts a .mp3 to .pdf

    global amazing_midi_tune
    mp3_2_midi_converter_setting = setting_read('mp3_2_midi_converter')
    file_conversion_user_control = eval(setting_read('file_conversion_user_control'))

    clean_temp_folder()
    if mp3_2_midi_converter_setting == 'amazingmidi':
        converted_wav_input = auto_audacity(mp3_input,temp_folder_path)
        converted_mid_input = auto_amazing_midi(converted_wav_input, temp_folder_path, amazing_midi_tune, file_conversion_user_control)
        converted_pdf_input = auto_midi_music_sheet(converted_mid_input, temp_folder_path)
    elif mp3_2_midi_converter_setting == 'anthemscore':
        converted_pdf_input, converted_mid_input = auto_anthemscore(mp3_input, temp_folder_path, '.pdf', file_conversion_user_control)

    print("Overall .mp3 -> .pdf complete")
    return converted_mid_input

def mp3_to_mid(mp3_input):
    # This function converts a .mp3 to .mid

    global amazing_midi_tune
    mp3_2_midi_converter_setting = setting_read('mp3_2_midi_converter')
    file_conversion_user_control = eval(setting_read('file_conversion_user_control'))

    clean_temp_folder()
    if mp3_2_midi_converter_setting == 'amazingmidi':
        converted_wav_input = auto_audacity(mp3_input, temp_folder_path)
        converted_mid_input = auto_amazing_midi(converted_wav_input, temp_folder_path, amazing_midi_tune, file_conversion_user_control)
    elif mp3_2_midi_converter_setting == 'anthemscore':
        converted_mid_input, trash = auto_anthemscore(mp3_input, temp_folder_path, '.mid', file_conversion_user_control)
    print("Overall .mp3 -> .mid complete")
    return converted_mid_input

def mid_to_pdf(mid_input):
    # This function converts a .mid to .pdf
    mp3_2_midi_converter_setting = setting_read('mp3_2_midi_converter')
    file_conversion_user_control = eval(setting_read('file_conversion_user_control'))

    clean_temp_folder()
    if mp3_2_midi_converter_setting == 'amazingmidi':
        converted_pdf_input = auto_midi_music_sheet(mid_input, temp_folder_path)
    elif mp3_2_midi_converter_setting == 'anthemscore':
        converted_pdf_input = auto_anthemscore(mid_input, temp_folder_path, '.pdf', file_conversion_user_control)
    print("Overall .mid -> .pdf complete")
    return mid_input

def pdf_to_mid(pdf_input):
    # This function converts a .pdf to .mid

    clean_temp_folder()
    converted_mxl_input = auto_audiveris(pdf_input, temp_folder_path)
    converted_mid_input = auto_xenoplay(converted_mxl_input, temp_folder_path)
    print("Overall .pdf -> .mid complete")
    return converted_mid_input

####################HIGHEST LEVEL FILE CONVERSION FUNCTIONS#####################

def input_to_pdf(input, progress_bar_object):
    # This function converts any file into a .pdf

    global progress_bar, conversion_identifier

    progress_bar = progress_bar_object
    progress_bar.current_action_label.setText('Staring input to pdf')
    progress_bar.progress.setValue(0)

    if(is_mid(input)):
        conversion_identifier = 'mid_to_pdf'
        mid_path = mid_to_pdf(input)
    elif(is_mp3(input)):
        conversion_identifier = 'mp3_to_pdf'
        mid_path = mp3_to_pdf(input)
    else:
        raise RuntimeError("Input file type is invalid")
    return mid_path

def input_to_mid(input, progress_bar_object):
    # This function converts any file into a .mid

    global progress_bar, conversion_identifier

    progress_bar = progress_bar_object
    progress_bar.current_action_label.setText('Staring input to mid')
    progress_bar.progress.setValue(0)

    if(is_pdf(input)):
        conversion_identifier = 'pdf_to_mid'
        mid_path = pdf_to_mid(input)
    elif(is_mp3(input)):
        conversion_identifier = 'mp3_to_mid'
        mid_path = mp3_to_mid(input)
    else:
        raise RuntimeError("Input file type is invalid")
    return mid_path
