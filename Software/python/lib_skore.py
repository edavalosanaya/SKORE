# General Utility Libraries
import sys
import time
import os
#import statistics

# File, Folder, and Directory Manipulation Library
import ntpath
import pathlib
import glob
#from pathlib import Path
#from shutil import move
import shutil
import yaml

# Image Procressing Library
#import cv2
import numpy as np
#import pyautogui

# Music Library
import hook_pydub # SKORE MODULE
import pydub

# GUI Automation Library
import pywinauto

# SKORE imports
import globals

#-------------------------------------------------------------------------------
# Class Definitions

class FileContainer:

    """
    The FileContainer class is responsible of keeping track of the uploaded files
    and performing the file conversion in the back-end side of the SKORE
    application.
    """

    def __init__(self, file_path = None):

        """
        This function initializes the class, setting up list variables, and
        determing the location of the SKORE application.
        """

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

        self.amazing_midi_tune_path = self.complete_path + r"\misc\piano0.wav"

        return None

    def add_file_type(self, file_path):

        """ This function addes a file type to the file container. """

        file_name = os.path.basename(file_path)
        file_type = os.path.splitext(file_name)[1]
        self.file_path[file_type] = file_path

        return None

    def remove_file_type(self, file_path):

        """ This function removes a file type from the file container. """

        file_name = os.path.basename(file_path)
        file_type = os.path.splitext(file_name)[1]
        self.file_path.pop(file_type)

        return None

    def output_file_path_generator(self, input_address, file_extension):

        """
        This function creates a output file path depending on the file
        extension and input address of the input file.
        """

        file = ntpath.basename(input_address)
        filename = file.split(".")[0]

        #output_address = globals.OUTPUT_FILE_DIR + '\\' + filename + file_extension
        output_address = globals.OUTPUT_FILE_DIR + '\\' + globals.OUTPUT_FILENAME + file_extension
        return output_address

    def stringify_container(self):

        """
        This function stringifies the file container, mostly for troubleshooting
        purposes.
        """
        if len(self.file_path) == 0:
            print("Container is empty")

        for key, value in self.file_path.items():
            print("{0} : {1}".format(key, value))

        return None

    #---------------------------------------------------------------------------
    # File Information and Control

    def has_midi_file(self):

        """ Returns true if the file container has a midi file. """

        if '.mid' in self.file_path.keys():
            return True

        else:
            return False

    def has_pdf_file(self):

        """ Returns true if the file container has a pdf file. """

        if '.pdf' in self.file_path.keys():
            return True

        else:
            return False

    def has_mp3_file(self):

        """ Returns true if the file container has a mp3 file. """

        if '.mp3' in self.file_path.keys():
            return True

        else:
            return False

    def is_empty(self):

        #self.stringify_container()

        """ Returns true if the file container is empty. """

        #print("Checking if the file container is empty")
        #print("self.file_path: ", self.file_path)

        if len(self.file_path) == 0:
            return True

        else:
            return False

    def remove_all(self):

        """ Removes all of the track files by the file container. """

        self.file_path = {}
        self.original_file = ''

        return None

    #---------------------------------------------------------------------------
    # Single-Step File Conversion

    def waiting_for_file(self, output_file):

        while True:
            if output_file.is_file() is True:
                break
            else:
                print(".", end = "")
                time.sleep(0.5)

        return None

    def mp3_to_wav(self):

        """
        Function converts an input .mp3 file to a output .wav file. This is done
        with a python library called pydub.
        """

        mp3_file = self.file_path['.mp3']
        wav_file = self.output_file_path_generator(mp3_file, '.wav')

        score = pydub.AudioSegment.from_mp3(mp3_file)
        score.export(wav_file, format = "wav")
        self.add_file_type(wav_file)

        output_file = pathlib.Path(wav_file)
        self.waiting_for_file(output_file)

        return None

    def wav_to_mid(self):

        """
        Function converts an input .wav file to a output .mid file. This file
        conversion is open-source, done through the GUI of the AmazingMIDI
        application.
        """

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

        """
        Function converts an input .pdf file to a output .mxl file. This file
        conversion is performed through the CLI of the open-source Audiveris
        software.
        """

        # Add gradle to PATH if necessary
        cfg = read_config()

        pdf_file = self.file_path['.pdf']
        pdf_filename = os.path.basename(pdf_file)
        pdf_filename = pdf_filename.split('.')[0]

        aud_app_exe_path = cfg['app_path']['audiveris']
        aud_app_exe_directory = os.path.dirname(aud_app_exe_path)

        embed_mxl_dir = globals.OUTPUT_FILE_DIR + '\\' + globals.OUTPUT_FILENAME

        #print('cd {0} && gradle run -PcmdLineArgs="-batch,-export,-output,{1},--,{2}"'.format(aud_app_exe_path, embed_mxl_dir, pdf_file))
        #os.system('cd {0} && gradle run -PcmdLineArgs="-batch,-export,-output,{1},--,{2}"'.format(aud_app_exe_path, embed_mxl_dir, pdf_file))
        print('cd {0} && audiveris -batch -export "{1}" -output "{2}"'.format(aud_app_exe_directory, pdf_file, embed_mxl_dir))
        os.system('cd {0} && audiveris -batch -export "{1}" -output "{2}"'.format(aud_app_exe_directory, pdf_file, embed_mxl_dir))

        # Move the pdf file into temp and then remove the rest
        time.sleep(1)
        embed_mxl_file = embed_mxl_dir + '\\' + pdf_filename + '\\' + pdf_filename + '.mxl'
        mxl_file = globals.OUTPUT_FILE_DIR + '\\' + globals.OUTPUT_FILENAME + '.mxl'

        output_file = pathlib.Path(embed_mxl_file)
        self.waiting_for_file(output_file)

        shutil.move(embed_mxl_file, mxl_file)
        shutil.rmtree(embed_mxl_dir)
        self.add_file_type(mxl_file)

        output_file = pathlib.Path(mxl_file)
        self.waiting_for_file(output_file)

        return None

    def mxl_to_mid(self):

        """
        Function converts an input .mxl file to a output .mid file. This is done
        with the CLI of the open-source MuseScore application.
        """

        cfg = read_config()

        mxl_file = self.file_path['.mxl']
        mid_file = self.output_file_path_generator(mxl_file, '.mid')

        mus_app_exe_path = cfg['app_path']['muse_score']
        mus_app_exe_directory = os.path.dirname(mus_app_exe_path)
        mus_app_exe_filename = os.path.basename(mus_app_exe_path)

        print("1")
        print('cd {0} && {1} "{2}" -o "{3}"'.format(mus_app_exe_directory, mus_app_exe_filename, mxl_file, mid_file))
        os.system('cd {0} && {1} "{2}" -o "{3}"'.format(mus_app_exe_directory, mus_app_exe_filename, mxl_file, mid_file))
        print("2")
        self.add_file_type(mid_file)
        output_file = pathlib.Path(mid_file)
        print("3")

        self.waiting_for_file(output_file)

        print("4")
        print("Overall .mxl -> .mid complete")

        return None

    def mid_to_pdf(self):

        """
        Function converts an input .mid file to a output .pdf file. This is done
        with the CLI of the open-source MuseScore application.
        """

        cfg = read_config()

        mid_file = self.file_path['.mid']
        pdf_file = self.output_file_path_generator(mid_file, '.pdf')

        mus_app_exe_path = cfg['app_path']['muse_score']
        mus_app_exe_directory = os.path.dirname(mus_app_exe_path)
        mus_app_exe_filename = os.path.basename(mus_app_exe_path)

        print("1")
        print('cd {0} && {1} "{2}" -o "{3}"'.format(mus_app_exe_directory, mus_app_exe_filename, mid_file, pdf_file))
        os.system('cd {0} && {1} "{2}" -o "{3}"'.format(mus_app_exe_directory, mus_app_exe_filename, mid_file, pdf_file))
        print("2")
        self.add_file_type(pdf_file)
        output_file = pathlib.Path(pdf_file)
        print("3")

        self.waiting_for_file(output_file)

        print("4")
        print("Overall .mid -> .pdf complete")

        return None

    def mp3_to_mid_anthemscore(self):

        """
        Function converts an input .mp3 file to a output .mid file. This is done
        with the CLI of the close-source AnthemScore application.
        """

        cfg = read_config()

        print("Using Anthemscore mp3 -> midi")

        mp3_file = self.file_path['.mp3']
        mid_file = self.output_file_path_generator(mp3_file, '.mid')

        ant_app_exe_path = cfg['app_path']['anthemscore']
        ant_app_exe_directory = os.path.dirname(ant_app_exe_path)
        ant_app_exe_filename = os.path.basename(ant_app_exe_path)

        os.system("start \"\" cmd /c \"cd {0} && {1} -a {2} -m {3} \"".format(ant_app_exe_directory, ant_app_exe_filename, mp3_file, mid_file))

        output_file = pathlib.Path(mid_file)
        self.waiting_for_file(output_file)

        print("Midi File Generation Complete")
        self.add_file_type(mid_file)

        return None

    #---------------------------------------------------------------------------
    # Multi-step FIle Conversion

    def mp3_to_pdf(self):

        """
        This function converts an .mp3 to .pdf .
        """

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

        """
        This function converts a .mp3 to .mid .
        """

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

        """
        This function converts a .pdf to .mid .
        """

        self.pdf_to_mxl()
        self.mxl_to_mid()

        print("Overall .pdf -> .mid complete")

        return None

    #-------------------------------------------------------------------------------
    # Input to Output File Conversion

    def input_to_pdf(self):

        """
        This function converts any file into a .pdf .
        """

        #print("Before file conversion")
        #self.stringify_container()

        if self.has_pdf_file() is True:
            print("Pre-existing pdf file found. File Conversion Cancelled")
            return None

        if self.has_midi_file() is True:
            self.mid_to_pdf()

        elif self.has_mp3_file() is True:
            self.mp3_to_pdf()

        #print("After file conversion")
        #self.stringify_container()

        return None

    def input_to_mid(self):

        """
        This function converts any file into a .mid .
        """

        #print("Before file conversion")
        #self.stringify_container()

        if self.has_midi_file() is True:
            print("Pre-existing midi file found. File Conversion Cancelled")
            return None

        if self.has_pdf_file() is True:
            self.pdf_to_mid()

        elif self.has_mp3_file() is True:
            self.mp3_to_mid()

        #print("After file conversion")
        #self.stringify_container()

        return None

#-------------------------------------------------------------------------------
# Utility Functions

def read_config():

    """ Reads the config file and returns its contents. """

    with open("config.yml", 'r') as ymlfile:
        return yaml.load(ymlfile)

def update_config(cfg):

    """ Updates the config file with the given settings. """

    with open('config.yml', 'w') as outfile:
        yaml.dump(cfg, outfile, default_flow_style=False)

    return None

def is_mid(file_path):

    """ Test if the input file is .mid """

    file_name = os.path.basename(file_path)
    file_type = os.path.splitext(file_name)[1]

    if file_type.endswith('mid') is True:
        return True

    return False

def is_mp3(file_path):

    """ Test if the input file is .mp3 """

    file_name = os.path.basename(file_path)
    file_type = os.path.splitext(file_name)[1]

    if file_name.endswith('mp3') is True:
        return True

    return False

def is_pdf(file_path):

    """ Test if the input file is .pdf """

    file_name = os.path.basename(file_path)
    file_type = os.path.splitext(file_name)[1]

    if file_type.endswith('pdf') is True:
        return True

    return False
