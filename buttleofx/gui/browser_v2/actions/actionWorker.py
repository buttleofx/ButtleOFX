import threading
import logging
import queue


class ActionWorker(threading.Thread):
    """
        ActionWorker is used to execute actions with multi-threading
        inside the ActionManager.
    """

    def __init__(self, actionManager):
        logging.debug('ActionWorker constructor')
        super(ActionWorker, self).__init__()
        self._actionManager = actionManager

    def __del__(self):
        logging.debug('ActionWorker destructor')

    def executeAction(self, actionWrapper):

        self._inProgress.append(actionWrapper)
        for action in actionWrapper.getActions():
            action.process()
            actionWrapper.upProcessed()
            self._actionManager.actionChanged.emit()

        # search in progressList the index to push into doneList
        self._actionManager._runningActions.remove(actionWrapper)
        self._actionManager._endedActions.append(actionWrapper)

    def run(self):
        while True:
            try:
                # logging.debug('ActionWorker queue get')
                actionWrapper = self._actionManager._waitingActionsQueue.get(timeout=1)
                # stop the worker if we meet an end-of-queue markers
                if not actionWrapper:
                    logging.debug('ActionWorker end-of-queue markers')
                    return
                self.executeAction(actionWrapper)
            except queue.Empty:
                # logging.debug('ActionWorker queue empty')
                pass
