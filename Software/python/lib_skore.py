# General Utility Libraries
import sys
import time
import os
import statistics

# File, Folder, and Directory Manipulation Library
import ntpath
import pathlib
import glob
from pathlib import Path
from shutil import copyfile, move
import shutil
import yaml

# Image Procressing Library
import cv2
import numpy as np
import pyautogui

# Music Library
#import pydub

# GUI Automation Library
import pywinauto

#-------------------------------------------------------------------------------
# Class Definitions

class FileContainer:

    def __init__(self, file_path = None):

        self.file_path = {}
        self.original_file = ''

        if file_path is not None:
            file_name = os.path.basename(file_path)
            file_type = os.path.splitext(file_name)[1]
            self.file_path[file_type] = file_path

        # Determing the address of the entire SKORE system
        self.complete_path = os.path.dirname(os.path.abspath(__file__))
        if self.complete_path == '' or self.complete_path.find('SKORE') == -1:
                self.complete_path = os.path.dirname(sys.argv[0])

        skore_index = self.complete_path.find('SKORE') + len('SKORE')
        self.skore_path = self.complete_path[0: skore_index + 1]
        self.temp_folder_path = self.skore_path + r".\Software\python\temp"
        self.amazing_midi_tune_path = self.skore_path + r".\Software\python\misc\piano0.wav"

        return None

    def add_file_type(self, file_path):

        file_name = os.path.basename(file_path)
        file_type = os.path.splitext(file_name)[1]
        self.file_path[file_type] = file_path

        return None

    def remove_file_type(self, file_path):

        file_name = os.path.basename(file_path)
        file_type = os.path.splitext(file_name)[1]
        self.file_path.pop(file_type)

        return None

    def output_file_path_generator(self, input_address, file_extension):

        file = ntpath.basename(input_address)
        filename = file.split(".")[0]

        exist_path = pathlib.Path(input_address)
        file_path = exist_path.parent

        output_address = self.temp_folder_path + '\\' + filename + file_extension
        return output_address

    def clean_temp_folder(self):

        files = glob.glob(self.temp_folder_path + '\*')

        for file in files:
            os.remove(file)
            print("Removing file: {0}".format(file))
            try:
                self.remove_file_type(file)
            except KeyError:
                print("Excess File Removed that was not in the file container")

        return None

    def temp_to_folder(self, destination_folder, filename):
        # This functions transfer all the files found within temp folder into
        # "destination_folder" with the "filename" given.

        print("Transfering files with name: " + filename + "\t To directory: " + destination_folder)

        for file in self.file_path.values():
            if file.find(self.temp_folder_path) != -1:
                # File is in temp folder
                old_file = os.path.basename(file)
                file_type = os.path.splitext(old_file)[1]
                new_file_path = destination_folder + '\\' + filename + file_type

                shutil.move(file, new_file_path)
                self.file_path[file_type] = new_file_path

        return None

    def stringify_container(self):

        for key, value in self.file_path.items():
            print("{0} : {1}".format(key, value))

        return None

    #---------------------------------------------------------------------------
    # File Information and Control

    def has_midi_file(self):

        if '.mid' in self.file_path.keys():
            return True

        else:
            return False

    def has_pdf_file(self):

        if '.pdf' in self.file_path.keys():
            return True

        else:
            return False

    def has_mp3_file(self):

        if '.mp3' in self.file_path.keys():
            return True

        else:
            return False

    def is_empty(self):

        if len(self.file_path) == 0:
            return True

        else:
            return False

    def remove_all(self):

        self.file_path = {}
        self.original_file = ''

        return None

    #---------------------------------------------------------------------------
    # Single-Step File Conversion

    def mp3_to_wav(self):

        mp3_file = self.file_path['.mp3']
        wav_file = self.output_file_path_generator(mp3_file, '.wav')

        score = pydub.AudioSegment.from_mp3(mp3_file)
        score.export(wav_file, format = "wav")
        self.add_file_type(wav_file)

        output_file = Path(wav_file)

        while True :
            if output_file.is_file() is True:
                time.sleep(0.1)
                break
            else:
                print(".",end = "")
                time.sleep(0.5)

        return None

    def wav_to_mid(self):

        # AmazingMIDI
        cfg = read_config()

        # This function does the .wav to .mid file conversions
        wav_file = self.file_path['.wav']
        mid_file = self.output_file_path_generator(wav_file, '.mid')

        ama_app = pywinauto.application.Application()
        ama_app_exe_path = cfg['app_path']['amazing_midi']
        ama_app.start(ama_app_exe_path)
        print("Initialized AmazingMIDI")

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

        t_window.type_keys(self.amazing_midi_tune_path)
        t_window.type_keys('{ENTER}')

        # Clicking on file menu, selecting input file
        window.menu_item(u'&File->&Specify Input File...').click()

        # Entering the user input file's address
        #i_handle = pywinauto.findwindows.find_windows(title='Specify Input File')[0]
        i_handle = pywinauto.findwindows.find_windows(parent=w_handle)[0]
        i_window = ama_app.window(handle=i_handle)

        i_window.type_keys(wav_file)
        i_window.type_keys('{ENTER}')

        # Clicking on file menu, selecting output files
        window.menu_item(u'&File->&Specify Output File...').click()

        # Entering the output file's end_address
        #o_handle = pywinauto.findwindows.find_windows(title='Specify Output File')[0]
        o_handle = pywinauto.findwindows.find_windows(parent=w_handle)[0]
        o_window = ama_app.window(handle=o_handle)

        o_window.type_keys(mid_file)
        o_window.type_keys('{ENTER}')

        # Clicking on Transcribe menu, selecting Transcribe
        time.sleep(1)
        window.wait('enabled',timeout = 30)
        window.menu_item(u'&Transcribe->&Transcribe...').click()

        # Entering Transcribe Options
        to_handle = pywinauto.findwindows.find_windows(parent=w_handle)[0]
        to_window = ama_app.window(handle=to_handle)
        to_window.type_keys('{ENTER}')

        # Closing amazingmidi
        time.sleep(1)
        window.wait('enabled', timeout = 30)
        window.menu_item(u'&File->Exit').click()

        self.add_file_type(mid_file)
        print(".wav -> .mid complete")

        return None

    def pdf_to_mxl(self):

        cfg = read_config()

        pdf_file = self.file_path['.pdf']
        aud_app_exe_path = cfg['app_path']['audiveris']
        os.system('cd {0} && gradle run -PcmdLineArgs="-batch,-export,-output,{1},--,{2}"'.format(aud_app_exe_path, self.temp_folder_path,pdf_file))

        # Move the pdf file into temp and then remove the rest
        time.sleep(1)
        filename = os.path.splitext(os.path.basename(pdf_file))[0]
        embed_mxl_dir = self.temp_folder_path + '\\' + filename
        embed_mxl_file = embed_mxl_dir + '\\' + filename + '.mxl'
        mxl_file = self.temp_folder_path + '\\' + filename + '.mxl'

        output_file = Path(embed_mxl_file)

        while True:
            if output_file.is_file() is True:
                break
            else:
                print(".", end = "")
                time.sleep(0.5)

        shutil.move(embed_mxl_file, mxl_file)
        shutil.rmtree(embed_mxl_dir)
        self.add_file_type(mxl_file)

        return None

    def mxl_to_mid(self):

        cfg = read_config()

        mxl_file = self.file_path['.mxl']
        mid_file = self.output_file_path_generator(mxl_file, '.mid')

        mus_app_exe_path = cfg['app_path']['muse_score']
        mus_app_exe_directory = os.path.dirname(mus_app_exe_path)
        mus_app_exe_filename = os.path.basename(mus_app_exe_path)

        os.system('cd {0} && {1} "{2}" -o "{3}"'.format(mus_app_exe_directory, mus_app_exe_filename, mxl_file, mid_file))
        self.add_file_type(mid_file)
        output_file = Path(mid_file)

        while True:
            if output_file.is_file() is True:
                time.sleep(0.1)
                break
            else:
                time.sleep(0.5)

        print("Overall .mxl -> .mid complete")

        return None

    def mid_to_pdf(self):

        cfg = read_config()

        mid_file = self.file_path['.mid']
        pdf_file =self.output_file_path_generator(mid_file, '.pdf')

        mus_app_exe_path = cfg['app_path']['muse_score']
        mus_app_exe_directory = os.path.dirname(mus_app_exe_path)
        mus_app_exe_filename = os.path.basename(mus_app_exe_path)

        os.system('cd {0} && {1} "{2}" -o "{3}"'.format(mus_app_exe_directory, mus_app_exe_filename, mid_file, pdf_file))
        self.add_file_type(pdf_file)
        output_file = Path(pdf_file)

        while True:
            if output_file.is_file() is True:
                time.sleep(0.1)
                break
            else:
                time.sleep(0.5)

        print("Overall .mid -> .pdf complete")

        return None

    def mp3_to_mid_anthemscore(self):

        cfg = read_config()

        print("Using Anthemscore mp3 -> midi")

        mp3_file = self.file_path['.mp3']
        mid_file = self.output_file_path_generator(mp3_file, '.mid')

        ant_app_exe_path = cfg['app_path']['anthemscore']
        ant_app_exe_directory = os.path.dirname(ant_app_exe_path)
        ant_app_exe_filename = os.path.basename(ant_app_exe_path)

        os.system("start \"\" cmd /c \"cd {0} && {1} -a {2} -m {3} \"".format(ant_app_exe_directory, ant_app_exe_filename, mp3_file,mid_file))

        output_file = Path(mid_file)

        while True :
            if output_file.is_file() is True:
                time.sleep(0.1)
                break
            else:
                print(".",end = "")
                time.sleep(0.5)

        print("Midi File Generation Complete")
        self.add_file_type(mid_file)

        return None

    #---------------------------------------------------------------------------
    # Multi-step FIle Conversion

    def mp3_to_pdf(self):

        # This function converts a .mp3 to .pdf
        cfg = read_config()

        mp3_to_midi_converter_setting = cfg['app_path']['open_close_source']

        if mp3_to_midi_converter_setting == 'open_source':
            self.mp3_to_wav()
            self.wav_to_mid()
            self.mid_to_pdf()

        elif mp3_to_midi_converter_setting == 'close_source':
            self.mp3_to_mid_anthemscore()
            self.mid_to_pdf()

        print("Overall .mp3 -> .pdf complete")

        return None

    def mp3_to_mid(self):

        # This function converts a .mp3 to .mid
        cfg = read_config()

        mp3_to_midi_converter_setting = cfg['app_path']['open_close_source']

        #self.clean_temp_folder()
        if mp3_to_midi_converter_setting == 'open_source':
            self.mp3_to_wav()
            self.wav_to_mid()

        elif mp3_to_midi_converter_setting == 'close_source':
            self.mp3_to_mid_anthemscore()

        print("Overall .mp3 -> .mid complete")

        return None

    def pdf_to_mid(self):

        # This function converts a .pdf to .mid

        self.pdf_to_mxl()
        self.mxl_to_mid()

        print("Overall .pdf -> .mid complete")

        return None

    #-------------------------------------------------------------------------------
    # Input to Output File Conversion

    def input_to_pdf(self):

        # This function converts any file into a .pdf

        print("Before file conversion")
        self.stringify_container()

        if self.has_pdf_file() is True:
            print("Pre-existing pdf file found. File Conversion Cancelled")
            return None

        if self.has_midi_file() is True:
            self.mid_to_pdf()

        elif self.has_mp3_file() is True:
            self.mp3_to_pdf()

        print("After file conversion")
        self.stringify_container()

        return None

    def input_to_mid(self):
        # This function converts any file into a .mid.

        print("Before file conversion")
        self.stringify_container()

        if self.has_midi_file() is True:
            print("Pre-existing midi file found. File Conversion Cancelled")
            return None

        if self.has_pdf_file() is True:
            self.pdf_to_mid()

        elif self.has_mp3_file() is True:
            self.mp3_to_mid()

        print("After file conversion")
        self.stringify_container()

        return None

