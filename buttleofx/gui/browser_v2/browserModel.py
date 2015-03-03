import os
from PyQt5 import QtCore
from fnmatch import fnmatch
from pySequenceParser import sequenceParser
from buttleofx.gui.browser_v2.browserItem import BrowserItem
from buttleofx.gui.browser_v2.browserSortOn import SortOn
from buttleofx.gui.browser_v2.threadWrapper import ThreadWrapper
from buttleofx.gui.browser_v2.actions.worker import Worker
from buttleofx.gui.browser_v2.actions.actionManager import ActionManagerSingleton
from quickmamba.models import QObjectListModel
from quickmamba.patterns import Singleton
import copy
import re


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

    def __init__(self, path="", sync=False, recursivePattern="", showSeq=True, hideDotFiles=True, filter="*", parent=None):
        """
            Build an BrowserModel instance.
            :param parent: Qt parent
        """
        super(BrowserModel, self).__init__(parent)
        self._debugMode = False
        self.debug("MODEL BUILDING")
        self._currentPath = ""
        self._browserItems = []
        self._browserItemsModel = QObjectListModel(self)
        self._filter = filter
        self._hideDotFiles = hideDotFiles
        self._showSeq = showSeq
        self._sortOn = SortOn()
        self._threadLoading = ThreadWrapper()
        self._actionManager = ActionManagerSingleton.get()  # locking and search BrowserItem when updating
        self._currentPath = path.strip() if path.strip() else os.path.expanduser("~/")
        self._isLoading = False
        self.initSlotConnection(sync)
        self.loadData(recursivePattern)

    def debug(self, *output):
        if self._debugMode:
            print(*output)

    def initSlotConnection(self, isSync):
        typeConnection = QtCore.Qt.DirectConnection
        if not isSync:
            typeConnection = QtCore.Qt.QueuedConnection
            self.sortBrowserItems.connect(self.onSortBrowserItems, QtCore.Qt.DirectConnection)  # sort only if async
        self.addItemSync.connect(self.onAddItemSync, typeConnection)
        self.clearItemsSync.connect(self.onClearItemsSync, typeConnection)

    def getThreadWrapperLoading(self):
        return self._threadLoading

    @QtCore.pyqtSlot(str)
    def loadData(self, recursivePattern=""):
        self._threadLoading.start(self.updateItems, argsParam=(recursivePattern,))

    def updateItems(self, recursivePattern):
        """
            Update browserItemsModel according model's current path and filter options
        """
        self._threadLoading.lock()
        self.debug("LOAD: ", self._currentPath)
        self.setLoading(True)

        if not os.path.exists(self._currentPath):
            self.setLoading(False)
            return
        Worker.wait()  # lock lists in actionManager

        # update threading process
        if self._threadLoading.isStopped():
            if self._threadLoading.getPoolSize() > 0:
                self._threadLoading.setStopFlag(False)
            else:
                self.setLoading(False)
                Worker.work()
                self._threadLoading.unlock()
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
                self.debug("after recurse", self._threadLoading)
        except Exception as e:
            print(e)

        if not self._threadLoading.isStopped():
            self._threadLoading.pop()

        self.setLoading(False)
        Worker.work()
        self._threadLoading.unlock()

    def pushBrowserItems(self, allItems):
        self.debug("push data: size all items", len(allItems))
        for item in allItems:
            # if the process was canceled, we stop
            if self._threadLoading.isStopped():
                break
            addItem = fnmatch(item.getFilename(), self._filter)
            if addItem and item.getType() == BrowserItem.ItemType.sequence:
                addItem = self._showSeq
            if addItem:
                itemToAdd = self._actionManager.searchItem(item.getAbsoluteFilepath())
                if not itemToAdd:
                    itemToAdd = BrowserItem(copy.copy(item), False)
                itemToAdd.moveToThread(self.thread())
                self.addItemSync.emit(itemToAdd)

    @QtCore.pyqtSlot(object)
    def onAddItemSync(self, bItem):
        self.debug("Add item: ", bItem.getPath())
        self._browserItems.append(bItem)
        self.sortBrowserItems.emit()  # sync
        self._browserItemsModel.insert(self.searchIndexItem(bItem), bItem)
        self.debug(self._browserItemsModel.count)

    @QtCore.pyqtSlot()
    def onClearItemsSync(self):
        self._browserItems.clear()
        self._browserItemsModel.clear()
        self.modelChanged.emit()

    @QtCore.pyqtSlot(str, object)
    def searchRecursively(self, pattern, modelRequester):
        self.debug("Start recursive search:", self._currentPath)
        if modelRequester.getThreadWrapperLoading().isStopped():
            return

        listToBrowse = self._browserItems
        if self == modelRequester:
            listToBrowse = self._browserItems.copy()  # copy: _browserItems deleted line after
            modelRequester.clearItemsSync.emit()
        for bItem in listToBrowse:
            self.debug("processing", bItem.getPath())
            if bItem.getName().lower().startswith(pattern.lower()):
                bItem.moveToThread(modelRequester.thread())
                modelRequester.addItemSync.emit(bItem)
                self.debug("add items recurseSearch")
            if bItem.isFolder():
                self.debug("folder:", bItem.getPath())
                recursiveModel = BrowserModel(bItem.getPath(), True, "", self._showSeq, self._hideDotFiles, self._filter)
                recursiveModel.getThreadWrapperLoading().join()
                recursiveModel.searchRecursively(pattern.lower(), modelRequester)
        self.debug("end recurse...", self._currentPath)

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
        if not newCurrentPath.strip():
            return
        self._currentPath = newCurrentPath.strip()
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
        cpt = 0
        for item in self._browserItems:
            if item == bItem:
                return cpt
            cpt += 1
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
        return self._isLoading

    def setLoading(self, loading):
        self._isLoading = loading
        self.loadingChanged.emit()

    @QtCore.pyqtSlot(result=QtCore.QObject)
    def getItemsSelected(self):
        items = QObjectListModel(self)
        items.append([item for item in self._browserItems if item.getSelected()])
        return items

    @QtCore.pyqtSlot(result=QtCore.QObject)
    def getItems(self):
        self.debug("getItems()*******************************", len(self._browserItemsModel))
        return self._browserItemsModel

    @QtCore.pyqtSlot(result=str)
    def getParentPath(self):
        tmp = os.path.dirname(self.currentPath)
        # if path ended by // or simply / we repeat process to get real parent
        if self._currentPath.rfind("/") == len(self._currentPath)-1:
            tmp = os.path.dirname(tmp)
        return tmp + ("/" if tmp != "/" else "")

    @QtCore.pyqtSlot(result=QObjectListModel)
    def getSplittedCurrentPath(self):
        """
            Used into qml navbar
            :return: absolute path and dirname for each folder in the current path into a list via QObjectList
        """
        self.debug("BEGIN SPLITTED PATH")
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
        self.debug("END SPLITTED PATH")
        return model

    @QtCore.pyqtSlot(result=QtCore.QObject)
    def getListFolderNavBar(self, path=""):
        path = path.strip()
        path = path if path else self._currentPath
        nameFiltering = ""
        modelToNav = self

        if not os.path.exists(path) and not os.path.exists(os.path.dirname(path)):
            return QObjectListModel(self)
        if not os.path.exists(path):
            nameFiltering = os.path.basename(path).lower()
            modelToNav = BrowserModel(path=os.path.dirname(path), sync=True, showSeq=self._showSeq, hideDotFiles=self._hideDotFiles)
            modelToNav._threadLoading.join()
        # get dirs with filtering if exists
        if nameFiltering:
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

        crescentLoop = 1
        index += 1

        if firstSelected > index:
            index -= 2
            crescentLoop = -1

        for i in range(firstSelected, index, crescentLoop):
            self._browserItems[i].setSelected(True)
        self._browserItemsModel.setObjectList(self._browserItems)

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


class BrowserModelSingleton(Singleton):
    _browserModel = BrowserModel()

    @staticmethod
    def get():
        return BrowserModelSingleton._browserModel