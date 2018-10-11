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
#from shutil import move
from shutil import copyfile, move
import shutil

################################################################################
##############################CONSTANTS#########################################
################################################################################

templates_address = []
destination_address = []

#Determing the address of the entire SKORE system
complete_path = os.path.dirname(os.path.abspath(__file__))
skore_index = complete_path.find('SKORE') + len('SKORE')
skore_path = complete_path[0:skore_index+1]

skore_program_controller_extension_path = r"user_interface\app_control"
temp_folder_extension_path = r"user_interface\app_control\temp"
templates_folder_extension_path = r"user_interface\app_control\templates"
conversion_test_folder_extension_path = r"user_interface\app_control\conversion_test"
misc_folder_extension_path = r"user_interface\app_control\misc"
output_folder_extension_path = r"user_interface\app_control\output"

#Determing the address of the temp and templates folders
temp_folder_path = skore_path + temp_folder_extension_path
templates_folder_path = skore_path + templates_folder_extension_path
conversion_test_folder_path = skore_path + conversion_test_folder_extension_path
misc_folder_path = skore_path + misc_folder_extension_path
output_folder_path = skore_path + output_folder_extension_path
skore_program_controller_path = skore_path + skore_program_controller_extension_path

#Purely Testing Purposes
default_or_temp_mode = 'temp'
amazing_midi_tune = misc_folder_path + '\\' + 'piano0.wav'

################################################################################
##############################FUNCTIONS#########################################
################################################################################

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

################################################################################

def click_center(button):
    #This function utilizes screen shoots and determines the location of certain
    #buttons within the screenshot.

    #global templates_folder_path

    image = pyautogui.screenshot()
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
    file_button_center_coords = [ int((top_left[0]+bottom_right[0])/2) , int((top_left[1]+bottom_right[1])/2) ]
    pywinauto.mouse.click(button="left",coords=(file_button_center_coords[0],file_button_center_coords[1]))
    os.remove('gui_screenshot.png')
    time.sleep(0.1)
    return

################################################################################

def click_center_try(button):
    #This functions does the same as click_center, but allows the function to wait
    #Until the image is found.

    while(True):
        try:
            click_center(button)
            break
        except AttributeError:
            #print('.', end='')
            time.sleep(0.5)
    return

################################################################################

def clean_temp_folder():
    #This function cleans the temp file within SKORE repository

    #global temp_folder_path

    files = glob.glob(temp_folder_path + '\*')

    for file in files:
        os.remove(file)
    return

################################################################################

def temp_to_folder(**kwargs):
    #This functions transfer all the files found within temp folder into
    #"destination_folder" with the "filename" given.

    filename = kwargs.get('filename', None)
    destination_folder = kwargs.get('destination_folder', None)
    print("Transfering files with name: " + filename + "\t To directory: " + destination_folder)
    #print(filename)
    #print(destination_folder)

    files = glob.glob(temp_folder_path + '\*')

    for file in files:
        old_file = os.path.basename(file)
        file_type = os.path.splitext(old_file)[1]

        if(filename):
            if(destination_folder):
                shutil.move(file, destination_folder + '\\' + filename + file_type)
            else:
                shutil.move(file, output_folder_path + '\\' + filename + file_type)
        else:
            if(destination_folder):
                shutil.move(file, destination_folder + '\\' + old_file)
            else:
                shutil.move(file, output_folder_path + '\\' + old_file)
    return


################################################################################

def setting_read(setting):
    #Reading the value of the setting
    import sys
    #Opening File

    """
    if(default_or_temp == 'default'):
        file = open(skore_path + skore_program_controller_extension_path + '\\' + 'settings_default.txt', 'r')
    elif(default_or_temp == 'temp'):
        file = open(skore_path + skore_program_controller_extension_path + '\\' + 'settings_temp.txt', 'r')
    else:
        raise RuntimeError('Invalid setting file selection')
    """

    file = open(skore_path + skore_program_controller_extension_path + '\\' + 'settings.txt', 'r')
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

