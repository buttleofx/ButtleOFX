# 'little' managers
from .nodeManager import NodeManager
from .connectionManager import ConnectionManager
from .viewerManager import ViewerManager

from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.data import ButtleDataSingleton

from quickmamba.patterns import Singleton

from PyQt5 import QtCore


class ButtleManager(QtCore.QObject):
    """
        This class catches events from QML, and manages them by calling the right manager or the right methods in core.
        It's like the front manager, which delegate to other managers.
        This class also catches events from QML about undo / redo.
    """

    def init(self):
        self._nodeManager = NodeManager()
        self._connectionManager = ConnectionManager()
        self._viewerManager = ViewerManager()

        # connect undoRedoChanged signal
        self._nodeManager.undoRedoChanged.connect(self.emitUndoRedoChanged)
        self._connectionManager.undoRedoChanged.connect(self.emitUndoRedoChanged)
        self._viewerManager.undoRedoChanged.connect(self.emitUndoRedoChanged)

        return self
        
    @QtCore.pyqtSlot()  
    def selectAllNodes(self):
        buttleData = ButtleDataSingleton().get()
        for nodeWrapper in buttleData.graphWrapper.getNodeWrappers():
            buttleData.appendNodeWrapper(nodeWrapper)
        
    ############### getters ###############

    def getNodeManager(self):
        return self._nodeManager

    def getConnectionManager(self):
        return self._connectionManager

    def getViewerManager(self):
        return self._viewerManager

    ############### UNDO & REDO ###############

    @QtCore.pyqtSlot()
    def undo(self):
        """
            Calls the cmdManager to undo the last command.
        """
        cmdManager = CommandManager()
        cmdManager.undo()

        # emit undo/redo display
        self.emitUndoRedoChanged()

        # if we need to update params or viewer
        buttleData = ButtleDataSingleton().get()
        buttleData.currentParamNodeChanged.emit()
        buttleData.currentViewerNodeChanged.emit()

    @QtCore.pyqtSlot()
    def redo(self):
        """
            Calls the cmdManager to redo the last command.
        """
        cmdManager = CommandManager()
        cmdManager.redo()

        # emit undo/redo display
        self.emitUndoRedoChanged()

        # if we need to update params or viewer
        buttleData = ButtleDataSingleton().get()
        buttleData.currentParamNodeChanged.emit()
        buttleData.currentViewerNodeChanged.emit()

    def signalUndoRedo(self):
        self.undoRedoChanged.emit()

    def canUndo(self):
        """
            Calls the cmdManager to return if we can undo or not.
        """
        cmdManager = CommandManager()
        return cmdManager.canUndo()

    def canRedo(self):
        """
            Calls the cmdManager to return if we can redo or not.
        """
        cmdManager = CommandManager()
        return cmdManager.canRedo()

    ############### DELETION ###############
    @QtCore.pyqtSlot()
    def deleteSelection(self):
        buttleData = ButtleDataSingleton().get()
        if(buttleData.currentConnectionWrapper):
            self._connectionManager.disconnect(buttleData.currentConnectionWrapper)
        else:
            self._nodeManager.destructionNodes()

    ################################################## DATA EXPOSED TO QML ##################################################

    changed = QtCore.pyqtSignal()

    def emitUndoRedoChanged(self):
        self.changed.emit()

    # undo redo
    canUndo = QtCore.pyqtProperty(bool, canUndo, notify=changed)
    canRedo = QtCore.pyqtProperty(bool, canRedo, notify=changed)

    # managers
    nodeManager = QtCore.pyqtProperty(QtCore.QObject, getNodeManager, constant=True)
    connectionManager = QtCore.pyqtProperty(QtCore.QObject, getConnectionManager, constant=True)
    viewerManager = QtCore.pyqtProperty(QtCore.QObject, getViewerManager, constant=True)


# This class exists just because thre are problems when a class extends 2 other class (Singleton and QObject)
class ButtleManagerSingleton(Singleton):

    _buttleManager = ButtleManager()

    def get(self):
        return self._buttleManager
