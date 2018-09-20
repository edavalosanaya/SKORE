import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QAction, QMainWindow, QInputDialog, QLineEdit, QFileDialog, QMessageBox, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

#Determining where SKORE application is located

complete_path = os.path.dirname(os.path.abspath(__file__))
skore_index = complete_path.find('SKORE') + len('SKORE')
skore_path = complete_path[0:skore_index+1]

#Importing SKORE functions and additional windows
skore_program_controller_extension = r'\user_interface\app_control'
sys.path.append(skore_path + skore_program_controller_extension)
#from skore_program_controller import *


file_dialog_output = []

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(916, 579)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #upload button
        self.uploadAudioFile_toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.uploadAudioFile_toolButton.setGeometry(QtCore.QRect(20, 20, 421, 171))
        self.uploadAudioFile_toolButton.setObjectName("uploadAudioFile_toolButton")
        self.uploadAudioFile_toolButton.clicked.connect(self.openFileNameDialog_UserInput)

        #record button
        self.record_toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.record_toolButton.setGeometry(QtCore.QRect(470, 20, 421, 171))
        self.record_toolButton.setObjectName("record_toolButton")

        #settings button
        self.settings_toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.settings_toolButton.setGeometry(QtCore.QRect(20, 260, 871, 41))
        self.settings_toolButton.setObjectName("settings_toolButton")

        #Tutoring Group
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

        #Expert Buttton
        self.expert_pushButton = QtWidgets.QPushButton(self.tutor_groupBox)
        self.expert_pushButton.setGeometry(QtCore.QRect(20, 140, 381, 51))
        self.expert_pushButton.setObjectName("expert_pushButton")

        #Generate Musich Sheet
        self.generateMusicSheet_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.generateMusicSheet_pushButton.setGeometry(QtCore.QRect(470, 330, 421, 171))
        self.generateMusicSheet_pushButton.setObjectName("generateMusicSheet_pushButton")

        #TextBrowser
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 200, 871, 51))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)

        #menubar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 916, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        #StatusBar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MaiWindown", "SKORE"))
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
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Uploaded File: " + str(file_dialog_output) + " </p></body></html>"))
        return

    def openFileNameDialog_UserInput(self):
        global file_dialog_output
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(caption = "Select Audio File",filter = "MIDI files (*.mid);;MP3 Files (*.mp3);;PDF files (*.pdf)")

        if fileName:
            file_dialog_output = str(fileName)
            print(file_dialog_output)

        self.retranslateUi(MainWindow)
        return

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