################################################################################

def setting_write(setting, write_data, temp_mode):
    #Writing the configuration settings of the settings_temp.txt file

    #Opening File
    """
    if(temp_mode == 'write'):
        #overwrite complete settings_temp.txt
        file_read = open(skore_path + skore_program_controller_extension_path + '\\' + 'settings_default.txt', 'r')
    elif(temp_mode == 'append'):
        #only edit sections of settings_temp.txt
        file_read = open(skore_path + skore_program_controller_extension_path + '\\' + 'settings_temp.txt', 'r')
    else:
        raise RuntimeError('Invalid overwriting/appending mode')
    """

    file_read = open(skore_path + skore_program_controller_extension_path + '\\' + 'settings.txt', 'r')
    contents_all = file_read.read()
    contents_line = file_read.readlines()
    file_read.close()

    #Finding the setting wanted to be changed
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

    #Writing the value of the setting onto the file
    file_write = open(skore_path + skore_program_controller_extension_path + '\\' + 'settings.txt', 'w')
    file_write.write(contents_all)
    file_write.close()
    print("Settings for " + setting + " have been modified to " + write_data)
    return

def is_mid(file_path):
    #Test if the input file is .mid

    file_name = os.path.basename(file_path)
    file_type = os.path.splitext(file_name)[1]

    if(file_type == '.mid'):
        return True

    return False

def is_mp3(file_path):
    #Test if the input file is .mp3

    file_name = os.path.basename(file_path)
    file_type = os.path.splitext(file_name)[1]

    if(file_type == '.mp3'):
        return True

    return False

def is_pdf(file_path):
    #Test if the input file is .pdf

    file_name = os.path.basename(file_path)
    file_type = os.path.splitext(file_name)[1]

    if(file_type == '.pdf'):
        return True

    return False

################################################################################
#################################AUTO FUNCTIONS#################################
################################################################################

def auto_amazing_midi(user_input_address_amaz, destination_address, tone_address):
    #This function does the .wav to .mid file conversions
    #global default_or_temp_mode

    [end_address, filename] = output_address(user_input_address_amaz, destination_address, '.mid')

    delay = 1
    ama_app = pywinauto.application.Application()
    #ama_app_exe_path = setting_read('ama_app_exe_path', default_or_temp_mode)
    ama_app_exe_path = setting_read('ama_app_exe_path')
    #ama_app.start(r"C:\Program Files (x86)\AmazingMIDI\amazingmidi.exe")
    ama_app.start(ama_app_exe_path)
    print("Initialized AmazingMIDI")

    #Creating a window variable for AmazingMIDI
    while(True):
        try:
            w_handle = pywinauto.findwindows.find_windows(title='AmazingMIDI ')[0]
            window = ama_app.window(handle=w_handle) #pywinauto.application.WindowSpecification Object
            #print()
            break
        except IndexError:
            #print('.', end = '')
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
    time.sleep(1)
    window.wait('enabled',timeout = 30)
    window.menu_item(u'&Transcribe->&Transcribe...').click()

    #Entering Transcribe Options
    to_handle = pywinauto.findwindows.find_windows(title='Transcribe')[0]
    to_window = ama_app.window(handle=to_handle)
    to_window.type_keys('{ENTER}')

    #Closing amazingmidi
    time.sleep(1)
    window.wait('enabled', timeout = 30)
    window.menu_item(u'&File->Exit').click()

    print(".wav -> .mid complete")
    return end_address

###############################################################################

def auto_audacity(user_input_address_auda,destination_address):
    #This function does the automation of the audacity application
    #global default_or_temp_mode

    [end_address, filename] = output_address(user_input_address_auda, destination_address, '.wav')
    aud_app = pywinauto.application.Application()
    #aud_app_exe_path = setting_read('aud_app_exe_path', default_or_temp_mode)
    aud_app_exe_path = setting_read('aud_app_exe_path')
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
    time.sleep(1)
    window.wait('enabled', timeout = 30)
    time.sleep(0.1)

    #Closing Audacity
    window.menu_item('&File->&Close').click()
    time.sleep(0.1)
    aud_app.SaveChanges.No.click()
    aud_app.kill()
    time.sleep(0.1)

    print(".mp3 -> .wav complete")
    return end_address

