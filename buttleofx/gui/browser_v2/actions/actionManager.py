from buttleofx.gui.browser_v2.actions.actionInterface import ActionInterface
from buttleofx.gui.browser_v2.actions.worker import Worker
from quickmamba.patterns import Singleton
from PyQt5 import QtCore
from queue import Queue


class ActionManager(QtCore.QObject):
    """
        Handle the requested actions on browserItem(s) by a Queue FIFO.
        A second pile 'actionsEnded' is used for history
    """

    actionChanged = QtCore.pyqtSignal()
    num_threads_workers = 5

    def __init__(self):
        super(ActionManager, self).__init__()
        self._waiting = Queue(maxsize=0)
        self._running = []
        self._ended = []
        self._workers = [Worker(self._waiting, self._running, self._ended, self.actionChanged) for _ in range(self.num_threads_workers)]
        self.startWorkers()

    def startWorkers(self):
        for worker in self._workers:
            worker.start()

    def push(self, actionWrapper):
        self._waiting.put(actionWrapper)
        self.actionChanged.emit()

    def clearEndedActions(self):
        self._ended.clear()
        self.actionChanged.emit()

    def clearRunningActions(self):
        self._running.clear()
        self.actionChanged.emit()

    # ################################### Methods exposed also to QML ############################### #

    @QtCore.pyqtSlot(result=list)
    def getEndedActions(self):
        return self._ended

    @QtCore.pyqtSlot(result=list)
    def getRunningActions(self):
        return self._running

    @QtCore.pyqtSlot(result=list)
    def getWaitingActions(self):
        return self._waiting


class ActionManagerSingleton(Singleton):
    _actionManager = ActionManager()

    @staticmethod
    def get():
        return ActionManagerSingleton._actionManager
