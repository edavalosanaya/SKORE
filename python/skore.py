# General Utility Libraries
import sys
import os

# PyQt5, GUI LIbrary
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Importing the Settings Dialog (CAUSES ERROR)
from settings_dialog import *

# This is to prevent an error caused when importing skore_program_controller
import warnings
warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2

# SKORE Library
from skore_program_controller import *
#from skore_companion import *
from skore_glass import *

################################VARIABLES#######################################
#File Information
upload_file_path = []
save_folder_path = []
upload_file_name = []
upload_file_type = []
mid_file_obtained_path = []
animation_group = []
blink_button_group = []

#Event Information
file_conversion_event = 0
mid_file_obtained_event = 0

#####################################PYQT5######################################

class Skore(QtWidgets.QMainWindow):
    # This is the main window of the SKORE application

    def __init__(self):
        super(QtWidgets.QMainWindow, self).__init__()
        self.setupUI()

    def setupUI(self):

        global animation_group, blink_button_group

        self.setObjectName("MainWindow")
        self.resize(916,530)
        self.setStyleSheet("""
            background-color: rgb(50,50,50);
            color: white;
            """)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

###############################Main Buttons#####################################
        #Upload Button
        #self.uploadAudioFile_toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.uploadAudioFile_toolButton = BlinkButton("Upload File", self.centralwidget)
        self.uploadAudioFile_toolButton.setGeometry(QtCore.QRect(20, 20, 421, 171))
        self.uploadAudioFile_toolButton.setObjectName("uploadAudioFile_toolButton")
        self.uploadAudioFile_toolButton.clicked.connect(self.upload_file)
        self.uploadAudioFile_animation = BlinkAnimation(self.uploadAudioFile_toolButton, b'color', self)

        #Record Button
        #self.record_toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.record_toolButton = BlinkButton("Record", self.centralwidget)
        self.record_toolButton.setGeometry(QtCore.QRect(470, 20, 421, 171))
        self.record_toolButton.setObjectName("record_toolButton")
        self.record_toolButton.clicked.connect(self.open_red_dot_forever)
        self.record_animation = BlinkAnimation(self.record_toolButton, b'color', self)

        #Settings Button
        self.settings_toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.settings_toolButton.setGeometry(QtCore.QRect(20, 280, 871, 41))
        self.settings_toolButton.setObjectName("settings_toolButton")
        self.settings_toolButton.clicked.connect(self.settingsDialog)

#############################Tutoring Button####################################

        #Tutor Button
        #self.tutor_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.tutor_pushButton = BlinkButton("Tutoring", self.centralwidget)
        self.tutor_pushButton.setGeometry(QtCore.QRect(20, 330, 421, 171))
        self.tutor_pushButton.setObjectName("tutor_pushButton")
        #self.tutor_pushButton.setText("Tutoring")
        self.tutor_pushButton.clicked.connect(self.open_pianobooster)
        self.tutor_animation = BlinkAnimation(self.tutor_pushButton, b'color', self)

##########################Conversion Buttons####################################

        #Generate Music Sheet Button
        #self.generateMusicSheet_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.generateMusicSheet_pushButton = BlinkButton("Generate Music Sheet (and MIDI File)",self.centralwidget)
        self.generateMusicSheet_pushButton.setGeometry(QtCore.QRect(470, 330, 421, 51))
        self.generateMusicSheet_pushButton.setObjectName("generateMusicSheet_pushButton")
        self.generateMusicSheet_pushButton.clicked.connect(self.generateMusicSheet)
        self.generateMusicSheet_animation = BlinkAnimation(self.generateMusicSheet_pushButton, b'color', self)

        #Generate MID Button
        #self.generateMIDFile_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.generateMIDFile_pushButton = BlinkButton("Generate MIDI File", self.centralwidget)
        self.generateMIDFile_pushButton.setGeometry(QtCore.QRect(470, 390, 421, 51))
        self.generateMIDFile_pushButton.setObjectName("generateMIDFile_pushButton")
        self.generateMIDFile_pushButton.clicked.connect(self.generateMIDFile)
        self.generateMIDFile_animation = BlinkAnimation(self.generateMIDFile_pushButton, b'color', self)

        #Save Generated
        #self.saveGeneratedFiles_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveGeneratedFiles_pushButton = BlinkButton("Save Generated Files", self.centralwidget)
        self.saveGeneratedFiles_pushButton.setGeometry(QtCore.QRect(470, 450, 421, 51))
        self.saveGeneratedFiles_pushButton.setObjectName("saveGeneratedFiles_pushButton")
        self.saveGeneratedFiles_pushButton.clicked.connect(self.saveGeneratedFiles)
        self.saveGeneratedFiles_animation = BlinkAnimation(self.saveGeneratedFiles_pushButton, b'color', self)

