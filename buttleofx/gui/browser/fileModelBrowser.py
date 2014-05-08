import logging
import os

#Tuttle
import getBestPlugin

from quickmamba.models import QObjectListModel
from quickmamba.patterns import Singleton
from pySequenceParser import sequenceParser

from PyQt5 import QtGui, QtCore, QtQuick
from PyQt5.QtWidgets import QWidget, QFileDialog
#gui
from .sequenceWrapper import SequenceWrapper


class FileItem(QtCore.QObject):
    
    _isSelected = False
    
    class Type():
        """ Enum """
        File = 'File'
        Folder = 'Folder'
        Sequence = 'Sequence'
    
    def __init__(self, folder, fileName, fileType, seq, supported):
        super(FileItem, self).__init__()
        if folder == "/":
            self._filepath = folder + fileName
        else:
            self._filepath = folder + "/" + fileName
        self._fileType = fileType
        
        if fileType == FileItem.Type.File:
            if supported == True:
                self._fileImg = 'image://buttleofx/' + self._filepath
            else:
                self._fileImg = "../../img/buttons/browser/file-icon.png"
            self._seq = None
            self._fileWeight = os.stat(self._filepath).st_size
            (_, extension) = os.path.splitext(fileName)
            self._fileExtension = extension
            
        elif fileType == FileItem.Type.Folder:
            self._fileImg = "../../img/buttons/browser/folder-icon.png"
            self._seq = None
            self._fileWeight = 0.0
            self._fileExtension = ""
                        
        elif fileType == FileItem.Type.Sequence:
            if supported == True:
                self._fileImg = self._seq.getFirstFilePath()
            else:
                self._fileImg = "../../img/buttons/browser/file-icon.png"
            self._seq = SequenceWrapper(seq)
            self._fileWeight = self._seq.getWeight()
            (_, extension) = os.path.splitext(self._seq.getFirstFileName())
            self._fileExtension = extension
           
    def getFilepath(self):
        return self._filepath
    
    def setFilepath(self, newpath):
        import shutil
        shutil.move(self.filepath, newpath + "/" + self.fileName)
    
    def getFileType(self):
        return self._fileType
    
    def getFileName(self):
        return os.path.basename(self._filepath)
    
    def setFileName(self, newName):
        os.rename(self.filepath, os.path.dirname(self._filepath) + "/" + newName)
        
    def getFileWeight(self):
        return self._fileWeight
    
    @QtCore.pyqtSlot(result=QtCore.QObject)
    def getFileSize(self):
        #Get information from Tuttle
        from pyTuttle import tuttle
        g = tuttle.Graph()
        node = g.createNode(getBestPlugin.getBestReader(self._fileExtension), self._fileImg).asImageEffectNode()
        g.setup()
        timeMin = self.getFileTime().min
        g.setupAtTime(timeMin)
        size = node.getRegionOfDefinition(timeMin)
        fileSize = QObjectListModel(self)
        fileSize.append(size.x2 - size.x1)
        fileSize.append(size.x2 - size.y1)
        return fileSize
    
    def getFileTime(self):
        from pyTuttle import tuttle
        g = tuttle.Graph()
        node = g.createNode(getBestPlugin.getBestReader(self._fileExtension), self._filepath).asImageEffectNode()
        g.setup()
        time = node.getTimeDomain()
        return time
    
    def getFileExtension(self):
        return self._fileExtension
        
    def getSelected(self):
        return self._isSelected
    
    def setSelected(self, isSelected):
        self._isSelected = isSelected
        self.isSelectedChange.emit()
        
    def getFileImg(self):
        return self._fileImg
    
    def getSequence(self):
        return self._seq

    filepath = QtCore.pyqtProperty(str, getFilepath, setFilepath, constant=True)
    fileType = QtCore.pyqtProperty(str, getFileType, constant=True)
    fileName = QtCore.pyqtProperty(str, getFileName, setFileName, constant=True)
    #Infos about the file
    fileWeight = QtCore.pyqtProperty(float, getFileWeight, constant=True)
    fileExtension = QtCore.pyqtProperty(str, getFileExtension, constant=True)
    
    isSelectedChange = QtCore.pyqtSignal()
    isSelected = QtCore.pyqtProperty(bool, getSelected, setSelected, notify=isSelectedChange)
    fileImg = QtCore.pyqtProperty(str, getFileImg, constant=True)
    seq = QtCore.pyqtProperty(QtCore.QObject, getSequence, constant=True)


