import os
import logging
from datetime import datetime
from pwd import getpwuid
from stat import filemode

from PyQt5 import QtCore

from pySequenceParser import sequenceParser

from pyTuttle import tuttle

from buttleofx.gui.browser_v2.sequenceWrapper import SequenceWrapper


class BrowserItem(QtCore.QObject):
    # even if sequenceParser.eType exists: more flexible if modification
    class ItemType:
        file = sequenceParser.eTypeFile
        folder = sequenceParser.eTypeFolder
        sequence = sequenceParser.eTypeSequence

    _isSelected = False
    _sequence = None
    _weight = 0.0
    _fileExtension = ""
    _owner = ""
    _lastModification = ""
    _permissions = ""
    _isSupported = False

    # gui operations, int for the moment
    _actionStatus = 0

    statusChanged = QtCore.pyqtSignal()
    selectedChanged = QtCore.pyqtSignal()
    fileChanged = QtCore.pyqtSignal()

    def __init__(self, sequenceParserItem):
        super(BrowserItem, self).__init__()

        self._path = sequenceParserItem.getAbsoluteFilepath()
        self._typeItem = sequenceParserItem.getType()
        logging.debug('BrowserItem constructor - file:%s, type:%s' % (self._path, self._typeItem))

        if self.isFile():
            self._fileExtension = os.path.splitext(self._path)[1]
        elif self.isSequence():
            self._sequence = SequenceWrapper(sequenceParserItem, self._path)

        self._isSupported = self.isSupportedFromTuttle()
        self._pathImg = self.getRealPathImg()
        self._lastModification = self.getLastModification_fileSystem()
        self._permissions = self.getPermissions_fileSystem()
        self._owner = self.getOwner_fileSystem()
        self._weight = self.getWeight_fileSystem()

    def notifyAddAction(self):
        self._actionStatus += 1
        self.statusChanged.emit()

    def notifyRemoveAction(self):
        self._actionStatus -= 1
        self.statusChanged.emit()

    def getSelected(self):
        return self._isSelected

    def setSelected(self, selected):
        self._isSelected = selected
        self.selectedChanged.emit()

    def getWeight(self):
        return self._weight

    def getFileExtension(self):
        return self._fileExtension

    def getPathImg(self):
        return self._pathImg

    def getSequence(self):
        return self._sequence

    def getParentPath(self):
        return os.path.dirname(self._path)

    def getName(self):
        return os.path.basename(self._path)

    def isRemoved(self):
        return not os.path.exists(self._path)

    def getLastModification(self):
        return self._lastModification

    def updatePath(self, newPath):
        self._path = newPath
        self.fileChanged.emit()

    def updatePermissions(self):
        self._permissions = self.getPermissions_fileSystem()
        self.fileChanged.emit()

    def updateOwner(self):
        self._owner = self.getOwner_fileSystem()
        self.fileChanged.emit()

    def getOwner_fileSystem(self):
        try:
            path = self._sequence.getFirstFilePath() if self.isSequence() else self._path
            return getpwuid(os.stat(path).st_uid).pw_name
        except:
            return "-"

    def getPermissions_fileSystem(self):
        try:
            path = self._sequence.getFirstFilePath() if self.isSequence() else self._path
            return filemode(os.stat(path).st_mode)
        except:
            return "-"

    def getLastModification_fileSystem(self):
        try:
            path = self._sequence.getFirstFilePath() if self.isSequence() else self._path
            return datetime.fromtimestamp(os.stat(path).st_mtime).strftime("%c")
        except:
            return "-"

    def getWeight_fileSystem(self):
        try:
            if self.isFolder():
                return len(sequenceParser.browse(self._path))
            if self.isFile():
                return os.stat(self._path).st_size
            if self.isSequence():
                return self._sequence.getWeight()
        except Exception as e:
            logging.debug('BrowserItem.getWeight_fileSystem: %s, %s' % (self.getPath(), str(e)))

        return 0

    def getWeightFormatted(self):
        if self.isFile() or self.isSequence():
            nbFiles = " | %d Files" % (self._sequence.getNbFiles()) if self.isSequence() else ""
            suffix = "B"  # Bytes by default
            size = float(self._weight)
            for unit in ["", "K", "M", "G", "T", " P", "E", "Z"]:
                if size < 1000:
                    return "%d %s%s%s" % (size, unit, suffix, nbFiles)  # 3 numbers after comma
                size /= 1000
            return "%d %s%s%s" % (size, "Y", suffix, nbFiles)

        elif self.isFolder():
            formattedReturn = "%d %s" % (self._weight, "Element")
            return "%s%s" % (formattedReturn, 's') if self.getWeight() > 1 else formattedReturn
        else:
            return ""

    def isSupportedFromTuttle(self):
        if self.isFile() or self.isSequence():
            try:
                tuttleReaders = tuttle.getReaders(self.getName())
                logging.debug('BrowserItem.isSupportedFromTuttle - %s => %s' % (self.getPath(), str(tuttleReaders)))
                return bool(tuttleReaders)
            except Exception as e:
                logging.debug('BrowserItem.isSupportedFromTuttle - %s => %s' % (self.getPath(), str(e)))
                pass
        return False

    def getRealPathImg(self):
        if self.isSupported():
            return 'image://buttleofx/' + self._path

        if self.isFolder():
            return "img/folder-icon.png"  # default
        if self.isSequence():
            return "img/file-icon.png"  # TODO: seq icon
        if self.isFile():
            return "img/file-icon.png"
        return "img/file-icon.png"  # TODO: err


    # ############################################ Methods exposed to QML ############################################ #

    @QtCore.pyqtSlot(result=bool)
    def isFile(self):
        return self._typeItem == BrowserItem.ItemType.file

    @QtCore.pyqtSlot(result=bool)
    def isFolder(self):
        return self._typeItem == BrowserItem.ItemType.folder

    @QtCore.pyqtSlot(result=bool)
    def isSequence(self):
        return self._typeItem == BrowserItem.ItemType.sequence

    @QtCore.pyqtSlot(result=list)
    def getActionStatus(self):
        return self._actionStatus

    @QtCore.pyqtSlot(result=str)
    def getPath(self):
        return self._path

    @QtCore.pyqtSlot(result=int)
    def getType(self):
        return self._typeItem

    @QtCore.pyqtSlot(result=str)
    def getPermissions(self):
        return self._permissions

    @QtCore.pyqtSlot(result=str)
    def getOwner(self):
        return self._owner

    @QtCore.pyqtSlot(result=bool)
    def isSupported(self):
        return self._isSupported

    # ################################### Data exposed to QML #################################### #

    isSelected = QtCore.pyqtProperty(bool, getSelected, setSelected, notify=selectedChanged)
    actionStatus = QtCore.pyqtProperty(list, getActionStatus, notify=statusChanged)

    path = QtCore.pyqtProperty(str, getPath, updatePath, notify=fileChanged)
    type = QtCore.pyqtProperty(int, getType, notify=fileChanged)
    weight = QtCore.pyqtProperty(float, getWeightFormatted, notify=fileChanged)
    pathImg = QtCore.pyqtProperty(str, getPathImg, constant=True)
    name = QtCore.pyqtProperty(str, getName, notify=fileChanged)
    permissions = QtCore.pyqtProperty(str, getPermissions, notify=fileChanged)
    owner = QtCore.pyqtProperty(str, getOwner, notify=fileChanged)