############################Misc Buttons and Objects############################

        #Text Browser
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 200, 871, 70))
        self.textBrowser.setObjectName("textBrowser")

        #Menubar
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 916, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        #Status Bar
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.progress_bar = ProgressBarDialog()
        self.progress_bar.show()

        self.uploadAudioFile_animation.start()
        self.record_animation.start()

        animation_group = [self.uploadAudioFile_animation, self.generateMusicSheet_animation,
                            self.generateMIDFile_animation, self.saveGeneratedFiles_animation,
                            self.tutor_animation, self.record_animation]

        blink_button_group = [self.uploadAudioFile_toolButton, self.generateMusicSheet_pushButton,
                                self.generateMIDFile_pushButton, self.saveGeneratedFiles_pushButton,
                                self.tutor_pushButton, self.record_toolButton]

################################################################################

    def retranslateUi(self):
        # This function applies all the text changes in the main SKORE app.

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle('SKORE')
        #self.uploadAudioFile_toolButton.setText(_translate("MainWindow", "Upload audio file"))
        #self.record_toolButton.setText(_translate("MainWindow", "Record"))
        self.settings_toolButton.setText(_translate("MainWindow", "Settings"))
        #self.generateMusicSheet_pushButton.setText(_translate("MainWindow", "Generate Music Sheet (and MIDI file)"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">To open previous files, access the files from the output folder within app_control folder. </p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Uploaded File: " + str(upload_file_path) + " </p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">MIDI File Location: " + str(mid_file_obtained_path) + "</p></body></html>"))
        #self.generateMIDFile_pushButton.setText(_translate("MainWindow", "Generate MIDI File"))
        #self.saveGeneratedFiles_pushButton.setText(_translate("MainWindow", "Save Generated Files"))

    def closeEvent(self, event):
        # Closes any open threads and additional GUIs

        try:
            #self.skore_companion_dialog.close()
            self.skore_glass_overlay.close()
            print("skore_glass_overlay closure successful")
        except:
            print("skore_glass_overlay closure failed")

        try:
            self.progress_bar.close()
            print("progress_bar closure successful")
        except:
            print("progress_bar closure failed")

        try:
            self.settings_dialog.close()
            print("progress_bar closure successful")
        except:
            print("dialog closure failed")

        try:
            self.red_dot_thread.terminate()
            print("Red Dot Thread termination successful")
        except:
            print("Red Dot Thread termination failed")
        return

