import os
import sys

#Determing the address of the entire SKORE system
#complete_path = os.path.dirname(os.path.abspath(__file__))
#skore_index = complete_path.find('SKORE') + len('SKORE')
#skore_path = complete_path[0:skore_index+1]
#path_skore_function_extension = r"user_interface\app_control"

#importing skore functions
#sys.path.append(r'C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control')
#sys.path.append(skore_path + path_skore_function_extension)
#from skore_function import setting_read

os.system(r"cd C:\Users\daval\audiveris && gradle build && gradle run")
#audi_app_exe_path = setting_read('audi_app_exe_path','temp')
#os.system(r'cd ' + audi_app_exe_path + ' && gradle build && gradle run')
