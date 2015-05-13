import os
import logging
import copy
import re
from fnmatch import fnmatch

from PyQt5 import QtCore

from pySequenceParser import sequenceParser

from quickmamba.models import QObjectListModel

from buttleofx.gui.browser_v2.browserItem import BrowserItem
from buttleofx.gui.browser_v2.browserSortOn import SortOn
from buttleofx.gui.browser_v2.threadParallel import ThreadParallel
from buttleofx.gui.browser_v2.actions.actionManager import globalActionManager


class WithBool:
    def __init__(self, value=False, notifyChange=QtCore.pyqtSignal()):
        self.value = value
        self.notifyChange = notifyChange
    
    def __bool__(self):
        return self.value
    
    def __enter__(self):
        self.value = True
        self.notifyChange.emit()
        return self
    
    def __exit__(self, type, value, traceback):
        self.notifyChange.emit()
        self.value = False


class WithMutex:
    def __init__(self, mutex):
        self.mutex = mutex
    
    def __enter__(self):
        self.mutex.lock()
        return self
    
    def __exit__(self, type, value, traceback):
        self.mutex.unlock()


class BrowserModel(QtCore.QObject):
    """
        Model of files based on pySequenceParser. It recognises files, folders and sequences.
        Possibility to filter the model: sequence, hidden dir/files or not (regexp is coming)
    """

    filterChanged = QtCore.pyqtSignal()
    sortOnChanged = QtCore.pyqtSignal()
    currentPathChanged = QtCore.pyqtSignal()
    hideDotFilesChanged = QtCore.pyqtSignal()
    modelChanged = QtCore.pyqtSignal()
    addItemSync = QtCore.pyqtSignal(object)
    clearItemsSync = QtCore.pyqtSignal()
    sortBrowserItems = QtCore.pyqtSignal()
    loadingChanged = QtCore.pyqtSignal()

    def __init__(self, path=os.path.expanduser("~/"), sync=False, showSeq=True, hideDotFiles=True, filter="*", parent=None):
        """
            Build an BrowserModel instance.
            :param parent: Qt parent
        """
        super(BrowserModel, self).__init__(parent)
        logging.debug("MODEL BUILDING")
        self._currentPath = path
        self._browserItems = []
        self._browserItemsModel = QObjectListModel(self)
        self._filter = filter
        self._hideDotFiles = hideDotFiles
        self._showSeq = showSeq
        self._sortOn = SortOn()
        self._threadParallel = ThreadParallel()
        self._actionManager = globalActionManager  # locking and search BrowserItem when updating
        self._isLoading = WithBool(False, self.loadingChanged)
        self.initSlotConnection(sync)

    def initSlotConnection(self, isSync):
        typeConnection = QtCore.Qt.DirectConnection
        if not isSync:
            typeConnection = QtCore.Qt.QueuedConnection
            self.sortBrowserItems.connect(self.onSortBrowserItems, QtCore.Qt.DirectConnection)  # sort only if async
        self.addItemSync.connect(self.onAddItemSync, typeConnection)
        self.clearItemsSync.connect(self.onClearItemsSync, typeConnection)

    def getThreadParallel(self):
        return self._threadParallel

    @QtCore.pyqtSlot(str)
    def loadData(self, recursivePattern=""):
        self._threadParallel.start(self.updateItems, argsParam=(recursivePattern,))

    @QtCore.pyqtSlot()
    def stopLoading(self):
        self._threadParallel.stop()

    def updateItems(self, recursivePattern):
        """
            Update browserItemsModel according model's current path and filter options
        """
        with WithMutex(self._threadParallel.getMutex()), self._isLoading:
            logging.debug("LOAD: %s" % self._currentPath)
            if not os.path.exists(self._currentPath):
                return

            # if no permission: try
            try:
                self.clearItemsSync.emit()
                detectOption = sequenceParser.eDetectionDefaultWithDotFile
                if self._hideDotFiles:
                    detectOption = sequenceParser.eDetectionDefault
                allItems = sequenceParser.browse(self._currentPath, detectOption, self._filter)
                self.pushBrowserItems(allItems)

                if recursivePattern.strip():
                    self.searchRecursively(recursivePattern, self)
                    logging.debug("after recurse: %s" % self._threadParallel)
            except Exception as e:
                logging.info(e)

    def pushBrowserItems(self, allItems):
        logging.debug("push data: size all items %s" % len(allItems))
        for item in allItems:
            # if the process was canceled, we stop
            if self._threadParallel.isStopped():
                break
            addItem = fnmatch(item.getFilename(), self._filter)
            if addItem and item.getType() == BrowserItem.ItemType.sequence:
                addItem = self._showSeq
            if addItem:
                itemToAdd = self._actionManager.searchItem(item.getAbsoluteFilepath())
                if not itemToAdd:
                    itemToAdd = BrowserItem(copy.copy(item))
                itemToAdd.moveToThread(self.thread())
                self.addItemSync.emit(itemToAdd)

    @QtCore.pyqtSlot(object)
    def onAddItemSync(self, bItem):
        logging.debug("Add item: %s" % bItem.getPath())
        self._browserItems.append(bItem)
        self.sortBrowserItems.emit()  # sync
        self._browserItemsModel.insert(self.searchIndexItem(bItem), bItem)
        logging.debug("model item count %i" %   self._browserItemsModel.count)

    @QtCore.pyqtSlot()
    def onClearItemsSync(self):
        self._browserItems.clear()
        self._browserItemsModel.clear()
        self.modelChanged.emit()

    @QtCore.pyqtSlot(str, object)
    def searchRecursively(self, pattern, modelRequester):
        logging.debug("Start recursive search: %s" % self._currentPath)
        if modelRequester.getThreadParallel().isStopped():
            return

        listToBrowse = self._browserItems
        if self == modelRequester:
            listToBrowse = self._browserItems.copy()  # copy: _browserItems deleted line after
            modelRequester.clearItemsSync.emit()

        for bItem in listToBrowse:  # 1st pass, all files in current dir
            logging.debug("processing %s" % bItem.getPath())
            if pattern.lower() in bItem.getName().lower():
                bItem.moveToThread(modelRequester.thread())
                modelRequester.addItemSync.emit(bItem)
                logging.debug("add items recurseSearch")

        for bItem in listToBrowse:  # 2nd pass, recurse
            if bItem.isFolder():
                logging.debug("loading recurse folder: %s" % bItem.getPath())
                recursiveModel = BrowserModel(bItem.getPath(), True, self._showSeq, self._hideDotFiles, self._filter)
                recursiveModel.loadData()
                recursiveModel.getThreadParallel().join()
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
        logging.debug('browserModel.setCurrentPath("%s")' % newCurrentPath)
        # strip path: remove spaces at the begenning and at the end
        newCurrentPathStrip = newCurrentPath.strip()
        if not newCurrentPathStrip:
            return
        self._currentPath = newCurrentPathStrip
        self.loadData()
        self.currentPathChanged.emit()

    def setCurrentPathHome(self):
        self.setCurrentPath(self.getHomePath())

    @staticmethod
    def getHomePath():
        return os.path.expanduser("~")

    def isCurrentPathExists(self):
        return os.path.exists(self._currentPath)

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
            self._browserItems.sort(key=lambda it: (it.getType(), os.path.basename(it.getPath().lower())), reverse=rev)
        elif self._sortOn.getFieldToSort() == SortOn.onSize:
            self._browserItems.sort(key=lambda it: (it.getType(), it.getWeight()), reverse=rev)

        self._browserItems.sort(key=lambda it: (it.getType()))

    def searchIndexItem(self, bItem):
        """
        :param bItem: BrowserItem
        :return: Index of bItem in self._browserItems
        """
        index = 0
        for item in self._browserItems:
            if item == bItem:
                return index
            index += 1
        return -1

    # ################################### Methods exposed to QML ############################### #

    @QtCore.pyqtSlot(str, bool)
    def setFieldToSort(self, newField, reverse=0):
        self._sortOn.setFieldToSort(newField, reverse)
        self.onSortBrowserItems()
        self.sortOnChanged.emit()
        self.modelChanged.emit()  # refresh view

    @QtCore.pyqtSlot(bool)
    def setShowSequence(self, seqBool):
        self._showSeq = seqBool
        self.filterChanged.emit()

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
        logging.debug("getItems()******************************* %s" % len(self._browserItemsModel))
        return self._browserItemsModel

    @QtCore.pyqtSlot(result=str)
    def getParentPath(self):
        parent = os.path.dirname(self.currentPath.rstrip('/'))
        return parent + ("/" if not parent else '')

    @QtCore.pyqtSlot(result=QObjectListModel)
    def getSplittedCurrentPath(self):
        """
            Used into qml navbar
            :return: absolute path and dirname for each folder in the current path into a list via QObjectList
        """
        logging.debug("BEGIN SPLITTED PATH")
        tmpList = []
        absolutePath = self._currentPath

        if not absolutePath or not ("/" in absolutePath):
            return QObjectListModel(self)

        while absolutePath and not re.search("^\/{1,}$", absolutePath):
            if os.path.exists(absolutePath):
                tmpList.append([absolutePath, os.path.basename(absolutePath)])
            absolutePath = os.path.dirname(absolutePath)
        if os.sep == "/":
            tmpList.append(["/", ""])

        tmpList.reverse()
        model = QObjectListModel(self)
        model.append(tmpList)
        logging.debug("END SPLITTED PATH")
        return model

    @QtCore.pyqtSlot(result=QtCore.QObject)
    def getListFolderNavBar(self, path=""):
        path = path.strip() if path.strip() else self._currentPath
        nameFiltering = ""
        modelToNav = self

        if not os.path.exists(path) and not os.path.exists(os.path.dirname(path)):
            return QObjectListModel(self)
        if not os.path.exists(path):
            nameFiltering = os.path.basename(path).lower()
            modelToNav = BrowserModel(path=os.path.dirname(path), sync=True, showSeq=self._showSeq, hideDotFiles=self._hideDotFiles)
            modelToNav.loadData()
            modelToNav._threadParallel.join()

        if nameFiltering:  # get dirs with filtering if exists
            tmpList = [item for item in modelToNav.getItems() if item.isFolder()
                       and item.getName().lower().startswith(nameFiltering)]
        else:
            tmpList = [item for item in modelToNav.getItems() if item.isFolder()]

        model = QObjectListModel(self)
        model.append(tmpList)
        return model

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


globalBrowserModel = BrowserModel()
