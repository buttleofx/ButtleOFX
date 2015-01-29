import os
from buttleofx.gui.browser_v2.browserItem import BrowserItem
from PyQt5 import QtCore
from quickmamba.models import QObjectListModel
from pySequenceParser import sequenceParser
from buttleofx.gui.browser_v2.browserSortOn import SortOn
from fnmatch import fnmatch
from buttleofx.gui.browser_v2.threadWrapper import ThreadWrapper
from buttleofx.gui.browser_v2.actions.actionManager import ActionManagerSingleton
from buttleofx.gui.browser_v2.actions.worker import Worker
import copy
from pyTuttle import tuttle
from quickmamba.patterns import Singleton


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

    def __init__(self, asyncMode=False, path="", parent=None):
        """
            Build an BrowserModel instance.
            :param parent: Qt parent
        """
        super(BrowserModel, self).__init__(parent)
        # default values
        self._currentPath = ""
        self._browserItems = []
        self._browserItemsModel = None
        self._filter = "*"
        self._hideDotFiles = True
        self._showSeq = True
        self._sortOn = SortOn()
        self._threadUpdateItem = ThreadWrapper()
        self._threadRecursiveSearch = ThreadWrapper()
        self._browserItemsModel = QObjectListModel(self)

        self._asyncMode = asyncMode
        self._actionManager = ActionManagerSingleton.get()  # for locking and search BrowserItem when updating
        self._currentPath = path.strip() if path.strip() else os.path.expanduser("~")
        self.updateItemsWrapperAsync()

    def updateItemsWrapperAsync(self):
        if self._asyncMode:
            self._threadUpdateItem.startThread(self.updateItems)
        else:
            self.updateItems()

    def updateItems(self):
        """
            Update browserItemsModel according model's current path and filter options
        """
        if not os.path.exists(self._currentPath):
            return

        Worker.wait()  # lock lists in actionManager
        self._threadRecursiveSearch.stopAllThreads()  # avoid bad comportment

        if self._asyncMode:
            # if all threads were stopped, we stop process
            if not self._threadUpdateItem.getNbJobs():
                self._threadUpdateItem.release()
                return
            self._threadUpdateItem.lock()

        try:
            # if no permissions fail
            self._browserItems.clear()
            self._browserItemsModel.clear()

            detectOption = sequenceParser.eDetectionDefault if self._hideDotFiles else sequenceParser.eDetectionDefaultWithDotFile
            allItems = sequenceParser.browse(self._currentPath, detectOption, self._filter)
            self.pushBrowserItems(allItems)  # handle async mode
        except Exception as e:
            print(e)

        self.sortBrowserItems()
        self._browserItemsModel.setObjectList(self._browserItems)
        self.modelChanged.emit()

        if self._asyncMode:
            self._threadUpdateItem.pop()
            self._threadUpdateItem.unlock()
        Worker.work()

    def isItemInActionManager(self, path):

        for actionWrapper in list(self._actionManager.getWaitingActions().queue):
            for action in actionWrapper.getActions():
                if action.getBrowserItem().getPath() == path:
                    return action.getBrowserItem()

        for actionWrapper in self._actionManager.getRunningActions():
            for action in actionWrapper.getActions():
                if action.getBrowserItem().getPath() == path:
                    return action.getBrowserItem()
        return None

    def pushBrowserItems(self, allItems):
        """
            Handle async mode: possibility to stop thread, and notify view for each addition.
            :param allItems:
        """
        # split treatment to avoid 2 useless conditions per pass even if redundant: faster
        if self._asyncMode:
            for item in allItems:
                if self._threadUpdateItem.getNbJobs() != 1:
                    break

                addItem = fnmatch(item.getFilename(), self._filter)
                if addItem and item.getType() == BrowserItem.ItemType.sequence:
                    addItem = self._showSeq

                if addItem:
                    itemToAdd = self.isItemInActionManager(item.getAbsoluteFilepath())

                    if not itemToAdd:
                        itemToAdd = BrowserItem(item, False)
                    self._browserItems.append(itemToAdd)
                    self._browserItemsModel.setObjectList(self._browserItems)
                    self.modelChanged.emit()
        else:
            for item in allItems:
                addItem = fnmatch(item.getFilename(), self._filter)
                if addItem and item.getType() == BrowserItem.ItemType.sequence:
                    addItem = self._showSeq
                if addItem:
                    itemToAdd = self.isItemInActionManager(item.getAbsoluteFilepath())
                    if not itemToAdd:
                        itemToAdd = BrowserItem(item, False)
                    self._browserItems.append(itemToAdd)

        # if asyncMode don't forgive to pop thread and releaseLock after all process(sort and set model)

    def searchRecursiveFromPattern(self, pattern, modelRequester):
        # # if all threads started were stopped, we stop process
        # if not modelRequester._threadRecursiveSearch.getNbJobs():
        #     modelRequester._threadRecursiveSearch.unlock()
        #     return

        listToBrowse = self._browserItems

        if self == modelRequester:
            # modelRequester._threadRecursiveSearch.lock()
            listToBrowse = BrowserModel(False, modelRequester._currentPath)._browserItems
            modelRequester._browserItems.clear()
            modelRequester._browserItemsModel.clear()
            modelRequester.modelChanged.emit()

        for bItem in listToBrowse:
            # if modelRequester._threadRecursiveSearch.getNbJobs() != 1:
            #     break
            # cancel util

            if pattern in bItem.getName().lower():
                modelRequester._browserItems.append(bItem)
                modelRequester._browserItemsModel.setObjectList(modelRequester._browserItems)
                modelRequester.modelChanged.emit()
            if bItem.isFolder():
                BrowserModel(self._asyncMode, bItem.getPath()).searchRecursiveFromPattern(pattern, modelRequester)

        if self == modelRequester:
            modelRequester._browserItemsModel.setObjectList(modelRequester._browserItems)  # force notify ...
            modelRequester.modelChanged.emit()
            self.modelChanged.emit()
        #     modelRequester._threadRecursiveSearch.pop()
        #     modelRequester._threadRecursiveSearch.unlock()

    @QtCore.pyqtSlot(str)
    # function to call, ensure async
    def doSearchRecursive(self, pattern):
        pattern = pattern.strip().lower()
        self.searchRecursiveFromPattern(pattern, self)
        # self._threadRecursiveSearch.startThread(self.searchRecursiveFromPattern, argsParam=(pattern, self))

    def getFilter(self):
        return self._filter

    def setFilter(self, newFilter):
        self._filter = newFilter
        self.updateItemsWrapperAsync()
        self.filterChanged.emit()

    def getCurrentPath(self):
        return self._currentPath

    @QtCore.pyqtSlot(str)
    def setCurrentPath(self, newCurrentPath):
        self._currentPath = newCurrentPath.strip()
        self.currentPathChanged.emit()
        self.updateItemsWrapperAsync()

    def setCurrentPathHome(self):
        self.setCurrentPath(self.getHomePath())

    def getHomePath(self):
        return os.path.expanduser("~")

    def isCurrentPathExists(self):
        return os.path.exists(self._currentPath)

    def isHiddenDotFiles(self):
        return self._hideDotFiles

    def setHideDotFiles(self, hide):
        self._hideDotFiles = hide
        self.updateItemsWrapperAsync()
        self.hideDotFilesChanged.emit()

    def getFieldToSort(self):
        return self._sortOn.getFieldToSort()

    def isSortReversed(self):
        return self._sortOn.isReversed()

    def sortBrowserItems(self):
        rev = self._sortOn.isReversed()

        if self._sortOn.getFieldToSort() == SortOn.onName:
            self._browserItems.sort(key=lambda it: (it.getType(), os.path.basename(it.getPath().lower())), reverse=rev)

        elif self._sortOn.getFieldToSort() == SortOn.onSize:
            self._browserItems.sort(key=lambda it: (it.getType(), it.getWeight()), reverse=rev)

        self._browserItems.sort(key=lambda it: (it.getType()))

    # ################################### Methods exposed to QML ############################### #

    @QtCore.pyqtSlot(str, bool)
    def setFieldToSort(self, newField, reverse=0):
        self._sortOn.setFieldToSort(newField, reverse)
        self.sortBrowserItems()
        self.sortOnChanged.emit()
        self.modelChanged.emit()  # refresh view

    @QtCore.pyqtSlot(bool)
    def setShowSequence(self, seqBool):
        self._showSeq = seqBool
        self.filterChanged.emit()

    @QtCore.pyqtSlot(result=bool)
    def isShowSequence(self):
        return self._showSeq

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
        return os.path.dirname(self._currentPath)

    @QtCore.pyqtSlot(result=QObjectListModel)
    def getSplittedCurrentPath(self):
        """
            Used into navbar in qml
            :return: absolute path and dirname for each folder in the current path into a list via QObjectList
        """
        tmpList = []
        absolutePath = self._currentPath
        if not absolutePath:
            return QObjectListModel(self)

        # not absolutePath: for windows
        while not absolutePath or absolutePath != os.path.abspath(os.sep):
            if os.path.exists(absolutePath):
                tmpList.append([absolutePath, os.path.basename(absolutePath)])
            absolutePath = os.path.dirname(absolutePath)
        if os.sep == "/":
            tmpList.append(["/", ""])

        tmpList.reverse()
        model = QObjectListModel(self)
        model.append(tmpList)
        return model

    @QtCore.pyqtSlot(result=QtCore.QObject)
    def getListFolderNavBar(self, path=""):
        path = path.strip()
        path = path if path else self._currentPath
        nameFiltering = ""
        modelToNav = self

        if not os.path.exists(path):
            nameFiltering = os.path.basename(path)
            modelToNav = BrowserModel(asyncMode=False, path=os.path.dirname(path))  # need to be sync

        # get dirs with filtering if exists
        if nameFiltering:
            tmpList = [item for item in modelToNav.getItems() if item.isFolder() and nameFiltering in item.getName()]
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
        self.updateItemsWrapperAsync()

    @QtCore.pyqtSlot()
    def unselectAllItems(self):
        for bItem in self._browserItems:
            bItem.setSelected(False)

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
        index = index +1

        if firstSelected > index:
            index = index -2
            crescentLoop = -1

        for i in range(firstSelected, index, crescentLoop):
            self._browserItems[i].setSelected(True)
        self._browserItemsModel.setObjectList(self._browserItems)

    # ############################################# Data exposed to QML ############################################# #

    currentPath = QtCore.pyqtProperty(str, getCurrentPath, setCurrentPath, notify=currentPathChanged)
    currentPathExists = QtCore.pyqtProperty(bool, isCurrentPathExists, notify=currentPathChanged)
    fileItems = QtCore.pyqtProperty(QtCore.QObject, getItems, notify=modelChanged)
    parentFolder = QtCore.pyqtProperty(str, getParentPath, notify=currentPathChanged)
    showSequence = QtCore.pyqtProperty(bool, isShowSequence, setShowSequence, notify=filterChanged)

    hideDotFiles = QtCore.pyqtProperty(bool, isHiddenDotFiles, setHideDotFiles, notify=hideDotFilesChanged)
    splittedCurrentPath = QtCore.pyqtProperty(QObjectListModel, getSplittedCurrentPath, notify=currentPathChanged)
    listFolderNavBar = QtCore.pyqtProperty(QtCore.QObject, getListFolderNavBar, notify=currentPathChanged)
    sortOn = QtCore.pyqtProperty(str, getFieldToSort, notify=sortOnChanged)
    selectedItems = QtCore.pyqtProperty(QObjectListModel, getSelectedItems, notify=modelChanged)


class BrowserModelSingleton(Singleton):
    _browserModel = BrowserModel()

    @staticmethod
    def get():
        return BrowserModelSingleton._browserModel