################################################################################

    def open_red_dot_forever(self):
        # This function start red dot forever thread
        self.stop_all_animation()
        self.red_dot_thread = RedDotThread()
        self.red_dot_thread.start()
        self.red_dot_thread.red_dot_signal.connect(self.red_dot_forever_translate)

        return

    def red_dot_forever_translate(self):

        # MIDI File Recorded!
        self.stop_all_animation()
        self.tutor_animation.start()
        self.generateMusicSheet_animation.start()
        self.retranslateUi()

        return

    def open_pianobooster(self):
        # This function initializes PianoBooster and opens the SKORE Companion app

        if(mid_file_obtained_event == 0):
            print("No midi file uploaded or generated")
            QMessageBox.about(self, "MIDI File Needed", "Please upload or generate a MIDI file before tutoring.")
            return

        #self.skore_companion_dialog = Companion_Dialog()
        #self.skore_companion_dialog.show()
        self.progress_bar.current_action_label.setText("Initializing SKORE Glass")
        self.progress_bar.progress.setValue(50)
        self.skore_glass_overlay = SkoreGlassGui()
        self.skore_glass_overlay.show()
        self.progress_bar.current_action_label.setText("SKORE Glass Enabled")
        self.progress_bar.progress.setValue(100)

        return

    def upload_file(self):
        # This function allows the user to upload a file for file conversions

        global upload_file_path, upload_file_name, upload_file_type
        global mid_file_obtained_event, mid_file_obtained_path

        temp_upload_file_path = self.openFileNameDialog_UserInput()

        if temp_upload_file_path:
            upload_file_path = temp_upload_file_path
            upload_file_name = os.path.splitext(os.path.basename(upload_file_path))[0]
            upload_file_type = os.path.splitext(os.path.basename(upload_file_path))[1]

            self.stop_all_animation()

            print(upload_file_path)

            if(is_mid(upload_file_path)):
                # Obtaining mid file location
                mid_file_obtained_event = 1
                mid_file_obtained_path = upload_file_path
                self.tutor_animation.start()
                self.generateMusicSheet_animation.start()
            elif(is_pdf(upload_file_path)):
                self.generateMIDFile_animation.start()
                mid_file_obtained_event = 0
                mid_file_obtained_path = []
            elif(is_mp3(upload_file_path)):
                self.generateMIDFile_animation.start()
                self.generateMusicSheet_animation.start()
                mid_file_obtained_event = 0
                mid_file_obtained_path = []

            setting_write('midi_file_location', mid_file_obtained_path)
            #self.retranslateUi(MainWindow)
            self.retranslateUi()

        return

    def generateMusicSheet(self):
        # This functions converts the file uploaded to .pdf. It checkes if the
        # user has actually uploaded a file and if the conversion is valid.

        global file_conversion_event, mid_file_obtained_event, mid_file_obtained_path

        if(upload_file_path):
            if(is_pdf(upload_file_path)):
                QMessageBox.about(self, "Invalid Conversion", "Cannot convert .pdf to .pdf")
                return
            # Obtaining mid file location
            self.stop_all_animation()
            file_conversion_event = 1
            mid_file_obtained_event = 1
            mid_file_obtained_path = input_to_pdf(upload_file_path, self.progress_bar)
            setting_write('midi_file_location',mid_file_obtained_path)

            self.saveGeneratedFiles_animation.start()
            self.tutor_animation.start()

            self.retranslateUi()


        else:
            print("No file uploaded")
            QMessageBox.about(self, "File Needed", "Please upload a file before taking an action.")
        return

    def generateMIDFile(self):
        # This functions converts the file uploaded to .mid. It checkes if the
        # user has actually uploaded a file and if the conversion is valid.

        global file_conversion_event, mid_file_obtained_event, mid_file_obtained_path
        mp3_2_midi_converter = setting_read('mp3_2_midi_converter')

        if(upload_file_path):
            if(is_mid(upload_file_path)):
                QMessageBox.about(self, "Invalid Conversion", "Cannot convert .mid to .mid")
                return
            # Obtaining mid file location
            self.stop_all_animation()
            file_conversion_event = 1
            mid_file_obtained_event = 1
            mid_file_obtained_path = input_to_mid(upload_file_path, self.progress_bar)
            setting_write('midi_file_location',mid_file_obtained_path)

            if(is_pdf(upload_file_path)):
                self.saveGeneratedFiles_animation.start()
                self.tutor_animation.start()
            elif(is_mp3(upload_file_path)):
                if mp3_2_midi_converter == 'amazingmidi':
                    self.saveGeneratedFiles_animation.start()
                    self.tutor_animation.start()
                    self.generateMusicSheet_animation.start()
                elif mp3_2_midi_converter == 'anthemscore':
                    self.tutor_animation.start()
                    self.generateMusicSheet_animation.start()
            self.retranslateUi()

        else:
            #QMessageBox.about(MainWindow, "File Needed", "Please upload a file before taking an action")
            QMessageBox.about(self, "File Needed", "Please upload a file before taking an action")
        return

    def saveGeneratedFiles(self):
        # This functions saves all the files generated by the user. Effectively
        # it relocates all the files found temp to the user's choice of directory

        global save_folder_path, file_conversion_event, mid_file_obtained_path

        if(file_conversion_event):
            user_given_filename, okPressed = QInputDialog.getText(self, "Save Files","Files Group Name:", QLineEdit.Normal, upload_file_name)
            if(okPressed):
                save_folder_path = self.openDirectoryDialog_UserInput()
                print(save_folder_path)
                file_conversion_event = 0

                self.stop_all_animation()

                # Obtaining mid file location
                file = temp_to_folder(destination_folder = save_folder_path, filename = user_given_filename)

                if file != []:
                    mid_file_obtained_path = file
                    setting_write('midi_file_location',mid_file_obtained_path)
                    print(mid_file_obtained_path)
                    self.retranslateUi()
                    self.tutor_animation.start()

                if is_mid(upload_file_path):
                    self.tutor_animation.start()

        else:
            QMessageBox.about(self, "No Conversion Present", "Please upload and convert a file before saving it.")
        return

