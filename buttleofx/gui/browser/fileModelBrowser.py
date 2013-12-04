import logging

from quickmamba.models import QObjectListModel

from PyQt5 import QtGui, QtCore, QtQuick
from PyQt5.QtWidgets import QWidget, QFileDialog


class FileItem(QtCore.QObject):
    
    class Type():
        """ Enum """
        File = 'File'
        Folder = 'Folder'
        Sequence = 'Sequence'
    
    def __init__(self, filepath, fileType):
        super(FileItem, self).__init__()
        self._filepath = filepath
        self._fileType = fileType
    
    def getFilepath(self):
        return self._filepath
    
    def getFileType(self):
        return self._fileType
    
    filepath = QtCore.pyqtProperty(str, getFilepath, constant=True)
    fileType = QtCore.pyqtProperty(str, getFileType, constant=True)
    
    # isSelected = QtCore.pyqtProperty(bool, getSelected, setSelected)


class FileModelBrowser(QtQuick.QQuickItem):
    """Class FileModelBrowser"""
    
    _folder = ""
    
    def __init__(self, parent=None):
        super(FileModelBrowser, self).__init__(parent)
        self._fileItemsModel = QObjectListModel(self)
    
    def getFolder(self):
        return self._folder
    
    def setFolder(self, folder):
        self._folder = folder
        self.updateFileItems(folder)
        self.folderChanged.emit()
    
    def getFolderExists(self):
        import os
        return os.path.exists(self._folder)

    folderChanged = QtCore.pyqtSignal()
    folder = QtCore.pyqtProperty(str, getFolder, setFolder, notify=folderChanged)
    exists = QtCore.pyqtProperty(bool, getFolderExists, notify=folderChanged)
    
    def updateFileItems(self, folder):
        self._fileItems = []
        self._fileItemsModel.clear()
        import os
        try:
            _, dirs, files = next(os.walk(folder))
            for d in dirs:
                self._fileItems.append(FileItem(d, FileItem.Type.Folder))
            for f in files:
                self._fileItems.append(FileItem(f, FileItem.Type.File))
        except Exception:
            pass
        self._fileItemsModel.setObjectList(self._fileItems)
    
    _fileItems = []
    _fileItemsModel = None
    
    def getFileItems(self):
        return self._fileItemsModel
    
    fileItems = QtCore.pyqtProperty(QtCore.QObject, getFileItems, notify=folderChanged)
    
    # nameFilters = QtCore.pyqtProperty(str, setFilters)
