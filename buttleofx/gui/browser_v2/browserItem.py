import os
import logging
from datetime import datetime
from pwd import getpwuid
from stat import filemode
from multiprocessing import Process, Pool, Manager, Queue
from queue import Empty
import sys

from PyQt5 import QtCore

from pySequenceParser import sequenceParser

from pyTuttle import tuttle

from buttleofx.gui.browser_v2.sequenceWrapper import SequenceWrapper
from buttleofx.gui.browser_v2.thumbnailUtil import ThumbnailUtil
from buttleofx.gui.browser_v2.parallelThread import *


class BrowserItem(QtCore.QObject):
    # even if sequenceParser.eType exists: more flexible if modification
    class ItemType:
        file = sequenceParser.eTypeFile
        folder = sequenceParser.eTypeFolder
        sequence = sequenceParser.eTypeSequence

    class ThumbnailState:
        loading = "loading"
        built = "built"
        loadFailed = "loadFailed"
        loadCrashed = "loadCrashed"
        notSupported = "notSupported"

    thumbnailUtil = ThumbnailUtil()

    statusChanged = QtCore.pyqtSignal()
    selectedChanged = QtCore.pyqtSignal()
    fileChanged = QtCore.pyqtSignal()
    thumbnailChanged = QtCore.pyqtSignal()

    imgFileThumbnailDefault = 'img/file-icon.png'
    imgFolderThumbnailDefault = 'img/folder-icon.png'
    imgErrorThumbnail = 'img/folder-icon.png'

    def __init__(self, sequenceParserItem, isBuildThumbnail=True):
        super(BrowserItem, self).__init__()
        self._path = sequenceParserItem.getAbsoluteFilepath()
        self._typeItem = sequenceParserItem.getType()
        self._actionStatus = 0  # gui operations(ActionManager), int for the moment
        self._isSelected = False
        self._sequence = None
        self._fileExtension = ''

        if self.isFile():
            self._fileExtension = os.path.splitext(self._path)[1]
        elif self.isSequence():
            self._sequence = SequenceWrapper(sequenceParserItem, self._path)

        self._isSupported = self.isSupportedFromTuttle()
        self._lastModification = self.getLastModification_fileSystem()
        self._permissions = self.getPermissions_fileSystem()
        self._owner = self.getOwner_fileSystem()
        self._weight = self.getWeight_fileSystem()
        self._imgPath = self.getRealImgPath()

        # we need to share some data between process while computing thumbnail
        # process inside a thread: parallel thread for control on the process result + kill process if needed
        self._isBuildThumbnail = isBuildThumbnail
        self._thumbnailData = Manager().dict()
        self._thumbnailData['path'] = ''
        self._thumbnailData['state'] = BrowserItem.ThumbnailState.loading
        self._thumbnailProcess = Process(target=self.buildThumbnailProcess, args=(self._imgPath,))
        self._thumbnailThread = ParallelThread()
        self._queueThumbnailBuildResult = Queue()
        if isBuildThumbnail:
            self.startBuildThumbnail()

        logging.debug('BrowserItem constructor - file:%s, type:%s' % (self._path, self._typeItem))

    def __del__(self):
        if self._isBuildThumbnail:
            if self._thumbnailThread.getWorkerThread():
                self._thumbnailThread.getWorkerThread().terminate()
            logging.debug("thumbnail process terminated")

    def startBuildThumbnail(self):
        self._isBuildThumbnail = True
        if not self._thumbnailProcess.is_alive():
            self._thumbnailThread.start(self.buildThumbnailParallel)

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

    def getThumbnailPath(self):
        return self._thumbnailData["path"]

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
        except Exception as e:
            logging.debug(e)
            return "-"

    def getPermissions_fileSystem(self):
        try:
            path = self._sequence.getFirstFilePath() if self.isSequence() else self._path
            return filemode(os.stat(path).st_mode)
        except Exception as e:
            logging.debug(e)
            return "-"

    def getLastModification_fileSystem(self):
        try:
            path = self._sequence.getFirstFilePath() if self.isSequence() else self._path
            return datetime.fromtimestamp(os.stat(path).st_mtime).strftime("%c")
        except Exception as e:
            logging.debug(e)
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
        return False

    def getRealImgPath(self):
        if self.isFolder():
            return BrowserItem.imgFolderThumbnailDefault
        if self.isSequence():
            return self._sequence.getFirstFilePath()
        if self.isSupportedFromTuttle():
            return self._path
        return BrowserItem.imgFileThumbnailDefault

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

    def updateThumbnailState(self, state):
        # setter used inside the parallel thread
        self._thumbnailData["state"] = state

        if self.isFolder():
            self._thumbnailData["path"] = BrowserItem.imgFolderThumbnailDefault
        else:
            if state == BrowserItem.ThumbnailState.notSupported:
                self._thumbnailData["path"] = BrowserItem.imgFileThumbnailDefault
            elif state == BrowserItem.ThumbnailState.loadCrashed:
                self._thumbnailData["path"] = BrowserItem.imgFileThumbnailDefault
            elif state == BrowserItem.ThumbnailState.loadFailed:
                self._thumbnailData["path"] = "img/parent_hover.png"
            elif state == BrowserItem.ThumbnailState.loading:
                self._thumbnailData["path"] = "img/refresh_hover.png"
            elif state == BrowserItem.ThumbnailState.built:
                try:
                    self._thumbnailData["path"] = BrowserItem.thumbnailUtil.getThumbnailPath(self._imgPath)
                except Exception as e:
                    logging.debug(str(e))
                    self._thumbnailData["path"] = BrowserItem.imgFileThumbnailDefault
        self.thumbnailChanged.emit()

    def getThumbnailState(self):
        return self._thumbnailData["state"]

    def buildThumbnailParallel(self):
        """
            Method launched inside the parallel thread
        """
        if self.isFolder():
            self.updateThumbnailState(BrowserItem.ThumbnailState.built)
            return
        if not self.isSupported():
            self.updateThumbnailState(BrowserItem.ThumbnailState.notSupported)
            logging.debug("Thumbnail not supported for %s" % self.path)
            return

        # thumbnail already exists ?
        try:
            if os.path.exists(BrowserItem.thumbnailUtil.getThumbnailPath(self._imgPath)):
                self.updateThumbnailState(BrowserItem.ThumbnailState.built)
                return
        except Exception as e:
            logging.debug(str(e))

        self.updateThumbnailState(BrowserItem.ThumbnailState.loading)
        self._thumbnailProcess.start()
        self._thumbnailProcess.join(timeout=10)

        if self._thumbnailProcess.exitcode != 0:
            logging.debug("Thumbnail crash for %s" % self.path)
            self.updateThumbnailState(BrowserItem.ThumbnailState.loadCrashed)
        else:
            try:
                resultBuild = self._queueThumbnailBuildResult.get(timeout=1)
            except Empty as e:
                logging.debug(str(e))
                return

            self.updateThumbnailState(resultBuild)

    def buildThumbnailProcess(self, imgPath):
        """
            Method launched inside the process wrapped into the parallel thread
        """
        try:
            self.thumbnailUtil.getThumbnail(imgPath)
            self._queueThumbnailBuildResult.put(BrowserItem.ThumbnailState.built)
            logging.debug("Thumbnail built for %s" % self.path)
        except Exception as e:
            self._queueThumbnailBuildResult.put(BrowserItem.ThumbnailState.loadFailed)
            logging.debug("Thumbnail failed for %s" % self.path)
            logging.debug(str(e))

    # ################################### Data exposed to QML #################################### #

    isSelected = QtCore.pyqtProperty(bool, getSelected, setSelected, notify=selectedChanged)
    actionStatus = QtCore.pyqtProperty(list, getActionStatus, notify=statusChanged)

    path = QtCore.pyqtProperty(str, getPath, updatePath, notify=fileChanged)
    type = QtCore.pyqtProperty(int, getType, notify=fileChanged)
    weight = QtCore.pyqtProperty(float, getWeightFormatted, notify=fileChanged)
    pathImg = QtCore.pyqtProperty(str, getThumbnailPath, notify=thumbnailChanged)
    name = QtCore.pyqtProperty(str, getName, notify=fileChanged)
    permissions = QtCore.pyqtProperty(str, getPermissions, notify=fileChanged)
    owner = QtCore.pyqtProperty(str, getOwner, notify=fileChanged)
    thumbnailState = QtCore.pyqtProperty(str, getThumbnailState, notify=thumbnailChanged)
    sequence = QtCore.pyqtProperty(QtCore.QObject, getSequence, notify=fileChanged)