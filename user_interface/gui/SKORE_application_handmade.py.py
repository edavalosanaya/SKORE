import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QAction, QMainWindow, QInputDialog, QLineEdit, QFileDialog, QMessageBox, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

file_dialog_output = []

class SKORE_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'SKORE'
        self.left = 40
        self.top = 70
        self.width = 1100
        self.height = 600
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)


        #Main Menu
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        openButton = QAction('Open File', self)
        openButton.triggered.connect(self.openFileNameDialog_UserInput)
        fileMenu.addAction(openButton)

        settingsMenu = mainMenu.addMenu('Settings')
        configureExecPathButton = QAction('Configure program paths',self)
        configureExecPathButton.setStatusTip("Edit the executable paths of each program")
        configureExecPathButton.triggered.connect(self.callExecPathConfigurationWindow)
        settingsMenu.addAction(configureExecPathButton)


        self.show()

    def callExecPathConfigurationWindow(self):
        self.next = ExecPathConfigureWindow()

    def openFileNameDialog_AllFileTypes(self):
        global file_dialog_output
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Specifu Input File", "","All Files (*)", options=options)
        if fileName:
            file_dialog_output = fileName

    def openFileNameDialog_UserInput(self):
        global file_dialog_output
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Specifu Input File", "","MIDI files (*.mid);;MP3 Files (*.mp3);;PDF files (*.pdf)", options=options)
        if fileName:
            file_dialog_output = fileName

class ExecPathConfigureWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Program Path Configuration'
        self.left = 200
        self.top = 200
        self.width = 700
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #Creating instruction label
        text_instructions = 'Configure the executable paths for each program\n for the SKORE application to function.'
        self.instruction_label = QLabel(text_instructions, self)
        self.instruction_label.move(20,10)
        self.instruction_label.resize(400,40)

        #Creating textbox
        self.audiveris_textbox = QLineEdit(self)
        self.audiveris_textbox.move(20,70)
        self.audiveris_textbox.resize(280,30)

        self.audiveris_button = QPushButton('Show text', self)
        self.audiveris_button.move(320,70)

        self.audiveris_button.clicked.connect(self.on_click)


        self.show()

    def on_click(self):
        textboxValue = self.audiveris_textbox.text()
        QMessageBox.question(self, 'Message - SKORE App', 'You typed ' + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        self.audiveris_textbox.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SKORE_MainWindow()
    sys.exit(app.exec_())
