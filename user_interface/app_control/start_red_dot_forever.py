import pywinauto
from skore_function import setting_grab
red_app = pywinauto.application.Application()
red_app_exe_path = setting_grab('red_app_exe_path')
#red_app.start(r"C:\Program Files (x86)\Red Dot Forever\reddot.exe")
red_app.start(red_app_exe_path)
