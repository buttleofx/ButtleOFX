import logging
from PyQt5 import QtCore


class ActionInterface(QtCore.QObject):
    """
        Interface which determines the template comportment for an action on a BrowserItem
        execute and revert methods must be implemented.
    """
    _progressChanged = QtCore.pyqtSignal()  # used to reporting in actionWrapper(via connectProgression)

    def __init__(self, browserItem):
        super(ActionInterface, self).__init__()
        self._browserItem = browserItem

        # required for abort processing
        self._abortFlag = False      # if action have been aborted
        self._progress = 0.0         # progression of action between 0 and 1,will be used with Tuttle process in execute

    def __del__(self):
        # logging.debug("Action destroyed")
        pass

    def begin(self):
        if self._browserItem:
            self._browserItem.notifyAddAction()

    def end(self):
        if self._browserItem:
            self._browserItem.notifyRemoveAction()

    def abort(self):
        """
            Process revert() if action processed
        """
        if self._browserItem:
            self._abortFlag = True
            if self.isProcessed():
                self.revert()
                self._browserItem.notifyRemoveAction()

    def execute(self):
        raise NotImplementedError("ActionInterface::execute() must be implemented")

    def revert(self):
        raise NotImplementedError("ActionInterface::revert() must be implemented")

    def process(self):
        if self._abortFlag:
            return
        self.begin()
        self.execute()
        self.end()
        self._progress = 1
        self._progressChanged.emit()

    def getBrowserItem(self):
        return self._browserItem

    def isProcessed(self):
        return self._progress >= 1

    def getProgression(self):
        return self._progress

    def getProgressSignal(self):
        return self._progressChanged
