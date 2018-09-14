from shutil import copyfile
import os
import sys
#Determing the address of the entire SKORE system
complete_path = os.path.dirname(os.path.abspath(__file__))
skore_index = complete_path.find('SKORE') + len('SKORE')
skore_path = complete_path[0:skore_index+1]
path_temp_folder_extension = r"user_interface\app_control\temp"
path_skore_function_extension = r"user_interface\app_control"
path_setting_extension = r"user_interface\app_control"

sys.path.append(skore_path + path_skore_function_extension)
from skore_function import clean_temp_folder

clean_temp_folder()

def create_setting_temp():
    copyfile('settings.txt', skore_path + path_temp_folder_extension + '\\' + 'settings_temp.txt')

def setting_temp_write(setting, write_data):

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


setting_temp_write('destination_address', 'blah')
