# General Utility Libraries
import time

# PyQt5, GUI Library
from PyQt5 import QtCore, QtGui, QtWidgets

# Serial and Midi Port Library
import mido

# SKORE Modules
import globals

#-------------------------------------------------------------------------------

class GraphicsRecorderText(QtWidgets.QGraphicsItem):

    """
    This class is the graphics item for the timer text of the SKORE recorder
    dialog.
    """

    def __init__(self, recorder_gui):

        """
        This function sets the location, size, font size, and additional
        variables to prepare the class.
        """

        super(QtWidgets.QGraphicsItem, self).__init__()

        self.width = 270 * globals.S_W_R
        self.height = 130 * globals.S_H_R
        self.x = 0
        self.y = 0

        self.recorder_gui = recorder_gui

        self.font = QtGui.QFont()
        self.font.setPixelSize(30 * globals.S_W_R)

        self.operation_mode = "in-active"
        self.flicker = 20
        self.sec_count = 0

        self.displayed_timer = QtCore.QTimer()
        self.displayed_timer.timeout.connect(self.increase_second_count)
        self.empty_midi = True

        return None

    def paint(self, painter, option, widget):

        """ This function draws the flickering timer text. """

        painter.setPen(QtCore.Qt.green)
        painter.setFont(self.font)

        if self.operation_mode == "in-active":
            painter.drawText(round(self.x - self.width), round(self.y - self.height), self.width, self.height, QtCore.Qt.AlignCenter, "Ready!")
        elif self.operation_mode == "waiting_for_first_event":

            if self.flicker > 0:
                painter.drawText(round(self.x - self.width), round(self.y - self.height), self.width, self.height, QtCore.Qt.AlignCenter, "-----")
                self.flicker -= 1
            elif self.flicker <= 0 and self.flicker > -20:
                self.flicker -= 1
            elif self.flicker <= -20:
                self.flicker = 20

        elif self.operation_mode == "timer":
            #print("seconds: ", self.sec_count)
            m, s = divmod(self.sec_count, 60)
            painter.drawText(round(self.x - self.width), round(self.y - self.height), self.width, self.height, QtCore.Qt.AlignCenter, "%02d:%02d" % (m, s))

        elif self.operation_mode == "complete":
            painter.drawText(round(self.x - self.width), round(self.y - self.height), self.width, self.height, QtCore.Qt.AlignCenter, "Complete")

        elif self.operation_mode == "complete-no-midi":
            painter.drawText(round(self.x - self.width), round(self.y - self.height), self.width, self.height, QtCore.Qt.AlignCenter, "Empty MIDI!")

        return None

    def set_timer(self):

        """ This function starts the timer. """

        self.empty_midi = False
        self.displayed_timer.start(1000)
        self.operation_mode = "timer"

        return None

    def stop_timer(self):

        """ This function stops the timer. """

        if self.empty_midi == True:
            self.operation_mode = "complete-no-midi"
        else:
            self.operation_mode = "complete"
        self.displayed_timer.stop()
        self.sec_count = 0

        return None

    def increase_second_count(self):

        """ This function increases the second count of the timer. """

        self.sec_count += 1

        return None

    def boundingRect(self):

        """ This is a necessary function that returns the bounding dimensions. """

        return QtCore.QRectF(self.x - self.width, self.y - self.height, self.width, self.height)

class HandlerToGraphicsController(QtCore.QObject):

    """
    This graphics controller is simply utlizes to implement a signal/slot
    attribute to the RecorderMidiHandler.
    """

    trigger_signal = QtCore.pyqtSignal()

    def __init__(self):

        """ Inheriting the QObject attributes. """

        super(QtCore.QObject, self).__init__()

        return None

