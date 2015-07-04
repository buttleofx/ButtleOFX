from PyQt5 import QtCore
from .nodeManager import NodeManager
from .viewerManager import ViewerManager
from buttleofx.data import globalButtleData
from quickmamba.models import QObjectListModel
from .connectionManager import ConnectionManager
from buttleofx.core.undo_redo.manageTools import globalCommandManager


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

        # Connect undoRedoChanged signal
        self._nodeManager.undoRedoChanged.connect(self.emitUndoRedoChanged)
        self._connectionManager.undoRedoChanged.connect(self.emitUndoRedoChanged)
        self._viewerManager.undoRedoChanged.connect(self.emitUndoRedoChanged)

        return self

    # ############################################ Methods exposed to QML ############################################ #

    # ## Getters ## #

    @QtCore.pyqtSlot(result=int)
    def getIndex(self):
        listOfCommand = globalCommandManager
        return listOfCommand.index

    @QtCore.pyqtSlot(str, result=int)
    def getIndexOfUndoRedoStack(self, cmd):
        listOfCommand = self.getUndoRedoStack()
        return listOfCommand.indexOf(cmd)

    # ## Others ## #

    @QtCore.pyqtSlot()
    def clean(self):
        """
            Calls the cmdManager to clean the undo redo pile.
        """
        cmdManager = globalCommandManager
        cmdManager.clean()

    @QtCore.pyqtSlot(result=int)
    def count(self):
        listOfCommand = globalCommandManager
        return len(listOfCommand.commands)

    @QtCore.pyqtSlot(result=int)
    def countRedo(self):
        listOfCommand = globalCommandManager
        return len(listOfCommand.commands) - listOfCommand.index

    @QtCore.pyqtSlot(result=int)
    def countUndo(self):
        listOfCommand = globalCommandManager
        return listOfCommand.index

    @QtCore.pyqtSlot()
    def deleteSelection(self):
        if globalButtleData.currentConnectionWrapper:
            self._connectionManager.disconnect(globalButtleData.currentConnectionWrapper)
        else:
            self._nodeManager.destructionNodes()

    @QtCore.pyqtSlot()
    def redo(self):
        """
            Calls the cmdManager to redo the last command.
        """
        cmdManager = globalCommandManager
        cmdManager.redo()

        # Emit undo/redo display
        self.emitUndoRedoChanged()

        # If we need to update params or viewer
        globalButtleData.currentParamNodeChanged.emit()
        globalButtleData.currentViewerNodeChanged.emit()

    @QtCore.pyqtSlot(int)
    def redoNTimes(self, n):
        """
            Calls the cmdManager to redo n commands.
        """
        cmdManager = globalCommandManager
        for _ in range(n + 1):
            cmdManager.redo()

        # Emit undo/redo display
        self.emitUndoRedoChanged()

        # If we need to update params or viewer
        globalButtleData.currentParamNodeChanged.emit()
        globalButtleData.currentViewerNodeChanged.emit()

    @QtCore.pyqtSlot()
    def selectAllNodes(self):
        for nodeWrapper in globalButtleData.graphWrapper.getNodeWrappers():
            globalButtleData.appendNodeWrapper(nodeWrapper)

    @QtCore.pyqtSlot()
    def undo(self):
        """
            Calls the cmdManager to undo the last command.
        """
        cmdManager = globalCommandManager
        cmdManager.undo()

        # Emit undo/redo display
        self.emitUndoRedoChanged()

        # If we need to update params or viewer
        globalButtleData.currentParamNodeChanged.emit()
        globalButtleData.currentViewerNodeChanged.emit()

    @QtCore.pyqtSlot(int)
    def undoNTimes(self, n):
        """
            Calls the cmdManager to undo n commands.
        """
        cmdManager = globalCommandManager
        for _ in range(n - 1):
            cmdManager.undo()

        # Emit undo/redo display
        self.emitUndoRedoChanged()

        # If we need to update params or viewer
        globalButtleData.currentParamNodeChanged.emit()
        globalButtleData.currentViewerNodeChanged.emit()

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getConnectionManager(self):
        return self._connectionManager

    def getNodeManager(self):
        return self._nodeManager

    def getUndoRedoStack(self):
        listOfCommand = QObjectListModel(self)

        for cmd in globalCommandManager.getCommands():
            listOfCommand.append(str(globalCommandManager.getCommands().index(cmd)) + " : " + cmd.getLabel())
        return listOfCommand

    def getViewerManager(self):
        return self._viewerManager

    # ## Others ## #

    def canRedo(self):
        """
            Calls the cmdManager to return if we can redo or not.
        """
        cmdManager = globalCommandManager
        return cmdManager.canRedo()

    def canUndo(self):
        """
            Calls the cmdManager to return if we can undo or not.
        """
        cmdManager = globalCommandManager
        return cmdManager.canUndo()

    def emitUndoRedoChanged(self):
        self.changed.emit()

    def signalUndoRedo(self):
        self.undoRedoChanged.emit()

    # ############################################# Data exposed to QML ############################################## #

    changed = QtCore.pyqtSignal()

    # Undo redo
    canUndo = QtCore.pyqtProperty(bool, canUndo, notify=changed)
    canRedo = QtCore.pyqtProperty(bool, canRedo, notify=changed)
    undoRedoStack = QtCore.pyqtProperty(QtCore.QObject, getUndoRedoStack, constant=True)

    # Managers
    nodeManager = QtCore.pyqtProperty(QtCore.QObject, getNodeManager, constant=True)
    connectionManager = QtCore.pyqtProperty(QtCore.QObject, getConnectionManager, constant=True)
    viewerManager = QtCore.pyqtProperty(QtCore.QObject, getViewerManager, constant=True)


globalButtleManager = ButtleManager()

