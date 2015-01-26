from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtQuick
from PyQt5 import QtGui
import sys


class ColorPickingEventFilter(QtCore.QObject):
    def __init__(self, parent = None):
        QtCore.QObject.__init__(self, parent)

    def eventFilter(self, QObject, QEvent):
        print(QEvent.type())
        return False


class ScreenPicker(QtQuick.QQuickItem):
    """
        Define the common methods and fields for screenPicker.
    """

    def __init__(self, parent = None):
        super(ScreenPicker, self).__init__(parent)
        self._currentColor = QtGui.QColor("#FFFFFF")
        self._grabbing = False
        self._desktop = QtWidgets.QDesktopWidget()
        self._cursor = QtGui.QCursor()
        self._colorPickingEventFilter = ColorPickingEventFilter(self)

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
        if(self._grabbing != grabbing):
            self._grabbing = grabbing
            if(self._grabbing):
                self.installEventFilter(self._colorPickingEventFilter)
                self.grabMouse()
            else:
                self.removeEventFilter(self._colorPickingEventFilter)
            self.grabbingChanged.emit()

    # ## Others ## #


# ############################################# Data exposed to QML ############################################## #

    currentColorChanged = QtCore.pyqtSignal()
    currentColor = QtCore.pyqtProperty(QtGui.QColor, getCurrentColor, setCurrentColor, notify=currentColorChanged)

    grabbingChanged = QtCore.pyqtSignal()
    grabbing = QtCore.pyqtProperty(bool, isGrabbing, setGrabbing, notify=grabbingChanged)