################################################################################

def auto_midi_music_sheet(user_input_address_midi,destination_address):
    #This functions does the automation of the midi_music_sheet application.
    #global default_or_temp_mode

    [end_address, filename] = output_address(user_input_address_midi, destination_address, '.pdf')
    midi_app = pywinauto.application.Application()
    #midi_app_exe_path = setting_read('midi_app_exe_path', default_or_temp_mode)
    midi_app_exe_path = setting_read('midi_app_exe_path')
    #midi_app.start(r"C:\Users\daval\Desktop\MidiSheetMusic-2.6.exe")
    midi_app.start(midi_app_exe_path)
    print("Initialized MidiSheetMusic")

    #Creating a window variable for Midi Sheet Music
    while(True):
        try:
            w_handle = pywinauto.findwindows.find_windows(title='Midi Sheet Music')[0]
            window = midi_app.window(handle=w_handle) #pywinauto.application.WindowSpecification Object
            #print()
            break
        except IndexError:
            #print('.', end = '')
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

    #Creating file_size_dependent_delay_time
    file_size = os.path.getsize(user_input_address_midi)
    file_size_dependent_delay_time = file_size/2000 + 1
    time.sleep(file_size_dependent_delay_time)
    #window.menu_item(u'&File->&Exit')
    midi_app.kill()

    print(".mid -> .pdf complete")
    return end_address

################################################################################

def auto_audiveris(user_input_address_audi, destination_address):
    #This function automates the program audiveris.

    [end_address,filename] = output_address(user_input_address_audi,destination_address, '.mxl')
    #os.system("start cmd /c start_audiveris.py")
    os.system("start \"\" cmd /c \"cd " + skore_program_controller_path +" & start_audiveris.py \"")

    time.sleep(1)
    print('Initialized Audiveris.', end = '')

    #Trying to handle Audiveris, waiting until the window is available
    while(True):
        try:
            audi_app = pywinauto.application.Application().connect(title = 'Audiveris')
            break
        except pywinauto.findwindows.ElementNotFoundError:
            print('.', end = '')
            time.sleep(0.5)

    #Once the window is available, obtain control of the application
    w_handle = pywinauto.findwindows.find_windows(title='Audiveris')[0]
    window = audi_app.window(handle=w_handle) #pywinauto.application.WindowSpecification Object

    #Place the Audiveris window above all and maximize
    window.type_keys("{TAB}")
    window.maximize()
    time.sleep(0.1)

    #Accessing the input menu
    click_center_try('file_button')
    click_center_try('input_button')

    #Inputting the .pdf file address to load into audiveris
    while(True):
        try:
            window.type_keys(user_input_address_audi)
            time.sleep(0.5)
            break
        except pywinauto.base_wrapper.ElementNotEnabled:
            print(".", end = '')
            time.sleep(0.1)

    #Entering the export menu
    click_center_try('open_button')
    click_center_try('book_button')
    #time.sleep(5) HARD CODED

    #Creating file_size_dependent_delay_time
    file_size = os.path.getsize(user_input_address_audi)
    file_size_dependent_delay_time = file_size/7000 + 1
    print(file_size_dependent_delay_time)
    time.sleep(file_size_dependent_delay_time)

    click_center_try('export_book_as_button')

    #Entering final address to export book as button
    while(True):
        try:
            window.type_keys(end_address)
            time.sleep(0.5)
            break
        except pywinauto.base_wrapper.ElementNotEnabled:
            print(".", end = '')
            time.sleep(0.1)

    time.sleep(1)

    #Image porcessing to select "Save" button
    click_center_try('save_button')

    #Waiting for the completion of the transcribing of the book
    output_file = Path(end_address)
    while(True):
        if(output_file.is_file()):
            time.sleep(0.1)
            break
        else:
            time.sleep(0.5)

    #Closing Audiveris
    audi_app.kill()
    print(".pdf -> .mxl complete")
    return end_address


