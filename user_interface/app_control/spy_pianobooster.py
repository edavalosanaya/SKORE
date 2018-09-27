

#print(main_qwidget.__dict__)
#print(main_qwidget.__dict__)
#print(dir(main_qwidget))

from skore_program_controller import *

from pywinauto.controls.win32_controls import ButtonWrapper
from time import sleep

pia_app = pywinauto.application.Application()
pia_app_exe_path = setting_read('pia_app_exe_path', default_or_temp_mode)
#pia_app.start(r"C:\Program Files (x86)\Piano Booster\pianobooster.exe")
pia_app.start(pia_app_exe_path)
print("Initialized PianoBooser")

#w_handle = pywinauto.findwindows.find_windows(title='Piano Booster - ')[0]
possible_handles = pywinauto.findwindows.find_elements()
#print(possible_handles)
#print()

for i in range(len(possible_handles)):
    key = str(possible_handles[i])
    if(key.find('Piano Booster') != -1):
        wanted_key = key
        #print('Found it ' + key)

first_index = wanted_key.find("'")
last_index = wanted_key.find(',')
pia_app_title = wanted_key[first_index + 1 :last_index - 1]
#print(pia_app_title)

w_handle = pywinauto.findwindows.find_windows(title=pia_app_title)[0]
window = pia_app.window(handle=w_handle) #pywinauto.application.WindowSpecification Object


#Initialization
window.maximize()
time.sleep(1)
#delay_time = 0
click_center_try('skill_groupBox_pia')
#time.sleep(delay_time)
click_center_try('hands_groupBox_pia')
#time.sleep(delay_time)
click_center_try('book_song_buttons_pia')
#time.sleep(delay_time)
click_center_try('flag_button_pia')
#time.sleep(delay_time)

main_qwidget = pia_app.QWidget
main_qwidget.wait('ready')

print(main_qwidget.children())
group_box = main_qwidget.groupBox
print(group_box.children())

button = group_box.Hands1

a = ButtonWrapper(button.wrapper_object())
print(a.get_check_state())

button2 = group_box.Hands2

a2 = ButtonWrapper(button2.wrapper_object())
print(a2.get_check_state())

button3 = group_box.Hands3

a3 = ButtonWrapper(button3.wrapper_object())
print(a3.get_check_state())

"""
listen_button = main_qwidget.Skill3
follow_you_button = main_qwidget.Skill2
play_along_button = main_qwidget.Skill

right_hand = main_qwidget.Hands4
both_hands = main_qwidget.Hands3
left_hands = main_qwidget.Hands2
"""


"""
listen_checkbox = ButtonWrapper(listen_button.wrapper_object())

follow_you_checkbox = ButtonWrapper(follow_you_button.wrapper_object())
print(follow_you_checkbox.get_check_state())

play_along_checkbox = ButtonWrapper(play_along_button.wrapper_object())
print(play_along_checkbox.get_check_state())
"""

"""
print(listen_button.get_properties())
print(follow_you_button.get_properties())
print(play_along_button.get_properties())
print()
print()

all_qwidgets = [listen_button, follow_you_button, play_along_button, right_hand, both_hands, left_hands]
for i in range(len(all_qwidgets)):
    all_qwidgets[i].click()
    #all_qwidgets[i].get_check_state()
    time.sleep(1)

print(listen_button.get_properties())
print(follow_you_button.get_properties())
print(play_along_button.get_properties())
"""

#print(listen_button.user_data())
#print(follow_you_button.user_data())