class RecorderMidiHandler:

    """
    This class is the communication handler used to recorder the MIDI input into
    a MIDI file.
    """

    def __init__(self, skore_gui, tempo=120):

        """
        This function initializes the RecorderMidiHandler by connecting the
        handler to the SKORE application, connecting it to the
        HandlerToGraphicsController, and other important setting up.
        """

        self.gui = skore_gui
        self.tempo = tempo
        self.active = False

        self.graphics_controller = HandlerToGraphicsController()
        self.first_note = True

        return None

    def __call__(self, event, data=None):

        """
        This function is the callback from receiving information from the piano.
        """

        print("------------------------------------------------------------")

        if self.active is True:
            print("EVENT: ", event)
            message, deltatime = event

            if self.first_note is True:
                self.original_time = time.time()
                self.timer = 0
                self.graphics_controller.trigger_signal.emit()
                self.first_note = False

            else:
                deltatime = round(time.time() - self.original_time, 3)
                self.timer += deltatime
                self.original_time = time.time()

            if message[0] != 254:
                midi_time = int(round(mido.second2tick(self.timer, self.midi_file.ticks_per_beat, mido.bpm2tempo(self.tempo))))

                # To smoothen the recorder and make suppose-chord notes actual chords, I am going to the do the following
                if midi_time < globals.RECORD_CHORD_TOLERANCE:
                    midi_time = 0

                print("msg: {0}\tdeltatime: {1}\ttimer: {2}\tmidi_time: {3}".format(message, deltatime, self.timer, midi_time))

                if message[0] == 0x90 and message[2] != 0: # Turn ON
                    print("ON")
                    self.track.append(mido.Message('note_on', note = message[1], velocity = message[2], time = midi_time))
                    self.timer = 0
                elif message[0] == 176: # Control
                    print("CONTROL")
                    self.track.append(mido.Message('control_change', channel = 1, control = message[1], value = message[2], time = midi_time))
                #else:
                elif message[0] == 0x80 or message[2] == 0: # Turn OFF
                    print("OFF")
                    self.track.append(mido.Message('note_off', note = message[1], velocity = message[2], time = midi_time))
                    self.timer = 0

            print("Track: ", self.track)

        return None

    def start(self):

        """
        This begins the 'start' process of recording from the handler's
        perspective.
        """

        self.midi_file = mido.MidiFile(ticks_per_beat = 96)
        self.track = mido.MidiTrack()
        self.midi_file.tracks.append(self.track)
        self.timer = 0
        self.active = True
        self.first_note = True

        self.track.append(mido.MetaMessage('set_tempo'))

        print("Finished Start")

        return None

    def stop(self):

        """ This stops recording from the handler's perspective. """

        self.active = False
        self.track.append(mido.MetaMessage("end_of_track"))

        return None

    def save(self, save_file_location):

        """ This is helper function to save the generated midi file. """

        self.midi_file.save(save_file_location)

        return None

