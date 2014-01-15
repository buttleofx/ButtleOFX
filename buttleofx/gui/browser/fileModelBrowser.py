import logging
import os

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
        self._fileType = fileType

    def getFilepath(self):
        return self._filepath
    
    def getFileType(self):
        return self._fileType
    
    def getFileName(self):
        return os.path.basename(self._filepath)
    
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


class SuggestionItem(QtCore.QObject):
    
    def __init__(self, folder, dirName):
        super(SuggestionItem, self).__init__()
        self._dirpath = folder + "/" + dirName

    def getDirpath(self):
        return self._dirpath
    
    def getDirName(self):
        return os.path.basename(self._dirpath)

    dirpath = QtCore.pyqtProperty(str, getDirpath, constant=True)
    dirName = QtCore.pyqtProperty(str, getDirName, constant=True)


class FileModelBrowser(QtQuick.QQuickItem):
    """Class FileModelBrowser"""
    
    _folder = ""
    
    def __init__(self, parent=None):
        super(FileModelBrowser, self).__init__(parent)
        self._fileItemsModel = QObjectListModel(self)
        self._suggestionItemsModel = QObjectListModel(self)
    
    def getFolder(self):
        return self._folder
    
    def setFolder(self, folder):
        self._folder = folder
        self.updateFileItems(folder)
        self.updateSuggestionItems(folder)
        self.folderChanged.emit()
    
    def getFolderExists(self):
        import os
        return os.path.exists(self._folder)
    
    def getParentFolder(self):
        return os.path.dirname(self._folder)

    folderChanged = QtCore.pyqtSignal()
    folder = QtCore.pyqtProperty(str, getFolder, setFolder, notify=folderChanged)
    exists = QtCore.pyqtProperty(bool, getFolderExists, notify=folderChanged)
    parentFolder = QtCore.pyqtProperty(str, getParentFolder, constant=True)
    
    def updateFileItems(self, folder):
        self._fileItems = []
        self._fileItemsModel.clear()
        import os
        try:
            _, dirs, files = next(os.walk(folder))
            for d in dirs:
                self._fileItems.append(FileItem(folder, d, FileItem.Type.Folder))
            
            if self._nameFilter == "*":
                for f in files:
                    self._fileItems.append(FileItem(folder, f, FileItem.Type.File))
                    
            else:
                for f in files:
                    (shortname, extension) = os.path.splitext(f)
                    if extension == self._nameFilter:
                        print("Only ", extension, " files")
                        self._fileItems.append(FileItem(folder, f, FileItem.Type.File))
                          
                #self._fileItems.append(FileItem(folder, f, FileItem.Type.File))
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
    
    def getFilter(self):
        return self._nameFilter
     
    @QtCore.pyqtSlot(str)
    def setFilter(self, nameFilter):
        self._nameFilter = nameFilter
        self.updateFileItems(self._folder)
        self.nameFilterChange.emit()

    fileItems = QtCore.pyqtProperty(QtCore.QObject, getFileItems, notify=folderChanged)
    nameFilterChange = QtCore.pyqtSignal()
    nameFilter = QtCore.pyqtProperty(str, getFilter, setFilter, notify=nameFilterChange)
    
    def updateSuggestionItems(self, folder):
        self._suggestionItems = []
        self._suggestionItemsModel.clear()
        import os
        try:
            _, dirs, files = next(os.walk(os.path.dirname(folder)))
            for d in dirs:
                if d.startswith(os.path.basename(folder)):
                    self._fileItems.append(SuggestionItem(folder, d))
            
        except Exception:
            pass
        self._suggestionItemsModel.setObjectList(self._suggestionItems)
    
    _suggestionItems = []
    _suggestionItemsModel = None
    
    def getSuggestionItems(self):
        return self._suggestionItemsModel
    
    suggestionItems = QtCore.pyqtProperty(QtCore.QObject, getSuggestionItems, notify=folderChanged)

