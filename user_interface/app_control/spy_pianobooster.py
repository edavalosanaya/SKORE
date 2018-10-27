import win32api
import psutil
import time
from threading import Thread, Event
import inspect
import pywinauto
import sys
from pywinauto.controls.win32_controls import ButtonWrapper
from time import sleep

from skore_program_controller import setting_read, click_center_try, setting_write

from PyQt5 import QtCore, QtGui, QtWidgets
import os
import warnings
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QAction, QMainWindow, QInputDialog, QLineEdit, QFileDialog, QMessageBox, QLabel, QButtonGroup, QDialogButtonBox, QColorDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread

app_running_stop_event = Event()
all_qwidgets = []
button_history = []
processed_button_history = []
processed_index = 0
message_box_active = 0
all_qwidgets = []
all_qwidgets_names = []

################################################################################
def track_mouse_clicks():
    # Code to check if left or right mouse buttons were pressed, only while the
    # PianoBooster application is running.

    state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
    state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128

    while True:

        # Checking if the pianobooster application is running
        processes = [p.name() for p in psutil.process_iter()]

        for process in processes:
            if process == 'pianobooster.exe':
                # PianoBooster is running
                break

        if process != 'pianobooster.exe':
            # if the PianoBooster is not running, end mouse tracking
            app_running_stop_event.set()
            break

        # Checking if the mouse has been clicked and obtain its coordinates
        a = win32api.GetKeyState(0x01)
        #b = win32api.GetKeyState(0x02)

        if a != state_left:  # Button state changed
            state_left = a
            #print(a)

            if a < 0:
                c = 1
            else:
                x, y = win32api.GetCursorPos()
                determine_button(x,y)

def determine_button(x , y):
    # This function determines where the mouse click coordinates are within the
    # dimensions of a button or qwigets of the PianoBooster application
    int_dimensions = [0,0,0,0]

    #print("Click Detected")

    for widget in all_qwidgets:

        # Obtaining the dimensions of the qwidgets
        try:
            dimensions = str(widget.rectangle())
        except pywinauto.findbestmatch.MatchError:
            return

        # Editing the values of the dimensions to integers
        dimensions = dimensions[1:-1]
        dimensions = dimensions.split(',')

        for dimension in dimensions:

            int_dimension = dimension.replace("L","")
            int_dimension = int_dimension.replace("T","")
            int_dimension = int_dimension.replace("R","")
            int_dimension = int_dimension.replace("B","")
            int_dimension = int(int_dimension)
            int_dimensions[dimensions.index(dimension)] = int_dimension

        # Checking if the mouse click is within the integer coordinates
        if x > int_dimensions[0] and x < int_dimensions[2] and y > int_dimensions[1] and y < int_dimensions[3]:
            # Found the qwidget
            #print("QWidget Pressed Detected: " + str(all_qwidgets_names[all_qwidgets.index(widget)]))
            button = all_qwidgets_names[all_qwidgets.index(widget)]
            button_history.append(button)

    return

