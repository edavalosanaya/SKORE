from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
import warnings
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QAction, QMainWindow, QInputDialog, QLineEdit, QFileDialog, QMessageBox, QLabel, QButtonGroup, QDialogButtonBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2

#Determining where SKORE application is located
complete_path = os.path.dirname(os.path.abspath(__file__))
skore_index = complete_path.find('SKORE') + len('SKORE')
skore_path = complete_path[0:skore_index+1]

#Importing SKORE functions and additional windows
skore_program_controller_extension_path = r'user_interface\app_control'
sys.path.append(skore_path + skore_program_controller_extension_path)
from skore_program_controller import setting_read, setting_write
#default_or_temp_mode = 'temp'

#Variable Array for Executiable path
app_exe_path = ['','','','','','','','']
possible_app = ['audiveris','amazingmidi','audacity','midiSheetMusic','xenoplay','reddotforever','pianobooster','anthemscore']
app_exe_setting_label = ['audi_app_exe_path','ama_app_exe_path','aud_app_exe_path','midi_app_exe_path','xeno_app_exe_path','red_app_exe_path','pia_app_exe_path','ant_app_exe_path']
################################################################################

class Ui_Dialog(object):
    def setupUiDialog(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(509, 613)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(300, 570, 201, 32))
        self.buttonBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")


        self.pianobooster_pushButton = QtWidgets.QPushButton(Dialog)
        self.pianobooster_pushButton.setGeometry(QtCore.QRect(400, 270, 93, 31))
        self.pianobooster_pushButton.setObjectName("pianobooster_pushButton")
        self.midiSheetMusic_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.midiSheetMusic_lineEdit.setGeometry(QtCore.QRect(10, 330, 381, 31))
        self.midiSheetMusic_lineEdit.setObjectName("midiSheetMusic_lineEdit")
        self.amazingmidi_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.amazingmidi_lineEdit.setGeometry(QtCore.QRect(10, 150, 381, 31))
        self.amazingmidi_lineEdit.setObjectName("amazingmidi_lineEdit")
        self.audiveris_label = QtWidgets.QLabel(Dialog)
        self.audiveris_label.setGeometry(QtCore.QRect(10, 70, 101, 16))
        self.audiveris_label.setObjectName("audiveris_label")
        self.midiSheetMusic_pushButton = QtWidgets.QPushButton(Dialog)
        self.midiSheetMusic_pushButton.setGeometry(QtCore.QRect(400, 330, 93, 31))
        self.midiSheetMusic_pushButton.setObjectName("midiSheetMusic_pushButton")
        self.audiveris_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.audiveris_lineEdit.setGeometry(QtCore.QRect(10, 90, 381, 31))
        self.audiveris_lineEdit.setObjectName("audiveris_lineEdit")
        self.reddotforever_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.reddotforever_lineEdit.setGeometry(QtCore.QRect(10, 210, 381, 31))
        self.reddotforever_lineEdit.setObjectName("reddotforever_lineEdit")
        self.audiveris_pushButton = QtWidgets.QPushButton(Dialog)
        self.audiveris_pushButton.setGeometry(QtCore.QRect(400, 90, 93, 31))
        self.audiveris_pushButton.setObjectName("audiveris_pushButton")
        self.xenoplay_label = QtWidgets.QLabel(Dialog)
        self.xenoplay_label.setGeometry(QtCore.QRect(10, 370, 121, 16))
        self.xenoplay_label.setObjectName("xenoplay_label")
        self.reddotforever_label = QtWidgets.QLabel(Dialog)
        self.reddotforever_label.setGeometry(QtCore.QRect(10, 190, 131, 16))
        self.reddotforever_label.setObjectName("reddotforever_label")
        self.amazingmidi_label = QtWidgets.QLabel(Dialog)
        self.amazingmidi_label.setGeometry(QtCore.QRect(10, 130, 121, 16))
        self.amazingmidi_label.setObjectName("amazingmidi_label")
        self.audacity_label = QtWidgets.QLabel(Dialog)
        self.audacity_label.setGeometry(QtCore.QRect(10, 430, 191, 16))
        self.audacity_label.setObjectName("audacity_label")
        self.xenoplay_pushButton = QtWidgets.QPushButton(Dialog)
        self.xenoplay_pushButton.setGeometry(QtCore.QRect(400, 390, 93, 31))
        self.xenoplay_pushButton.setObjectName("xenoplay_pushButton")
        self.reddotforever_pushButton = QtWidgets.QPushButton(Dialog)
        self.reddotforever_pushButton.setGeometry(QtCore.QRect(400, 210, 93, 31))
        self.reddotforever_pushButton.setObjectName("reddotforever_pushButton")
        self.xenoplay_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.xenoplay_lineEdit.setGeometry(QtCore.QRect(10, 390, 381, 31))
        self.xenoplay_lineEdit.setObjectName("xenoplay_lineEdit")
        self.audacity_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.audacity_lineEdit.setGeometry(QtCore.QRect(10, 450, 381, 31))
        self.audacity_lineEdit.setObjectName("audacity_lineEdit")
        self.pianobooster_label = QtWidgets.QLabel(Dialog)
        self.pianobooster_label.setGeometry(QtCore.QRect(10, 250, 121, 16))
        self.pianobooster_label.setObjectName("pianobooster_label")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(10, 50, 621, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.amazingmidi_pushButton = QtWidgets.QPushButton(Dialog)
        self.amazingmidi_pushButton.setGeometry(QtCore.QRect(400, 150, 93, 31))
        self.amazingmidi_pushButton.setObjectName("amazingmidi_pushButton")
        self.pianobooster_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.pianobooster_lineEdit.setGeometry(QtCore.QRect(10, 270, 381, 31))
        self.pianobooster_lineEdit.setObjectName("pianobooster_lineEdit")
        self.audacity_pushButton = QtWidgets.QPushButton(Dialog)
        self.audacity_pushButton.setGeometry(QtCore.QRect(400, 450, 93, 31))
        self.audacity_pushButton.setObjectName("audacity_pushButton")
        self.midisheetmusic_label = QtWidgets.QLabel(Dialog)
        self.midisheetmusic_label.setGeometry(QtCore.QRect(10, 310, 141, 16))
        self.midisheetmusic_label.setObjectName("midisheetmusic_label")
        self.configurePath_label = QtWidgets.QLabel(Dialog)
        self.configurePath_label.setGeometry(QtCore.QRect(10, 20, 231, 16))
        self.configurePath_label.setObjectName("configurePath_label")
        self.anthemscore_label = QtWidgets.QLabel(Dialog)
        self.anthemscore_label.setGeometry(QtCore.QRect(10, 490, 191, 16))
        self.anthemscore_label.setObjectName("anthemscore_label")
        self.anthemscore_pushButton = QtWidgets.QPushButton(Dialog)
        self.anthemscore_pushButton.setGeometry(QtCore.QRect(400, 510, 93, 31))
        self.anthemscore_pushButton.setObjectName("anthemscore_pushButton")
        self.anthemscore_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.anthemscore_lineEdit.setGeometry(QtCore.QRect(10, 510, 381, 31))
        self.anthemscore_lineEdit.setObjectName("anthemscore_lineEdit")

        #Button Browsing Addition
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        self.button_group.addButton(self.audiveris_pushButton)
        self.button_group.addButton(self.amazingmidi_pushButton)
        self.button_group.addButton(self.audacity_pushButton)
        self.button_group.addButton(self.midiSheetMusic_pushButton)
        self.button_group.addButton(self.xenoplay_pushButton)
        self.button_group.addButton(self.reddotforever_pushButton)
        self.button_group.addButton(self.pianobooster_pushButton)
        self.button_group.addButton(self.anthemscore_pushButton)
        self.button_group.buttonClicked.connect(self.upload_exe_file)

        self.retranslateUi(Dialog)
        self.settings_path_read()
        self.update_paths()

        self.buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.apply_path)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