class GuiManipulator:

    def __init__(self):

        self.complete_path = os.path.dirname(os.path.abspath(__file__))
        if self.complete_path == '' or self.complete_path.find('SKORE') == -1:
                self.complete_path = os.path.dirname(sys.argv[0])

        skore_index = self.complete_path.find('SKORE') + len('SKORE')
        self.skore_path = self.complete_path[0: skore_index + 1]
        self.templates_path = self.skore_path + r"\Software\python\templates"

        return None

    def click_center(self, button, dimensions):
        # This function utilizes screen shoots and determines the location of certain
        # buttons within the screenshot. The screenshot will then be cropped to only
        # include the application that is being clicked

        image = pyautogui.screenshot(region=dimensions)
        x_coord_list = []
        y_coord_list = []

        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        cv2.imwrite('gui_screenshot.png', image)
        img = cv2.imread('gui_screenshot.png', 0)
        template = cv2.imread(self.templates_path + '\\' + button + '.png', 0)

        w, h = template.shape[::-1]

        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

        desirable_methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED','cv2.TM_CCORR_NORMED']

        for method in desirable_methods:
            method = eval(method)
            res = cv2.matchTemplate(img, template, method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)

            top_left = [top_left[0] + dimensions[0], top_left[1] + dimensions[1]]
            bottom_right = (top_left[0] + w, top_left[1] + h)

            file_button_center_coords = [ int((top_left[0]+bottom_right[0])/2) , int((top_left[1]+bottom_right[1])/2) ]

            x_coord_list.append(file_button_center_coords[0])
            y_coord_list.append(file_button_center_coords[1])

        try:
            x_coord_mode = statistics.mode(x_coord_list)
            y_coord_mode = statistics.mode(y_coord_list)
        except:
            x_coord_mode = x_coord_list[0]
            y_coord_mode = y_coord_list[0]

        pywinauto.mouse.click(button="left",coords=(x_coord_mode,y_coord_mode))
        os.remove('gui_screenshot.png')
        time.sleep(0.1)

        return None

    def click_center_try(self, button, dimensions):
        # This functions does the same as click_center, but allows the function to wait
        # Until the image is found.

        while(True):
            try:
                self.click_center(button, dimensions)
                break
            except AttributeError:
                #print('.', end='')
                time.sleep(0.5)

        return None