class FileModelBrowser(QtQuick.QQuickItem):
    """Class FileModelBrowser"""
    
    _folder = ""
    _firstFolder = ""
    
    def __init__(self, parent=None):
        super(FileModelBrowser, self).__init__(parent)
        self._fileItemsModel = QObjectListModel(self)
        self._showSeq = False
    
    def getFolder(self):
        return self._folder

    @QtCore.pyqtSlot(result=str)
    def getFirstFolder(self):
        return self._firstFolder

    @QtCore.pyqtSlot(str)
    def setFirstFolder(self, firstFolder):
        self._firstFolder = firstFolder
    
    def setFolder(self, folder):
        self._folder = folder
        self.updateFileItems(folder)
        self.folderChanged.emit()
  
    @QtCore.pyqtSlot(str)
    def createFolder(self, path):
        os.mkdir(path)
        self.updateFileItems(self._folder)
        
    @QtCore.pyqtSlot(int, str)
    def moveItem(self, index, newpath):
        if index < len(self._fileItems):
            self._fileItems[index].filepath = newpath
        self.updateFileItems(self._folder)
    
    def getFolderExists(self):
        return os.path.exists(self._folder)
    
    def getParentFolder(self):
        return os.path.dirname(self._folder)

    folderChanged = QtCore.pyqtSignal()
    folder = QtCore.pyqtProperty(str, getFolder, setFolder, notify=folderChanged)
    exists = QtCore.pyqtProperty(bool, getFolderExists, notify=folderChanged)
    parentFolder = QtCore.pyqtProperty(str, getParentFolder, constant=True)
    
    @QtCore.pyqtSlot(str)
    def updateFileItems(self, folder):
        self._fileItems = []
        self._fileItemsModel.clear()
        allDirs = []
        allFiles = []
        allSeqs = []
        
        if self._showSeq:
            items = sequenceParser.browse(folder)
            dirs = [item._filename for item in items if item._type == sequenceParser.eTypeFolder]
            seqs = [item._sequence for item in items if item._type == sequenceParser.eTypeSequence]
            files = [item._filename for item in items if item._type == sequenceParser.eTypeFile]
                    
            for d in dirs:
                if not d.startswith("."):
                    allDirs.append(FileItem(folder, d, FileItem.Type.Folder, "", True))
            
            if self._nameFilter == "*":
                for s in seqs:
                    (_, extension) = os.path.splitext(s.getStandardPattern())
                    try:
                        supported = True
                    except Exception:
                        supported = False
                    allSeqs.append(FileItem(folder, s.getStandardPattern(), FileItem.Type.Sequence, s, supported))
                        
                    for f in files:
                        if f.startswith("."):
                            # Ignore hidden files by default
                            # TODO: need an option for that
                            continue
                        (_, extension) = os.path.splitext(f)
                        try:
                            # getBestReader will raise an exception if the file extension is not supported.
                            getBestPlugin.getBestReader(extension)
                            supported = True
                        except Exception:
                            supported = False
                        allFiles.append(FileItem(folder, f, FileItem.Type.File, "", supported))
                    
            else:
                for s in seqs:
                    (_, extension) = os.path.splitext(s.getStandardPattern())
                    supported = True
                    try:
                        getBestPlugin.getBestReader(extension)
                    except Exception:
                        supported = False
                    if supported and not s.getStandardPattern().startswith("."):
                        allSeqs.append(FileItem(folder, s.getStandardPattern(), FileItem.Type.Sequence, s, supported))
                    
                for f in files:
                    if f.startswith("."):
                        # Ignore hidden files by default
                        # TODO: need an option for that
                        continue
                    (_, extension) = os.path.splitext(f)
                    try:
                        # getBestReader will raise an exception if the file extension is not supported.
                        getBestPlugin.getBestReader(extension)
                        allFiles.append(FileItem(folder, f, FileItem.Type.File, "", True))
                    except Exception:
                        pass
                                      
            allDirs.sort(key=lambda fileItem: fileItem.fileName.lower())
            allFiles.sort(key=lambda fileItem: fileItem.fileName.lower())
            allSeqs.sort(key=lambda fileItem: fileItem.fileName.lower())
            self._fileItems = allDirs + allFiles + allSeqs
                    
        else:
            try:
                _, dirs, files = next(os.walk(folder))
                    
                for d in dirs:
                    if not d.startswith("."):
                        allDirs.append(FileItem(folder, d, FileItem.Type.Folder, "", True))
                
                if self._nameFilter == "*":
                    for f in files:
                        if f.startswith("."):
                            # Ignore hidden files by default
                            # TODO: need an option for that
                            continue
                        (_, extension) = os.path.splitext(f)
                        try:
                            # getBestReader will raise an exception if the file extension is not supported.
                            getBestPlugin.getBestReader(extension)
                            supported = True
                        except Exception:
                            supported = False
                        allFiles.append(FileItem(folder, f, FileItem.Type.File, "", supported))
                        
                else:
                    for f in files:
                        if f.startswith("."):
                            # Ignore hidden files by default
                            # TODO: need an option for that
                            continue
                        (_, extension) = os.path.splitext(f)
                        try:
                            # getBestReader will raise an exception if the file extension is not supported.
                            getBestPlugin.getBestReader(extension)
                            allFiles.append(FileItem(folder, f, FileItem.Type.File, "", True))
                        except Exception:
                            pass
                              
            except Exception:
                pass
    
            allDirs.sort(key=lambda fileItem: fileItem.fileName.lower())
            allFiles.sort(key=lambda fileItem: fileItem.fileName.lower())
            self._fileItems = allDirs + allFiles

        self._fileItemsModel.setObjectList(self._fileItems)
                
    @QtCore.pyqtSlot(str, result=QtCore.QObject)
    def getFilteredFileItems(self, fileFilter):
        suggestions = []

        try:
            _, dirs, _ = next(os.walk(os.path.dirname(fileFilter)))
            dirs = sorted(dirs, key=lambda v: v.upper())
            for d in dirs:
                if d.startswith("."):
                    # Ignore hidden files by default
                    # TODO: need an option for that
                    continue
                if d.startswith(os.path.basename(fileFilter)):
                    suggestions.append(FileItem(os.path.dirname(fileFilter), d, FileItem.Type.Folder, "", True))
            
        except Exception:
            pass
        suggestions.sort(key=lambda fileItem: fileItem.fileName.lower())
        
        suggestionsQt = QObjectListModel(self)
        suggestionsQt.setObjectList(suggestions)
        return suggestionsQt
    
    _fileItems = []
    _fileItemsModel = None
    
    @QtCore.pyqtSlot(str, int)
    def changeFileName(self, newName, index):
        if index < len(self._fileItems):
            self._fileItems[index].fileName = newName
        self.updateFileItems(self._folder)
            
    @QtCore.pyqtSlot(int)
    def deleteItem(self, index):
        if index < len(self._fileItems):
            if self._fileItems[index].fileType == FileItem.Type.Folder:
                import shutil
                shutil.rmtree(self._fileItems[index].filepath)
            if self._fileItems[index].fileType == FileItem.Type.File:
                os.remove(self._fileItems[index].filepath)
        self.updateFileItems(self._folder)
                
    @QtCore.pyqtSlot(result=QtCore.QObject)
    def getSelectedItems(self):
        selectedList = QObjectListModel(self)
        for item in self._fileItems:
            if item.isSelected == True:
                selectedList.append(item)

        return selectedList
    
    def getFileItems(self):
        return self._fileItemsModel
    
    @QtCore.pyqtSlot(int)
    def selectItem(self, index):
        for item in self._fileItems:
            item.isSelected = False
        if index < len(self._fileItems):
            self._fileItems[index].isSelected = True

    @QtCore.pyqtSlot(int)
    def selectItems(self, index):
        if index < len(self._fileItems):
            self._fileItems[index].isSelected = True
            
    @QtCore.pyqtSlot(int, int)
    def selectItemsByShift(self, begin, end):
        if(begin > end):
            tmp = begin
            begin = end
            end = tmp
        for i in range(begin, end + 1):
            if i < len(self._fileItems):
                self._fileItems[i].isSelected = True
    
    def getFilter(self):
        return self._nameFilter
     
    def setFilter(self, nameFilter):
        self._nameFilter = nameFilter
        self.updateFileItems(self._folder)
        self.nameFilterChange.emit()
        
    def getSize(self):
        return len(self._fileItems) - 1

    fileItems = QtCore.pyqtProperty(QtCore.QObject, getFileItems, notify=folderChanged)
    nameFilterChange = QtCore.pyqtSignal()
    nameFilter = QtCore.pyqtProperty(str, getFilter, setFilter, notify=nameFilterChange)
    size = QtCore.pyqtProperty(int, getSize, constant=True)
    
    def getShowSeq(self):
        return self._showSeq
    
    def setShowSeq(self, checkSeq):
        self._showSeq = checkSeq
        self.updateFileItems(self._folder)
        self.showSeqChanged.emit()
    
    showSeqChanged = QtCore.pyqtSignal()
    showSeq = QtCore.pyqtProperty(bool, getShowSeq, setShowSeq, notify=showSeqChanged)

    @QtCore.pyqtSlot(result=bool)
    def isEmpty(self):
        if (len(self._fileItems) <= 0):
            return True
        else:
            return False


# This class exists just because there are problems when a class extends 2 other classes (Singleton and QObject)
class FileModelBrowserSingleton(Singleton):

    _fileModelBrowser = FileModelBrowser()

    def get(self):
        return self._fileModelBrowser