################################################################################
    def upload_exe_file(self, button):
        #This function allows the user to upload a file for file conversion.

        button_name = str(button.objectName())
        app_name = button_name.split('_')[0]
        #print(button_name)
        #print(app_name)

        if(app_name == 'audiveris'):
            upload_exe_path = self.openDirectoryDialog_ExecPath()
        else:
            upload_exe_path = self.openFileNameDialog_ExecPath()

        for i in range(len(possible_app)):
            if(possible_app[i] == app_name):
                app_exe_path[i] = upload_exe_path
                #print(app_exe_path[i])

        self.update_paths()

        return

################################################################################

    def openFileNameDialog_ExecPath(self):
        #This file dialog is used to obtain the file location of the .exe file.

        fileName, _ = QFileDialog.getOpenFileName(caption = "Select .exe File", filter = "Executiable files (*.exe)")

        if fileName:
            fileName = str(fileName)
        else:
            return ""

        fileName = fileName.replace('/' , '\\' )
        return fileName

    def openDirectoryDialog_ExecPath(self):
        #This file dialog is used to obtain the folder directory of the desired
        #save location for the generated files

        options = QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(caption = 'Open a folder', directory = skore_path, options = options)

        if directory:
            file_dialog_output = str(directory)
        else:
            return ""

        file_dialog_output = file_dialog_output.replace('/' , '\\' )
        return file_dialog_output

