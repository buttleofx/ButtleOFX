import os
import logging

from PyQt5 import QtCore

from pySequenceParser import sequenceParser

from buttleofx.gui.browser_v2.actions.actionManager import globalActionManager
from buttleofx.gui.browser_v2.actions.actionWrapper import ActionWrapper
from buttleofx.gui.browser_v2.browserItem import BrowserItem
from buttleofx.gui.browser_v2.actions.concreteActions.copy import Copy
from buttleofx.gui.browser_v2.actions.concreteActions.move import Move
from buttleofx.gui.browser_v2.actions.concreteActions.create import Create
from buttleofx.gui.browser_v2.actions.concreteActions.delete import Delete
from buttleofx.gui.browser_v2.browserModel import globalBrowserDialog, globalBrowser


class BrowserAction(QtCore.QObject):
    """
        Controller of browser for actions
    """
    cacheChanged = QtCore.pyqtSignal()

    def __init__(self, bModel):
        logging.debug('BrowserAction begin constructor')
        QtCore.QObject.__init__(self)
        self._cacheActions = None  # for copy, move actions
        self._browserModel = bModel
        logging.debug('BrowserAction end constructor')

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
            globalActionManager.push(actionWrapper)
        else:
            if self._cacheActions:
                globalActionManager.push(self._cacheActions)

    @QtCore.pyqtSlot()
    def handleCopy(self):
        self._cacheActions = None
        listActions = []
        for bItem in self._browserModel.getItems():
            if bItem.getSelected():
                listActions.append(Copy(bItem))
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

    @QtCore.pyqtSlot(str)
    def handlePaste(self, destination):
        destination = destination.strip() if destination.strip() else self._browserModel.getCurrentPath()
        if not self._cacheActions or not destination or not os.path.exists(destination):
            return

        for action in self._cacheActions.getActions():
            action.setDestinationPath(destination)
        self.pushToActionManager()

    @QtCore.pyqtSlot()
    def handleDelete(self):
        listActions = []
        for item in [bItem for bItem in self._browserModel.getItems() if bItem.getSelected()]:
            listActions.append(Delete(item))
        self.pushToActionManager(ActionWrapper(listActions))

    @QtCore.pyqtSlot(str)
    def handleNew(self, typeItem):
        if typeItem == "Folder":
            new = BrowserItem(sequenceParser.Item(sequenceParser.eTypeFolder, "New_Folder"))
        elif typeItem == "File":
            new = BrowserItem(sequenceParser.Item(sequenceParser.eTypeFile, "NewDocument.txt"))
        else:
            return

        parent = BrowserItem(sequenceParser.Item(sequenceParser.eTypeFolder, self._browserModel.getCurrentPath()))
        self.pushToActionManager(ActionWrapper([Create(parent, new)]))

    # cache empty ?
    isCache = QtCore.pyqtProperty(bool, isEmptyCache, notify=cacheChanged)


globalBrowserAction = BrowserAction(globalBrowser)
globalBrowserActionDialog = BrowserAction(globalBrowserDialog)
