# General Utility
import sys

# PYQT5, GUI Library
from PyQt5 import QtCore, QtGui, QtWidgets

#-------------------------------------------------------------------------------
# Classes

class AboutDialog(QtWidgets.QDialog):

    def __init__(self):

        super(QtWidgets.QDialog, self).__init__()

        self.setWindowTitle("About SKORE")
        self.setWindowIcon(QtGui.QIcon('.\images\skore_icon.png'))
        self.resize(558, 576)

        self.setup_ui()

        return None

    def setup_ui(self):

        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 541, 551))
        self.tabWidget.setObjectName("tabWidget")

        #-----------------------------------------------------------------------
        # tabWidget -> skore_tab

        self.skore_tab = QtWidgets.QWidget()
        self.skore_tab.setObjectName("skore_tab")

        self.logo_label = QtWidgets.QLabel(self.skore_tab)
        self.logo_label.setGeometry(QtCore.QRect(10, 20, 511, 151))
        self.logo_label.setObjectName("logo_label")

        self.logo_pixmap = QtGui.QPixmap('.\images\skore_icon.png').scaled(200,200)
        self.logo_label.setPixmap(self.logo_pixmap)
        self.logo_label.setAlignment(QtCore.Qt.AlignCenter)

        self.textBrowser = QtWidgets.QTextBrowser(self.skore_tab)
        self.textBrowser.setGeometry(QtCore.QRect(10, 201, 511, 311))
        self.textBrowser.setObjectName("textBrowser")

        self.tabWidget.addTab(self.skore_tab, "")

        #-----------------------------------------------------------------------
        # tabWidget -> license_tab

        self.license_tab = QtWidgets.QWidget()
        self.license_tab.setObjectName("license_tab")

        self.license_plainTextEdit = QtWidgets.QPlainTextEdit(self.license_tab)
        self.license_plainTextEdit.setGeometry(QtCore.QRect(10, 10, 511, 501))
        self.license_plainTextEdit.setObjectName("license_plainTextEdit")

        self.tabWidget.addTab(self.license_tab, "")

        self.retranslate_ui()
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.skore_tab), "SKORE")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.license_tab), "License")

        self.textBrowser.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">SKORE 1.0</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Free software, YAY!</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">SKORE is an open-source project developed by a group of people inspired to make learning how to play the piano fun and easy. Without the support of our family and friends, this project would have remained as an idea. Thank you all for your kindness. </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">If you find any bugs or have recommendations for future versions, please let us know via email or GitHub. For help, our wiki in GitHub is a good place to start.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p></body></html>")

        self.license_plainTextEdit.setPlainText("MIT License\n"
"\n"
"Copyright (c) 2019 Ashkan Aminian, Zachary Bosker, and Eduardo Davalos Anaya\n"
"\n"
"Permission is hereby granted, free of charge, to any person obtaining a copy\n"
"of this software and associated documentation files (the \"Software\"), to deal\n"
"in the Software without restriction, including without limitation the rights\n"
"to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
"copies of the Software, and to permit persons to whom the Software is\n"
"furnished to do so, subject to the following conditions:\n"
"\n"
"The above copyright notice and this permission notice shall be included in all\n"
"copies or substantial portions of the Software.\n"
"\n"
"THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
"IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
"FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
"AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
"LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
"OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
"SOFTWARE.")

        return None

#-------------------------------------------------------------------------------
# Main Code

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    about_dialog = AboutDialog()
    about_dialog.show()
    sys.exit(app.exec_())
