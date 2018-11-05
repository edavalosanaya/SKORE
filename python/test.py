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

from skore_program_controller import output_address, setting_read, rect_to_int, click_center_try, clean_temp_folder

def auto_anthemscore(user_input_address_anth, destination_address, file_type, file_conversion_user_control):

    [end_address, filename] = output_address(user_input_address_anth, destination_address, file_type)

    if file_type == '.pdf':
        end_address_mid, trash = output_address(user_input_address_anth, destination_address, '.mid')
    else:
        end_address_mid = end_address

    if file_conversion_user_control == False and file_type != '.pdf':
        print("Easy")
        os.system(r'AnthemScore -a ' + user_input_address_anth + ' -m ' + end_address)
    else:
        print("Difficult")
        ant_app_exe_path = setting_read('ant_app_exe_path')
        ant_app = pywinauto.application.Application()
        ant_app.start(ant_app_exe_path)
        print("Initializing AnthemScore")

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
        click_center_try('file_button_anthem', ant_dimensions)
        click_center_try('open_button_anthem', ant_dimensions)

        # Creating a window variable for File Browser Dialog
        while(True):
            try:
                w_open_handle = pywinauto.findwindows.find_windows(title="Select File")[0]
                w_open_window = ant_app.window(handle=w_open_handle)
                break
            except IndexError:
                time.sleep(0.2)

        # Entering the user's input file
        w_open_window.type_keys(user_input_address_anth)
        w_open_window.type_keys("{ENTER}")

        # Wait until the file has been processed
        time.sleep(1)

        # Creating a window variable for Select File Dialog
        while(True):
            try:
                s_open_handle = pywinauto.findwindows.find_windows(title=u'Select File')[0]
                s_open_window = ant_app.window(handle=s_open_handle)
                break
            except IndexError:
                time.sleep(0.2)

        # Selecting Save As option
        original_rect_dimensions = s_open_window.rectangle()
        ant_open_dimensions = rect_to_int(original_rect_dimensions)
        click_center_try('save_as_button_anthem', ant_open_dimensions)

        # Creating a window variable for Save As Dialog
        while(True):
            try:
                s_handle = pywinauto.findwindows.find_windows(title=u'Save As')[0]
                s_window = ant_app.window(handle=s_handle)
                break
            except IndexError:
                time.sleep(0.2)

        s_window.type_keys(end_address)
        s_window.type_keys("{ENTER}")
        time.sleep(2.5)

        click_center_try('ok_button_anthem', ant_open_dimensions)

        # Creating a window variable for Viewer Dialog
        while(True):
            try:
                v_handle = pywinauto.findwindows.find_windows(title=u'Viewer')[0]
                v_window = ant_app.window(handle=v_handle)
                break
            except IndexError:
                time.sleep(1)

        print("File Processing Done")
        v_window.close()

        # Now actually saving the transformed files
        click_center_try('file_button_anthem', ant_dimensions)
        click_center_try('save_as_button2_anthem', ant_dimensions)

        # Creating a window variable for Save As Dialog
        while(True):
            try:
                s2_handle = pywinauto.findwindows.find_windows(title=u'Save As')[0]
                s2_window = ant_app.window(handle=s2_handle)
                break
            except IndexError:
                time.sleep(0.2)

        original_rect_dimensions = s2_window.rectangle()
        ant_save_dimensions = rect_to_int(original_rect_dimensions)

        # Selecting file type and saving the file
        click_center_try('format_button_anthem', ant_save_dimensions)
        if file_type == '.mid':
            click_center_try('format_pdf_button_anthem', ant_save_dimensions)
        elif file_type == '.pdf':
            click_center_try('format_mid_button_anthem', ant_save_dimensions)
        click_center_try('ok_button_anthem', ant_save_dimensions)

        time.sleep(2)
        ant_app.kill()

    return end_address, end_address_mid

file_name_test = r'C:\Users\daval\Documents\GitHub\SKORE\python\conversion_test\Original_MP3\OdeToJoy.mp3'
destination_folder_test = r"C:\Users\daval\Documents\GitHub\SKORE\python\temp"
file_type_test = '.mid'
file_conversion_user_control_test = False

clean_temp_folder()
auto_anthemscore(file_name_test, destination_folder_test, file_type_test, file_conversion_user_control_test)
