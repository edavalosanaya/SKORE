from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import mido
from mido import MidiFile, Message, MidiTrack, second2tick, bpm2tempo, MetaMessage

CLOCK_DELAY = 16

#-------------------------------------------------------------------------------

class GraphicsRecorderText(QGraphicsItem):

    def __init__(self, recorder_gui):
        super(GraphicsRecorderText, self).__init__()

        self.width = 270
        self.height = 130
        self.x = 0
        self.y = 0

        self.recorder_gui = recorder_gui

        self.font = QFont()
        self.font.setPixelSize(30)

        self.operation_mode = "in-active"
        self.flicker = 20
        self.sec_count = 0

        self.displayed_timer = QtCore.QTimer()
        self.displayed_timer.timeout.connect(self.increase_second_count)
        self.empty_midi = True

        return None

    def paint(self, painter, option, widget):

        painter.setPen(Qt.green)
        painter.setFont(self.font)
        #painter.drawRect(round(self.x - self.width), round(self.y - self.height), self.width, self.height)

        if self.operation_mode == "in-active":
            painter.drawText(round(self.x - self.width), round(self.y - self.height), self.width, self.height, Qt.AlignCenter, "Ready!")
        elif self.operation_mode == "waiting_for_first_event":

            if self.flicker > 0:
                painter.drawText(round(self.x - self.width), round(self.y - self.height), self.width, self.height, Qt.AlignCenter, "-----")
                self.flicker -= 1
            elif self.flicker <= 0 and self.flicker > -20:
                self.flicker -= 1
            elif self.flicker <= -20:
                self.flicker = 20

        elif self.operation_mode == "timer":
            print("seconds: ", self.sec_count)
            m, s = divmod(self.sec_count, 60)
            painter.drawText(round(self.x - self.width), round(self.y - self.height), self.width, self.height, Qt.AlignCenter, "%02d:%02d" % (m, s))

        elif self.operation_mode == "complete":
            painter.drawText(round(self.x - self.width), round(self.y - self.height), self.width, self.height, Qt.AlignCenter, "Complete")

        elif self.operation_mode == "complete-no-midi":
            painter.drawText(round(self.x - self.width), round(self.y - self.height), self.width, self.height, Qt.AlignCenter, "Empty MIDI!")

        return None

    def set_timer(self):
        self.empty_midi = False
        self.displayed_timer.start(1000)
        self.operation_mode = "timer"
        return None

    def stop_timer(self):
        if self.empty_midi == True:
            self.operation_mode = "complete-no-midi"
        else:
            self.operation_mode = "complete"
        self.displayed_timer.stop()
        self.sec_count = 0

        return None

    def increase_second_count(self):
        self.sec_count += 1
        return None

    def boundingRect(self):

        return QRectF(self.x - self.width, self.y - self.height, self.width, self.height)

class HandlerToGraphicsController(QObject):

    trigger_signal = QtCore.pyqtSignal()

    def __init__(self):
        super(HandlerToGraphicsController, self).__init__()

        return None

class RecorderMidiHandler(object):

    def __init__(self, skore_gui, tempo=120):
        self.gui = skore_gui
        self.tempo = tempo
        self.active = False

        self.graphics_controller = HandlerToGraphicsController()
        self.first_note = True

        return None

    def __call__(self, event, data=None):

        if self.active is True:
            message, deltatime = event
            self.timer += deltatime

            if message[0] != 254:
                midi_time = int(round(second2tick(self.timer, self.midi_file.ticks_per_beat, bpm2tempo(self.tempo))))
                print("msg: {0}\tdeltatime: {1}\ttimer: {2}".format(message, deltatime, self.timer))

                if message[0] == 0x90 and message[2] != 0: # Turn ON
                    print("ON")
                    self.track.append(Message('note_on', note = message[1], velocity = message[2], time = midi_time))
                    self.timer = 0
                elif message[0] == 176: # Control
                    print("CONTROL")
                    self.track.append(Message('control_change', channel = 1, control = message[1], value = message[2], time = midi_time))
                #else:
                elif message[0] == 0x80: # Turn OFF
                    print("OFF")
                    self.track.append(Message('note_off', note = message[1], velocity = message[2], time = midi_time))
                    self.timer = 0

            if self.first_note is True:
                self.graphics_controller.trigger_signal.emit()
                self.first_note = False

            print("Track: ", self.track)

        return None

    def start(self):
        self.midi_file = MidiFile(ticks_per_beat = 96)
        self.track = MidiTrack()
        self.midi_file.tracks.append(self.track)
        self.timer = 0
        self.active = True
        self.first_note = True

        self.track.append(MetaMessage('set_tempo'))

        # Smoothing the start of the recording
        #self.track.append(Message('note_off', note = 60, velocity = 0, time = int(round(second2tick(0.5, self.midi_file.ticks_per_beat, bpm2tempo(self.tempo))))))

        return None

    def stop(self):
        self.active = False

        # Smoothing the end of the recording
        #midi_time = int(round(second2tick(self.timer + 1, self.midi_file.ticks_per_beat, bpm2tempo(self.tempo))))
        #self.track.append(Message('note_off', note = 60, velocity = 0, time = midi_time))
        self.track.append(MetaMessage("end_of_track"))
        return None

    def save(self, save_file_location):

        self.midi_file.save(save_file_location)

        return None