################################################################################

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Settings"))
        self.pianobooster_pushButton.setText(_translate("Dialog", "Browse"))
        self.audiveris_label.setText(_translate("Dialog", "Audiveris [folder]"))
        self.midiSheetMusic_pushButton.setText(_translate("Dialog", "Browse"))
        self.audiveris_pushButton.setText(_translate("Dialog", "Browse"))
        self.xenoplay_label.setText(_translate("Dialog", "Xenoplay [.jar]"))
        self.reddotforever_label.setText(_translate("Dialog", "Red Dot Forever [.exe]"))
        self.amazingmidi_label.setText(_translate("Dialog", "AmazingMIDI [.exe]"))
        self.audacity_label.setText(_translate("Dialog", "Audacity [.exe]"))
        self.xenoplay_pushButton.setText(_translate("Dialog", "Browse"))
        self.reddotforever_pushButton.setText(_translate("Dialog", "Browse"))
        self.pianobooster_label.setText(_translate("Dialog", "PianoBooster [.exe]"))
        self.amazingmidi_pushButton.setText(_translate("Dialog", "Browse"))
        self.audacity_pushButton.setText(_translate("Dialog", "Browse"))
        self.midisheetmusic_label.setText(_translate("Dialog", "Midi Sheet Music [.exe]"))
        self.configurePath_label.setText(_translate("Dialog", "Configure that path for each program."))
        self.anthemscore_label.setText(_translate("Dialog", "AnthemScore [.exe] (Optional)"))
        self.anthemscore_pushButton.setText(_translate("Dialog", "Browse"))

    def settings_path_read(self):

        for i in range(len(possible_app)):
            #app_exe_path[i] = setting_read(app_exe_setting_label[i], default_or_temp_mode)
            app_exe_path[i] = setting_read(app_exe_setting_label[i])

        return

    def update_paths(self):

        for i in range(len(possible_app)):
            lineEdit_attribute = getattr(self, possible_app[i] + '_lineEdit')
            lineEdit_attribute.setText(app_exe_path[i])

        return

    def apply_path(self):

        self.settings_path_read()

        for i in range(len(possible_app)):
            lineEdit_attribute = getattr(self, possible_app[i] + '_lineEdit')
            text = lineEdit_attribute.text()
            if(app_exe_path[i] != text):
                app_exe_path[i] = text
                setting_write(app_exe_setting_label[i], app_exe_path[i], 'append')

        return

################################################################################

"""
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUiDialog(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
"""
