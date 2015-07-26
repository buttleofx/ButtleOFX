import os
import os.path as op
import logging
import copy
import re
from fnmatch import fnmatch

from PyQt5 import QtCore

from pySequenceParser import sequenceParser

from quickmamba.models import QObjectListModel

from buttleofx.gui.browser.browserItem import BrowserItem, ItemType
from buttleofx.gui.browser.browserSortOn import SortOn
from buttleofx.gui.browser.parallelThread import ParallelThread, WithMutex, WithBool
from buttleofx.gui.browser.actions.actionManager import globalActionManager


class BrowserModel(QtCore.QObject):
    """
        Model of files based on pySequenceParser. It recognises files, folders and sequences.
        Possibility to filter the model: sequence, hidden dir/files or not (regexp is coming)
        Async loading
    """

    filterChanged = QtCore.pyqtSignal()
    sortOnChanged = QtCore.pyqtSignal()
    currentPathChanged = QtCore.pyqtSignal()
    hideDotFilesChanged = QtCore.pyqtSignal()
    modelChanged = QtCore.pyqtSignal()
    addItemSync = QtCore.pyqtSignal(object, bool)
    clearItemsSync = QtCore.pyqtSignal()
    sortBrowserItems = QtCore.pyqtSignal()
    loadingChanged = QtCore.pyqtSignal()

    def __init__(self, path=op.expanduser("~/"), sync=False, showSeq=True, hideDotFiles=True, filterFiles="*",
                 parent=None, buildThumbnail=True):
        """
            Engine of browser user interaction with browserUI
            :param parent: Qt parent
        """
        QtCore.QObject.__init__(self, parent)
        self._currentPath = path
        self._bufferBrowserItems = []  # used when recursive process: fix async signal connection when add object
        self._browserItems = []  # used only in python side
        self._browserItemsModel = QObjectListModel(self)  # used for UI
        self._filter = filterFiles
        self._hideDotFiles = hideDotFiles
        self._showSeq = showSeq
        self._sortOn = SortOn()
        self._actionManager = globalActionManager  # used to check if item already exists in actions list
        self._parallelThread = ParallelThread()
        self._isLoading = WithBool(False, self.loadingChanged)
        self._buildThumbnails = buildThumbnail
        self._listFolderNavBar = QObjectListModel(self)
        self._isSync = sync
        self.initSlotConnection(sync)

    def initSlotConnection(self, isSync):
        """
            Init signal connections depending the async/sync loading
            We have to use signals to add or clear Browser Items: sync connection between Qt event loop and QThreads
        """
        typeConnection = QtCore.Qt.DirectConnection
        if not isSync:
            typeConnection = QtCore.Qt.QueuedConnection
            self.sortBrowserItems.connect(self.onSortBrowserItems, QtCore.Qt.DirectConnection)  # sort only if async
        self.addItemSync.connect(self.onAddItemSync, typeConnection)
        self.clearItemsSync.connect(self.onClearItemsSync, typeConnection)

    def getParallelThread(self):
        return self._parallelThread

    @QtCore.pyqtSlot(str)
    def loadData(self, recursivePattern=''):
        if self._isSync:
            self.updateItems(recursivePattern)
        else:
            self._parallelThread.start(self.updateItems, argsParam=(recursivePattern,))

    @QtCore.pyqtSlot()
    def stopLoading(self):
        self._parallelThread.stop()

    def updateItems(self, recursivePattern):
        """
            Update browserItemsModel according model's current path and filter options
        """
        with WithMutex(self._parallelThread.getMutex()), self._isLoading:
            filtersName = ''
            rootPath = self._currentPath

            # filtersName detect
            if not op.exists(self._currentPath):
                filtersName = op.basename(self._currentPath).lower()
                rootPath = op.dirname(self._currentPath)
                if not op.exists(op.dirname(self._currentPath)):
                    return

            self.clearItemsSync.emit()
            self._bufferBrowserItems.clear()
            detectOption = sequenceParser.eDetectionDefaultWithDotFile
            if self._hideDotFiles:
                detectOption = sequenceParser.eDetectionDefault

            try:
                # sequence parser excep: no permission on file ?
                allItems = list(sequenceParser.browse(rootPath, detectOption, self._filter))
                if filtersName:
                    allItems = list(filter(lambda item: item.getFilename().lower().startswith(filtersName), allItems))
                self.pushBrowserItems(allItems, not bool(recursivePattern))
            except Exception as e:
                logging.debug(str(e))
            if recursivePattern.strip():
                self.searchRecursively(recursivePattern, self)

    def seqToItems(self, itemSeq):
        items = []
        seq = itemSeq.getSequence()
        for f in seq.getFramesIterable():
            filePath = op.join(op.dirname(itemSeq.getAbsoluteFilepath()), seq.getFilenameAt(f))
            items.append(sequenceParser.Item(sequenceParser.eTypeFile, filePath))
        return items

    def pushBrowserItems(self, allItems, toModel=True):
        """
        Add item into bItem list (and to model if toModel)
        :param toModel: if recurse process: useless to add into QobjectListModel
        """
        logging.debug('BrowserModel: push to model %d items', len(allItems))
        for idx, item in enumerate(allItems):
            # if the process was canceled, we stop
            if not self._isSync and self._parallelThread.isStopped():
                break

            # if sequence and showSeq not activated: convert seq to files and add them
            if item.getType() == ItemType.sequence and not self._showSeq:
                allItems.pop(idx)
                allItems[idx:idx] = self.seqToItems(item)  # inject files in all items
                item = allItems[idx]

            addItem = fnmatch(item.getFilename(), self._filter)
            if addItem:
                itemToAdd = self._actionManager.searchItem(item.getAbsoluteFilepath())
                if not itemToAdd:
                    itemToAdd = BrowserItem(copy.copy(item), self._buildThumbnails)
                if not self._isSync:
                    itemToAdd.moveToThread(self.thread())
                self.addItemSync.emit(itemToAdd, toModel)
                self._bufferBrowserItems.append(itemToAdd)

    @QtCore.pyqtSlot(object, bool)
    def onAddItemSync(self, bItem, toModel=True):
        self._browserItems.append(bItem)
        self.sortBrowserItems.emit()
        if toModel:
            indexToInsert = self.searchIndexItem(bItem)
            if indexToInsert == -1:
                return
            self._browserItemsModel.insert(indexToInsert, bItem)

    @QtCore.pyqtSlot()
    def onClearItemsSync(self):
        for bItem in filter(lambda item: item.isSupported(), self._browserItems):
            bItem.killThumbnailProcess()
        self._browserItems.clear()
        self._browserItemsModel.clear()
        self.modelChanged.emit()

    @QtCore.pyqtSlot(str, object)
    def searchRecursively(self, pattern, modelRequester):
        """
        Process a recursive search. Disable thumbnail build for sub BrowserModel.

        :param pattern: user input search pattern
        :param modelRequester: main model which starts the recursive search
        """
        logging.debug("Start recursive search: %s", self._currentPath)
        if modelRequester.getParallelThread().isStopped():
            return

        listToBrowse = self._bufferBrowserItems
        # Clear on the first level
        if self == modelRequester:
            modelRequester.clearItemsSync.emit()

        for bItem in listToBrowse:  # 1st pass, all files in current dir
            logging.debug("processing %s" % bItem.getPath())
            if pattern.lower() in bItem.getName().lower():
                bItem.moveToThread(modelRequester.thread())
                # Build thumbnails manually only on matching files
                bItem.startBuildThumbnail()
                modelRequester.addItemSync.emit(bItem, True)

        for bItem in listToBrowse:  # 2nd pass, recurse
            if not modelRequester._isSync and modelRequester.getParallelThread().isStopped():
                return
            if bItem.isFolder():
                # Do not compute thumbnails on all elements, but only manually on matching files.
                recursiveModel = BrowserModel(bItem.getPath(), True, self._showSeq, self._hideDotFiles, self._filter, buildThumbnail=False)
                # Browse items for this folder and fill model
                recursiveModel.loadData()
                # Launch a search on all sub directories
                recursiveModel.searchRecursively(pattern.lower(), modelRequester)

    def getFilter(self):
        return self._filter

    def setFilter(self, newFilter):
        self._filter = newFilter
        self.loadData()
        self.filterChanged.emit()

    def getCurrentPath(self):
        return self._currentPath

    @QtCore.pyqtSlot(str)
    def setCurrentPath(self, newCurrentPath):
        newCurrentPath = newCurrentPath.strip()
        if not newCurrentPath:
            return

        logging.debug('browserModel.setCurrentPath("%s")', newCurrentPath)
        self._currentPath = newCurrentPath
        self.loadData()
        self.refresh_listFolderNavbar()
        self.currentPathChanged.emit()

    def setCurrentPathHome(self):
        self.setCurrentPath(self.getHomePath())

    @staticmethod
    def getHomePath():
        return op.expanduser("~")

    def isCurrentPathExists(self):
        return op.exists(self._currentPath)

    def isHiddenDotFiles(self):
        return self._hideDotFiles

    def setHideDotFiles(self, hide):
        self._hideDotFiles = hide
        self.loadData()
        self.hideDotFilesChanged.emit()

    def getFieldToSort(self):
        return self._sortOn.getFieldToSort()

    def isSortReversed(self):
        return self._sortOn.isReversed()

    @QtCore.pyqtSlot()
    def onSortBrowserItems(self):
        rev = self._sortOn.isReversed()
        if self._sortOn.getFieldToSort() == SortOn.onName:
            self._browserItems.sort(key=lambda it: (it.getType(), op.basename(it.getPath().lower())), reverse=rev)
        elif self._sortOn.getFieldToSort() == SortOn.onSize:
            self._browserItems.sort(key=lambda it: (it.getType(), it.getWeight()), reverse=rev)

        # sort by folder, file
        self._browserItems.sort(key=lambda it: (it.getType()))  # TODO: check needed

    def searchIndexItem(self, bItem):
        """
        :param bItem: BrowserItem
        :return: Index of bItem in self._browserItems
        """
        try:
            return self._browserItems.index(bItem)
        except Exception as e:
            logging.debug(str(e))
            return -1
    # ################################### Methods exposed to QML ############################### #

    @QtCore.pyqtSlot(str, bool)
    def setFieldToSort(self, newField, reverse=False):
        self._sortOn.setFieldToSort(newField, reverse)
        self.onSortBrowserItems()
        self.sortOnChanged.emit()
        self.loadData()

    @QtCore.pyqtSlot(bool)
    def setShowSequence(self, seqBool):
        self._showSeq = seqBool
        self.filterChanged.emit()
        self.loadData()

    @QtCore.pyqtSlot(result=bool)
    def isShownSequence(self):
        return self._showSeq

    @QtCore.pyqtSlot(result=bool)
    def isLoading(self):
        return self._isLoading.value

    def setLoading(self, loading):
        self._isLoading.value = loading
        self.loadingChanged.emit()

    @QtCore.pyqtSlot(result=QtCore.QObject)
    def getItemsSelected(self):
        items = QObjectListModel(self)
        items.append([item for item in self._browserItems if item.getSelected()])
        return items

    @QtCore.pyqtSlot(result=QtCore.QObject)
    def getItems(self):
        return self._browserItemsModel

    @QtCore.pyqtSlot(result=str)
    def getParentPath(self):
        parent = op.dirname(self._currentPath.rstrip('/'))
        return parent + ("/" if not parent else '')

    @QtCore.pyqtSlot(result=QObjectListModel)
    def getSplittedCurrentPath(self):
        """
            Used into qml navbar breadcrum
            :return: absolute path and dirname for each folder in the current path into a list via QObjectList
        """
        tmpList = []
        absolutePath = self._currentPath

        if not absolutePath or not ('/' in absolutePath):
            return QObjectListModel(self)

        # if op.dirname('///') -> '///'=> regex
        while not re.search('^/+$', absolutePath) and absolutePath:
            if op.exists(absolutePath):
                tmpList.insert(-(len(tmpList) + 1), [absolutePath, op.basename(absolutePath)])
            absolutePath = op.dirname(absolutePath)
        tmpList.insert(-(len(tmpList) + 1), ['/', ''])

        model = QObjectListModel(self)
        model.append(tmpList)
        return model

    @QtCore.pyqtSlot(result=QObjectListModel)
    def getListFolderNavBar(self):
        return self._listFolderNavBar

    def refresh_listFolderNavbar(self):
        """
            :return: Model of folder suggestions in path field (qml), according the current path: [[dirname, absPath], ..]
        """
        self._listFolderNavBar = QObjectListModel(self)
        dirs = []
        rootPath = self.currentPath
        filterDir = ''

        if not op.exists(self.currentPath):
            filterDir = op.basename(rootPath).lower()
            rootPath = op.dirname(rootPath)
        if not op.exists(op.dirname(rootPath)):
            return

        try:
            for dirname in next(os.walk(rootPath))[1]:
                if not dirname.lower().startswith(filterDir) or (self._hideDotFiles and dirname.startswith('.')):
                    continue
                dirs.append([dirname, op.join(rootPath, dirname)])
            dirs.sort(key=lambda x: x[0])
        except Exception as e:
            logging.debug(str(e))

        self._listFolderNavBar.append(dirs)

    @QtCore.pyqtSlot(result=QObjectListModel)
    def getSelectedItems(self):
        model = QObjectListModel(self)
        model.append([item for item in self._browserItems if item.getSelected()])
        return model

    @QtCore.pyqtSlot()
    def refresh(self):
        self.loadData()

    @QtCore.pyqtSlot()
    def unselectAllItems(self):
        for bItem in self._browserItems:
            bItem.setSelected(False)

    @QtCore.pyqtSlot()
    def selectAllItems(self):
        for bItem in self._browserItems:
            bItem.setSelected(True)

    @QtCore.pyqtSlot(int)
    def selectItem(self, index):
        self.unselectAllItems()
        if index in range(len(self._browserItems)):
            self._browserItems[index].setSelected(True)

    @QtCore.pyqtSlot(int)
    def selectItemTo(self, index):
        if not len(self._browserItems) or index < 0 or index > len(self._browserItems)-1:
            return

        firstSelected = 0
        for i, bItem in enumerate(self._browserItems):
            if bItem.getSelected():
                firstSelected = i
                break

        if firstSelected > index:
            firstSelected, index = index, firstSelected

        for i in range(firstSelected, index+1):
            self._browserItems[i].setSelected(True)

    # ############################################# Data exposed to QML ############################################# #

    currentPath = QtCore.pyqtProperty(str, getCurrentPath, setCurrentPath, notify=currentPathChanged)
    currentPathExists = QtCore.pyqtProperty(bool, isCurrentPathExists, notify=currentPathChanged)
    fileItems = QtCore.pyqtProperty(QtCore.QObject, getItems, notify=modelChanged)
    parentFolder = QtCore.pyqtProperty(str, getParentPath, notify=currentPathChanged)
    showSequence = QtCore.pyqtProperty(bool, isShownSequence, setShowSequence, notify=filterChanged)
    filter = QtCore.pyqtProperty(str, getFilter, setFilter, notify=filterChanged)

    hideDotFiles = QtCore.pyqtProperty(bool, isHiddenDotFiles, setHideDotFiles, notify=hideDotFilesChanged)
    splittedCurrentPath = QtCore.pyqtProperty(QObjectListModel, getSplittedCurrentPath, notify=currentPathChanged)
    listFolderNavBar = QtCore.pyqtProperty(QtCore.QObject, getListFolderNavBar, notify=currentPathChanged)
    sortOn = QtCore.pyqtProperty(str, getFieldToSort, notify=sortOnChanged)
    selectedItems = QtCore.pyqtProperty(QObjectListModel, getSelectedItems, notify=modelChanged)
    loading = QtCore.pyqtProperty(bool, isLoading, notify=loadingChanged)


globalBrowser = BrowserModel()
globalBrowserDialog = BrowserModel()