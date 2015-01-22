import os
from buttleofx.gui.browser_v2.browserItem import BrowserItem
from PyQt5 import QtCore
from quickmamba.models import QObjectListModel
from pySequenceParser import sequenceParser
from buttleofx.gui.browser_v2.browserSortOn import SortOn


class BrowserModel(QtCore.QObject):
    # singleton? only one model?
    """
        Model of files based on pySequenceParser. It recognises files, folder and sequences.
        Possibility to filter the model: sequence, hidden dir/files or not (regexp is coming)
    """
    _currentPath = ""
    _browserItems = []
    _browserItemsModel = None
    _filter = "*"
    _ignoreHiddenItems = True
    _showSeq = True
    _sortOn = SortOn()

    filterChanged = QtCore.pyqtSignal()
    sortOnChanged = QtCore.pyqtSignal()
    currentPathChanged = QtCore.pyqtSignal()
    ignoreHiddenChanged = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        """
            Build an BrowserModel instance.
            :param parent: Qt parent
        """

        super(BrowserModel, self).__init__(parent)
        self._browserItemsModel = QObjectListModel(self)
        self._currentPath = os.path.expanduser("~")
        self.updateItems()

    def updateItems(self):
        """
            Update browserItemsModel according model's current path and filter options
        """
        try:
            # if no permissions
            self._browserItems.clear()
            self._browserItemsModel.clear()
            allItems = sequenceParser.browse(self._currentPath)

            for item in allItems:
                # hidden files
                addItem = not(self._ignoreHiddenItems and item.getFilename().startswith("."))

                # show sequence
                if addItem and item.getType() == BrowserItem.ItemType.sequence:
                    addItem = self._showSeq

                if addItem:
                    # TODO: handle regexp + handle supported?
                    self._browserItems.append(BrowserItem(item, True))

            self.sortBrowserItems()
            self._browserItemsModel.setObjectList(self._browserItems)
        except Exception as e:
            print(e)
            return

    def getFilter(self):
        return self._filter

    def setFilter(self, newFilter):
        self._filter = newFilter
        self.updateItems()
        self.filterChanged.emit()

    def getCurrentPath(self):
        return self._currentPath

    def setCurrentPath(self, newCurrentPath):
        self._currentPath = newCurrentPath
        self.updateItems()
        self.currentPathChanged.emit()

    def isCurrentPathExists(self):
        return os.path.exists(self._currentPath)

    def isIgnoreHidden(self):
        return self._ignoreHiddenItems

    def setIgnoreHidden(self, hide):
        self._ignoreHiddenItems = hide
        self.updateItems()
        self.ignoreHiddenChanged.emit()

    def getFieldToSort(self):
        return self._sortOn.getFieldToSort()

    def setFieldToSort(self, newField, reverse=0):
        self._sortOn.setFieldToSort(newField, reverse)
        self.sortOnChanged.emit()

    def sortBrowserItems(self):
        rev = self._sortOn.isReversed()

        if self._sortOn.getFieldToSort() == SortOn.onName:
            self._browserItems.sort(key=lambda it: (it.getType(), os.path.basename(it.getPath().lower())), reverse=rev)

        if self._sortOn.getFieldToSort() == SortOn.onSize:
            self._browserItems.sort(key=lambda it: (it.getType(), it.getWeight()), reverse=rev)

    @QtCore.pyqtSlot(bool)
    def setShowSequence(self, seqBool):
        self._showSeq = seqBool
        self.filterChanged.emit()

    @QtCore.pyqtSlot(result=bool)
    def getShowSequence(self):
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
        while absolutePath != os.path.abspath(os.sep):
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
        model.append([item for item in self._browserItems if item.getSelected])
        return model

    # ############################################# Data exposed to QML ############################################# #

    currentPath = QtCore.pyqtProperty(str, getCurrentPath, setCurrentPath, notify=currentPathChanged)
    exists = QtCore.pyqtProperty(bool, isCurrentPathExists, notify=currentPathChanged)
    fileItems = QtCore.pyqtProperty(QtCore.QObject, getItems, notify=currentPathChanged)
    parentFolder = QtCore.pyqtProperty(str, getParentPath, notify=currentPathChanged)
    showSequence = QtCore.pyqtProperty(bool, getShowSequence, setShowSequence, notify=currentPathChanged)

    ignoreHiddenFiles = QtCore.pyqtProperty(bool, isIgnoreHidden, setIgnoreHidden, notify=ignoreHiddenChanged)
    splitedCurrentPath = QtCore.pyqtProperty(QObjectListModel, getSplitedCurrentPath, notify=currentPathChanged)
    listFolderNavBar = QtCore.pyqtProperty(QObjectListModel, getListFolderNavBar, notify=currentPathChanged)
    selectedItems = QtCore.pyqtProperty(QObjectListModel, getSelectedItems, constant=True)
    sortOn = QtCore.pyqtProperty(str, getFieldToSort, setFieldToSort, notify=sortOnChanged)