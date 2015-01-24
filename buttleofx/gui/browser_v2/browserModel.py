import os
from buttleofx.gui.browser_v2.browserItem import BrowserItem
from PyQt5 import QtCore
from quickmamba.models import QObjectListModel
from pySequenceParser import sequenceParser
from buttleofx.gui.browser_v2.browserSortOn import SortOn
from fnmatch import fnmatch
from buttleofx.gui.browser_v2.threadWrapper import ThreadWrapper


class BrowserModel(QtCore.QObject):
    # singleton? only one model?
    """
        Model of files based on pySequenceParser. It recognises files, folders and sequences.
        Possibility to filter the model: sequence, hidden dir/files or not (regexp is coming)
    """
    _currentPath = ""
    _browserItems = []
    _browserItemsModel = None
    _filter = "*"
    _hideDotFiles = True
    _showSeq = True
    _sortOn = SortOn()

    _threadUpdateItem = ThreadWrapper()
    _threadRecursiveSearch = ThreadWrapper()

    filterChanged = QtCore.pyqtSignal()
    sortOnChanged = QtCore.pyqtSignal()
    currentPathChanged = QtCore.pyqtSignal()
    hideDotFilesChanged = QtCore.pyqtSignal()
    modelChanged = QtCore.pyqtSignal()

    def __init__(self, asyncMode=True, parent=None):
        """
            Build an BrowserModel instance.
            :param parent: Qt parent
        """
        super(BrowserModel, self).__init__(parent)
        self._asyncMode = asyncMode
        self._browserItemsModel = QObjectListModel(self)
        self._currentPath = os.path.expanduser("~")
        self.updateItemsWrapperAsync()

    # def recursiveResearch(self, folder):

    def updateItemsWrapperAsync(self):
        if self._asyncMode:
            self._threadUpdateItem.startThread(self.updateItems)
        else:
            self.updateItems()

    def updateItems(self):
        """
            Update browserItemsModel according model's current path and filter options
        """
        if self._asyncMode:
            self._threadUpdateItem.getLock().acquire()

        # if no permissions fail
        try:
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
            self._threadUpdateItem.getLock().release()

    def pushBrowserItems(self, allItems):
        """
            Handle async mode: possibility to stop thread, and notify view for each adding.
            :param allItems:
        """
        # split treatment to avoid 2 useless conditions per pass even if redundant: faster
        if self._asyncMode:
            for item in allItems:
                # TODO:handle supported
                if self._threadUpdateItem.getNbJobs() != 1:
                    break

                addItem = fnmatch(item.getFilename(), self._filter)
                if addItem and item.getType() == BrowserItem.ItemType.sequence:
                    addItem = self._showSeq

                if addItem:
                    self._browserItems.append(BrowserItem(item, False))
                    self._browserItemsModel.setObjectList(self._browserItems)
                    self.modelChanged.emit()
        else:
            for item in allItems:
                addItem = fnmatch(item.getFilename(), self._filter)
                if addItem and item.getType() == BrowserItem.ItemType.sequence:
                    addItem = self._showSeq
                if addItem:
                    self._browserItems.append(BrowserItem(item, False))

        # if asyncMode don't forgive to pop thread and releaseLock after all process(sort and set model)

    def getFilter(self):
        return self._filter

    def setFilter(self, newFilter):
        self._filter = newFilter
        self.updateItemsWrapperAsync()
        self.filterChanged.emit()

    def getCurrentPath(self):
        return self._currentPath

    def setCurrentPath(self, newCurrentPath):
        self._currentPath = newCurrentPath
        self.updateItemsWrapperAsync()
        self.currentPathChanged.emit()

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
            self._browserItems.sort(key=lambda it: (it.getType()))

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
    def getSplitedCurrentPath(self):
        """
            Use for navbar in qml
            :return: absolute path and dirname for each folder in the current path into a list via QObjectList
        """
        tmpList = []
        absolutePath = self._currentPath

        # not absolutePath: for windows
        while absolutePath != os.path.abspath(os.sep) or not absolutePath:
            tmpList.append([absolutePath, os.path.basename(absolutePath)])
            absolutePath = os.path.dirname(absolutePath)
        if os.sep == "/":
            tmpList.append(["/", ""])

        tmpList.reverse()
        model = QObjectListModel(self)
        model.append(tmpList)
        return model

    @QtCore.pyqtSlot(result=QObjectListModel)
    def getListFolderNavBar(self):
        tmpList = [browserItem for browserItem in self._browserItems if browserItem.isFolder()]
        model = QObjectListModel(self)
        model.append(tmpList)
        return model

    @QtCore.pyqtSlot(result=QObjectListModel)
    def getSelectedItems(self):
        model = QObjectListModel(self)
        model.append([item for item in self._browserItems if item.getSelected()])
        return model

    # ############################################# Data exposed to QML ############################################# #

    currentPath = QtCore.pyqtProperty(str, getCurrentPath, setCurrentPath, notify=currentPathChanged)
    currentPathExists = QtCore.pyqtProperty(bool, isCurrentPathExists, notify=currentPathChanged)
    fileItems = QtCore.pyqtProperty(QtCore.QObject, getItems, notify=modelChanged)
    parentFolder = QtCore.pyqtProperty(str, getParentPath, notify=currentPathChanged)
    showSequence = QtCore.pyqtProperty(bool, isShowSequence, setShowSequence, notify=filterChanged)

    hideDotFiles = QtCore.pyqtProperty(bool, isHiddenDotFiles, setHideDotFiles, notify=hideDotFilesChanged)
    splitedCurrentPath = QtCore.pyqtProperty(QObjectListModel, getSplitedCurrentPath, notify=currentPathChanged)
    listFolderNavBar = QtCore.pyqtProperty(QObjectListModel, getListFolderNavBar, notify=currentPathChanged)
    selectedItems = QtCore.pyqtProperty(QObjectListModel, getSelectedItems, constant=True)
    sortOn = QtCore.pyqtProperty(str, getFieldToSort, notify=sortOnChanged)