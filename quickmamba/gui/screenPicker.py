from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import random

class ScreenPicker(QtCore.QObject):
    """
        Define the common methods and fields for paramWrappers.
    """

    def __init__(self, parent = None):
        QtCore.QObject.__init__(self, parent)
        self._currentColor = QtGui.QColor("#FFFFFF")
        self._grabbing = False
        self._desktop = QtWidgets.QDesktopWidget()
        self._cursor = QtGui.QCursor()


    # ######################################## Methods private to this class ####################################### #

    def _updateCurrentColor(self):
        pixmap = QtGui.QGuiApplication.screens()[self._desktop.screenNumber()].grabWindow(self._desktop.winId(), self._cursor.pos().x(), self._cursor.pos().y(), 1, 1)
        qImage = pixmap.toImage()
        qColor = QtGui.QColor(qImage.pixel(0, 0))
        self.setTestColor(qColor)

    # ## Getters ## #

    def getCurrentColor(self):
        return self._currentColor

    def setCurrentColor(self, currentColor):
        self._currentColor = currentColor
        self.currentColorChanged.emit()

    def isGrabbing(self):
        return self._grabbing

    def setGrabbing(self, grabbing):
        self._grabbing = grabbing

    # ## Others ## #


    # ############################################# Data exposed to QML ############################################## #

    currentColorChanged = QtCore.pyqtSignal()
    testColor = QtCore.pyqtProperty(QtGui.QColor, getCurrentColor, setCurrentColor, notify=currentColorChanged)

    grabbingChanged = QtCore.pyqtSignal()
    grabbing = QtCore.pyqtProperty(QtGui.QColor, isGrabbing, setGrabbing, notify=grabbingChanged)
