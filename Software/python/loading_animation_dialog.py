# General Utility Libraries
import sys
import math

# PyQt5, GUI Library
from PyQt5 import QtCore, QtGui, QtWidgets

# SKORE Modules
import globals

#-------------------------------------------------------------------------------
# Classes

class LoadingAnimationDialog(QtWidgets.QDialog):

    """
    This class is a dialog to provide with a loading animation. The intent of
    this object is to inform the user of the initialization and completion of a
    file conversion.
    """

    def __init__(self):

        """
        This function initializes the dialog, settings its size and trait.
        """

        super(QtWidgets.QDialog, self).__init__()
        self.setObjectName("LoadingAnimationDialog")
        self.resize(320 * globals.S_W_R, 250 * globals.S_H_R)
        self.setWindowTitle("Converting...")
        self.setWindowIcon(QtGui.QIcon('.\images\skore_icon.png'))
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, True)

        self.setup_ui()

        self.count = 0

        # Timer Setup
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.clock)
        self.timer.start(100) # 60 FPS, 16ms, 30 FPS, 33ms

        return None

    def setup_ui(self):

        """ This function sets the graphics view widget in the dialog class.  """

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setItemIndexMethod(-1)
        self.graphics_view_loading = QtWidgets.QGraphicsView(self.scene, self)
        self.graphics_view_loading.setGeometry(QtCore.QRect(-1 * globals.S_W_R, 0, 322 * globals.S_W_R, 251 * globals.S_H_R))
        self.graphics_view_loading.setObjectName("graphicsView")

        self.graphics_view_loading.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.black))
        self.ellipse_group = {}

        QtCore.QMetaObject.connectSlotsByName(self)

        return None

    def clock(self):

        """ This function sets the painted graphics and updates the graphics. """

        self.paint()
        self.scene.update()

        return None

    def paint(self):

        """
        This function draws, removes, and opaces the necessary circles to create
        a circular and fading loading animation.
        """

        for (ellipse, opacity) in self.ellipse_group.items():
            opacity -= 0.2
            ellipse.setOpacity(opacity)
            self.ellipse_group[ellipse] = opacity

        green_pen = QtGui.QPen(QtCore.Qt.green)
        green_brush = QtGui.QBrush(QtCore.Qt.green)

        path_radius = 50 *  globals.S_W_R
        circle_radius = 30
        circle_quantity = 8
        shift = 0
        x_value = 0
        y_value = 0

        ellipse = self.scene.addEllipse(x_value + path_radius * math.cos(2 * math.pi * self.count / circle_quantity) - shift,
                                        y_value + path_radius * math.sin(2 * math.pi * self.count / circle_quantity) - shift, circle_radius * globals.S_W_R, circle_radius * globals.S_H_R, green_pen, green_brush)

        self.ellipse_group[ellipse] = 1

        self.count += 1
        if self.count >= circle_quantity:
            self.count = 0

        return None

#-------------------------------------------------------------------------------
# Main Code

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    theme_list = QtWidgets.QStyleFactory.keys()
    app.setStyle(QtWidgets.QStyleFactory.create(theme_list[2])) #Fusion

    ui = LoadingAnimationDialog()
    ui.show()
    sys.exit(app.exec_())
