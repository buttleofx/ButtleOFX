import os
from PyQt5 import QtCore
from buttleofx.gui.browser_v2.actions.actionManager import ActionManagerSingleton
from buttleofx.gui.browser_v2.actions.actionWrapper import ActionWrapper
from quickmamba.patterns.singleton import Singleton
from buttleofx.gui.browser_v2.browserModel import BrowserModelSingleton
from buttleofx.gui.browser_v2.browserItem import BrowserItem
from buttleofx.gui.browser_v2.actions.concreteActions import *
from pySequenceParser import sequenceParser


class BrowserAction(QtCore.QObject):
    """
        Controller of browser for actions
    """
    cacheChanged = QtCore.pyqtSignal()

    def __init__(self):
        super(BrowserAction, self).__init__()
        self._cacheActions = None  # for copy, move actions
        self._browserModel = BrowserModelSingleton().get()

    def pushCache(self, listActions):
        self._cacheActions = ActionWrapper(listActions)

    def isEmptyCache(self):
        return bool(self._cacheActions)

    @QtCore.pyqtSlot(QtCore.QObject)
    def getCache(self):
        return self._cacheActions

    @QtCore.pyqtSlot(QtCore.QObject)
    def pushToActionManager(self, actionWrapper=None):
        if actionWrapper:
            ActionManagerSingleton.get().push(actionWrapper)
        else:
            if self._cacheActions:
                ActionManagerSingleton.get().push(self._cacheActions)

    @QtCore.pyqtSlot()
    def handleCopy(self):
        self._cacheActions = None
        listActions = []
        for bItem in self._browserModel.getItems():
            if bItem.getSelected():
                listActions.append(Copy(bItem, None))
        self.pushCache(listActions)
        self.cacheChanged.emit()

    @QtCore.pyqtSlot()
    def handleMove(self):
        self._cacheActions = None
        listActions = []
        for bItem in self._browserModel.getItems():
            if bItem.getSelected():
                listActions.append(Move(bItem))
        self.pushCache(listActions)
        self.cacheChanged.emit()

    @QtCore.pyqtSlot()
    def handlePaste(self):
        if not self._cacheActions:
            return
        for action in self._cacheActions.getActions():
            action.setDestinationPath(self._browserModel.getCurrentPath())
        self.pushToActionManager()

    @QtCore.pyqtSlot()
    def handleDelete(self):
        listActions = []
        for item in [bItem for bItem in self._browserModel.getItems() if bItem.getSelected()]:
            listActions.append(Delete(item))
        self.pushToActionManager(ActionWrapper(listActions))

    @QtCore.pyqtSlot(str)
    def handleNew(self, type):
        if type == "Folder":
            new = BrowserItem(sequenceParser.Item(sequenceParser.eTypeFolder, "New_Folder"), True)
        elif type == "File":
            new = BrowserItem(sequenceParser.Item(sequenceParser.eTypeFile, "NewDocument.txt"), True)
        else:
            return

        parent = BrowserItem(sequenceParser.Item(sequenceParser.eTypeFolder, self._browserModel.getCurrentPath()), False)
        self.pushToActionManager(ActionWrapper([Create(parent, new)]))

    # cache empty ?
    isCache = QtCore.pyqtProperty(bool, isEmptyCache, notify=cacheChanged)


class BrowserActionSingleton(Singleton):
    _bAction = BrowserAction()

    @staticmethod
    def get():
        return BrowserActionSingleton._bAction