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

    """ This class informs the user about communication failures. """

    def __init__(self):

        """ This function establishes the size and font size of the text. """

        super(QtWidgets.QGraphicsItem, self).__init__()

        self.width = 400 * globals.S_W_R
        self.height = 50 * globals.S_H_R
        self.x = -900 * globals.S_W_R
        self.y = -500 * globals.S_H_R

        self.font = QtGui.QFont()
        self.font.setPixelSize(25 * globals.S_W_R)

        self.text = ""

        return None

    def set_text(self, text):

        """ This helper function sets the text ofthe system message. """

        self.text = text

        return None

    def paint(self, painter, option, widget):

        """ This function draws the text with a green pen. """

        painter.setPen(QtCore.Qt.green)
        painter.setFont(self.font)
        painter.drawText(self.x, self.y, self.width, self.height, QtCore.Qt.AlignLeft, self.text)

        return None

    def boundingRect(self):

        """ This is a necessary function that returns the bounding dimensions. """

        return QtCore.QRectF(self.x + self.width, self.y, self.width, self.height)

class GraphicsPlayedLabel(QtWidgets.QGraphicsItem):

    """
    This class is the graphics note label above the drawn notes. This is the
    rectangle that is in the same y value. This is not the actual drawn note
    pitch text.
    """

    def __init__(self, note, correct = None):

        """
        This function setups up the label, with its dimensions and corresponding
        drawn note.
        """

        super(QtWidgets.QGraphicsItem, self).__init__()

        self.x = -510 * globals.S_W_R
        self.width = 20 * globals.S_W_R
        self.height = 5 * globals.S_H_R
        self.correct = correct

        if type(note) is int:
            note_name = globals.NOTE_PITCH_TO_NOTE_NAME[note]

            if ',' in note_name:
                #print("flat/sharp note detected")
                #pritn("for now, always flats")
                note_name = note_name[:2]

            self.note_name = note_name
            self.y = globals.NOTE_NAME_TO_Y_LOCATION[note_name] * globals.S_H_R

        elif type(note) is str:

            self.note_name = note
            self.y = globals.NOTE_NAME_TO_Y_LOCATION[note] * globals.S_H_R

        return None

    def paint(self, painter, option, widget):

        """
        This function draws the rectangle object that indicates the pitch of the
        drawn note.
        """

        if self.correct is True:
            painter.setBrush(QtGui.QColor(0,255,255))
        elif self.correct is None:
            painter.setBrush(QtGui.QColor(255,255,0))
        else:
            painter.setBrush(QtGui.QColor(255,0,0))

        painter.drawRect(round(self.x - self.width/2), round(self.y - self.height/2), self.width, self.height)

        return None

    def boundingRect(self):

        """ This is a necessary function that returns the bounding dimensions. """

        return QtCore.QRectF(self.x, self.y, self.width, self.height)

class GraphicsPlayedNameLabel(QtWidgets.QGraphicsItem):

    """
    This class is the graphics element for the note label name. This is the
    name tag for the played note.
    """

    def __init__(self, note):

        """
        This function determines the size, dimensions, and location of the
        graphical element.
        """

        super(QtWidgets.QGraphicsItem, self).__init__()

        self.x = -530 * globals.S_W_R
        self.width = 20 * globals.S_W_R
        self.height = 20 * globals.S_H_R

        if type(note) is int:
            note_name = globals.NOTE_PITCH_TO_NOTE_NAME[note]

            if ',' in note_name:
                #print("flat/sharp note detected")
                #pritn("for now, always flats")
                note_name = note_name[:2]

            self.note_name = note_name
            self.y = globals.NOTE_NAME_TO_Y_LOCATION[note_name] * globals.S_W_R

        elif type(note) is str:

            self.note_name = note
            self.y = globals.NOTE_NAME_TO_Y_LOCATION[note] * globals.S_H_R

        return None

    def paint(self, painter, option, widget):

        """ This function draws the text corresponding to the drawn note. """

        painter.setPen(QtCore.Qt.white)
        painter.drawText(round(self.x - self.width/2), round(self.y - self.height/2), self.width, self.height, 0, self.note_name)

        return None

    def boundingRect(self):

        """ This is a necessary function that returns the bounding dimensions. """

        return QtCore.QRectF(self.x, self.y, self.width, self.height)

