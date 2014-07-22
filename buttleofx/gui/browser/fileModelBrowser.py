import os
import logging

from pyTuttle import tuttle

from quickmamba.patterns import Singleton
from pySequenceParser import sequenceParser
from quickmamba.models import QObjectListModel

from PyQt5 import QtGui, QtCore, QtQuick
from PyQt5.QtWidgets import QWidget, QFileDialog

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

        self._filepath = os.path.join(folder, fileName)
        self._fileType = fileType
        self._isSupported = supported

        if fileType == FileItem.Type.File:
            if supported:
                self._fileImg = 'image://buttleofx/' + self._filepath
            else:
                self._fileImg = "../../img/buttons/browser/file-icon.png"

            try:
                # May throw exception on bad symlink
                self._fileWeight = os.stat(self._filepath).st_size
            except FileNotFoundError:
                self._fileWeight = 0

            self._fileExtension = os.path.splitext(fileName)[1]
            self._seq = None

        elif fileType == FileItem.Type.Folder:
            self._fileImg = "../../img/buttons/browser/folder-icon.png"
            self._seq = None
            self._fileWeight = 0.0
            self._fileExtension = ""

        elif fileType == FileItem.Type.Sequence:
            time = int(seq.getFirstTime() + (seq.getLastTime() - seq.getFirstTime()) * 0.5)
            seqPath = seq.getAbsoluteFilenameAt(time)
            if not os.path.exists(seqPath):
                time = seq.getFirstTime()
                seqPath = seq.getAbsoluteFilenameAt(time)

            seqPath = seq.getAbsoluteStandardPattern()

            if supported:
                self._fileImg = 'image://buttleofx/' + seqPath
            else:
                self._fileImg = "../../img/buttons/browser/file-icon.png"

            self._seq = SequenceWrapper(seq)
            self._fileWeight = self._seq.getWeight()
            (_, extension) = os.path.splitext(seqPath)
            self._fileExtension = extension

    @QtCore.pyqtSlot(result=str)
    def getFilepath(self):
        return self._filepath

    @QtCore.pyqtSlot(result=str)
    def getFileType(self):
        return self._fileType

    @QtCore.pyqtSlot(result=QtCore.QSizeF)
    def getImageSize(self):
        from pyTuttle import tuttle
        g = tuttle.Graph()
        node = g.createNode(tuttle.getBestReader(self._fileExtension), self._fileImg).asImageEffectNode()
        g.setup()
        timeMin = self.getFileTime().min
        g.setupAtTime(timeMin)
        rod = node.getRegionOfDefinition(timeMin)
        width = rod.x2 - rod.x1
        height = rod.y2 - rod.y1
        return QtCore.QSizeF(width, height)

    @QtCore.pyqtSlot(result=bool)
    def getSupported(self):
        return self._isSupported

    def setFilepath(self, newpath):
        import shutil
        shutil.move(self.filepath, os.path.join(newpath, self.fileName))

    def getFileName(self):
        return os.path.basename(self._filepath)

    def setFileName(self, newName):
        os.rename(self.filepath, os.path.join(os.path.dirname(self._filepath), newName))

    def getFileWeight(self):
        return self._fileWeight

    def getFileTime(self):
        from pyTuttle import tuttle
        g = tuttle.Graph()
        node = g.createNode(tuttle.getBestReader(self._fileExtension), self._filepath).asImageEffectNode()
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

    # Info about the file
    filepath = QtCore.pyqtProperty(str, getFilepath, setFilepath, constant=True)
    fileType = QtCore.pyqtProperty(str, getFileType, constant=True)
    fileName = QtCore.pyqtProperty(str, getFileName, setFileName, constant=True)
    fileWeight = QtCore.pyqtProperty(float, getFileWeight, constant=True)
    fileExtension = QtCore.pyqtProperty(str, getFileExtension, constant=True)

    imageSize = QtCore.pyqtProperty(QtCore.QSize, getImageSize, constant=True)
    isSelectedChange = QtCore.pyqtSignal()
    isSelected = QtCore.pyqtProperty(bool, getSelected, setSelected, notify=isSelectedChange)
    fileImg = QtCore.pyqtProperty(str, getFileImg, constant=True)
    seq = QtCore.pyqtProperty(QtCore.QObject, getSequence, constant=True)


