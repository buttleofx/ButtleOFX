from buttleofx.gui.browser_v2.action.actionInterface import ActionInterface
from PyQt5 import QtCore
from quickmamba.patterns import Singleton


class ActionManager(QtCore.QObject):
    """
        Handle the requested actions on browserItem(s) by a pile FIFO.
        A second pile 'actionsEnded' is used for history
    """

    actionChanged = QtCore.pyqtSignal()

    def __init__(self):
        super(ActionManager, self).__init__()
        self._actionsEnded = []
        self._actionsRunning = []

    def pull(self):
        if not self._actionsRunning:
            return
        self._actionsRunning[0].process()
        self._actionsEnded.append(self._actionsRunning.pop(0))
        self.actionChanged.emit()

    def push(self, action):
        self._actionsRunning.append(action)
        self.actionChanged.emit()

    def clearEndedActions(self):
        self._actionsEnded.clear()
        self.actionChanged.emit()

    # ################################### Methods exposed also to QML ############################### #

    @QtCore.pyqtSlot(result=list)
    def getEndedActions(self):
        return self._actionsEnded

    @QtCore.pyqtSlot(result=list)
    def getRunningActions(self):
        return self._actionsRunning

    @QtCore.pyqtSlot(int)
    def removeAt(self, i):
        if i not in len(self._actionsRunning):
            raise IndexError("ActionManager::removeAt(i) bad index")

        self._actionsRunning[i].abort()
        self._actionsEnded.append(self._actionsRunning.pop(i))
        self.actionChanged.emit()


class ActionManagerSingleton(Singleton):
    _actionManager = ActionManager()

    def get(self):
        return self._actionManager