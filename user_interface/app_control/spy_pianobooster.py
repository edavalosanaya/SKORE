import win32api
import psutil
import time
from threading import Thread, Event
import inspect
import pywinauto

from skore_program_controller import setting_read, click_center_try

from pywinauto.controls.win32_controls import ButtonWrapper
from time import sleep

app_running_stop_event = Event()
all_qwidgets = []
default_or_temp_mode = 'temp'

################################################################################
def track_mouse_clicks():
    #Code to check if left or right mouse buttons were pressed, only while the
    #PianoBooster application is running.

    state_left = win32api.GetKeyState(0x01)  #Left button down = 0 or 1. Button up = -127 or -128
    state_right = win32api.GetKeyState(0x02)  #Right button down = 0 or 1. Button up = -127 or -128

    while True:

        #Checking if the pianobooster application is running
        processes = [p.name() for p in psutil.process_iter()]

        for process in processes:
            if process == 'pianobooster.exe':
                #PianoBooster is running
                break

        if process != 'pianobooster.exe':
            #if the PianoBooster is not running, end mouse tracking
            app_running_stop_event.set()
            break

        #Checking if the mouse has been clicked and obtain its coordinates
        a = win32api.GetKeyState(0x01)
        #b = win32api.GetKeyState(0x02)

        if a != state_left:  # Button state changed
            state_left = a
            #print(a)

            if a < 0:
                c = 1
                #x, y = win32api.GetCursorPos()
                #print(str(x) + ',' + str(y))
                #print('Left Button Pressed')
            else:
                x, y = win32api.GetCursorPos()
                #print(str(x) + ',' + str(y))
                #print('Left Button Released')
                determine_button(x,y)
            """
            if a > 0:
                #print('Left Button Released')
                x, y = win32api.GetCursorPos()
                print(str(x) + ',' + str(y))
            """

        """
        if b != state_right:  # Button state changed
            state_right = b
            #print(b)
            if b < 0:
                print('Right Button Pressed')
            else:
                print('Right Button Released')
        """

def determine_button(x , y):
    #This function determines where the mouse click coordinates are within the
    #dimensions of a button or qwigets of the PianoBooster application
    int_dimensions = [0,0,0,0]

    for widget in all_qwidgets:

        #Obtaining the dimensions of the qwidgets
        try:
            dimensions = str(widget.rectangle())
        except pywinauto.findbestmatch.MatchError:
            return

        #Editing the values of the dimensions to integers
        dimensions = dimensions[1:-1]
        dimensions = dimensions.split(',')

        for dimension in dimensions:

            int_dimension = dimension.replace("L","")
            int_dimension = int_dimension.replace("T","")
            int_dimension = int_dimension.replace("R","")
            int_dimension = int_dimension.replace("B","")
            int_dimension = int(int_dimension)
            int_dimensions[dimensions.index(dimension)] = int_dimension

        #Checking if the mouse click is within the integer coordinates
        if x > int_dimensions[0] and x < int_dimensions[2] and y > int_dimensions[1] and y < int_dimensions[3]:
            #Found the qwidget
            print(all_qwidgets_names[all_qwidgets.index(widget)])

    return

################################################################################
def retrieve_name(var):
    #This function retrieves the name of a variable
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]

################################################################################

#Initilizing the PianoBooster Application
pia_app = pywinauto.application.Application()
pia_app_exe_path = setting_read('pia_app_exe_path', default_or_temp_mode)
pia_app.start(pia_app_exe_path)
print("Initialized PianoBooser")

#Getting a handle of the application, the application's title changes depending
#on the .mid file opened by the application.
possible_handles = pywinauto.findwindows.find_elements()

for i in range(len(possible_handles)):
    key = str(possible_handles[i])
    if(key.find('Piano Booster') != -1):
        wanted_key = key
        #print('Found it ' + key)

first_index = wanted_key.find("'")
last_index = wanted_key.find(',')
pia_app_title = wanted_key[first_index + 1 :last_index - 1]

#Once with the handle, control over the window is achieved.
w_handle = pywinauto.findwindows.find_windows(title=pia_app_title)[0]
window = pia_app.window(handle=w_handle) #pywinauto.application.WindowSpecification Object

#Initializion of the Qwidget within the application
window.maximize()
time.sleep(1)

click_center_try('skill_groupBox_pia')
click_center_try('hands_groupBox_pia')
click_center_try('book_song_buttons_pia')
click_center_try('flag_button_pia')

#Aquiring the qwigets from the application
main_qwidget = pia_app.QWidget
main_qwidget.wait('ready')

#Skill Group Box
listen_button = main_qwidget.Skill3
follow_you_button = main_qwidget.Skill2
play_along_button = main_qwidget.Skill

#Hands Group Box
right_hand = main_qwidget.Hands4
both_hands = main_qwidget.Hands3
left_hands = main_qwidget.Hands2

#Song and
song_combo_button = main_qwidget.songCombo
book_combo_button = main_qwidget.bookCombo

#GuiTopBar
key_combo_button = main_qwidget.keyCombo
play_button = main_qwidget.playButton
play_from_the_start_button = main_qwidget.playFromStartButton
save_bar_button = main_qwidget.savebarButton
speed_spin_button = main_qwidget.speedSpin
start_bar_spin_button = main_qwidget.startBarSpin
transpose_spin_button = main_qwidget.transposeSpin
looping_bars_popup_button = main_qwidget.loopingBarsPopupButton

all_qwidgets = [listen_button, follow_you_button, play_along_button, right_hand, both_hands, left_hands, key_combo_button, song_combo_button, book_combo_button, key_combo_button,
                play_button, play_from_the_start_button, save_bar_button, speed_spin_button, start_bar_spin_button, transpose_spin_button,looping_bars_popup_button]
#all_qwidgets_names = ['listen_button', 'follow_you_button','play_along_button','right_hand','both_hands','left_hands',]
all_qwidgets_names = ['','','','',''
                      '','','','','',
                      '','','','','',
                      '','','','','']

#Getting the name of the applications
for qwigets in all_qwidgets:
    all_qwidgets_names[all_qwidgets.index(qwigets)] = retrieve_name(qwigets)[0]

#Enabling the mouse tracking
print("Mouse Tracking Enabled")
click_action_thread = Thread(target=track_mouse_clicks)
click_action_thread.start()
click_action_thread.join()