################################################################################
class ButtonThread(QThread):
    signal = QtCore.pyqtSignal('QString')

    def __init__(self):
        QThread.__init__(self)

    def run(self):

        global button_history
        global processed_button_history
        global processed_index
        global message_box_active

        print("User Usage Tracking Enabled")

        while(True):
            time.sleep(0.1)


            if len(button_history) != len(processed_button_history):

                #print("BEFORE: Button History: " + str(button_history) + "\t Processed Button History: " + str(processed_button_history))
                processed_button_history.append(button_history[processed_index])
                #print("AFTER: Button History: " + str(button_history) + "\t Processed Button History: " + str(processed_button_history))
                #print("Current Processed Action: " + str(processed_button_history[processed_index]))

                for index, item in enumerate(all_qwidgets_names):
                    if item == processed_button_history[processed_index]:
                        if index <= 2: # Skill Selection
                            print("Tutoring Mode Change")
                            setting_write('skill',str(item),'append')

                        elif index > 2 and index <= 5: # Hand Selection
                            print("Hand Mode Change")
                            setting_write('hand',str(item),'append')

                        elif index > 5 and index <= 7: # Song and Book Combo
                            print("Song and Combo Boxes were pressed. Please do not change the song")

                        elif index == 8: # Play Button
                            playing_state = setting_read('playing_state')
                            playing_state = eval(playing_state)
                            playing_state = not playing_state
                            setting_write('playing_state',str(playing_state),'append')

                        elif index == 9: # Restart Button
                            print("Restart Detected")
                            setting_write('restart','1','append')
                            setting_write('playing_state','1','append')

                        elif index > 9 and index <= 11: # Spin Boxes
                            print("Spin Buttons Pressed")
                            if message_box_active == 0:
                                self.signal.emit(item)
                            else:
                                print("message box in use")
                        else:
                            print("Current Button: " + item + " is not functional yet")

                        #print("Current Processed Action Complete")
                        processed_index += 1
                        break
                    else:
                        continue