################################################################################

    def openFileNameDialog_UserInput(self):
        # This file dialog is used to obtain the file location of the .mid, .mp3,
        # and .pdf file.

        fileName, _ = QFileDialog.getOpenFileName(caption = "Select Audio File", filter = "All Supported Files (*.mid *.mp3 *.pdf);;All Files (*.*);;MIDI Files(*.mid);;MP3 Files(*.mp3);;PDF Files (*.pdf)")

        if fileName:
            file_dialog_output = str(fileName)
        else:
            return ""

        file_dialog_output = file_dialog_output.replace('/' , '\\' )
        file_upload_event = 1
        return file_dialog_output

    def openDirectoryDialog_UserInput(self):
        # This file dialog is used to obtain the folder directory of the desired
        # save location for the generated files

        options = QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, caption = 'Open a folder', directory = skore_path, options = options)

        if directory:
            file_dialog_output = str(directory)
        else:
            return ""

        file_dialog_output = file_dialog_output.replace('/' , '\\' )
        return file_dialog_output

    def settingsDialog(self):
        # This function opens the settings dialog

        self.settings_dialog = SettingsDialog()
        self.settings_dialog.show()

        return

    def stop_all_animation(self):

        for animation in animation_group:
            animation.stop()

        for blink_button in blink_button_group:
            blink_button.reset_color()
        return

################################################################################

class ProgressBarDialog(QtWidgets.QDialog):
    # This QtWidget deals with the display of the progress bar during the file
    # conversion. This is to inform the user the state of the file conversion
    # to ensure no malfunction due to user interference.

    def __init__(self):
        super(QtWidgets.QDialog, self).__init__()
        self.init_dialog()

    def init_dialog(self):
        # This initializes the individual qtwidgets ontop of the progress bar dialog

        self.setObjectName("ProgressBarDialog")
        self.resize(350,150)
        print("Initializing Progress Bar Dialog")
        self.setWindowTitle("Progress Bar")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.relocate()
        self.setStyleSheet("""
            background-color: rgb(50,50,50);
            color: white;
            """)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(40,40,250,25)
        self.progress.setStyleSheet("""
        .QProgressBar {
            color: red;
        }
        """)

        self.current_action_label = QtWidgets.QLabel(self)
        self.current_action_label.setGeometry(QtCore.QRect(40,70,300,25))
        self.current_action_label.setObjectName("current_action_label")
        self.current_action_label.setText("Please wait while we calibrate ... The Nozzle")

        #self.quit_pushButton = QPushButton("Quit",self)
        #self.quit_pushButton.setGeometry(193,100,100,30)

        print("Finished Initializing Progress Bar Dialog")

        #self.show()

    def relocate(self):
        # Relocates the ProgressBarDialog in the center of the fourth quadrant
        # of the screen. This is to ensure that the ProgressBarDialog does not
        # affect the image processing to click the buttons.

        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        x_center = centerPoint.x()
        y_center = centerPoint.y()
        x_desired = int(x_center + x_center/1.5)
        y_desired = int(y_center + y_center/1.5)
        centerPoint.setX(x_desired)
        centerPoint.setY(y_desired)
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        return