class RecorderDialog(QtWidgets.QDialog):

    """
    The RecorderDialog is the dialog that the user utlizes to record their own
    midi files.
    """

    def __init__(self, skore_gui, parent=None):

        """
        This function initlizes the RecorderDialog by connect it to the main
        SKORE GUI and sets up the main attributes of the dialog.
        """

        QtWidgets.QDialog.__init__(self, parent)
        self.setObjectName("SKORE Recorder")
        self.setWindowTitle("SKORE Recorder")
        self.setWindowIcon(QtGui.QIcon('.\images\skore_icon.png'))
        self.resize(373, 224)

        self.skore_gui = skore_gui

        self.setup_ui()
        self.setup_func()
        self.setup_graphics()

        print("Recorder Initializing")
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.recorder_clock)
        self.timer.start(globals.CLOCK_DELAY)

        return None

    def setup_ui(self):

        """
        This function setups up the widgets within the recorder dialog.
        """

        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 20, 311, 181))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setItemIndexMethod(-1)
        self.graphicsView = QtWidgets.QGraphicsView(self.scene, self.verticalLayoutWidget)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)

        #-----------------------------------------------------------------------
        # First horizontalLayout
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.toolButton_record = QtWidgets.QToolButton(self.verticalLayoutWidget)
        self.toolButton_record.setObjectName("toolButton_record")
        self.horizontalLayout.addWidget(self.toolButton_record)

        self.toolButton_play = QtWidgets.QToolButton(self.verticalLayoutWidget)
        self.toolButton_play.setObjectName("toolButton_play")
        self.horizontalLayout.addWidget(self.toolButton_play)

        self.toolButton_save = QtWidgets.QToolButton(self.verticalLayoutWidget)
        self.toolButton_save.setObjectName("toolButton_save")
        self.horizontalLayout.addWidget(self.toolButton_save)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)

        return None

    def setup_func(self):

        """
        This function setup the signal/slot of the widgets of the dialog.
        """

        self.toolButton_record.clicked.connect(self.start_record)
        self.toolButton_play.clicked.connect(self.play)
        self.toolButton_save.clicked.connect(self.save)

        self.toolButton_play.setEnabled(False)
        self.toolButton_save.setEnabled(False)

        return None

    def setup_graphics(self):

        """
        This function setups up the graphical elements of the record dialog.
        This includes the displayed text and ficklering timer text.
        """

        self.graphicsView.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.black))

        self.displayed_text = GraphicsRecorderText(self)
        self.scene.addItem(self.displayed_text)

        return None

    #---------------------------------------------------------------------------
    # Button Functions

    def start_record(self):

        """ This function starts the recording process. """

        print("Start Recording")
        self.toolButton_play.setEnabled(False)
        self.toolButton_save.setEnabled(False)

        self.toolButton_record.clicked.disconnect(self.start_record)
        self.toolButton_record.clicked.connect(self.stop_record)

        self.toolButton_record.setText("End Recording")

        self.skore_gui.recorder_handler.start()
        self.skore_gui.recorder_handler.graphics_controller.trigger_signal.connect(self.displayed_text.set_timer)
        self.displayed_text.operation_mode = "waiting_for_first_event"

        return None

    def stop_record(self):

        """ This function stops the recording process. """

        print("Stop Recording")
        self.skore_gui.recorder_handler.stop()

        self.toolButton_play.setEnabled(True)
        self.toolButton_save.setEnabled(True)

        self.toolButton_record.clicked.connect(self.start_record)
        self.toolButton_record.clicked.disconnect(self.stop_record)

        self.toolButton_record.setText("Record")
        self.skore_gui.recorder_handler.graphics_controller.trigger_signal.disconnect(self.displayed_text.set_timer)
        self.displayed_text.stop_timer()

        return None

    def play(self):

        """ This function plays the recording made by the user. """

        print("Play")
        print("Track: ", self.skore_gui.recorder_handler.track)

        for msg in self.skore_gui.recorder_handler.midi_file.play():
            print(msg.bytes())
            self.skore_gui.midi_out.send_message(msg.bytes()) # rtmidi Midi In Object

        return None

    def save(self):

        """
        This function saves the recorder file into the destination directory
        selected by the user.
        """

        save_file_location = self.open_filename_dialog_user_input("Save MIDI file", "MIDI files (*.mid)")

        if save_file_location == '':
            return None

        if save_file_location.endswith(".mid") is False:
            save_file_location += ".mid"

        print("SAVE FILE LOCATION: ", save_file_location)
        self.skore_gui.recorder_handler.save(save_file_location)

        return None

    #---------------------------------------------------------------------------
    # Misc Functions

    def recorder_clock(self):

        """ This function is performed by the clock to update the graphics. """

        self.scene.update()

        return None

    def retranslate_ui(self):

        """
        This function places all the text content into the widgets of the dialog.
        """

        _translate = QtCore.QCoreApplication.translate
        self.toolButton_record.setText(_translate("Dialog", "Rec"))
        self.toolButton_play.setText(_translate("Dialog", "Play"))
        self.toolButton_save.setText(_translate("Dialog", "Save"))

        return None

    #---------------------------------------------------------------------------
    # File Handling

    def open_filename_dialog_user_input(self, title, supported_files):

        """
        This file dialog is used to obtain the destination path of the midi file.
        """

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, title, "", supported_files, options=options)

        if fileName:
            file_dialog_output = str(fileName)
        else:
            return ""

        file_dialog_output = file_dialog_output.replace('/' , '\\' )
        return file_dialog_output

#-------------------------------------------------------------------------------
# Main Code

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    theme_list = QtWidgets.QStyleFactory.keys()
    app.setStyle(QtWidgets.QStyleFactory.create(theme_list[2])) #Fusion

    recorder = RecorderDialog()
    recorder.show()
    sys.exit(app.exec_())
