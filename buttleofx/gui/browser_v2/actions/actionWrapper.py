import time
from PyQt5 import QtCore


class ActionWrapper(QtCore.QObject):
    """
        Expose useful data for qml such as nbActions and progression
    """
    # signals for qml
    nbProcessedChanged = QtCore.pyqtSignal()
    abortNotified = QtCore.pyqtSignal()
    progressChanged = QtCore.pyqtSignal()
    timeProcessChange = QtCore.pyqtSignal()

    def __init__(self, actions):
        super(ActionWrapper, self).__init__()
        self._actions = actions  # actionInterface list objects
        self._nbProcessed = 0    # nb of actions processed from self._actions
        self._progress = 0
        self._nbActions = len(actions)
        self._abortFlag = False
        self._timeProcess = ""
        self.updateTimeProcess()
        self.connectProgressionToActions()

    def updateTimeProcess(self):
        self._timeProcess = time.strftime("%X", time.localtime())
        self.timeProcessChange.emit()

    def getTimeProcess(self):
        return self._timeProcess

    def executeActions(self):
        self.updateTimeProcess()
        for action in self._actions:
            action.process()
            self.upProcessed()
        self.updateTimeProcess()

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

    @QtCore.pyqtSlot(result=str)
    def getName(self):
        return self._actions[0].__class__.__name__ if self._actions and len(self._actions) > 0 else "Action"

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

    def getNbTotalActions(self):
        return len(self._actions)

    def getIdObject(self):
        return id(self)


    # ################################## Data exposed to QML ###################################### #

    aborted = QtCore.pyqtProperty(bool, isAborted, setAbort, notify=abortNotified)
    progress = QtCore.pyqtProperty(float, getProgress, notify=progressChanged)
    nbProcessed = QtCore.pyqtProperty(int, getNbProcessed, notify=nbProcessedChanged)
    timeProcess = QtCore.pyqtProperty(str, getTimeProcess, notify=timeProcessChange)
    nbTotalActions = QtCore.pyqtProperty(int, getNbTotalActions, constant=True)