#-------------------------------------------------------------------------------
# Utility Functions

def rect_to_int(rect_object):
    # This function is catered to help click_center by converting the RECT object
    # to a list of integers that is compatible with the cropping feature of the
    # click_center_try function

    int_dimensions = [0,0,0,0]

    tolerance = 10

    int_dimensions[0] = rect_object.left
    int_dimensions[1] = rect_object.top
    int_dimensions[2] = rect_object.right - rect_object.left + tolerance
    int_dimensions[3] = rect_object.bottom - rect_object.top + tolerance

    return int_dimensions

def read_config():

    with open("config.yml", 'r') as ymlfile:
        return yaml.load(ymlfile)

def update_config(cfg):

    with open('config.yml', 'w') as outfile:
        yaml.dump(cfg, outfile, default_flow_style=False)

    return None

def is_mid(file_path):
    # Test if the input file is .mid

    file_name = os.path.basename(file_path)
    file_type = os.path.splitext(file_name)[1]

    if file_type.endswith('mid') is True:
        return True

    return False

def is_mp3(file_path):
    # Test if the input file is .mp3

    file_name = os.path.basename(file_path)
    file_type = os.path.splitext(file_name)[1]

    if file_name.endswith('mp3') is True:
        return True

    return False

def is_pdf(file_path):
    # Test if the input file is .pdf

    file_name = os.path.basename(file_path)
    file_type = os.path.splitext(file_name)[1]

    if file_type.endswith('pdf') is True:
        return True

    return False