class GraphicsController(QtWidgets.QGraphicsObject):

    """
    This object is simply a work around slot and signals. The QGraphicsItem does
    not support slot and signals, but the GraphicsNote class needs to signal the
    tutor thread to perform the stop action. Therefore, this class provides the
    slot and signals attribute while simply only using one object to track all
    possible signals from the all the drawn notes.
    """

    stop_signal = QtCore.pyqtSignal()

    def __init__(self):

        """ This sets the QGraphicsObject to provide the slot and signals attribute. """

        super(QtWidgets.QGraphicsObject, self).__init__()

        return None

class GraphicsNote(QtWidgets.QGraphicsItem):

    """
    This class is the base foundation of the SKORE application. This is the
    graphics note which indicates the user and the tutor thread when the user
    needs to play a note.
    """

    def __init__(self, note, x, gui):

        """
        This function setups up the main attributes of the graphics note, such
        as its location, speed, played state, lateness, and if it should be
        played now or not.
        """

        super(GraphicsNote, self).__init__()

        self.gui = gui
        self.xr = 8 * globals.S_W_R
        self.yr = 8 * globals.S_H_R
        self.x = x * globals.S_W_R
        self.h_speed = 0
        self.played = False
        self.should_be_played_now = False
        self.is_late = False
        self.top_note = False
        self.shaded = False

        self.set_note_pitch(note)

        return None

    def set_note_pitch(self, note):

        """
        This function sets the note pitch, its y location, and sets if the
        note is sharped or flat.
        """

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
            self.y = globals.NOTE_NAME_TO_Y_LOCATION[note_name] * globals.S_H_R

        elif type(note) is str:

            self.note_name = note
            self.y = globals.NOTE_NAME_TO_Y_LOCATION[note] * globals.S_H_R

        #print("Pitch: {2}\tNote: {0}\t Y: {1}".format(self.note_name, self.y, self.note_pitch))

        return None

    #---------------------------------------------------------------------------
    # Speed Control

    def set_speed(self, h_speed = None):

        """ This is a helper function for setting the note speed. """

        if h_speed is not None:
            self.h_speed = h_speed * globals.S_W_R

        return None

    def stop(self):

        """ This is helper function for stoping the note. """

        self.h_speed = 0

        return None

    #---------------------------------------------------------------------------
    # Drawning and Logic

    def beginner_mode_halting(self):

        """
        This function emits a signal to stop the Tutor Thread depending on
        multiple conditions.
        """

        if globals.LIVE_SETTINGS['mode'] == 'Beginner' and self.is_late is True and self.h_speed != 0 and self.played is False:
            #print("Stop signal emit")
            globals.GRAPHICS_CONTROLLER.stop_signal.emit()

        return None

    def should_be_visible(self):

        """ This function determines and tags if the note should be visible. """

        if globals.VISIBLE_NOTE_BOX.contains(QtCore.QPointF(self.x, self.y)) is True:
            if self.shaded is True:
                self.setOpacity(0.4)
            else:
                self.setOpacity(globals.VISIBLE)
                self.visible = True

            return True

        else:
            self.setOpacity(globals.HIDDEN)
            self.visible = False
            return False

    def color_selection(self):

        """
        This function selects the color depending on the location of note and
        its status (played).
        """

        should_change_color = globals.TIMING_NOTE_BOX.contains(QtCore.QPointF(self.x, self.y))

        if self.played is True:
            self.color = 'CYAN'
            self.ledger_pen_color = QtGui.QColor(0,255,255)

        elif should_change_color is True:
            self.color = 'YELLOW'
            self.should_be_played_now = True
            self.ledger_pen_color = QtCore.Qt.yellow
        else:
            self.color = 'GREEN'
            self.should_be_played_now = False
            self.ledger_pen_color = QtCore.Qt.green

        return None

    def draw_flat_sharp(self, painter):

        """
        This function draws the flats, sharps, and naturals of the notes if
        neccesary.
        """

        if self.sharp_flat is True:
            # Flat
            if self.sharp_flat is 'flat':
                painter.drawPixmap(self.x - 25 * globals.S_W_R, self.y - 25 * globals.S_H_R, globals.PIXMAPS[self.color][globals.FLAT])
            # Sharp
            if self.sharp_flat is 'sharp':
                painter.drawPixmap(self.x - 30 * globals.S_W_R, self.y - 23 * globals.S_H_R, globals.PIXMAPS[self.color][globals.SHARP])
            # Natural
            if self.sharp_flat is 'natural':
                painter.drawPixmap(self.x - 37 * globals.S_W_R, self.y - 23 * globals.S_H_R, globals.PIXMAPS[self.color][globals.NATURAL])

        return None

    def draw_ledger_lines(self, painter):

        """
        This function draws the ledger lines of a note depending on its location.
        """

        # Ledger lines
        painter.setPen(self.ledger_pen_color)

        # Top Ledger lines
        if self.y < (globals.TOP_STAFF_LINE_Y_LOCATION - 20) * globals.S_H_R:
            temp_y = (globals.TOP_STAFF_LINE_Y_LOCATION - 20) * globals.S_H_R
            while temp_y >= self.y:
                painter.drawLine(self.x - 20 * globals.S_W_R, temp_y, self.x + 20 * globals.S_W_R, temp_y)
                temp_y -= 20 * globals.S_H_R

        # Bottom Ledger Lines
        elif self.y > (globals.BOTTOM_STAFF_LINE_Y_LOCATION + 20) * globals.S_H_R:
            temp_y = (globals.BOTTOM_STAFF_LINE_Y_LOCATION + 20) *globals.S_H_R
            while temp_y <= self.y:
                painter.drawLine(self.x - 20 * globals.S_W_R, temp_y, self.x + 20 * globals.S_W_R, temp_y)
                temp_y += 20 * globals.S_H_R

        elif self.note_name == "C4":
            painter.drawLine(self.x - 20 * globals.S_W_R, self.y, self.x + 20 * globals.S_W_R, self.y)

        return None

    def draw_top_note_name(self, painter):

        """
        This function drawsa note label if the note is the top note of the chord
        or if it is a single note.
        """

        if self.top_note is True:
            painter.setPen(QtCore.Qt.white)
            w = 20
            h = 20
            painter.drawText(self.x - 5 * globals.S_W_R, self.y - 25 * globals.S_H_R, w * globals.S_W_R, h * globals.S_H_R, 0, self.note_name)

        return None

    def paint(self, painter, option, widget):

        """
        This function includes all the necessary steps to draw the complete note
        and performs additionall tutoring logic.
        """

        # Determing if the note is late
        if globals.LATE_NOTE_BOX.contains(QtCore.QPointF(self.x, self.y)):
            self.is_late = True
        else:
            self.is_late = False

        self.beginner_mode_halting()

        # Move
        self.x = round(self.x - self.h_speed)

        if self.should_be_visible() is False:
            return None

        # Paint all main attributes

        self.color_selection()

        painter.drawPixmap(self.x - 7 * globals.S_W_R, self.y - 9 * globals.S_H_R, globals.PIXMAPS[self.color][globals.NOTE])

        self.draw_flat_sharp(painter)

        self.draw_ledger_lines(painter)

        self.draw_top_note_name(painter)

        return None

    #---------------------------------------------------------------------------
    # Misc Functions

    def __repr__(self):

        """
        This function provides the note name if the graphics note is printed.
        """

        return str(self.note_name)

    def boundingRect(self):

        """ This is a necessary function that returns the bounding dimensions. """

        return QtCore.QRectF(-self.xr, -self.xr, 2*self.xr, 2*self.xr)
