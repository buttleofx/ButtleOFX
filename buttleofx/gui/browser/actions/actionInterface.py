import logging

from PyQt5 import QtCore


class ActionInterface(QtCore.QObject):
    """
        Interface which determines the template comportment for an action on a BrowserItem
        execute and revert methods must be implemented.
    """
    progressChanged = QtCore.pyqtSignal()  # used to reporting in actionWrapper(via connectProgression)

    def __init__(self, browserItem):
        QtCore.QObject.__init__(self)
        self._browserItem = browserItem

        # required for abort processing
        self._abortFlag = False      # if action has been aborted
        self._progress = 0.0         # progression of action between 0 and 1 will be used with Tuttle process in execute
        self._failed = False

    def __del__(self):
        logging.debug("Action destroyed")

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
        if not self._browserItem or self._failed:
            return

        self._abortFlag = True
        if self.isProcessed():
            self.revert()

    def execute(self):
        raise NotImplementedError("ActionInterface::execute() must be implemented")

    def revert(self):
        raise NotImplementedError("ActionInterface::revert() must be implemented")

    def process(self):
        if self._abortFlag:
            return

        self.begin()

        try:
            self.execute()
        except Exception as e:
            print(str(e))
            self._failed = True

        self.end()
        self._progress = 0 if self._failed else 1
        self.progressChanged.emit()

    def getBrowserItem(self):
        return self._browserItem

    def isProcessed(self):
        return self._progress >= 1

    def getProgression(self):
        return self._progress

    def getProgressSignal(self):
        return self.progressChanged
