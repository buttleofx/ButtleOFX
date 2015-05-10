import logging
import queue

from PyQt5 import QtCore

from quickmamba.patterns import Singleton

from buttleofx.gui.browser_v2.actions.actionWorker import ActionWorker


class ActionManager(QtCore.QObject):
    """
        Handle the requested actions on browserItem(s) by a Queue FIFO.
        A second pile 'actionsEnded' is used for history
    """

    actionChanged = QtCore.pyqtSignal()

    def __init__(self):
        logging.debug('ActionManager constructor')
        super(ActionManager, self).__init__()
        self._waitingActionsQueue = queue.Queue(maxsize=0)
        self._runningActions = []
        self._endedActions = []
        self._workers = []

    def __enter__(self):
        self.startWorkers()
        return self
    
    def __exit__(self, type, value, traceback):
        self.stopWorkers()

    def __del__(self):
        logging.debug('ActionManager destructor')
        self.stopWorkers()

    def createWorkers(self, numWorkerThreads=5):
        # Create all workers
        self._workers = [ActionWorker(self)
                         for _ in range(numWorkerThreads)]

    def startWorkers(self):
        logging.debug('ActionManager startWorkers')
        if not self._workers:
            self.createWorkers()
        for worker in self._workers:
            worker.start()

    def stopWorkers(self):
        for _ in self._workers:
            self._waitingActionsQueue.put(None)  # add end-of-queue markers
        # Blocks until all items in the queue have been gotten and processed.
        for worker in self._workers:
            worker.join()
        del self._workers[:]  # clear the list

    def push(self, actionWrapper):
        self._waitingActionsQueue.put(actionWrapper)
        self.actionChanged.emit()

    def clearEndedActions(self):
        self._endedActions.clear()
        self.actionChanged.emit()

    def clearRunningActions(self):
        self._runningActions.clear()
        self.actionChanged.emit()

    # ################################### Methods exposed also to QML ############################### #

    @QtCore.pyqtSlot(result=list)
    def getEndedActions(self):
        return self._endedActions

    @QtCore.pyqtSlot(result=list)
    def getRunningActions(self):
        return self._runningActions

#    @QtCore.pyqtSlot(result=list)
#    def getWaitingActions(self):
#        # TODO: does that work? Queue to List conversion?
#        return self._waitingActionsQueue

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
        bItem = self.searchItemInList(self._waitingActionsQueue.queue, path)
        if bItem:
            return bItem
        return self.searchItemInList(self._runningActions, path)


globalActionManager = ActionManager()