class Companion_Dialog(QtWidgets.QDialog):

    spinButtonClicked = QtCore.pyqtSignal('QString')

    def __init__(self):
        super(QtWidgets.QDialog, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setObjectName("Dialog")
        self.resize(420, 250)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("SKORE Companion")

        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(10,10,400,230))
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setObjectName("tabWidget")

        self.tutor_mode_tab = QtWidgets.QWidget()
        self.tutor_mode_tab.setObjectName("tutor_mode_tab")
        self.tabWidget.addTab(self.tutor_mode_tab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tutor_mode_tab), "Tutor Mode")

        # Tutor Mode Tab
        self.tutor_label = QtWidgets.QLabel(self.tutor_mode_tab)
        self.tutor_label.setGeometry(QtCore.QRect(10,5,381,20))
        self.tutor_label.setObjectName("tutor_label")
        self.tutor_label.setText("Select or change Tutoring Mode")

        self.beginner_companion_pushButton = QtWidgets.QPushButton(self.tutor_mode_tab)
        self.beginner_companion_pushButton.setGeometry(QtCore.QRect(10,30,381,51))
        self.beginner_companion_pushButton.setObjectName("beginner_companion_pushButton")
        self.beginner_companion_pushButton.setText("Beginner Mode")

        self.intermediate_companion_pushButton = QtWidgets.QPushButton(self.tutor_mode_tab)
        self.intermediate_companion_pushButton.setGeometry(QtCore.QRect(10,85,381,51))
        self.intermediate_companion_pushButton.setObjectName("intermediate_companion_pushButton")
        self.intermediate_companion_pushButton.setText("Intermediate Mode")

        self.expert_companion_pushButton = QtWidgets.QPushButton(self.tutor_mode_tab)
        self.expert_companion_pushButton.setGeometry(QtCore.QRect(10,140,381,51))
        self.expert_companion_pushButton.setObjectName("expert_companion_pushButton")
        self.expert_companion_pushButton.setText("Expert Mode")

        # Timing Mode Tab
        self.timing_tab = QtWidgets.QWidget()
        self.timing_tab.setObjectName("timing_mode_tab")
        self.tabWidget.addTab(self.timing_tab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.timing_tab), "Timing Settings")

        time_per_tick_y_value = 10
        increment_counter_y_value = time_per_tick_y_value + 40
        chord_timing_tolerance_y_value = increment_counter_y_value + 40
        manual_final_chord_sustain_y_value = chord_timing_tolerance_y_value + 40
        lineEdit_length = 120

        self.time_per_tick_label = QtWidgets.QLabel(self.timing_tab)
        self.time_per_tick_label.setGeometry(QtCore.QRect(20, time_per_tick_y_value, 91, 16))
        self.time_per_tick_label.setObjectName("time_per_tick_label")
        self.time_per_tick_label.setText("Time per Tick:")
        self.time_per_tick_lineEdit = QtWidgets.QLineEdit(self.timing_tab)
        self.time_per_tick_lineEdit.setGeometry(QtCore.QRect(250, time_per_tick_y_value, lineEdit_length, 22))
        self.time_per_tick_lineEdit.setObjectName("time_per_tick_lineEdit")

        self.increment_counter_label = QtWidgets.QLabel(self.timing_tab)
        self.increment_counter_label.setGeometry(QtCore.QRect(20, increment_counter_y_value, 151 , 16))
        self.increment_counter_label.setObjectName("increment_counter_label")
        self.increment_counter_label.setText("Increment Counter Value:")

        self.increment_counter_lineEdit = QtWidgets.QLineEdit(self.timing_tab)
        self.increment_counter_lineEdit.setGeometry(QtCore.QRect(250, increment_counter_y_value, lineEdit_length, 22))
        self.increment_counter_lineEdit.setObjectName("increment_counter_lineEdit")

        self.chord_timing_tolerance_label = QtWidgets.QLabel(self.timing_tab)
        self.chord_timing_tolerance_label.setGeometry(QtCore.QRect(20, chord_timing_tolerance_y_value, 151, 16))
        self.chord_timing_tolerance_label.setObjectName("chord_timing_tolerance_label")
        self.chord_timing_tolerance_label.setText("Chord Timing Tolerance:")
        self.chord_timing_tolerance_lineEdit = QtWidgets.QLineEdit(self.timing_tab)
        self.chord_timing_tolerance_lineEdit.setGeometry(QtCore.QRect(250, chord_timing_tolerance_y_value, lineEdit_length, 22))
        self.chord_timing_tolerance_lineEdit.setObjectName("chord_timing_tolerance_lineEdit")

        self.manual_final_chord_sustain_timing_label = QtWidgets.QLabel(self.timing_tab)
        self.manual_final_chord_sustain_timing_label.setGeometry(QtCore.QRect(20, manual_final_chord_sustain_y_value, 211, 16))
        self.manual_final_chord_sustain_timing_label.setObjectName("manual_final_chord_sustain_timing_label")
        self.manual_final_chord_sustain_timing_label.setText("Manual Final Chord Sustain Timing Value:")
        self.manual_final_chord_sustain_timing_lineEdit = QtWidgets.QLineEdit(self.timing_tab)
        self.manual_final_chord_sustain_timing_lineEdit.setGeometry(QtCore.QRect(250, manual_final_chord_sustain_y_value, lineEdit_length, 22))
        self.manual_final_chord_sustain_timing_lineEdit.setObjectName("manual_final_chord_sustain_timing_lineEdit")

        self.apply_pushButton = QtWidgets.QPushButton(self.timing_tab)
        self.apply_pushButton.setGeometry(QtCore.QRect(250, 170, lineEdit_length, 25))
        self.apply_pushButton.setObjectName("apply_pushButton")
        self.apply_pushButton.setText("Apply")

        # Initializing MutliThraeding
        self.user_tracking_thread = ButtonThread()
        self.user_tracking_thread.signal.connect(self.create_message_box)
        self.user_tracking_thread.start()

        self.show()

    @pyqtSlot('QString')
    def create_message_box(self, item):

        global speed
        global tranpose
        global message_box_active

        #QMessageBox.information(self, item + " Pressed", "Please enter the value for the " + item)
        message_box_active = 1
        num, ok = QInputDialog.getInt(self, item + "Pressed", "Enter the value for " + item)

        if ok:

            if item == 'speed_spin_button':
                #speed = num
                setting_write('speed',str(num),'append')
            elif item == 'transpose_spin_button':
                #tranpose = num
                setting_write('tranpose',str(num),'append')

        print("End of Message Box Usage")
        message_box_active = 0

        return

################################################################################

def retrieve_name(var):
    #This function retrieves the name of a variable
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]