class FileModelBrowser(QtQuick.QQuickItem):
    """Class FileModelBrowser"""

    _folder = ""
    _firstFolder = ""
    _fileItems = []
    _fileItemsModel = None
    _nameFilter = "*"

    def __init__(self, parent=None):
        super(FileModelBrowser, self).__init__(parent)
        self._fileItemsModel = QObjectListModel(self)
        self._showSeq = False

    ################################################## Methods exposed to QML ##################################################

    @QtCore.pyqtSlot(str, int)
    def changeFileName(self, newName, index):
        if index < len(self._fileItems):
            self._fileItems[index].fileName = newName
        self.updateFileItems(self._folder)

    @QtCore.pyqtSlot(str)
    def createFolder(self, path):
        os.mkdir(path)
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

    @QtCore.pyqtSlot(result=bool)
    def isEmpty(self):
        return not self._fileItems

    @QtCore.pyqtSlot(int, str)
    def moveItem(self, index, newpath):
        if index < len(self._fileItems):
            self._fileItems[index].filepath = newpath
        self.updateFileItems(self._folder)

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

    @QtCore.pyqtSlot(str)
    def updateFileItems(self, folder):
        self._fileItems = []
        self._fileItemsModel.clear()
        allDirs = []
        allFiles = []
        allSeqs = []

        items = sequenceParser.browse(folder)
        dirs = [item._filename for item in items if item._type == sequenceParser.eTypeFolder]
        seqs = [item._sequence for item in items if item._type == sequenceParser.eTypeSequence]
        files = [item._filename for item in items if item._type == sequenceParser.eTypeFile]

        for d in dirs:
            if d.startswith("."):
                # Ignore hidden files by default
                # TODO: need an option for that
                continue
            allDirs.append(FileItem(folder, d, FileItem.Type.Folder, "", True))

        if self._showSeq:
            for s in seqs:
                sPath = s.getStandardPattern()
                if sPath.startswith("."):
                    # Ignore hidden files by default
                    # TODO: need an option for that
                    continue
                readers = tuttle.getReaders(sPath)
                supported = bool(readers)
                if not supported and self._nameFilter != "*":
                    continue
                allSeqs.append(FileItem(folder, sPath, FileItem.Type.Sequence, s, supported))

        for f in files:
            if f.startswith("."):
                # Ignore hidden files by default
                # TODO: need an option for that
                continue
            readers = tuttle.getReaders(f)
            supported = bool(readers)
            if not supported and self._nameFilter != "*":
                continue
            allFiles.append(FileItem(folder, f, FileItem.Type.File, "", supported))

        allDirs.sort(key=lambda fileItem: fileItem.fileName.lower())
        allFiles.sort(key=lambda fileItem: fileItem.fileName.lower())
        allSeqs.sort(key=lambda fileItem: fileItem.fileName.lower())
        self._fileItems = allDirs + allFiles + allSeqs

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

    @QtCore.pyqtSlot(result=str)
    def getFirstFolder(self):
        return self._firstFolder

    @QtCore.pyqtSlot(result=QtCore.QObject)
    def getFileItems(self):
        return self._fileItemsModel

    @QtCore.pyqtSlot(result=QtCore.QObject)
    def getLastSelected(self):
        for item in reversed(self._fileItems):
            if item.isSelected == True:
                return item
        return None

    @QtCore.pyqtSlot(result=QtCore.QObject)
    def getSelectedItems(self):
        selectedList = QObjectListModel(self)
        for item in self._fileItems:
            if item.isSelected == True:
                selectedList.append(item)
        return selectedList

    @QtCore.pyqtSlot(str)
    def setFirstFolder(self, firstFolder):
        self._firstFolder = firstFolder

    ################################################## Methods private to this class ##################################################

    def getFilter(self):
        return self._nameFilter

    def getFolder(self):
        return self._folder

    def getFolderExists(self):
        return os.path.exists(self._folder)

    def getParentFolder(self):
        return os.path.dirname(self._folder)

    def getShowSeq(self):
        return self._showSeq

    def getSize(self):
        return len(self._fileItems) - 1

    def setFilter(self, nameFilter):
        self._nameFilter = nameFilter
        self.updateFileItems(self._folder)
        self.nameFilterChange.emit()

    def setFolder(self, folder):
        self._folder = folder
        self.updateFileItems(folder)
        self.folderChanged.emit()

    def setShowSeq(self, checkSeq):
        self._showSeq = checkSeq
        self.updateFileItems(self._folder)
        self.showSeqChanged.emit()

    ################################################## Data exposed to QML ##################################################

    folderChanged = QtCore.pyqtSignal()
    folder = QtCore.pyqtProperty(str, getFolder, setFolder, notify=folderChanged)
    exists = QtCore.pyqtProperty(bool, getFolderExists, notify=folderChanged)
    parentFolder = QtCore.pyqtProperty(str, getParentFolder, constant=True)

    fileItems = QtCore.pyqtProperty(QtCore.QObject, getFileItems, notify=folderChanged)
    nameFilterChange = QtCore.pyqtSignal()
    nameFilter = QtCore.pyqtProperty(str, getFilter, setFilter, notify=nameFilterChange)
    size = QtCore.pyqtProperty(int, getSize, constant=True)
    showSeqChanged = QtCore.pyqtSignal()
    showSeq = QtCore.pyqtProperty(bool, getShowSeq, setShowSeq, notify=showSeqChanged)


# This class exists just because there are problems when a class extends 2 other classes (Singleton and QObject)
class FileModelBrowserSingleton(Singleton):

    _fileModelBrowser = FileModelBrowser()

    def get(self):
        return self._fileModelBrowser
