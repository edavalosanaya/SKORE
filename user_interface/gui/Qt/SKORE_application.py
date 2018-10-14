import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QAction, QMainWindow, QInputDialog, QLineEdit, QFileDialog, QMessageBox, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

#Importing the Settings Dialog
#from settings_dialog import *
from settings_dialog2 import *

#This is to prevent an error caused when importing skore_program_controller
import warnings
warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2

#Determining where SKORE application is located
complete_path = os.path.dirname(os.path.abspath(__file__))
skore_index = complete_path.find('SKORE') + len('SKORE')
skore_path = complete_path[0:skore_index+1]

#Importing SKORE functions and additional windows
skore_program_controller_extension_path = r'user_interface\app_control'
sys.path.append(skore_path + skore_program_controller_extension_path)
from skore_program_controller import *

#File Information
upload_file_path = []
save_folder_path = []
upload_file_name = []
upload_file_type = []

#Event Information
file_conversion_event = 0

################################################################################

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(916, 579)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

###############################Main Buttons#####################################

        #Upload Button
        self.uploadAudioFile_toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.uploadAudioFile_toolButton.setGeometry(QtCore.QRect(20, 20, 421, 171))
        self.uploadAudioFile_toolButton.setObjectName("uploadAudioFile_toolButton")
        self.uploadAudioFile_toolButton.clicked.connect(self.upload_file)

        #Record Button
        self.record_toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.record_toolButton.setGeometry(QtCore.QRect(470, 20, 421, 171))
        self.record_toolButton.setObjectName("record_toolButton")
        self.record_toolButton.clicked.connect(self.open_red_dot_forever)

        #Settings Button
        self.settings_toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.settings_toolButton.setGeometry(QtCore.QRect(20, 260, 871, 41))
        self.settings_toolButton.setObjectName("settings_toolButton")
        self.settings_toolButton.clicked.connect(self.settingsDialog)

#############################Tutoring Buttons###################################

        #Tutor Group Box
        self.tutor_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.tutor_groupBox.setGeometry(QtCore.QRect(20, 310, 421, 201))
        self.tutor_groupBox.setObjectName("tutor_groupBox")

        #Beginner Button
        self.beginner_pushButton = QtWidgets.QPushButton(self.tutor_groupBox)
        self.beginner_pushButton.setGeometry(QtCore.QRect(20, 20, 381, 51))
        self.beginner_pushButton.setObjectName("beginner_pushButton")

        #Intermediate Button
        self.intermediate_pushButton = QtWidgets.QPushButton(self.tutor_groupBox)
        self.intermediate_pushButton.setGeometry(QtCore.QRect(20, 80, 381, 51))
        self.intermediate_pushButton.setObjectName("intermediate_pushButton")

        #Expert Button
        self.expert_pushButton = QtWidgets.QPushButton(self.tutor_groupBox)
        self.expert_pushButton.setGeometry(QtCore.QRect(20, 140, 381, 51))
        self.expert_pushButton.setObjectName("expert_pushButton")

        self.tutoring_buttonGroup = QButtonGroup()
        self.tutoring_buttonGroup.setExclusive(True)
        self.tutoring_buttonGroup.addButton(self.beginner_pushButton)
        self.tutoring_buttonGroup.addButton(self.intermediate_pushButton)
        self.tutoring_buttonGroup.addButton(self.expert_pushButton)
        self.tutoring_buttonGroup.buttonClicked.connect(self.open_pianobooster)


##########################Conversion Buttons####################################

        #Generate Music Sheet Button
        self.generateMusicSheet_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.generateMusicSheet_pushButton.setGeometry(QtCore.QRect(470, 330, 421, 51))
        self.generateMusicSheet_pushButton.setObjectName("generateMusicSheet_pushButton")
        self.generateMusicSheet_pushButton.clicked.connect(self.generateMusicSheet)

        #Generate MID Button
        self.generateMIDFile_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.generateMIDFile_pushButton.setGeometry(QtCore.QRect(470, 390, 421, 51))
        self.generateMIDFile_pushButton.setObjectName("generateMIDFile_pushButton")
        self.generateMIDFile_pushButton.clicked.connect(self.generateMIDFile)

        #Save Generated
        self.saveGeneratedFiles_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveGeneratedFiles_pushButton.setGeometry(QtCore.QRect(470, 450, 421, 51))
        self.saveGeneratedFiles_pushButton.setObjectName("saveGeneratedFiles_pushButton")
        self.saveGeneratedFiles_pushButton.clicked.connect(self.saveGeneratedFiles)

############################Misc Buttons and Objects############################

        #Text Browser
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 200, 871, 51))
        self.textBrowser.setObjectName("textBrowser")

        #Menubar
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 916, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        #Status Bar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