################################################################################

def auto_xenoplay(user_input_address_xeno, destination_address):
    #This function does the automation of the xenoplay application

    #This is the highest-possibility of failure function. THIS WORK

    [end_address, filename] = output_address(user_input_address_xeno, destination_address, '.mid')
    #os.system("start cmd /c start_xenoplay.py")
    os.system("start \"\" cmd /c \"cd " + skore_program_controller_path +" & start_xenoplay.py \"")

    #Trying to handle Xenoage Player, waiting until the window is available
    while(True):
        try:
            xeno_app = pywinauto.application.Application().connect(title = 'Xenoage Player 0.4')
            #print()
            break
        except pywinauto.findwindows.ElementNotFoundError:
            #print('.', end = '')
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
    print(".mxl -> .mid complete")
    return end_address

################################################################################

def start_red_dot_forever():
    #This function simply starts the red dot forever application
    red_app = pywinauto.application.Application()
    #red_app_exe_path = setting_read('red_app_exe_path', default_or_temp_mode)
    red_app_exe_path = setting_read('red_app_exe_path')
    #red_app.start(r"C:\Program Files (x86)\Red Dot Forever\reddot.exe")
    red_app.start(red_app_exe_path)
    print("Initialized Red Dot Forever")
    return

################################################################################

def start_piano_booster():
    #This function starts the piano booster application
    pia_app = pywinauto.application.Application()
    #pia_app_exe_path = setting_read('pia_app_exe_path', default_or_temp_mode)
    #pia_app.start(r"C:\Program Files (x86)\Piano Booster\pianobooster.exe")
    pia_app_exe_path = setting_read('pia_app_exe_path')
    pia_app.start(pia_app_exe_path)
    print("Initialized PianoBooser")

    return

################################################################################
########################MAJOR FILE CONVERSIONS FUNCTIONS########################
################################################################################

def mp3_to_pdf(mp3_input):
    #This function converts a .mp3 to .pdf
    global amazing_midi_tune
    clean_temp_folder()

    converted_wav_input = auto_audacity(mp3_input,temp_folder_path)
    converted_mid_input = auto_amazing_midi(converted_wav_input, temp_folder_path, amazing_midi_tune)
    converted_pdf_input = auto_midi_music_sheet(converted_mid_input, temp_folder_path)

    print("Overall .mp3 -> .pdf complete")
    return

def mp3_to_mid(mp3_input):
    #This function converts a .mp3 to .mid
    global amazing_midi_tune

    converted_wav_input = auto_audacity(mp3_input, temp_folder_path)
    converted_mid_input = auto_amazing_midi(converted_wav_input, temp_folder_path, amazing_midi_tune)

    print("Overall .mp3 -> .mid complete")
    return

def mid_to_pdf(mid_input):
    #This function converts a .mid to .pdf
    clean_temp_folder()

    converted_mid_input = auto_midi_music_sheet(mid_input, temp_folder_path)

    print("Overall .mid -> .pdf complete")
    return

def pdf_to_mid(pdf_input):
    #This function converts a .pdf to .mid
    clean_temp_folder()

    converted_mxl_input = auto_audiveris(pdf_input, temp_folder_path)
    converted_mp3_input = auto_xenoplay(converted_mxl_input, temp_folder_path)

    print("Overall .pdf -> .mid complete")
    return

def input_to_pdf(input):
    #This function converts any file into a .pdf
    if(is_mid(input)):
        mid_to_pdf(input)
    elif(is_mp3(input)):
        mp3_to_pdf(input)
    else:
        raise RuntimeError("Input file type is invalid")

    return

def input_to_mid(input):
    #This function converts any file into a .mid
    if(is_pdf(input)):
        pdf_to_mid(input)
    elif(is_mp3(input)):
        mp3_to_mid(input)
    else:
        raise RuntimeError("Input file type is invalid")

    return
