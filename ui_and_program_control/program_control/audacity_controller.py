
#from pywinauto.application import Application
import pywinauto
import time

user_input_address = r"C:\Users\daval\Documents\GitHub\SKORE\conversion_test\Original_MP3\SpiritedAway.mp3"

#Starting Audacity
aud_app = pywinauto.application.Application()
aud_app.start(r"c:\Program Files (x86)\Audacity\audacity.exe")

#Creating a window variable for Audacity
w_handle = pywinauto.findwindows.find_windows(title='Audacity')[0]
window = aud_app.window(handle=w_handle)

#Clicking on file menu
window.menu_item(u'&File->&Open').click()

#Creating a window variable for File Browser
w_open_handle = pywinauto.findwindows.find_windows(title='Select one or more audio files...')[0]
w_open = aud_app.window(handle=w_open_handle)

#Entering the user's input file
w_open.type_keys(user_input_address)
w_open.type_keys("{ENTER}")


#Click on file menu
#Possible not being enabled has something to do with timing issue
time.sleep(10)
window.menu_item('&File->Export Audio ...').click()
w_export_handle = pywinauto.findwindows.find_windows(title='Export Audio')[0]
w_export = aud_app.window(handle=w_export_handle)

w_export.type_keys("{ENTER}")
time.sleep(2)
w_export.type_keys("{ENTER}")

#aud_app.kill()

#print(w_export)
