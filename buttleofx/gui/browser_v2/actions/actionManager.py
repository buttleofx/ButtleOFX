from buttleofx.gui.browser_v2.actions.worker import Worker
from quickmamba.patterns import Singleton
from quickmamba.models import QObjectListModel
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
        # lists of ActionWrapper
        self._waiting = Queue(maxsize=0)
        self._running = []
        self._ended = []
        self._workers = [Worker(self._waiting, self._running, self._ended, self.actionChanged)
                         for _ in range(self.num_threads_workers)]
        self.startWorkers()

    def stopWorkers(self):
        Worker.destroy()
        for _ in self._workers:
            self._waiting.put(None)

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

    def getEndedActions(self):
        return self._ended

    def getRunningActions(self):
        return self._running

    def getWaitingActions(self):
        return self._waiting

    def getModelFromList(self, list):
        model = QObjectListModel(self)
        model.append(list)
        return model

    # ################################### Methods exposed also to QML ############################### #

    @QtCore.pyqtSlot(result=QtCore.QObject)
    def getEndedActionsModel(self):
        return self.getModelFromList(self._ended)

    @QtCore.pyqtSlot(result=QtCore.QObject)
    def getRunningActionsModel(self):
        return self.getModelFromList(self._running)

    @QtCore.pyqtSlot(result=QtCore.QObject)
    def getWaitingActionsModel(self):
        return self.getModelFromList(self._waiting)


    def searchItemInList(self, listBrowse, path):
        for actionWrapper in list(listBrowse):
            for action in actionWrapper.getActions():
                if action.getBrowserItem().getPath() == path:
                    return action.getBrowserItem()
        return None

    def searchItem(self, path):
        """
        :param path:
        :return: First BrowserItem instance found with a given path into running and waiting lists
        """
        bItem = self.searchItemInList(self._waiting.queue, path)
        if bItem:
            return bItem
        return self.searchItemInList(self._running, path)

    @QtCore.pyqtSlot()
    def abortAll(self):
        for a in self._waiting:
            a.abort()
        for a in self._running:
            a.abort()

    endedActions = QtCore.pyqtProperty(QObjectListModel, getEndedActionsModel, notify=actionChanged)
    runningActions = QtCore.pyqtProperty(QObjectListModel, getRunningActionsModel, notify=actionChanged)
    waitingActions = QtCore.pyqtProperty(QObjectListModel, getWaitingActionsModel, notify=actionChanged)



class ActionManagerSingleton(Singleton):
    _actionManager = ActionManager()

    @staticmethod
    def get():
        return ActionManagerSingleton._actionManager
