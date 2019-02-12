# General Utility
import time
import sys
from time import sleep
import os
import difflib
import webbrowser
import ast

# PYQT5, GUI Library
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *

import globals

class GraphicsSystemMessage(QGraphicsItem):

    def __init__(self):
        super(GraphicsSystemMessage, self).__init__()

        self.width = 400
        self.height = 50
        self.x = -900
        self.y = -500

        self.font = QFont()
        self.font.setPixelSize(25)

        self.text = ""

        return None

    def set_text(self, text):
        self.text = text
        return None

    def paint(self, painter, option, widget):

        painter.setPen(Qt.green)
        painter.setFont(self.font)
        painter.drawText(self.x, self.y, self.width, self.height, Qt.AlignLeft, self.text)

        return None

    def boundingRect(self):

        return QRectF(self.x + self.width, self.y, self.width, self.height)

class GraphicsPlayedLabel(QGraphicsItem):

    def __init__(self, note, correct = None):
        super(GraphicsPlayedLabel, self).__init__()

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
            painter.setBrush(QColor(0,255,255))
        elif self.correct is None:
            painter.setBrush(QColor(255,255,0))
        else:
            painter.setBrush(QColor(255,0,0))

        painter.drawRect(round(self.x - self.width/2), round(self.y - self.height/2), self.width, self.height)

        return None

    def boundingRect(self):
        return QRectF(self.x, self.y, self.width, self.height)

class GraphicsPlayedNameLabel(QGraphicsItem):

    def __init__(self, note):
        super(GraphicsPlayedNameLabel, self).__init__()

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

        painter.setPen(Qt.white)
        painter.drawText(round(self.x - self.width/2), round(self.y - self.height/2), self.width, self.height, 0, self.note_name)
        return None

    def boundingRect(self):
        return QRectF(self.x, self.y, self.width, self.height)

class GraphicsController(QGraphicsObject):

    stop_signal = QtCore.pyqtSignal()

    def __init__(self):
        super(GraphicsController, self).__init__()

class GraphicsNote(QGraphicsItem):

    def __init__(self, note, x, gui):
        super(GraphicsNote, self).__init__()

        self.gui = gui
        self.xr = 8
        self.yr = 8
        self.x = x
        self.h_speed = 0
        self.played = False
        self.should_be_played_now = False
        self.top_note = False
        self.shaded = False

        self.set_note_pitch(note)

        return None

    def __repr__(self):

        return str(self.note_name)

    def set_speed(self, h_speed = None):
        if h_speed is not None:
            self.h_speed = h_speed

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
                    #print('A')
                    self.sharp_flat = 'flat'
                elif note_name[0] == 'C': #C/D (select D flat)
                    #print('C')
                    self.sharp_flat = 'flat'
                elif note_name[0] == 'D': #D/E (select E flat)
                    #print('D')
                    self.sharp_flat = 'flat'
                elif note_name[0] == 'F': #F/G (select F sharp)
                    #print('F')
                    self.sharp_flat = 'sharp'
                elif note_name[0] == 'G': #G/A (select A flat)
                    #print('G')
                    self.sharp_flat = 'flat'

                if self.sharp_flat == 'sharp':
                    #print('sharp')
                    note_name = note_name[:2]

                elif self.sharp_flat == 'flat':
                    #print('flat')
                    note_name = note_name[3:]

                #print("After flat/sharp selection: ",note_name)
            else:
                self.sharp_flat = None

            #print("")

            self.note_name = note_name
            self.y = globals.NOTE_NAME_TO_Y_LOCATION[note_name]

        elif type(note) is str:

            self.note_name = note
            self.y = globals.NOTE_NAME_TO_Y_LOCATION[note]

        #print("Pitch: {2}\tNote: {0}\t Y: {1}".format(self.note_name, self.y, self.note_pitch))

        return None

    def stop(self):
        self.h_speed = 0

    def paint(self, painter, option, widget):

        # Beginner Mode Halting
        if self.gui.live_settings['mode'] == 'Beginner' and globals.TIMING_NOTE_LINE_CATCH.contains(QPointF(self.x, self.y)) and self.h_speed != 0 and self.played is False:
            #print("Stop signal emit")
            globals.GRAPHICS_CONTROLLER.stop_signal.emit()

        #-----------------------------------------------------------------------
        # Hiding the note if not withing the visible notes box and Hand Skill Effect

        if globals.VISIBLE_NOTE_BOX.contains(QPointF(self.x, self.y)) is True:
            if self.shaded is True:
                self.setOpacity(0.4)
            else:
                self.setOpacity(1)
                self.visible = True
        else:
            self.setOpacity(globals.HIDDEN)
            self.visible = False

        #-----------------------------------------------------------------------
        # Changing color the notes if within the timing notes box

        should_change_color = globals.TIMING_NOTE_BOX.contains(QPointF(self.x, self.y))

        if self.played is True:
            color = 'CYAN'
            ledger_pen_color = QColor(0,255,255)

        elif should_change_color is True:
            color = 'YELLOW'
            self.should_be_played_now = True
            ledger_pen_color = Qt.yellow
        else:
            color = 'GREEN'
            self.should_be_played_now = False
            ledger_pen_color = Qt.green

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
            painter.setPen(Qt.white)
            w = 20
            h = 20
            painter.drawText(self.x - 5, self.y - 25, w, h, 0, self.note_name)

        return None

    def boundingRect(self):
        return QRectF(-self.xr, -self.xr, 2*self.xr, 2*self.xr)
