import os
import logging
from datetime import datetime
from pwd import getpwuid
from stat import filemode
from multiprocessing import Process, Pool, Manager, Queue, ProcessError
from threading import Lock

from PyQt5 import QtCore

from pySequenceParser import sequenceParser

from pyTuttle import tuttle

from buttleofx.gui.browser_v2.sequenceWrapper import SequenceWrapper
from buttleofx.gui.browser_v2.thumbnailUtil import ThumbnailUtil, thumbnailPool


class ItemType:
    """
    Even if sequenceParser.eType exists: more flexible if modification
    """
    file = sequenceParser.eTypeFile
    folder = sequenceParser.eTypeFolder
    sequence = sequenceParser.eTypeSequence


class ThumbnailState:
    loading = "loading"
    built = "built"
    loadFailed = "loadFailed"
    loadCrashed = "loadCrashed"
    notSupported = "notSupported"


class BrowserItem(QtCore.QObject):
    thumbnailUtil = ThumbnailUtil()  # warning: use as class attribute, tuttle.core().preload(False) at init

    statusChanged = QtCore.pyqtSignal()
    selectedChanged = QtCore.pyqtSignal()
    fileChanged = QtCore.pyqtSignal()
    thumbnailChanged = QtCore.pyqtSignal()

    imgFileThumbnailDefault = 'img/file-icon.png'
    imgFolderThumbnailDefault = 'img/folder-icon.png'
    imgErrorThumbnail = 'img/folder-icon.png'

    def __init__(self, sequenceParserItem, isBuildThumbnail=True):
        QtCore.QObject.__init__(self)
        self._path = sequenceParserItem.getAbsoluteFilepath()
        self._typeItem = sequenceParserItem.getType()
        self._actionStatus = 0  # gui operations(ActionManager) on this browser item, int for the moment
        self._isSelected = False
        self._sequence = SequenceWrapper(sequenceParserItem, self._path) if self.isSequence() else None
        self._fileExtension = os.path.splitext(self._path)[1] if self.isFile() else ''

        self._isSupported = self.isSupportedFromTuttle()
        self._lastModification = self.getLastModification_fileSystem()
        self._permissions = self.getPermissions_fileSystem()
        self._owner = self.getOwner_fileSystem()
        self._weight = self.getWeight_fileSystem()
        self._imgPath = self.getRealImgPath()

        self._isBuildThumbnail = isBuildThumbnail
        self._thumbnailPath = ''
        self._thumbnailState = ThumbnailState.loading
        self._thumbnailProcess = Process(target=self.buildThumbnailProcess, args=(self._imgPath,))
        self._thumbnailHash = BrowserItem.thumbnailUtil.getThumbnailPath(self._imgPath) if not self.isFolder() else ''
        self._thumbnailMutex = Lock()
        self._killThumbnailFlag = False
        self.initThumbnailData()

        if not self.isFolder() and self._isSupported and isBuildThumbnail:
            thumbnailPool.apply_async(self.startBuildThumbnail)

        logging.debug('BrowserItem constructor - file:%s, type:%s' % (self._path, self._typeItem))

    def initThumbnailData(self):
        """
        Init thumbnail data according type and is supported from tuttle
        """
        if self.isFolder():
            self._thumbnailPath = BrowserItem.imgFolderThumbnailDefault
            self._thumbnailState = ThumbnailState.built
        elif not self._isSupported:
            self._thumbnailPath = BrowserItem.imgFileThumbnailDefault
            self._thumbnailState = ThumbnailState.built

    def killThumbnailProcess(self):
        if self._killThumbnailFlag:
            return

        self._killThumbnailFlag = True
        if not self._thumbnailProcess.is_alive():
            logging.debug('killThumbnail process not alive %s' % self.path)
            return
        try:
            self._thumbnailProcess.terminate()
        except ProcessError as e:
            logging.debug(str(e))
        logging.debug('process for %s terminated' % self.path)

    def startBuildThumbnail(self):
        self._thumbnailMutex.acquire()
        if self._killThumbnailFlag:
            self._thumbnailMutex.release()
            return
        self._isBuildThumbnail = True
        if not self._thumbnailProcess.is_alive():
            self.buildThumbnailParallel()
        self._thumbnailMutex.release()

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
        return self._thumbnailPath

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
        return self._typeItem == ItemType.file

    @QtCore.pyqtSlot(result=bool)
    def isFolder(self):
        return self._typeItem == ItemType.folder

    @QtCore.pyqtSlot(result=bool)
    def isSequence(self):
        return self._typeItem == ItemType.sequence

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
        # setter used inside the ThreadPool
        self._thumbnailState = state
        if state == ThumbnailState.notSupported:
            self._thumbnailPath = BrowserItem.imgFileThumbnailDefault
        elif state == ThumbnailState.loadCrashed:
            self._thumbnailPath = 'img/del.png'  # TODO: beautiful img
        elif state == ThumbnailState.loadFailed:
            self._thumbnailPath = "img/del.png"  # TODO: beautiful img
        elif state == ThumbnailState.loading:
            self._thumbnailPath = "img/refresh_hover.png"
        elif state == ThumbnailState.built:
            self._thumbnailPath = BrowserItem.thumbnailUtil.getThumbnailPath(self._imgPath)
        self.thumbnailChanged.emit()

    def getThumbnailState(self):
        return self._thumbnailState

    def buildThumbnailParallel(self):
        """
            Method launched inside the ThreadPool
        """
        if not self.isSupported():
            self.updateThumbnailState(ThumbnailState.notSupported)
            logging.debug("Thumbnail not supported for %s" % self.path)
            return

        # thumbnail already exists ?
        if os.path.exists(self._thumbnailHash):
            self.updateThumbnailState(ThumbnailState.built)
            return

        if self._killThumbnailFlag:
            self.updateThumbnailState(ThumbnailState.loadFailed)
            return

        self.updateThumbnailState(ThumbnailState.loading)
        self._thumbnailProcess.start()
        self._thumbnailProcess.join(timeout=10)

        if self._thumbnailProcess.exitcode != 0:
            logging.debug("Thumbnail crash or exceed the max timeout for %s" % self.path)
            self.updateThumbnailState(ThumbnailState.loadCrashed)
        else:
            if os.path.exists(self._thumbnailHash):
                self.updateThumbnailState(ThumbnailState.built)
            else:
                self.updateThumbnailState(ThumbnailState.loadFailed)
        if self._thumbnailProcess.is_alive():
            self._thumbnailProcess.terminate()

    def buildThumbnailProcess(self, imgPath):
        """
            Method launched inside the process wrapped into the ThreadPool
        """
        try:
            BrowserItem.thumbnailUtil.getThumbnail(imgPath)
            logging.debug("Thumbnail built for %s" % self.path)
        except Exception as e:
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
    folder = QtCore.pyqtProperty(bool, isFolder, constant=True)