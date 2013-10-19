from PyQt5 import QtGui, QtCore, QtQuick
from PyQt5.QtWidgets import QWidget, QFileDialog
import logging


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
        self._message = "Ouvrir un fichier"
        self._directory = "/home/"

    def getFile(self):
        return self._file

    def setFile(self, newPath):
        self._file = newPath
        self.changed.emit()

    def getType(self):
        return self._file

    def setType(self, type):
        self._type = type
        self.changed.emit()

    def getMessage(self):
        return self._message

    def setMessage(self, msg):
        self._message = msg
        self.changed.emit()

    def getDirectory(self):
        return self._directory

    def setDirectory(self, directory):
        self._directory = directory
        self.changed.emit()

    def getFinder(self):
        return self

    @QtCore.pyqtSlot()
    def browseFile(self):
        dialog = QFileDialog()

        # if the current node is a reader
        if self._type == "OpenFile":
            self._file = dialog.getOpenFileName(None, self._message, self._directory)
        # else it's a writer
        elif self._type == "SaveFile":
            self._file = dialog.getSaveFileName(None, self._message, self._directory)
        else:
            logging.error("Error : Unknown type of dialog")
            return
        self._file = self._file[0]

    finder = QtCore.pyqtProperty(QtCore.QObject, getFinder, constant=True)

    changed = QtCore.pyqtSignal()
    propFile = QtCore.pyqtProperty(str, getFile, setFile, notify=changed)
    typeDialog = QtCore.pyqtProperty(str, getType, setType, notify=changed)
    messageDialog = QtCore.pyqtProperty(str, getMessage, setMessage, notify=changed)
    directoryDialog = QtCore.pyqtProperty(str, getDirectory, setDirectory, notify=changed)
