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

###############################VARIABLES########################################
all_qwidgets = []
all_qwidgets_names = []

button_history = []
processed_button_history = []
processed_index = 0

message_box_active = 0

x_coord_history = []
y_coord_history = []
processed_x_coord_history = []
processed_y_coord_history = []
processed_index_coord = 0

timing_lineedit = ['time_per_tick','increment_counter','chord_timing_tolerance','manual_final_chord_sustain_timing']
timing_values = ['','','','']

#####################################PYQT5######################################

class AppOpenThread(QThread):
    # This thread deals with closure of the PianoBooster Application. Once the
    # application is closed, it will emit a signal to inform the SKORE Companion
    # application to close.

    app_close_signal = QtCore.pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def run(self):

        print("Piano Booster App State Thread Enabled")

        while(True):
            time.sleep(5)

            # Checking if the pianobooster application is running
            processes = [p.name() for p in psutil.process_iter()]

            for process in processes:
                if process == 'pianobooster.exe':
                    # PianoBooster is running
                    break

            if process != 'pianobooster.exe':
                # if the PianoBooster is not running, end mouse tracking
                print("PianoBooster Application Closure Detection")
                time.sleep(1)
                self.app_close_signal.emit()
                break

################################################################################

class CoordinateThread(QThread):
    # This thread determines the widget clicked with the given coordinates from
    # the ClickThread. Once it determines if the click coordinates fit within
    # a widget, it appends the clicked qwidget to a list of qwidgets pressed.

    def __init__(self):
        QThread.__init__(self)

    def run(self):

        print("Coordinate Tracking Thread Enabled")

        global button_history, x_coord_history, y_coord_history, processed_index_coord
        global processed_x_coord_history, processed_y_coord_history

        int_dimensions = [0,0,0,0]

        while(True):
            time.sleep(0.1)

            #print('x_coord_history: ' + str(x_coord_history))
            #print('y_coord_history: ' + str(y_coord_history))

            #print('processed_x_coord_history: ' + str(processed_x_coord_history))
            #print('processed_y_coord_history: ' + str(processed_y_coord_history))

            if len(x_coord_history) != len(processed_x_coord_history):

                processed_x_coord_history.append(x_coord_history[processed_index_coord])
                processed_y_coord_history.append(y_coord_history[processed_index_coord])

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
                    if processed_x_coord_history[processed_index_coord] > int_dimensions[0] and processed_x_coord_history[processed_index_coord] < int_dimensions[2] and processed_y_coord_history[processed_index_coord] > int_dimensions[1] and processed_y_coord_history[processed_index_coord] < int_dimensions[3]:
                        # Found the qwidget
                        #print("QWidget Pressed Detected: " + str(all_qwidgets_names[all_qwidgets.index(widget)]))
                        button = all_qwidgets_names[all_qwidgets.index(widget)]
                        button_history.append(button)
                        break

                processed_index_coord += 1

################################################################################

class ClickThread(QThread):
    # This thread constantly checks the status of the mouse, clicked or unclicked,
    # and determines whenever there is a unclicked to clicked event. Then it
    # appends the coordinates of the event to lists of coordinates

    global y_coord_history, x_coord_history


    def __init__(self):
        QThread.__init__(self)

    def run(self):

        print("Click Tracking Thread Enabled")

        global click_event

        state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
        state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128

        while True:

            # Checking if the mouse has been clicked and obtain its coordinates
            a = win32api.GetKeyState(0x01)
            #b = win32api.GetKeyState(0x02)

            if a != state_left:  # Button state changed
                state_left = a
                #print(a)

                if a < 0:
                    c = 1
                else:
                    x_coord, y_coord = win32api.GetCursorPos()
                    x_coord_history.append(x_coord)
                    y_coord_history.append(y_coord)


################################################################################