def piano_booster_setup():

    global all_qwidgets
    global all_qwidgets_names

    # Initilizing the PianoBooster Application
    pia_app = pywinauto.application.Application()
    #pia_app_exe_path = setting_read('pia_app_exe_path', default_or_temp_mode)
    pia_app_exe_path = setting_read('pia_app_exe_path')
    pia_app.start(pia_app_exe_path)
    print("Initialized PianoBooser")

    # Getting a handle of the application, the application's title changes depending
    # on the .mid file opened by the application.
    possible_handles = pywinauto.findwindows.find_elements()

    for i in range(len(possible_handles)):
        key = str(possible_handles[i])
        if(key.find('Piano Booster') != -1):
            wanted_key = key
            #print('Found it ' + key)

    first_index = wanted_key.find("'")
    last_index = wanted_key.find(',')
    pia_app_title = wanted_key[first_index + 1 :last_index - 1]

    # Once with the handle, control over the window is achieved.
    w_handle = pywinauto.findwindows.find_windows(title=pia_app_title)[0]
    window = pia_app.window(handle=w_handle) #pywinauto.application.WindowSpecification Object

    # Initializion of the Qwidget within the application
    window.maximize()
    time.sleep(1)

    click_center_try('skill_groupBox_pia')
    click_center_try('hands_groupBox_pia')
    click_center_try('book_song_buttons_pia')
    click_center_try('flag_button_pia')

    # Aquiring the qwigets from the application
    main_qwidget = pia_app.QWidget
    main_qwidget.wait('ready')

    # Skill Group Box
    listen_button = main_qwidget.Skill3
    follow_you_button = main_qwidget.Skill2
    play_along_button = main_qwidget.Skill

    # Hands Group Box
    right_hand = main_qwidget.Hands4
    both_hands = main_qwidget.Hands3
    left_hands = main_qwidget.Hands2

    # Song and
    song_combo_button = main_qwidget.songCombo
    book_combo_button = main_qwidget.bookCombo

    # GuiTopBar
    key_combo_button = main_qwidget.keyCombo
    play_button = main_qwidget.playButton
    play_from_the_start_button = main_qwidget.playFromStartButton
    save_bar_button = main_qwidget.savebarButton
    speed_spin_button = main_qwidget.speedSpin
    start_bar_spin_button = main_qwidget.startBarSpin
    transpose_spin_button = main_qwidget.transposeSpin
    looping_bars_popup_button = main_qwidget.loopingBarsPopupButton

    all_qwidgets = [listen_button, follow_you_button, play_along_button, right_hand,
                    both_hands, left_hands, song_combo_button, book_combo_button,
                    play_button, play_from_the_start_button, speed_spin_button,
                    transpose_spin_button, start_bar_spin_button,
                    looping_bars_popup_button, save_bar_button, key_combo_button]

    all_qwidgets_names = ['listen_button', 'follow_you_button', 'play_along_button', 'right_hand',
                          'both_hands', 'left_hands', 'song_combo_button', 'book_combo_button',
                          'play_button', 'play_from_the_start_button', 'speed_spin_button',
                          'transpose_spin_button', 'start_bar_spin_button',
                          'looping_bars_popup_button', 'save_bar_button', 'key_combo_button']

    """
    all_qwidgets_names = ['','','','',''
                          '','','','','',
                          '','','','','',
                          '','','','','']

    # Getting the name of the applications
    for qwigets in all_qwidgets:
        a = retrieve_name(qwigets)[0]
        print(a)
        all_qwidgets_names[all_qwidgets.index(qwigets)] = retrieve_name(qwigets)[0]

    """

    # Enabling the mouse tracking
    print("Mouse Tracking Enabled")
    click_action_thread = Thread(target=track_mouse_clicks)
    click_action_thread.start()

    return


################################################################################

#piano_booster_setup()

"""
#Initializing Live Settings UI
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #Dialog = QtWidgets.QDialog()
    ui = Companion_Dialog()
    #ui.setupUiDialog(Dialog)
    #Dialog.show()
    app.exec_()
"""
