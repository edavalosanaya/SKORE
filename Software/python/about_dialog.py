# General Utility
import sys

# PYQT5, GUI Library
from PyQt5 import QtCore, QtGui, QtWidgets

import globals

#-------------------------------------------------------------------------------
# Classes

class AboutDialog(QtWidgets.QDialog):

    """
    This class is the about dialog that informs the user about the SKORE
    application, including the license and personal message from the SKORE team.
    """

    def __init__(self):

        """
        This function setups up the size, title, and the widgets within
        the about dialog.
        """

        super(QtWidgets.QDialog, self).__init__()

        self.setWindowTitle("About SKORE")
        self.setWindowIcon(QtGui.QIcon('.\images\skore_icon.png'))
        self.resize(558 * globals.S_W_R, 576 * globals.S_H_R)

        self.setup_ui()

        return None

    def setup_ui(self):

        """
        This function setups up all the widgets within the about dialog.
        """

        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(10  * globals.S_W_R, 10  * globals.S_H_R, 541  * globals.S_W_R, 551  * globals.S_H_R))
        self.tabWidget.setObjectName("tabWidget")

        #-----------------------------------------------------------------------
        # tabWidget -> skore_tab

        self.skore_tab = QtWidgets.QWidget()
        self.skore_tab.setObjectName("skore_tab")

        self.logo_label = QtWidgets.QLabel(self.skore_tab)
        self.logo_label.setGeometry(QtCore.QRect(10  * globals.S_W_R, 20  * globals.S_H_R, 511  * globals.S_W_R, 151  * globals.S_H_R))
        self.logo_label.setObjectName("logo_label")

        self.logo_pixmap = QtGui.QPixmap('.\images\skore_icon.png').scaled(200  * globals.S_W_R, 200  * globals.S_H_R)
        self.logo_label.setPixmap(self.logo_pixmap)
        self.logo_label.setAlignment(QtCore.Qt.AlignCenter)

        self.textBrowser = QtWidgets.QTextBrowser(self.skore_tab)
        self.textBrowser.setGeometry(QtCore.QRect(10  * globals.S_W_R, 201  * globals.S_H_R, 511  * globals.S_W_R, 311  * globals.S_H_R))
        self.textBrowser.setObjectName("textBrowser")

        self.tabWidget.addTab(self.skore_tab, "")

        #-----------------------------------------------------------------------
        # tabWidget -> license_tab

        self.license_tab = QtWidgets.QWidget()
        self.license_tab.setObjectName("license_tab")

        self.license_plainTextEdit = QtWidgets.QPlainTextEdit(self.license_tab)
        self.license_plainTextEdit.setGeometry(QtCore.QRect(10  * globals.S_W_R, 10  * globals.S_H_R, 511  * globals.S_W_R, 501  * globals.S_H_R))
        self.license_plainTextEdit.setObjectName("license_plainTextEdit")

        self.tabWidget.addTab(self.license_tab, "")

        self.retranslate_ui()
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslate_ui(self):

        """
        This function places all the text content for the about dialog.
        """

        #-----------------------------------------------------------------------
        # Text Scaling

        font = self.tabWidget.font()

        font.setPixelSize(13)
        print("Prescaling Font Pixel Size: ", font.pixelSize())
        font.setPixelSize(font.pixelSize() * globals.S_W_R)
        print("Postscaling Font Pixel Size: ", font.pixelSize())

        text_group = [self.tabWidget, self.textBrowser, self.license_plainTextEdit,
                      self.skore_tab]

        for element in text_group:
            element.setFont(font)

        shift_value = 5 * globals.S_W_R

        #-----------------------------------------------------------------------
        # Text Content

        _translate = QtCore.QCoreApplication.translate

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.skore_tab), "SKORE")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.license_tab), "License")

        self.textBrowser.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:" + str(font.pixelSize() - shift_value) + "pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:" + str(font.pixelSize() - shift_value + 2) + "pt;\">SKORE 1.0</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:" + str(font.pixelSize() - shift_value) + "pt;\">Free software, YAY!</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:" + str(font.pixelSize() - shift_value) + "pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:" + str(font.pixelSize() - shift_value) + "pt;\">SKORE is an open-source project developed by a group of people inspired to make learning how to play the piano fun and easy. Without the support of our family and friends, this project would have remained as an idea. Thank you all for your kindness. </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:" + str(font.pixelSize() - shift_value) + "pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:" + str(font.pixelSize() - shift_value) + "pt;\">If you find any bugs or have recommendations for future versions, please let us know via email or GitHub. For help, our wiki in GitHub is a good place to start.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:" + str(font.pixelSize() - shift_value) + "pt;\"><br /></p></body></html>")

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
