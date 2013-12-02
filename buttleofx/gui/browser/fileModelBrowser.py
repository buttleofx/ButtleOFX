import logging
# from enum import Enum

from quickmamba.models import QObjectListModel

from PyQt5 import QtGui, QtCore, QtQuick
from PyQt5.QtWidgets import QWidget, QFileDialog


class FileItem(QtCore.QObject):
    
    # Type = Enum('File', 'Folder', 'Sequence')
    
    def __init__(self, filepath, type):
        self._filepath = filepath
        self._type = type
    
    def getFilepath(self):
        return self._filepath
    
    filepath = QtCore.pyqtProperty(str, getFilepath)
    
    # isSelected = QtCore.pyqtProperty(bool, getSelected, setSelected)


class FileModelBrowser(QtQuick.QQuickItem):
    """Class FileModelBrowser"""
    
    _folder = ""
    
    def getFolder(self):
        return self._folder
    
    def setFolder(self, folder):
        print("FileModelBrowser.setFolder", folder)
        self._folder = folder
        self.updateFileItems(folder)
        from pprint import pprint
        pprint(self._fileItems)
        self.folderChanged.emit()
    
    folderChanged = QtCore.pyqtSignal()
    folder = QtCore.pyqtProperty(str, getFolder, setFolder, notify=folderChanged)
    
    def updateFileItems(self, folder):
        self._fileItems = []
        import os
        try:
            _, dirs, files = next(os.walk(folder))
            for d in dirs:
                self._fileItems.append(FileItem(d, 'Folder'))  #FileItem.Type.Folder))
            for f in files:
                self._fileItems.append(FileItem(f, 'File'))  #FileItem.Type.File))
        except Exception:
            pass

    _fileItems = []
    
    def getFileItems(self):
        fileItemsList = QObjectListModel(self)
        fileItemsList.setObjectList(self._fileItems)
        return fileItemsList
    
    fileItems = QtCore.pyqtProperty(QtCore.QObject, getFileItems, notify=folderChanged)
    
    # nameFilters = QtCore.pyqtProperty(str, setFilters)
