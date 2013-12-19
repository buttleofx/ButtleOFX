import logging

from quickmamba.models import QObjectListModel

from PyQt5 import QtGui, QtCore, QtQuick
from PyQt5.QtWidgets import QWidget, QFileDialog


class FileItem(QtCore.QObject):
    
    _isSelected = False
    
    class Type():
        """ Enum """
        File = 'File'
        Folder = 'Folder'
        Sequence = 'Sequence'
    
    def __init__(self, folder, fileName, fileType):
        super(FileItem, self).__init__()
        self._filepath = folder + "/" + fileName
        self._fileName = fileName
        self._fileType = fileType

    def getFilepath(self):
        return self._filepath
    
    def getFileType(self):
        return self._fileType
    
    def getFileName(self):
        return self._fileName
    
    def getSelected(self):
        return self._isSelected
    
    def setSelected(self, isSelected):
        self._isSelected = isSelected
        self.isSelectedChange.emit()

    filepath = QtCore.pyqtProperty(str, getFilepath, constant=True)
    fileType = QtCore.pyqtProperty(str, getFileType, constant=True)
    fileName = QtCore.pyqtProperty(str, getFileName, constant=True)
    isSelectedChange = QtCore.pyqtSignal()
    isSelected = QtCore.pyqtProperty(bool, getSelected, setSelected, notify=isSelectedChange)


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
                self._fileItems.append(FileItem(folder, d, FileItem.Type.Folder))
            
            if self._nameFilter == "*":
                print("On recupère tous les fichiers")
                for f in files:
                    self._fileItems.append(FileItem(folder, f, FileItem.Type.File))
                    
            if self._nameFilter == ".jpg":
                print("On recupère seulement les fichiers en ",self._nameFilter)
                for f in files:
                    begin = f.find(".")
                    format = f[begin:len(f)]
                    print(format)
                    if format is self._nameFilter:
                        print("On recupère seulement les fichiers en ",format)
                        self._fileItems.append(FileItem(folder, f, FileItem.Type.File))
                        
            if self._nameFilter == ".png":
                for f in files:
                    begin = f.find(".")
                    format = f[begin:len(f)]
                    if format is self._nameFilter:
                        print("On recupère seulement les fichiers en ",format)
                        self._fileItems.append(FileItem(folder, f, FileItem.Type.File))
                
                self._fileItems.append(FileItem(folder, f, FileItem.Type.File))
        except Exception:
            pass
        self._fileItemsModel.setObjectList(self._fileItems)
    
    _fileItems = []
    _fileItemsModel = None
    
    def getFileItems(self):
        return self._fileItemsModel
    
    @QtCore.pyqtSlot(int)
    def selectItem(self, index):
        for item in self._fileItems:
            item.isSelected = False
        if index < len(self._fileItems):
            print("index", len(self._fileItems))
            self._fileItems[index].isSelected = True
        else:
            print("not index", len(self._fileItems))
    
#    class NameFilter():
#        """ Enum """
#        All = '*'
#        Jpeg = '.jpg'
#        Png = 'png'

    _nameFilter = ".png"
    
    def getFilter(self):
        return self._nameFilter
        
    def setFilter(self, nameFilter):
        self._nameFilter = nameFilter
        self.nameFilterChange.emit()

    fileItems = QtCore.pyqtProperty(QtCore.QObject, getFileItems, notify=folderChanged)
    nameFilterChange = QtCore.pyqtSignal()
    nameFilter = QtCore.pyqtProperty(str, getFilter, setFilter, notify=nameFilterChange)
