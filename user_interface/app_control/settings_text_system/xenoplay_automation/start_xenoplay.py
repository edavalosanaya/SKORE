import os
import pywinauto
import sys

#Determing the address of the entire SKORE system
complete_path = os.path.dirname(os.path.abspath(__file__))
skore_index = complete_path.find('SKORE') + len('SKORE')
skore_path = complete_path[0:skore_index+1]
path_skore_function_extension = r"user_interface\app_control"

sys.path.append(skore_path + path_skore_function_extension)

from skore_function import setting_read
xeno_app = pywinauto.application.Application()
xeno_app_exe_path = setting_read('xeno_app_exe_path','temp')

#os.system(r"cd C:\Program Files (x86)\xenoplay-0-4-src && xenoplay.jar")
os.system(r"cd " + xeno_app_exe_path + " && xenoplay.jar")