class RecorderDialog(QtWidgets.QDialog):

    def __init__(self, skore_gui, parent=None):

        QtWidgets.QDialog.__init__(self, parent)
        self.setObjectName("SKORE Recorder")
        self.setWindowTitle("SKORE Recorder")
        self.resize(373, 224)

        self.skore_gui = skore_gui

        self.setup_ui()
        self.setup_func()
        self.setup_graphics()

        print("Recorder Initializing")
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.recorder_clock)
        self.timer.start(CLOCK_DELAY)

        return None

    def setup_ui(self):

        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 20, 311, 181))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.scene = QGraphicsScene()
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

        #self.toolButton_stop = QtWidgets.QToolButton(self.verticalLayoutWidget)
        #self.toolButton_stop.setObjectName("toolButton_stop")
        #self.horizontalLayout.addWidget(self.toolButton_stop)

        self.toolButton_play = QtWidgets.QToolButton(self.verticalLayoutWidget)
        self.toolButton_play.setObjectName("toolButton_play")
        self.horizontalLayout.addWidget(self.toolButton_play)

        self.toolButton_save = QtWidgets.QToolButton(self.verticalLayoutWidget)
        self.toolButton_save.setObjectName("toolButton_save")
        self.horizontalLayout.addWidget(self.toolButton_save)

        self.verticalLayout.addLayout(self.horizontalLayout)

        #-----------------------------------------------------------------------
        # Second horizontalLayout

        #self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        #self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        #self.toolButton_play = QtWidgets.QToolButton(self.verticalLayoutWidget)
        #self.toolButton_play.setObjectName("toolButton_play")
        #self.horizontalLayout_2.addWidget(self.toolButton_play)

        #self.toolButton_save = QtWidgets.QToolButton(self.verticalLayoutWidget)
        #self.toolButton_save.setObjectName("toolButton_save")
        #self.horizontalLayout_2.addWidget(self.toolButton_save)

        #self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)

    def setup_func(self):

        self.toolButton_record.clicked.connect(self.start_record)
        self.toolButton_play.clicked.connect(self.play)
        self.toolButton_save.clicked.connect(self.save)

        self.toolButton_play.setEnabled(False)
        self.toolButton_save.setEnabled(False)

        return None

    def setup_graphics(self):

        self.graphicsView.setBackgroundBrush(QBrush(Qt.black))

        self.displayed_text = GraphicsRecorderText(self)
        self.scene.addItem(self.displayed_text)
        # Troubleshooting
        #self.displayed_text.set_timer()

        return None

    #---------------------------------------------------------------------------
    # Button Functions

    def start_record(self):

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

        print("Stop Recording")
        self.skore_gui.recorder_handler.stop()

        self.toolButton_play.setEnabled(True)
        self.toolButton_save.setEnabled(True)

        self.toolButton_record.clicked.connect(self.start_record)
        self.toolButton_record.clicked.disconnect(self.stop_record)

        self.toolButton_record.setText("Record")
        self.skore_gui.recorder_handler.graphics_controller.trigger_signal.disconnect(self.displayed_text.set_timer)
        self.displayed_text.stop_timer()

    def play(self):

        print("Play")
        for msg in self.skore_gui.recorder_handler.midi_file.play():
            print(msg.bytes())
            self.skore_gui.midi_out.send_message(msg.bytes()) # rtmidi Midi In Object

        return None

    def save(self):

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
        self.scene.update()

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.toolButton_record.setText(_translate("Dialog", "Rec"))
        self.toolButton_play.setText(_translate("Dialog", "Play"))
        self.toolButton_save.setText(_translate("Dialog", "Save"))

    #---------------------------------------------------------------------------
    # File Handling

    def open_filename_dialog_user_input(self, title, supported_files):
        # This file dialog is used to obtain the file location of the .mid, .mp3,
        # and .pdf file.


        #fileName, _ = QFileDialog.getOpenFileName(caption = "Select Audio File", filter = "All Supported Files (*.mid *.mp3 *.pdf);;All Files (*.*);;MIDI Files(*.mid);;MP3 Files(*.mp3);;PDF Files (*.pdf)")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, title, "", supported_files, options=options)

        if fileName:
            file_dialog_output = str(fileName)
        else:
            return ""

        file_dialog_output = file_dialog_output.replace('/' , '\\' )
        return file_dialog_output

#-------------------------------------------------------------------------------
# Main Code

"""
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    theme_list = QStyleFactory.keys()
    app.setStyle(QStyleFactory.create(theme_list[2])) #Fusion

    recorder = RecorderDialog()
    recorder.show()
    sys.exit(app.exec_())
"""
