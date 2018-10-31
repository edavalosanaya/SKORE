import os
import sys
from skore_program_controller import setting_read

#This program opens initializes the program Xenoplay. This has to be a separate
#program to run the application in a different command line.

xeno_app_exe_path = setting_read('xeno_app_exe_path')
os.system(r"cd " + xeno_app_exe_path + " && xenoplay.jar")
