# General Utility Libraries
import time
import sys
import os

# PyQt5, GUI Library
from PyQt5 import QtCore, QtGui, QtWidgets

# SKORE Modules
import globals

#-------------------------------------------------------------------------------
# Classes

class GraphicsSystemMessage(QtWidgets.QGraphicsItem):

    def __init__(self):

        super(QtWidgets.QGraphicsItem, self).__init__()

        self.width = 400
        self.height = 50
        self.x = -900
        self.y = -500

        self.font = QtGui.QFont()
        self.font.setPixelSize(25)

        self.text = ""

        return None

    def set_text(self, text):

        self.text = text

        return None

    def paint(self, painter, option, widget):

        painter.setPen(QtCore.Qt.green)
        painter.setFont(self.font)
        painter.drawText(self.x, self.y, self.width, self.height, QtCore.Qt.AlignLeft, self.text)

        return None

    def boundingRect(self):

        return QtCore.QRectF(self.x + self.width, self.y, self.width, self.height)

class GraphicsPlayedLabel(QtWidgets.QGraphicsItem):

    def __init__(self, note, correct = None):

        super(QtWidgets.QGraphicsItem, self).__init__()

        self.x = -510
        self.width = 20
        self.height = 5
        self.correct = correct

        if type(note) is int:
            note_name = globals.NOTE_PITCH_TO_NOTE_NAME[note]

            if ',' in note_name:
                #print("flat/sharp note detected")
                #pritn("for now, always flats")
                note_name = note_name[:2]

            self.note_name = note_name
            self.y = globals.NOTE_NAME_TO_Y_LOCATION[note_name]

        elif type(note) is str:

            self.note_name = note
            self.y = globals.NOTE_NAME_TO_Y_LOCATION[note]

        return None

    def paint(self, painter, option, widget):

        if self.correct is True:
            painter.setBrush(QtGui.QColor(0,255,255))
        elif self.correct is None:
            painter.setBrush(QtGui.QColor(255,255,0))
        else:
            painter.setBrush(QtGui.QColor(255,0,0))

        painter.drawRect(round(self.x - self.width/2), round(self.y - self.height/2), self.width, self.height)

        return None

    def boundingRect(self):

        return QtCore.QRectF(self.x, self.y, self.width, self.height)

class GraphicsPlayedNameLabel(QtWidgets.QGraphicsItem):

    def __init__(self, note):

        super(QtWidgets.QGraphicsItem, self).__init__()

        self.x = -530
        self.width = 20
        self.height = 20

        if type(note) is int:
            note_name = globals.NOTE_PITCH_TO_NOTE_NAME[note]

            if ',' in note_name:
                #print("flat/sharp note detected")
                #pritn("for now, always flats")
                note_name = note_name[:2]

            self.note_name = note_name
            self.y = globals.NOTE_NAME_TO_Y_LOCATION[note_name]

        elif type(note) is str:

            self.note_name = note
            self.y = globals.NOTE_NAME_TO_Y_LOCATION[note]

        return None

    def paint(self, painter, option, widget):

        painter.setPen(QtCore.Qt.white)
        painter.drawText(round(self.x - self.width/2), round(self.y - self.height/2), self.width, self.height, 0, self.note_name)

        return None

    def boundingRect(self):

        return QtCore.QRectF(self.x, self.y, self.width, self.height)

class GraphicsController(QtWidgets.QGraphicsObject):

    stop_signal = QtCore.pyqtSignal()

    def __init__(self):

        super(QtWidgets.QGraphicsObject, self).__init__()

        return None

