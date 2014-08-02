import logging
from PyQt5 import QtGui, QtCore, QtQuick
from PyQt5.QtWidgets import QWidget, QFileDialog


class Finder(QtQuick.QQuickItem):
    """
        Class finder
        _file : the file name
        _type : the type of the finder : "OpenFile" or "SaveFile"
        _message :
        _directory :
    """

    def __init__(self, parent=None):
        QtQuick.QQuickItem.__init__(self, parent)

        self._file = None
        self._filters = ["*.json"]
        self._type = None  # "OpenFile" / "SaveFile"
        self._message = "Open a file"
        self._directory = "/home/"

    # ############################################ Methods exposed to QML ############################################ #

    @QtCore.pyqtSlot()
    def browseFile(self):
        dialog = QFileDialog()

        # If the current node is a reader
        if self._type == "OpenFile":
            self._file = dialog.getOpenFileName(None, self._message, self._directory)
        # Else it's a writer
        elif self._type == "SaveFile":
            self._file = dialog.getSaveFileName(None, self._message, self._directory)
        else:
            logging.error("Error : Unknown type of dialog")
            return
        self._file = self._file[0]

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getDirectory(self):
        return self._directory

    def getFile(self):
        return self._file

    def getFinder(self):
        return self

    def getMessage(self):
        return self._message

    def getType(self):
        return self._file

    # ## Setters ## #

    def setDirectory(self, directory):
        self._directory = directory
        self.changed.emit()

    def setFile(self, newPath):
        self._file = newPath
        self.changed.emit()

    def setMessage(self, msg):
        self._message = msg
        self.changed.emit()

    def setType(self, type):
        self._type = type
        self.changed.emit()

    # ############################################# Data exposed to QML ############################################## #

    changed = QtCore.pyqtSignal()

    finder = QtCore.pyqtProperty(QtCore.QObject, getFinder, constant=True)
    propFile = QtCore.pyqtProperty(str, getFile, setFile, notify=changed)
    typeDialog = QtCore.pyqtProperty(str, getType, setType, notify=changed)
    messageDialog = QtCore.pyqtProperty(str, getMessage, setMessage, notify=changed)
    directoryDialog = QtCore.pyqtProperty(str, getDirectory, setDirectory, notify=changed)
