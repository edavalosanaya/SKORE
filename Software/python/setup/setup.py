# General Utility Libraries
import sys
import time
import os
from shutil import copyfile
import zipfile

# File, Folder, and Directory Manipulation Library
import ntpath
import pathlib

# PyQt5, GUI LIbrary
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

#-------------------------------------------------------------------------------
# Class Definitions

class SetupSkore(QtWidgets.QMainWindow):
    # This class is the main GUI for the installation. It helps visualize and provides
    # the user with the installation process of the applications required to run
    # SKORE

    def __init__(self):

        complete_path = os.path.dirname(os.path.abspath(__file__))
        if complete_path == '' or complete_path.find('SKORE') == -1:
                complete_path = os.path.dirname(sys.argv[0])

        self.setup_files_path = complete_path + r'\app_setup_files'

        super(QtWidgets.QMainWindow, self).__init__()
        self.setupUi()

    def setupUi(self):

        self.setWindowTitle('SKORE Accompanying-Application Installation Wizard')
        self.setObjectName("MainWindow")
        self.resize(637, 600)

        # Initializing central widget
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        # Icon and Instructions TextBrowsers
        self.icon_textBrower = QtWidgets.QTextBrowser(self.centralwidget)
        self.icon_textBrower.setGeometry(QtCore.QRect(30, 10, 571, 151))
        self.icon_textBrower.setObjectName("icon_textBrower")
        self.instructions_textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.instructions_textBrowser.setGeometry(QtCore.QRect(30, 170, 571, 91))
        self.instructions_textBrowser.setObjectName("instructions_textBrowser")

        #-----------------------------------------------------------------------
        # Major Grid Layout

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 270, 571, 231))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        # Amazing Midi
        self.amazingmidi_checkBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.amazingmidi_checkBox.setText("")
        self.amazingmidi_checkBox.setObjectName("amazing_midi_checkBox")
        self.gridLayout.addWidget(self.amazingmidi_checkBox, 2, 1, 1, 1, QtCore.Qt.AlignHCenter)

        self.amazingmidi_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.amazingmidi_label.setObjectName("amazingmidi_label")
        self.gridLayout.addWidget(self.amazingmidi_label, 2, 3, 1, 1)

        self.amazingmidi_completed_checkBox = ReadOnlyCheckBox(self.gridLayoutWidget)
        self.amazingmidi_completed_checkBox.setObjectName("amazingmidi_completed_checkBox")
        self.gridLayout.addWidget(self.amazingmidi_completed_checkBox, 2, 5, 1, 1, QtCore.Qt.AlignHCenter)

        # LoopBe
        self.loopbe1_checkBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.loopbe1_checkBox.setText("")
        self.loopbe1_checkBox.setObjectName("loopbe1_checkBox")
        self.gridLayout.addWidget(self.loopbe1_checkBox, 4, 1, 1, 1, QtCore.Qt.AlignHCenter)

        self.loopbe1_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.loopbe1_label.setObjectName("loopbe1_label")
        self.gridLayout.addWidget(self.loopbe1_label, 4, 3, 1, 1)

        self.loopbe1_completed_checkBox = ReadOnlyCheckBox(self.gridLayoutWidget)
        self.loopbe1_completed_checkBox.setObjectName("loopbe1_completed_checkBox")
        self.gridLayout.addWidget(self.loopbe1_completed_checkBox, 4, 5, 1, 1, QtCore.Qt.AlignHCenter)

        # MuseScore 2
        self.muse_score_checkBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.muse_score_checkBox.setText("")
        self.muse_score_checkBox.setObjectName("muse_score_checkBox")
        self.gridLayout.addWidget(self.muse_score_checkBox, 5, 1, 1, 1, QtCore.Qt.AlignHCenter)

        self.muse_score_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.muse_score_label.setObjectName("muse_score_label")
        self.gridLayout.addWidget(self.muse_score_label, 5, 3, 1, 1)

        self.muse_score_completed_checkBox = ReadOnlyCheckBox(self.gridLayoutWidget)
        self.muse_score_completed_checkBox.setObjectName("muse_score_completed_checkBox")
        self.gridLayout.addWidget(self.muse_score_completed_checkBox, 5, 5, 1, 1, QtCore.Qt.AlignHCenter)

        # PianoBooster
        self.pianobooster_checkBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.pianobooster_checkBox.setText("")
        self.pianobooster_checkBox.setObjectName("pianobooster_checkBox")
        self.gridLayout.addWidget(self.pianobooster_checkBox, 6, 1, 1, 1, QtCore.Qt.AlignHCenter)

        self.pianobooster_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.pianobooster_label.setObjectName("pianobooster_label")
        self.gridLayout.addWidget(self.pianobooster_label, 6, 3, 1, 1)

        self.pianobooster_completed_checkBox = ReadOnlyCheckBox(self.gridLayoutWidget)
        self.pianobooster_completed_checkBox.setObjectName("pianobooster_completed_checkBox")
        self.gridLayout.addWidget(self.pianobooster_completed_checkBox, 6, 5, 1, 1, QtCore.Qt.AlignHCenter)

        # Red Dot Forever
        self.red_dot_forever_checkBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.red_dot_forever_checkBox.setText("")
        self.red_dot_forever_checkBox.setObjectName("red_dot_forever_checkBox")
        self.gridLayout.addWidget(self.red_dot_forever_checkBox, 7, 1, 1, 1, QtCore.Qt.AlignHCenter)

        self.red_dot_forever_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.red_dot_forever_label.setObjectName("red_dot_forever_label")
        self.gridLayout.addWidget(self.red_dot_forever_label, 7, 3, 1, 1)

        self.red_dot_forever_completed_checkBox = ReadOnlyCheckBox(self.gridLayoutWidget)
        self.red_dot_forever_completed_checkBox.setObjectName("red_dot_forever_completed_checkBox")
        self.gridLayout.addWidget(self.red_dot_forever_completed_checkBox, 7, 5, 1, 1, QtCore.Qt.AlignHCenter)

        # Spacer Items
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 5, 6, 1, 1)

        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 5, 4, 1, 1)

        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 5, 2, 1, 1)

        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 0, 3, 1, 1)

        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 9, 3, 1, 1)

        # Misc Items
        self.to_be_installed_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.to_be_installed_label.setObjectName("to_be_installed_label")
        self.gridLayout.addWidget(self.to_be_installed_label, 1, 1, 1, 1)

        self.application_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.application_label.setObjectName("application_label")
        self.gridLayout.addWidget(self.application_label, 1, 3, 1, 1)

        self.installation_complete_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.installation_complete_label.setObjectName("installation_complete_label")
        self.gridLayout.addWidget(self.installation_complete_label, 1, 5, 1, 1)

        self.checkboxlist = [self.amazingmidi_checkBox, self.loopbe1_checkBox,
                             self.muse_score_checkBox, self.pianobooster_checkBox,
                             self.red_dot_forever_checkBox]

        #-----------------------------------------------------------------------
        # Installation and Closure QPushButtons
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(350, 520, 251, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.install_pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.install_pushButton.setObjectName("install_pushButton")
        self.horizontalLayout.addWidget(self.install_pushButton)
        self.close_pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.close_pushButton.setObjectName("close_pushButton")
        self.horizontalLayout.addWidget(self.close_pushButton)

        self.close_pushButton.clicked.connect(self.close)
        self.install_pushButton.clicked.connect(self.install_applications)

        # Final Touches with Menubar and actionContents
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 637, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.actionContents = QtWidgets.QAction(self)
        self.actionContents.setObjectName("actionContents")
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        # Creating Initial State
        self.amazingmidi_checkBox.setChecked(True)
        self.loopbe1_checkBox.setChecked(True)
        self.muse_score_checkBox.setChecked(True)
        self.pianobooster_checkBox.setChecked(True)
        self.red_dot_forever_checkBox.setChecked(True)

        self.show()

    def install_applications(self):
        # This function determines which applications the user requested to install
        # and starts the installation for such applications.

        list_of_applications_to_install = []

        for checkbox in self.checkboxlist:
            if checkbox.isChecked():
                list_of_applications_to_install.append(checkbox.objectName())

        if 'amazing_midi_checkBox' in list_of_applications_to_install:
            print("Install AmazingMidi")
            os.system(r"cd " + self.setup_files_path + "&& azmid170.exe")
            self.amazingmidi_completed_checkBox.setChecked(True)

        if 'loopbe1_checkBox' in list_of_applications_to_install:
            print("Installing LoopBe1")
            os.system(r"cd " + self.setup_files_path  + "&& setuploopbe1.exe")
            self.loopbe1_completed_checkBox.setChecked(True)

        if 'muse_score_checkBox' in list_of_applications_to_install:
            print("Installing Muse Score 2")
            os.system(r"cd " + self.setup_files_path  + "&& MuseScore-3.0.0.msi")
            self.muse_score_completed_checkBox.setChecked(True)

        if 'pianobooster_checkBox' in list_of_applications_to_install:
            print("Installing PianoBooster")
            os.system(r"cd " + self.setup_files_path  + "&& PianoBoosterInstall-0-6-4.exe")
            self.pianobooster_completed_checkBox.setChecked(True)

        if 'red_dot_forever_checkBox' in list_of_applications_to_install:
            print("Installing Red Dot Forever")
            os.system(r"cd " + self.setup_files_path  + "&& reddot-1_04.exe")
            self.red_dot_forever_completed_checkBox.setChecked(True)

        return None

    def openDirectoryDialog_UserInput(self):
        # This file dialog is used to obtain the folder directory of the desired
        # save location for the generated files

        options = QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, caption = 'Open a folder', directory = None, options = options)

        if directory:
            file_dialog_output = str(directory)
        else:
            return ""

        file_dialog_output = file_dialog_output.replace('/' , '\\' )
        return file_dialog_output

    def output_address(self, input_address, final_address, end_file_extension):
        # This function obtains the input_address of a file, and uses the final address
        # to create the address of the output of the file conversion, including extension

        file = ntpath.basename(input_address)
        filename = file.split(".")[0]

        exist_path = pathlib.Path(input_address)
        file_path = exist_path.parent

        #input_address_new_extension = str(file_path) + '\\' + filename + end_file_extension
        end_address = final_address + '\\' + filename + end_file_extension
        return end_address, filename

    def retranslateUi(self):
        # This function changes all the text in the application

        _translate = QtCore.QCoreApplication.translate
        self.amazingmidi_label.setText(_translate("MainWindow", "AmazingMidi v1.70"))
        self.amazingmidi_completed_checkBox.setText(_translate("MainWindow", "Completed"))

        self.loopbe1_completed_checkBox.setText(_translate("MainWindow", "Completed"))
        self.loopbe1_label.setText(_translate("MainWindow", "LoopBe1 v1.6"))

        self.muse_score_completed_checkBox.setText(_translate("MainWindow", "Completed"))
        self.muse_score_label.setText(_translate("MainWindow", "Muse Score 2 v2.3.2"))

        self.pianobooster_completed_checkBox.setText(_translate("MainWindow", "Completed"))
        self.pianobooster_label.setText(_translate("MainWindow", "PianoBooster v0.6.4"))

        self.red_dot_forever_completed_checkBox.setText(_translate("MainWindow", "Completed"))
        self.red_dot_forever_label.setText(_translate("MainWindow", "Red Dot Forever v1.04"))

        self.to_be_installed_label.setText(_translate("MainWindow", "To Be Installed"))
        self.application_label.setText(_translate("MainWindow", "Application"))
        self.installation_complete_label.setText(_translate("MainWindow", "Installation Completed"))
        self.icon_textBrower.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\"icon.png\" /></p></body></html>"))
        self.instructions_textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This installing wizard can assist you in the installation of the listed applications below. To complete the SKORE installation, please install Audiveris and (optional) AnthemScore. Their installations require more steps, specific computer requirements, and changes of enviornmental variables in your PC. Instructions on their installations can be found in their websites, respetively.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.install_pushButton.setText(_translate("MainWindow", "Install"))
        self.close_pushButton.setText(_translate("MainWindow", "Close"))
        self.actionContents.setText(_translate("MainWindow", "Contents"))