################################################################################

class RedDotThread(QThread):
    # This thread checks and determines the address given for the midi file
    # recorded by Red Dot Forever. It successfully changes the upload_file
    # variable and other necessary changes to account for any changes.

    red_dot_signal = QtCore.pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def run(self):

        global mid_file_obtained_path, upload_file_path, mid_file_obtained_event
        address_list = []
        filename_list = []
        s_handle = []

        red_app = pywinauto.application.Application()
        red_app_exe_path = setting_read('red_app_exe_path')
        red_app.start(red_app_exe_path)
        print("Initialized Red Dot Forever")

        while(True):
            try:
                w_handle = pywinauto.findwindows.find_windows(title="Red Dot Forever")[0]
                window = red_app.window(handle=w_handle)
                break
            except IndexError:
                time.sleep(0.2)


        while(True):
            try:
                #s_handle = pywinauto.findwindows.find_windows(title="Save As")[0]
                s_handle = pywinauto.findwindows.find_windows(parent=w_handle)[0]
                s_window = red_app.window(handle=s_handle)
                #print("Handle Found: " + str(s_handle))
            except IndexError:
                s_handle = []
                #print("waiting")

            if s_handle != []:
                toolbarwindow = s_window.Toolbar4
                edit = s_window.Edit
                while(True):
                    try:
                        address_list = toolbarwindow.texts()
                        #print(text[0])
                        filename_list = edit.texts()
                        #print(text2)
                    except:
                        break

                # User is Saving!
                #print("Address: " + str(text))
                #print("File Name: " + str(text2))

            # Checking if the Red Dot Forever application is running
            processes = [p.name() for p in psutil.process_iter()]

            for process in processes:
                if process == 'reddot.exe':
                    # Red Dot Forever is running
                    break

            if process != 'reddot.exe':
                print("Red Dot Forever Closed")
                break

        if address_list == [] or filename_list == []:
            return

        print("Final Data")
        print("Address: " + str(address_list))
        print("File Name: " + str(filename_list))
        red_dot_address = red_dot_address_conversion(address_list,filename_list)

        output_file = Path(red_dot_address)
        if(output_file.is_file()):
            upload_file_path = red_dot_address
            mid_file_obtained_path = upload_file_path
            setting_write('midi_file_location', mid_file_obtained_path)
            mid_file_obtained_event = 1
            self.red_dot_signal.emit()

        else:
            print("red dot midi file not found")

        return

################################################################################

class BlinkButton(QPushButton):
    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        self.default_color = self.getColor()

    def getColor(self):
        #return self.palette().color(QPalette.Button)
        #return self.palette().color(QColor(50,50,50))
        return QColor(50,50,50)

    def setColor(self, value):
        if value == self.getColor():
            return
        palette = self.palette()
        palette.setColor(self.backgroundRole(), value)
        self.setFlat(True)
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def reset_color(self):
        palette = self.palette()
        palette.setColor(self.backgroundRole(), self.default_color)
        self.setPalette(palette)
        self.setFlat(False)

    color = pyqtProperty(QColor, getColor, setColor)

################################################################################

class BlinkAnimation(QPropertyAnimation):

    qwidget = []

    def __init__(self, *args, **kwargs):
        QPropertyAnimation.__init__(self, *args, **kwargs)

        global qwidget
        qwidget = args[0]

        self.setDuration(3000)
        self.setLoopCount(-1) # Run infinitely
        self.setStartValue(qwidget.default_color)
        self.setEndValue(qwidget.default_color)
        self.setKeyValueAt(0.5, QColor(10,200,30))

#################################MAIN CODE######################################
# This starts the application

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    list = QStyleFactory.keys()
    #print(list)
    app.setStyle(QStyleFactory.create(list[2])) #Fusion
    ui = Skore()
    ui.show()
    sys.exit(app.exec_())