class ButtonThread(QThread):
    # This thread processes the list of the buttons clicked on. It determines if
    # the settings need to changed, and performs according to the users button
    # clicks

    button_signal = QtCore.pyqtSignal('QString')

    def __init__(self):
        QThread.__init__(self)

    def run(self):

        print("User Usage Tracking Thread Enabled")

        """
        global button_history
        global processed_button_history
        global processed_index
        global message_box_active
        """
        global button_history, processed_button_history, processed_index, message_box_active

        while(True):
            time.sleep(0.1)

            #print("button_history: " + str(button_history))

            if len(button_history) != len(processed_button_history):

                #print("BEFORE: Button History: " + str(button_history) + "\t Processed Button History: " + str(processed_button_history))
                processed_button_history.append(button_history[processed_index])
                #print("AFTER: Button History: " + str(button_history) + "\t Processed Button History: " + str(processed_button_history))
                #print("Current Processed Action: " + str(processed_button_history[processed_index]))

                for index, item in enumerate(all_qwidgets_names):
                    if item == processed_button_history[processed_index]:
                        if index <= 2: # Skill Selection
                            skill = setting_read('skill')
                            if skill != item:
                                print("Tutoring Mode Change")
                                setting_write('skill',str(item),'append')
                                setting_write('live_setting_change','1','append')

                        elif index > 2 and index <= 5: # Hand Selection
                            hand = setting_read('hand')
                            if hand != item:
                                print("Hand Mode Change")
                                setting_write('hand',str(item),'append')
                                setting_write('live_setting_change','1','append')

                        elif index > 5 and index <= 7: # Song and Book Combo
                            print("Song and Combo Boxes were pressed. Please do not change the song")

                        elif index == 8: # Play Button
                            playing_state = setting_read('playing_state')
                            playing_state = eval(playing_state)
                            playing_state = not playing_state
                            setting_write('playing_state',str(playing_state),'append')
                            setting_write('live_setting_change','1','append')

                        elif index == 9: # Restart Button
                            print("Restart Detected")
                            setting_write('restart','1','append')
                            setting_write('playing_state','1','append')
                            setting_write('live_setting_change','1','append')

                        elif index > 9 and index <= 11: # Spin Boxes
                            print("Spin Buttons Pressed")
                            if message_box_active == 0:
                                self.button_signal.emit(item)
                            else:
                                print("Message box in use")
                        else:
                            print("Current Button: " + item + " is not functional yet")

                        #print("Current Processed Action Complete")
                        processed_index += 1
                        break
                    else:
                        continue

################################################################################

