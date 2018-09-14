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

################################################################################
##############################CONSTANTS#########################################
################################################################################

templates_address = []
destination_address = []

#Determing the address of the entire SKORE system
complete_path = os.path.dirname(os.path.abspath(__file__))
skore_index = complete_path.find('SKORE') + len('SKORE')
skore_path = complete_path[0:skore_index+1]

temp_folder_extension_path = r"user_interface\app_control\function_system\temp"
templates_folder_extension_path = r"user_interface\app_control\function_system\templates"
conversion_test_folder_extension_path = r"user_interface\app_control\function_system\conversion_test"
misc_test_folder_extension_path = r"user_interface\app_control\function_system\misc"

#Determing the address of the temp and templates folders
temp_folder_path = skore_path + temp_folder_extension_path
templates_folder_path = skore_path + templates_folder_extension_path
conversion_test_folder_path = skore_path + conversion_test_folder_extension_path
misc_test_folder_path = skore_path + misc_test_folder_extension_path

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
    global templates_folder_path

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
            print('.', end='')
            time.sleep(0.5)
    return

################################################################################

def clean_temp_folder():
    global temp_folder_extension_path
    #This function cleans the temp file within SKORE repository
    #destination_address = temp_folder_extension_path
    #destination_address = destination_address + '\*'
    #destination_address = '%r' %destination_address
    #destination_address = destination_address[1:-1]
    #files = glob.glob(destination_address)
    files = glob.glob(temp_folder_extension_path)
    #files = glob.glob(r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\temp\*")
    for file in files:
        os.remove(file)
    return

################################################################################

def setting_read(setting):
    #Reading the value of the setting

    #Opening File
    global skore_path

    file = open('settings_function_system.txt', 'r')
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
#################################AUTO FUNCTIONS#################################
################################################################################

def auto_amazing_midi(user_input_address_amaz, destination_address, tone_address):
    #This function does the .wav to .mid file conversions

    [end_address, filename] = output_address(user_input_address_amaz, destination_address, '.mid')
    clean_temp_folder()

    delay = 1
    ama_app = pywinauto.application.Application()
    ama_app_exe_path = setting_read('ama_app_exe_path')
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

###############################################################################

def auto_audacity(user_input_address_auda,destination_address):
    #This function does the automatio of the audacity application

    [end_address, filename] = output_address(user_input_address_auda, destination_address, '.wav')
    aud_app = pywinauto.application.Application()
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
    window.wait('enabled', timeout = 30)
    time.sleep(0.1)

    #Closing Audacity
    window.menu_item('&File->&Close').click()
    time.sleep(0.1)
    aud_app.SaveChanges.No.click()
    aud_app.kill()
    time.sleep(0.1)

################################################################################

def auto_midi_music_sheet(user_input_address_midi,destination_address):
    #This functions does the automation of the midi_music_sheet application.

    [end_address, filename] = output_address(user_input_address_midi, destination_address, '.pdf')
    midi_app = pywinauto.application.Application()
    midi_exe_path = setting_read('midi_exe_path')
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

################################################################################

def auto_audiveris(user_input_address_audi, destination_address):
    #This function automates the program, audiveris.

    [final_address,filename] = output_address(user_input_address_audi,destination_address, '.mxl')
    os.system("start cmd /c start_audiveris_function_system.py")

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
    time.sleep(5)
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
    return

################################################################################

def auto_xenoplay(user_input_address_xeno, destination_address):
    #This function does the automation of the xenoplay application

    [end_address, filename] = output_address(user_input_address_xeno, destination_address, '.mid')
    os.system("start cmd /c start_xenoplay_function_system.py")

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

################################################################################

def start_red_dot_forever():
    #This function simply starts the red dot forever application
    red_app = pywinauto.application.Application()
    red_app_exe_path = setting_read('red_app_exe_path')
    #red_app.start(r"C:\Program Files (x86)\Red Dot Forever\reddot.exe")
    red_app.start(red_app_exe_path)
    return

################################################################################

def start_piano_booster():
    #This function starts the piano booster application
    pia_app = pywinauto.application.Application()
    pia_app_exe_path = setting_read('pia_app_exe_path')
    #pia_app.start(r"C:\Program Files (x86)\Piano Booster\pianobooster.exe")
    pia_app.start(pia_app_exe_path)
    return

################################################################################
###############################MAIN CODE########################################
################################################################################
#clean_temp_folder()
#Testing AmazingMIDI
#amazing_midi_test_input = r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\function_system\conversion_test\WAV_files\SpiritedAway.wav"
#amazing_midi_test_tune = r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\function_system\misc\piano0.wav"
#auto_amazing_midi(amazing_midi_test_input, temp_folder_path,amazing_midi_test_input)

#Testing Audacity
#audacity_test_input = r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\function_system\conversion_test\Original_MP3\SpiritedAway.mp3"
#auto_audacity(audacity_test_input,temp_folder_path)

#Testing MidiMusicSheet
#midi_music_sheet_input = r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\function_system\conversion_test\Red_Dot_Forever\ChrisPlaying.mid"
#auto_midi_music_sheet(midi_music_sheet_input,temp_folder_path)

#Testing Red Dot Forever
#start_red_dot_forever()

#Testing Audiveris
#audi_test_input = r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\function_system\conversion_test\AnthemScore\SpiritedAway.pdf"
#auto_audiveris(audi_test_input,temp_folder_path)

#Testing Xenoplay
#xeno_test_input = r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\function_system\conversion_test\audiverius_samples\SpiritedAway.mxl"
#auto_xenoplay(xeno_test_input, temp_folder_path)

#Testing PianoBooster
#start_piano_booster()
