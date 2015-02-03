from PyQt5 import QtCore


class ActionWrapper(QtCore.QObject):
    """
        Expose useful data for qml such as nbActions and progression
    """
    # signals for qml
    nbProcessedChanged = QtCore.pyqtSignal()
    abortNotified = QtCore.pyqtSignal()
    progressChanged = QtCore.pyqtSignal()

    def __init__(self, actions):
        super(ActionWrapper, self).__init__()
        self._actions = actions  # actionInterface list objects
        self._nbProcessed = 0    # nb of actions processed from self._actions
        self._progress = 0
        self._nbActions = len(actions)
        self._abortFlag = False
        self.connectProgressionToActions()

    def abort(self):
        for action in self._actions:
            action.abort()
        self._abortFlag = True
        self.abortNotified.emit()

    def setNbProcessed(self, i):
        self._nbProcessed = i
        self.nbProcessedChanged.emit()

    def upProcessed(self):
        self._nbProcessed += 1
        self.nbProcessedChanged.emit()

    def getNbProcessed(self):
        return self._nbProcessed

    @QtCore.pyqtSlot()
    def emitProgressChanged(self):
        self.progressChanged.emit()

    def getProgress(self):
        tmpProgress = 0.0
        for action in self._actions:
            tmpProgress += action.getProgression()
        self._progress = round(tmpProgress / self._nbActions, 2)
        return self._progress

    def isAborted(self):
        return self._abortFlag

    def setAbort(self, abortFlag):
        # method for qml
        if abortFlag:
            self.abort()

    def getActions(self):
        return self._actions

    def connectProgressionToActions(self):
        # when self._actions::_progressChanged is emitted, it calls self.getProgression()
        for action in self._actions:
            action.getProgressSignal().connect(self.emitProgressChanged)

    # ################################## Data exposed to QML ###################################### #

    aborted = QtCore.pyqtProperty(bool, isAborted, setAbort, notify=abortNotified)
    progress = QtCore.pyqtProperty(float, getProgress, notify=progressChanged)
    nbProcessed = QtCore.pyqtProperty(int, getNbProcessed, notify=nbProcessedChanged)