################################################################################
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SKORE"))
        self.uploadAudioFile_toolButton.setText(_translate("MainWindow", "Upload audio file"))
        self.record_toolButton.setText(_translate("MainWindow", "Record"))
        self.settings_toolButton.setText(_translate("MainWindow", "Settings"))
        self.tutor_groupBox.setTitle(_translate("MainWindow", "Tutoring"))
        self.beginner_pushButton.setText(_translate("MainWindow", "Beginner Mode"))
        self.intermediate_pushButton.setText(_translate("MainWindow", "Intermediate Mode"))
        self.expert_pushButton.setText(_translate("MainWindow", "Expert Mode"))
        self.generateMusicSheet_pushButton.setText(_translate("MainWindow", "Generate Music Sheet"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">To open previous files, access the files from the output folder within app_control folder. </p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Uploaded File: " + str(upload_file_path) + " </p></body></html>"))
        self.generateMIDFile_pushButton.setText(_translate("MainWindow", "Generate MID File"))
        self.saveGeneratedFiles_pushButton.setText(_translate("MainWindow", "Save Generated Files"))

################################################################################
    def open_red_dot_forever(self):
        #This function start red dot forever

        start_red_dot_forever()
        return

    def open_pianobooster(self, button):

        start_piano_booster()

    def upload_file(self):
        #This function allows the user to upload a file for file conversion.

        global upload_file_path
        global upload_file_name
        global upload_file_type

        upload_file_path = self.openFileNameDialog_UserInput()
        upload_file_name = os.path.splitext(os.path.basename(upload_file_path))[0]
        upload_file_type = os.path.splitext(os.path.basename(upload_file_path))[1]

        if(upload_file_path != ''):
            self.retranslateUi(MainWindow)
        return

    def generateMusicSheet(self):
        #This functions converts the file uploaded to .pdf. It checkes if the
        #user has actually uploaded a file and if the conversion is valid.

        global file_conversion_event

        if(upload_file_path):
            if(is_pdf(upload_file_path)):
                QMessageBox.about(MainWindow, "Invalid Conversion", "Cannot convert .pdf to .pdf")
                return
            file_conversion_event = 1
            input_to_pdf(upload_file_path)
        else:
            print("No file uploaded")
            QMessageBox.about(MainWindow, "File Needed", "Please upload a file before taking an action.")
        return

    def generateMIDFile(self):
        #This functions converts the file uploaded to .mid. It checkes if the
        #user has actually uploaded a file and if the conversion is valid.

        global file_conversion_event

        if(upload_file_path):
            if(is_mid(upload_file_path)):
                QMessageBox.about(MainWindow, "Invalid Conversion", "Cannot convert .mid to .mid")
                return
            file_conversion_event = 1
            input_to_mid(upload_file_path)
        else:
            QMessageBox.about(MainWindow, "File Needed", "Please upload a file before taking an action")
        return

    def saveGeneratedFiles(self):
        #This functions saves all the files generated by the user. Effectively
        #it relocates all the files found temp to the user's choice of directory

        global save_folder_path
        global file_conversion_event

        if(file_conversion_event):
            user_given_filename, okPressed = QInputDialog.getText(MainWindow, "Save Files","Files Group Name:", QLineEdit.Normal, upload_file_name)
            if(okPressed):
                save_folder_path = self.openDirectoryDialog_UserInput()
                print(save_folder_path)
                temp_to_folder(destination_folder = save_folder_path, filename = user_given_filename)
                file_conversion_event = 0

        else:
            QMessageBox.about(MainWindow, "No Conversion Present", "Please upload and convert a file before saving it.")
        return

################################################################################
    def openFileNameDialog_UserInput(self):
        #This file dialog is used to obtain the file location of the .mid, .mp3,
        #and .pdf file.

        fileName, _ = QFileDialog.getOpenFileName(caption = "Select Audio File", filter = "MIDI files (*.mid);;MP3 Files (*.mp3);;PDF files (*.pdf)")

        if fileName:
            file_dialog_output = str(fileName)
        else:
            return ""

        file_dialog_output = file_dialog_output.replace('/' , '\\' )
        file_upload_event = 1
        return file_dialog_output

    def openDirectoryDialog_UserInput(self):
        #This file dialog is used to obtain the folder directory of the desired
        #save location for the generated files

        options = QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(MainWindow, caption = 'Open a folder', directory = skore_path, options = options)

        if directory:
            file_dialog_output = str(directory)
        else:
            return ""

        file_dialog_output = file_dialog_output.replace('/' , '\\' )
        return file_dialog_output

    def settingsDialog(self):
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUiDialog(self.dialog)
        self.dialog.show()

        return

################################################################################
#This starts the application

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
