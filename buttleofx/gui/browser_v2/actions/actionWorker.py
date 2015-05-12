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

    def executeActionWrapper(self, actionWrapper):
        self._actionManager.getRunningActions().append(actionWrapper)
        self._actionManager.actionChanged.emit()
        actionWrapper.executeActions()
        self._actionManager.getRunningActions().remove(actionWrapper)
        self._actionManager.getEndedActions().append(actionWrapper)

    def run(self):
        while True:
            try:
                # logging.debug('ActionWorker queue get')
                actionWrapper = self._actionManager.getWaitingActionsQueue().get(timeout=1)
                # stop the worker if we meet an end-of-queue markers
                if not actionWrapper:
                    logging.debug('ActionWorker end-of-queue markers')
                    return
                self.executeActionWrapper(actionWrapper)
            except queue.Empty:
                # logging.debug('ActionWorker queue empty')
                pass
