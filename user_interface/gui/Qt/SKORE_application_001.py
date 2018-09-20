# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SKORE_application.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys

#Determining where SKORE application is located
complete_path = os.path.dirname(os.path.abspath(__file__))
skore_index = complete_path.find('SKORE') + len('SKORE')
skore_path = complete_path[0:skore_index+1]

#Importing SKORE functions and additional windows
skore_program_controller_extension = r'\user_interface\app_control'
sys.path.append(skore_path + skore_program_controller_extension)
from skore_program_controller import *
from configuration_path import *

file_dialog_output = []

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(961, 590)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setAutoFillBackground(False)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #Tab Code
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 941, 531))
        self.tabWidget.setObjectName("tabWidget")
        self.home_tab = QtWidgets.QWidget()

        #Home Tab Code
        self.home_tab.setObjectName("home_tab")
        self.instructions_textBrowser = QtWidgets.QTextBrowser(self.home_tab)
        self.instructions_textBrowser.setGeometry(QtCore.QRect(20, 280, 891, 171))
        self.instructions_textBrowser.setObjectName("instructions_textBrowser")
        self.image_textBrowser = QtWidgets.QTextBrowser(self.home_tab)
        self.image_textBrowser.setGeometry(QtCore.QRect(350, 11, 256, 251))
        self.image_textBrowser.setObjectName("image_textBrowser")
        self.tabWidget.addTab(self.home_tab, "")

        #Operation Tab Code
        self.operation_tab = QtWidgets.QWidget()
        self.operation_tab.setObjectName("operation_tab")
        self.fileTypeImage_textEdit = QtWidgets.QTextEdit(self.operation_tab)
        self.fileTypeImage_textEdit.setGeometry(QtCore.QRect(330, 10, 291, 121))
        self.fileTypeImage_textEdit.setObjectName("fileTypeImage_textEdit")
        self.CurretFile_label = QtWidgets.QLabel(self.operation_tab)
        self.CurretFile_label.setGeometry(QtCore.QRect(380, 150, 191, 20))
        self.CurretFile_label.setObjectName("CurretFile_label")
        self.WhatToDo_label = QtWidgets.QLabel(self.operation_tab)
        self.WhatToDo_label.setGeometry(QtCore.QRect(390, 200, 161, 20))
        self.WhatToDo_label.setObjectName("WhatToDo_label")
        self.tutoring_groupBox = QtWidgets.QGroupBox(self.operation_tab)
        self.tutoring_groupBox.setGeometry(QtCore.QRect(330, 240, 291, 241))
        self.tutoring_groupBox.setObjectName("tutoring_groupBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.tutoring_groupBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 30, 271, 191))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.beginner_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.beginner_label.setObjectName("beginner_label")
        self.verticalLayout.addWidget(self.beginner_label)

        #Beginner PushButton
        self.beginner_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.beginner_pushButton.setObjectName("beginner_pushButton")


        self.verticalLayout.addWidget(self.beginner_pushButton)
        self.intermediate_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.intermediate_label.setObjectName("intermediate_label")
        self.verticalLayout.addWidget(self.intermediate_label)

        #Intermediate PushButton
        self.intermediate_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.intermediate_pushButton.setObjectName("intermediate_pushButton")

        self.verticalLayout.addWidget(self.intermediate_pushButton)
        self.expert_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.expert_label.setObjectName("expert_label")
        self.verticalLayout.addWidget(self.expert_label)

        #Expert Push Button
        self.expert_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.expert_pushButton.setObjectName("expert_pushButton")

        self.verticalLayout.addWidget(self.expert_pushButton)
        self.musicgeneration_groupBox = QtWidgets.QGroupBox(self.operation_tab)
        self.musicgeneration_groupBox.setGeometry(QtCore.QRect(10, 240, 291, 241))
        self.musicgeneration_groupBox.setObjectName("musicgeneration_groupBox")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.musicgeneration_groupBox)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 30, 271, 191))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.amazingmidi_using_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.amazingmidi_using_label.setObjectName("amazingmidi_using_label")
        self.verticalLayout_2.addWidget(self.amazingmidi_using_label)

        #AmazingMIDI music sheet generation
        self.amazingmidi_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.amazingmidi_pushButton.setObjectName("amazingmidi_pushButton")

        self.verticalLayout_2.addWidget(self.amazingmidi_pushButton)
        self.anthemscore_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.anthemscore_label.setObjectName("anthemscore_label")
        self.verticalLayout_2.addWidget(self.anthemscore_label)

        #AnthemScore music sheet generation
        self.antehmscore_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.antehmscore_pushButton.setObjectName("antehmscore_pushButton")
        self.verticalLayout_2.addWidget(self.antehmscore_pushButton)
        self.record_groupBox = QtWidgets.QGroupBox(self.operation_tab)
        self.record_groupBox.setGeometry(QtCore.QRect(640, 240, 271, 241))
        self.record_groupBox.setObjectName("record_groupBox")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.record_groupBox)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(10, 30, 251, 191))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.recordonly_label = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.recordonly_label.setObjectName("recordonly_label")
        self.verticalLayout_4.addWidget(self.recordonly_label)

        #Record Only Button
        self.recordonly_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.recordonly_pushButton.setObjectName("recordonly_pushButton")

        self.verticalLayout_4.addWidget(self.recordonly_pushButton)
        self.record_and_generate_label = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.record_and_generate_label.setObjectName("record_and_generate_label")
        self.verticalLayout_4.addWidget(self.record_and_generate_label)

        #Record and Generate Button
        self.record_and_generate_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.record_and_generate_pushButton.setObjectName("record_and_generate_pushButton")

        self.verticalLayout_4.addWidget(self.record_and_generate_pushButton)
        self.tutoring_groupBox.raise_()
        self.fileTypeImage_textEdit.raise_()
        self.CurretFile_label.raise_()
        self.WhatToDo_label.raise_()
        self.musicgeneration_groupBox.raise_()
        self.record_groupBox.raise_()
        self.tabWidget.addTab(self.operation_tab, "")
        MainWindow.setCentralWidget(self.centralwidget)

        #Menu Bar Code
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 961, 26))
        self.menubar.setObjectName("menubar")

        #File Menu
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        #Settings Menu
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")

        #Help Menu
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")

        #Edit Menu
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")

        #View Menu
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")

        #End of Menu Bar
        MainWindow.setMenuBar(self.menubar)

        #Status Bar Code
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        #Action Code
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setCheckable(False)
        self.actionOpen.setObjectName("actionOpen")

        self.actionConfigureProgramPaths = QtWidgets.QAction(MainWindow)
        self.actionConfigureProgramPaths.setObjectName("actionConfigureProgramPaths")
        self.actionConfigureProgramPaths.triggered.connect(self.callExecPathConfigurationWindow)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")

        #Adding Action to the individual menus
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExit)
        self.menuSettings.addAction(self.actionConfigureProgramPaths)

        #Adding the menus to the menubar
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def openFileNameDialog_AllFileTypes(self):
        #This searches any file type
        global file_dialog_output
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Specify File", "","All Files (*)", options=options)
        if fileName:
            file_dialog_output = fileName

    def openFileNameDialog_UserInput(self):
        #This searches for only .mid, .mp3, and .pdf file types
        global file_dialog_output
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Specify Input File", "","MIDI files (*.mid);;MP3 Files (*.mp3);;PDF files (*.pdf)", options=options)
        if fileName:
            file_dialog_output = fileName

    def callExecPathConfigurationWindow(self):
        #self.nd = Ui_PathConfiguration()
        #elf.nd.show()

        self.next = Ui_PathConfiguration()
        #app2 = QtWidgets.QApplication(sys.argv)
        MainWindow2 = QtWidgets.QMainWindow()
        ui2 = Ui_PathConfiguration()
        ui2.setupUi(MainWindow2)
        MainWindow2.show()
        #app2.exec_()

    def retranslateUi(self, MainWindow):
        #Here are all the text boxes and label
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SKORE"))
        self.instructions_textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">Welcome to SKORE</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">To start, please open an .mp3, .pdf, or .mid file with the &quot;file&quot; menu button. Once opened, go to the Operation tab. </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">For help, click on the &quot;help&quot; menu button.</span></p></body></html>"))
        self.image_textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/newPrefix/music_note.jpg\" /></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.home_tab), _translate("MainWindow", "Home Tab"))
        self.fileTypeImage_textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Image of file type<img src=\":/newPrefix/MP3_icon.png\" /></p></body></html>"))
        self.CurretFile_label.setText(_translate("MainWindow", "Current File Uploaded: {variable}"))
        self.WhatToDo_label.setText(_translate("MainWindow", "What would you like to do?"))
        self.tutoring_groupBox.setTitle(_translate("MainWindow", "Tutoring"))
        self.beginner_label.setText(_translate("MainWindow", "Note indication and wait until user plays note."))
        self.beginner_pushButton.setText(_translate("MainWindow", "Beginner"))
        self.intermediate_label.setText(_translate("MainWindow", "Note indication and play along with piano."))
        self.intermediate_pushButton.setText(_translate("MainWindow", "Intermediate"))
        self.expert_label.setText(_translate("MainWindow", "Only note correction. "))
        self.expert_pushButton.setText(_translate("MainWindow", "Expert"))
        self.musicgeneration_groupBox.setTitle(_translate("MainWindow", "Music Sheet Generation"))
        self.amazingmidi_using_label.setText(_translate("MainWindow", "Utilizing AmazingMIDI (Free, lower quality)"))
        self.amazingmidi_pushButton.setText(_translate("MainWindow", "Generate with AmazingMIDI"))
        self.anthemscore_label.setText(_translate("MainWindow", "Utilizing AnthemScore (Higher quality, costly)"))
        self.antehmscore_pushButton.setText(_translate("MainWindow", "Generate with AnthemScore"))
        self.record_groupBox.setTitle(_translate("MainWindow", "Record"))
        self.recordonly_label.setText(_translate("MainWindow", "Only record (to .mid) from my piano."))
        self.recordonly_pushButton.setText(_translate("MainWindow", "Record Only"))
        self.record_and_generate_label.setText(_translate("MainWindow", "Record and generate music sheet."))
        self.record_and_generate_pushButton.setText(_translate("MainWindow", "Record and Generate"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.operation_tab), _translate("MainWindow", "Operation Tab"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionConfigureProgramPaths.setText(_translate("MainWindow", "Configure Program Paths"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))

#import images_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
