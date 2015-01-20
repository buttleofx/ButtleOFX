import os
from buttleofx.gui.browser_v2.browserItem import BrowserItem
from PyQt5 import QtCore
from quickmamba.models import QObjectListModel


class BrowserModel(QtCore.QObject):
    # singleton? only one model?

    _currentPath = ""
    _browserItems = []
    _browserItemsModel = None
    _filter = "*"
    _ignoreHiddenItems = True

    filterChanged = QtCore.pyqtSignal()
    currentPathChanged = QtCore.pyqtSignal()
    ignoreHiddenChanged = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(BrowserModel, self).__init__(parent)
        self._browserItemsModel = QObjectListModel(self)
        self.rootFolder = os.path.expanduser("~")

    def updateItems(self):
        pass

    def getFilter(self):
        return self._filter

    def setFilter(self, newFilter):
        self._filter = newFilter
        self.updateItems()
        self.filterChanged.emit()

    def getCurrentPath(self):
        return self._currentPath

    def setCurrentPath(self, newRoot):
        self._currentPath = newRoot
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
        splitedPath = [folder for folder in self._currentPath.split(os.sep) if folder]
        model = QObjectListModel(self)
        model.append(splitedPath)
        return model

    # ############################################# Data exposed to QML ############################################# #

    currentPath = QtCore.pyqtProperty(str, getCurrentPath, setCurrentPath, notify=currentPathChanged)
    exists = QtCore.pyqtProperty(bool, isCurrentPathExists, constant=True, notify=currentPathChanged)
    fileItems = QtCore.pyqtProperty(QtCore.QObject, getItems, constant=True, notify=currentPathChanged)
    parentFolder = QtCore.pyqtProperty(str, getParentPath, constant=True, notify=currentPathChanged)

    splitedCurrentPath = QtCore.pyqtProperty(QObjectListModel, getSplitedCurrentPath, constant=True, notify=currentPathChanged)