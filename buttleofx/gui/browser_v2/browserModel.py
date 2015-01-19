import os
from buttleofx.gui.browser_v2.browserItem import BrowserItem
from PyQt5 import QtCore
from quickmamba.models import QObjectListModel


class BrowserModel(QtCore.QObject):
    # singleton? only one model?
    _rootFolder = ""
    _browserItems = []
    _browserItemsModel = None
    _filter = "*"
    _ignoreHiddenItems = True

    filterChanged = QtCore.pyqtSignal()
    rootFolderChanged = QtCore.pyqtSignal()
    ignoreHiddenChanged = QtCore.pyqtSignal()

    def __init__(self):
        super(BrowserModel, self).__init__()
        self._browserItemsModel = QObjectListModel(self)

    def updateItems(self):
        pass

    def getFilter(self):
        return self._filter

    def setFilter(self, newFilter):
        self._filter = newFilter
        self.updateItems()
        self.filterChanged.emit()

    def getRootFolder(self):
        return self._rootFolder

    def setRootFolder(self, newRoot):
        self._rootFolder = newRoot
        self.updateItems()
        self.rootFolderChanged.emit()

    def isRootFolderExist(self):
        return os.path.exists(self._rootFolder)

    def isIgnoregHidden(self):
        return self._ignoreHiddenItems

    def setIgnoreHidden(self, hide):
        self._ignoreHiddenItems = hide
        self.updateItems()
        self.ignoreHiddenChanged.emit()

    @QtCore.pyqtSlot(result=QtCore.QObject)
    def getItemsSelected(self):
        selectedList = QObjectListModel(self)
        for item in self._browserItems:
            if item.getSelected():
                selectedList.append(item)
        return selectedList

    @QtCore.pyqtSlot(result=QtCore.QObject)
    def getItems(self):
        return self._browserItemsModel

    @QtCore.pyqtSlot(result=str)
    def getParentFolder(self):
        return os.path.dirname(self._rootFolder)

    # ############################################# Data exposed to QML ############################################# #

    rootFolder = QtCore.pyqtProperty(str, getRootFolder, setRootFolder, notify=rootFolderChanged)
    exists = QtCore.pyqtProperty(bool, isRootFolderExist, constant=True)
    fileItems = QtCore.pyqtProperty(QtCore.QObject, getItems, constant=True)
    parentFolder = QtCore.pyqtProperty(str, getParentFolder, constant=True)