class Companion_Dialog(QtWidgets.QDialog):
    # This is the SKORE Companion Application that aids the user in controlling
    # the tutoring mode and timing settings

    def __init__(self):
        super(QtWidgets.QDialog, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setObjectName("Dialog")
        self.resize(420, 250)
        self.setWindowTitle("SKORE Companion")
        # Making SKORE Companion always ontop
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # Removing the close button
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

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

        # Tutoring Mode
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
        self.apply_pushButton.clicked.connect(self.apply_timing_values)

        # Tutoring Mode Function Assignment
        self.beginner_companion_pushButton.clicked.connect(self.beginner_mode_setting)
        self.intermediate_companion_pushButton.clicked.connect(self.intermediate_mode_setting)
        self.expert_companion_pushButton.clicked.connect(self.expert_mode_setting)

        # Initializing PianoBooster App Open Check MultiThreading
        self.check_open_app_thread = AppOpenThread()
        self.check_open_app_thread.app_close_signal.connect(self.close_all_thread)
        self.check_open_app_thread.start()

        # Initializing CLick MultiThreading
        self.click_tracking_thread = ClickThread()
        #self.click_tracking_thread.click_signal.connect(self.determine_button)
        self.click_tracking_thread.start()

        # Initializing Coordinate MultiThreading
        self.coord_tracking_thread = CoordinateThread()
        self.coord_tracking_thread.start()

        # Initializing Button MultiThreading
        self.user_tracking_thread = ButtonThread()
        self.user_tracking_thread.button_signal.connect(self.create_message_box)
        self.user_tracking_thread.start()

        # Timing Tab Initialization
        self.settings_timing_read()
        self.update_timing_values()

        self.show()

###############################DIALOG FUNCTIONS#################################

    def beginner_mode_setting(self):
        current_mode = setting_read('mode')
        if current_mode != 'beginner':
            setting_write('mode','beginner','append')
            setting_write('live_setting_change','1','append')
        return

    def intermediate_mode_setting(self):
        current_mode = setting_read('mode')
        if current_mode != 'intermediate':
            setting_write('mode','intermediate','append')
            setting_write('live_setting_change','1','append')
        return

    def expert_mode_setting(self):
        current_mode = setting_read('mode')
        if current_mode != 'expert':
            setting_write('mode','expert','append')
            setting_write('live_setting_change','1','append')
        return

    def settings_timing_read(self):
        # This function reads the settings for the timing values

        global timing_values

        for i in range(len(timing_lineedit)):
            timing_values[i] = setting_read(timing_lineedit[i])
        return

    def update_timing_values(self):
        # This function updates the lineedits of the timing values

        for i in range(len(timing_lineedit)):
            lineEdit_attribute = getattr(self, timing_lineedit[i] + '_lineEdit')
            lineEdit_attribute.setText(timing_values[i])
        return

    def apply_timing_values(self):
        # This function applies the changes of the timings values to the settings file

        self.settings_timing_read()

        for i in range(len(timing_lineedit)):
            lineEdit_attribute = getattr(self, timing_lineedit[i] + '_lineEdit')
            text = lineEdit_attribute.text()
            if timing_values[i] != text:
                timing_values[i] = text
                current_setting = setting_read(timing_lineedit[i])
                if current_setting != text:
                    setting_write(timing_lineedit[i], timing_values[i], 'append')
                    setting_write('live_setting_change','1','append')
        return

    @pyqtSlot('QString')
    def create_message_box(self, item):
        # This function creates a QInputDialog box for the user to input
        # multivalue information, such as speed and tranpose

        global speed, tranpose, message_box_active

        flag = 0

        # Stopping the application
        playing_state = setting_read('playing_state')
        if eval(playing_state) == True:
            flag = 1
            print("Stoping app")
            all_qwidgets[8].click()
            setting_write('playing_state','0','append')

        # Asking user for value of spin button
        message_box_active = 1
        num, ok = QInputDialog.getInt(self, item + "Pressed", "Enter the value for " + item)

        # Processing data entered from QInputDialog
        if ok:
            if item == 'speed_spin_button':
                #speed = num
                speed = int(setting_read('speed'))
                if speed != num:
                    setting_write('speed',str(num),'append')
                    setting_write('live_setting_change','1','append')
            elif item == 'transpose_spin_button':
                #tranpose = num
                tranpose = int(setting_read('tranpose'))
                if tranpose != num:
                    setting_write('tranpose',str(num),'append')
                    setting_write('live_setting_change','1','append')

        print("End of Message Box Usage")
        message_box_active = 0

        if flag == 1:
            print("Continuing the app")
            all_qwidgets[8].click()
            setting_write('playing_state','1','append')

        return

    def close_all_thread(self):
        # This function terminates appropriately all the threads and then closes
        # the SKORE Companion Application

        print("Terminating all threads")
        self.click_tracking_thread.terminate()
        self.coord_tracking_thread.terminate()
        self.user_tracking_thread.terminate()
        self.check_open_app_thread.terminate()
        self.close()

        return

################################GENERAL FUNCTIONS###############################

def retrieve_name(var):
    # This function retrieves the name of a variable

    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]

def variable_setup():
    # This function assures that everytime PianoBooster and the SKORE Companion
    # applications are open, the variables are initialzed correctly

    global all_qwidgets,all_qwidgets_names,button_history,processed_button_history
    global processed_index, message_box_active,x_coord_history,y_coord_history
    global processed_x_coord_history,processed_y_coord_history,processed_index_coord

    all_qwidgets = []
    all_qwidgets = []
    all_qwidgets_names = []

    button_history = []
    processed_button_history = []
    processed_index = 0

    message_box_active = 0

    x_coord_history = []
    y_coord_history = []
    processed_x_coord_history = []
    processed_y_coord_history = []
    processed_index_coord = 0

    setting_write('live_setting_change','0','append')
    setting_write('mode','beginner','append')
    setting_write('playing_state','0','append')
    setting_write('hand','both_hands','append')
    setting_write('skill','follow_you_button','append')

    return

def piano_booster_setup():
    # This function performs the task of opening PianoBooster and appropriately
    # clicking on the majority of the qwidgets to make them addressable. When
    # PianoBooster is opened, the qwidgets are still not addressible via
    # pywinauto. For some weird reason, clicked on them enables them. The code
    # utilizes template matching to click on specific regions of the PianoBooster
    # GUI

    global all_qwidgets
    global all_qwidgets_names

    # Initilizing the PianoBooster Application
    pia_app = pywinauto.application.Application()
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
    window = pia_app.window(handle=w_handle)

    # Initializion of the Qwidget within the application
    window.maximize()
    time.sleep(0.5)

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

    # Creating list easily address each qwidget
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
