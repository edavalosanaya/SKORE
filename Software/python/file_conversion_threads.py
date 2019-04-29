# PyQt5, GUI Library
from PyQt5 import QtCore, QtGui, QtWidgets

#-------------------------------------------------------------------------------
# Classes

class FileConverter(QtCore.QThread):

    """
    This thread handles the file conversion process, this allows the loading
    animation dialog to animate. Without the implemetation of the thread, the
    graphics in the loading animation dialog could not be updated, rendering
    completely useless.
    """

    def __init__(self, gui, output_file_type):

        """ This function initializes the thread and sets essential arguments. """

        QtCore.QThread.__init__(self)
        self.gui = gui
        self.output_file_type = output_file_type

        return None

    def run(self):

        """
        This function runs when the thread is started by the GUI. This function
        simply handles the file conversion.
        """

        if self.output_file_type == '.mid':
            print("MIDI File Conversion")
            self.gui.file_container.input_to_mid()
        elif self.output_file_type == '.pdf':
            print("PDF File Conversion")
            self.gui.file_container.input_to_pdf()

        return None
