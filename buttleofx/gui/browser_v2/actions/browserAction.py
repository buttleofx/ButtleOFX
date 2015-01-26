from PyQt5 import QtCore
from buttleofx.gui.browser_v2.actions.actionManager import ActionManagerSingleton
from buttleofx.gui.browser_v2.actions.actionWrapper import ActionWrapper


class BrowserAction(QtCore.QObject):
    """
        Controller of browser for actions
    """
    def __init__(self):
        super(BrowserAction, self).__init__()
        self._cacheActions = None  # for copy, move actions

    def getCache(self):
        return self._cacheActions

    def pushCache(self, listActions):
        self._cacheActions = ActionWrapper(listActions)

    def pushToActionManager(self, actionWrapper=None):
        if actionWrapper:
            ActionManagerSingleton.get().push(actionWrapper)
        else:
            if self._cacheActions:
                ActionManagerSingleton.get().push(self._cacheActions)
            self._cacheActions = None