from PySide import QtGui, QtCore, QtDeclarative
from PySide.QtGui import QWidget, QFileDialog

import os,sys

class Finder(QtDeclarative.QDeclarativeItem, QWidget, QtCore.QObject):
    def __init__(self, parent=None):
        QtDeclarative.QDeclarativeItem.__init__(self, parent)

        self._file = None
       

    def getFile(self):
        return self._file

    def setFile(self, newPath):
        self._file = newPath

    def getFinder(self):
        return self

    @QtCore.Slot("QVariant")
    def browseFile(self, currentParamNode):
        # if the current node is a reader
        if "read" in currentParamNode.getType().lower():
            self._file = QFileDialog.getOpenFileName(self, "Ouvrir un fichier", "/home/")
        # else it's a writer
        else :
            self._file = QFileDialog.getSaveFileName(self, "Ouvrir un fichier", "/home/")
        self._file = self._file[0]

    finder = QtCore.Property(QtCore.QObject, getFinder, constant=True)

    fileChanged = QtCore.Signal()
    propFile = QtCore.Property(str, getFile, setFile, notify=fileChanged)