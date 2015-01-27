from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtQuick
from PyQt5.QtGui import QCursor, QColor, QGuiApplication

class ColorPickingEventFilter(QtCore.QObject):
    def __init__(self, screenpicker):
        QtCore.QObject.__init__(self, screenpicker)
        self._screenpicker = screenpicker

    def eventFilter(self, QObject, QEvent):
        if(QEvent.type() == QtCore.QEvent.MouseMove):
            self._screenpicker.updateCurrentColor()
        elif(QEvent.type() == QtCore.QEvent.MouseButtonRelease):
            self._screenpicker.setGrabbing(False)
            self._screenpicker.accepted.emit()

        return False


class ColorPicker(QtQuick.QQuickItem):
    """
        Define the common methods and fields for screenPicker.
    """

    def __init__(self, parent = None):
        QtQuick.QQuickItem.__init__(self, parent)
        self._currentColor = QColor("#FFFFFF")
        self._grabbing = False
        self._desktop = QtWidgets.QDesktopWidget()
        self._colorPickingEventFilter = ColorPickingEventFilter(self)

    # ######################################## Methods private to this class ####################################### #

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
                QGuiApplication.setOverrideCursor(QCursor(QtCore.Qt.CrossCursor))
                self.grabMouse()
            else:
                self.ungrabMouse()
                self.removeEventFilter(self._colorPickingEventFilter)
                QGuiApplication.restoreOverrideCursor()
            self.grabbingChanged.emit()

    # ## Others ## #

    def updateCurrentColor(self):
        cursorPos = QCursor.pos()
        # Catch the pixel pointed by the mouse on a pixmap
        pixmap = QGuiApplication.screens()[self._desktop.screenNumber()].grabWindow(self._desktop.winId(), cursorPos.x(), cursorPos.y(), 1, 1)
        qImage = pixmap.toImage()
        qColor = QColor(qImage.pixel(0, 0))
        self.setCurrentColor(qColor)

# ############################################# Data exposed to QML ############################################## #

    accepted = QtCore.pyqtSignal()

    currentColorChanged = QtCore.pyqtSignal()
    currentColor = QtCore.pyqtProperty(QColor, getCurrentColor, setCurrentColor, notify=currentColorChanged)

    grabbingChanged = QtCore.pyqtSignal()
    grabbing = QtCore.pyqtProperty(bool, isGrabbing, setGrabbing, notify=grabbingChanged)