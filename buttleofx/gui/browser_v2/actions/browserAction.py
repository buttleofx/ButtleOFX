from PyQt5 import QtCore
from buttleofx.gui.browser_v2.actions.actionManager import ActionManagerSingleton
from buttleofx.gui.browser_v2.actions.actionWrapper import ActionWrapper
from quickmamba.patterns.singleton import Singleton
from buttleofx.gui.browser_v2.browserModel import BrowserModelSingleton
from buttleofx.gui.browser_v2.actions.concreteActions import *
import os

class BrowserAction(QtCore.QObject):
    """
        Controller of browser for actions
    """
    def __init__(self):
        super(BrowserAction, self).__init__()
        self._cacheActions = None  # for copy, move actions
        self._browserModel = BrowserModelSingleton().get()

    @QtCore.pyqtSlot(QtCore.QObject)
    def getCache(self):
        return self._cacheActions

    def pushCache(self, listActions):
        self._cacheActions = ActionWrapper(listActions)

    @QtCore.pyqtSlot(QtCore.QObject)
    def pushToActionManager(self, actionWrapper=None):
        if actionWrapper:
            ActionManagerSingleton.get().push(actionWrapper)
        else:
            if self._cacheActions:
                ActionManagerSingleton.get().push(self._cacheActions)
            self._cacheActions = None

    @QtCore.pyqtSlot()
    def handleCopy(self):
        self._cacheActions = None
        listActions = []
        for bItem in self._browserModel.getItems():
            if bItem.getSelected():
                listActions.append(Copy(bItem, None))
        self.pushCache(listActions)

    @QtCore.pyqtSlot()
    def handleMove(self):
        self._cacheActions = None
        listActions = []
        for bItem in self._browserModel.getItems():
            if bItem.getSelected():
                listActions.append(Move(bItem))
        self.pushCache(listActions)

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


class BrowserActionSingleton(Singleton):
    _bAction = BrowserAction()

    @staticmethod
    def get():
        return BrowserActionSingleton._bAction