class ReadOnlyCheckBox(QtWidgets.QCheckBox):
    # This class was created to make a read-only checkbox. In principle, it just
    # accepts, or neglects any mouse press, mouse release, or keyboard press events.

    def __init__(self, *args):
        super(ReadOnlyCheckBox, self).__init__(*args)
        self._readOnly = True

    def isReadOnly(self):
        return self._readOnly

    def mousePressEvent(self, event):
        if (self.isReadOnly() ):
            event.accept()
        else:
            super(ReadOnlyCheckBox, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (self.isReadOnly() ):
            event.accept()
        else:
            super(ReadOnlyCheckBox, self).mouseMoveEvent(event)

    def mouseReleaseEvent( self, event):
        if ( self.isReadOnly() ):
            event.accept()
        else:
            super(ReadOnlyCheckBox, self).mouseReleaseEvent(event)

    # handle event in which the widget has focus and the spacebar is pressed
    def keyPressedEvent(self, event ):
        if ( self.isReadOnly() ):
            event.accept()
        else:
            super(ReadOnlyCheckBox, self).keyPressEvent(event)

    @QtCore.pyqtSlot(bool)
    def setReadOnly(self, state):
        self._readOnly = state

    readOnly = QtCore.pyqtProperty(bool, isReadOnly, setReadOnly)

#-------------------------------------------------------------------------------
# Main Code

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    setup = SetupSkore()
    sys.exit(app.exec_())
