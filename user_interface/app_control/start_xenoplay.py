import os
#import pywinauto
import sys
from skore_program_controller import setting_read

#This program opens initializes the program Xenoplay. This has to be a separate
#program to run the application in a different command line.

xeno_app_exe_path = setting_read('xeno_app_exe_path','default')
#os.system(r"cd C:\Program Files (x86)\xenoplay-0-4-src && xenoplay.jar")
os.system(r"cd " + xeno_app_exe_path + " && xenoplay.jar")