class GraphicsNote(QtWidgets.QGraphicsItem):

    def __init__(self, note, x, gui):

        super(GraphicsNote, self).__init__()

        self.gui = gui
        self.xr = 8
        self.yr = 8
        self.x = x
        self.h_speed = 0
        self.played = False
        self.should_be_played_now = False
        self.is_late = False
        self.top_note = False
        self.shaded = False

        self.set_note_pitch(note)

        return None

    def __repr__(self):

        return str(self.note_name)

    def set_speed(self, h_speed = None):

        if h_speed is not None:
            self.h_speed = h_speed

        return None

    def set_note_pitch(self, note):

        #-----------------------------------------------------------------------
        # Determining the note's y value
        self.sharp_flat = 'natural'

        if type(note) is int:
            self.note_pitch = note
            note_name = globals.NOTE_PITCH_TO_NOTE_NAME[note]
            #print("original note name: ", note_name)

            if ',' in note_name: # Flat/Sharp Detected

                if note_name[0] == 'A': #A/B (select B flat)
                    self.sharp_flat = 'flat'
                elif note_name[0] == 'C': #C/D (select D flat)
                    self.sharp_flat = 'flat'
                elif note_name[0] == 'D': #D/E (select E flat)
                    self.sharp_flat = 'flat'
                elif note_name[0] == 'F': #F/G (select F sharp)
                    self.sharp_flat = 'sharp'
                elif note_name[0] == 'G': #G/A (select A flat)
                    self.sharp_flat = 'flat'

                if self.sharp_flat == 'sharp':
                    note_name = note_name[:2]
                elif self.sharp_flat == 'flat':
                    note_name = note_name[3:]

            else:
                self.sharp_flat = None

            self.note_name = note_name
            self.y = globals.NOTE_NAME_TO_Y_LOCATION[note_name]

        elif type(note) is str:

            self.note_name = note
            self.y = globals.NOTE_NAME_TO_Y_LOCATION[note]

        #print("Pitch: {2}\tNote: {0}\t Y: {1}".format(self.note_name, self.y, self.note_pitch))

        return None

    def stop(self):

        self.h_speed = 0

        return None

    def paint(self, painter, option, widget):

        # Determing if the note is late
        if globals.LATE_NOTE_BOX.contains(QtCore.QPointF(self.x, self.y)):
            self.is_late = True
        else:
            self.is_late = False

        # Beginner Mode Halting
        if self.gui.live_settings['mode'] == 'Beginner' and self.is_late is True and self.h_speed != 0 and self.played is False:
            #print("Stop signal emit")
            globals.GRAPHICS_CONTROLLER.stop_signal.emit()

        #-----------------------------------------------------------------------
        # Hiding the note if not withing the visible notes box and Hand Skill Effect

        if globals.VISIBLE_NOTE_BOX.contains(QtCore.QPointF(self.x, self.y)) is True:
            if self.shaded is True:
                self.setOpacity(0.4)
            else:
                self.setOpacity(globals.VISIBLE)
                self.visible = True
        else:
            self.setOpacity(globals.HIDDEN)
            self.visible = False

        #-----------------------------------------------------------------------
        # Changing color the notes if within the timing notes box

        should_change_color = globals.TIMING_NOTE_BOX.contains(QtCore.QPointF(self.x, self.y))

        if self.played is True:
            color = 'CYAN'
            ledger_pen_color = QtGui.QColor(0,255,255)

        elif should_change_color is True:
            color = 'YELLOW'
            self.should_be_played_now = True
            ledger_pen_color = QtCore.Qt.yellow
        else:
            color = 'GREEN'
            self.should_be_played_now = False
            ledger_pen_color = QtCore.Qt.green

        # Move
        self.x = round(self.x - self.h_speed)
        painter.drawPixmap(self.x - 7, self.y - 9, globals.PIXMAPS[color][globals.NOTE])

        if self.sharp_flat is not False:
            # Flat
            if self.sharp_flat is 'flat':
                painter.drawPixmap(self.x - 25, self.y - 25, globals.PIXMAPS[color][globals.FLAT])
            # Sharp
            if self.sharp_flat is 'sharp':
                painter.drawPixmap(self.x - 30, self.y - 23, globals.PIXMAPS[color][globals.SHARP])
            # Natural
            if self.sharp_flat is 'natural':
                painter.drawPixmap(self.x - 37, self.y - 23, globals.PIXMAPS[color][globals.NATURAL])

        #-----------------------------------------------------------------------
        # Ledger lines
        painter.setPen(ledger_pen_color)

        # Top Ledger lines
        if self.y < globals.TOP_STAFF_LINE_Y_LOCATION - 20:
            temp_y = globals.TOP_STAFF_LINE_Y_LOCATION - 20
            while temp_y >= self.y:
                painter.drawLine(self.x - 20, temp_y, self.x + 20, temp_y)
                temp_y -= 20

        # Bottom Ledger Lines
        elif self.y > globals.BOTTOM_STAFF_LINE_Y_LOCATION + 20:
            temp_y = globals.BOTTOM_STAFF_LINE_Y_LOCATION + 20
            while temp_y <= self.y:
                painter.drawLine(self.x - 20, temp_y, self.x + 20, temp_y)
                temp_y += 20

        elif self.note_name == "C4":
            painter.drawLine(self.x - 20, self.y, self.x + 20, self.y)

        #-----------------------------------------------------------------------
        # Note label

        if self.top_note is True:
            painter.setPen(QtCore.Qt.white)
            w = 20
            h = 20
            painter.drawText(self.x - 5, self.y - 25, w, h, 0, self.note_name)

        return None

    def boundingRect(self):

        return QtCore.QRectF(-self.xr, -self.xr, 2*self.xr, 2*self.xr)
