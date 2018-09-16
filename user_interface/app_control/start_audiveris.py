import os
import sys
from skore_program_controller import setting_read

#This program opens initializes the program Audiveris. This has to be a separate
#program to run the application in a different command line.

#os.system(r"cd C:\Users\daval\audiveris && gradle build && gradle run")
audi_app_exe_path = setting_read('audi_app_exe_path')
os.system(r'cd ' + audi_app_exe_path + ' && gradle build && gradle run')
