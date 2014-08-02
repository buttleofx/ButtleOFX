from PyQt5 import QtCore
from .nodeManager import NodeManager
from .viewerManager import ViewerManager
from quickmamba.patterns import Singleton
from buttleofx.data import ButtleDataSingleton
from quickmamba.models import QObjectListModel
from .connectionManager import ConnectionManager
from buttleofx.core.undo_redo.manageTools import CommandManager


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
        listOfCommand = CommandManager()
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
        cmdManager = CommandManager()
        cmdManager.clean()

    @QtCore.pyqtSlot(result=int)
    def count(self):
        listOfCommand = CommandManager()
        return len(listOfCommand.commands)

    @QtCore.pyqtSlot(result=int)
    def countRedo(self):
        listOfCommand = CommandManager()
        return len(listOfCommand.commands) - listOfCommand.index

    @QtCore.pyqtSlot(result=int)
    def countUndo(self):
        listOfCommand = CommandManager()
        return listOfCommand.index

    @QtCore.pyqtSlot()
    def deleteSelection(self):
        buttleData = ButtleDataSingleton().get()
        if buttleData.currentConnectionWrapper:
            self._connectionManager.disconnect(buttleData.currentConnectionWrapper)
        else:
            self._nodeManager.destructionNodes()

    @QtCore.pyqtSlot()
    def redo(self):
        """
            Calls the cmdManager to redo the last command.
        """
        cmdManager = CommandManager()
        cmdManager.redo()

        # Emit undo/redo display
        self.emitUndoRedoChanged()

        # If we need to update params or viewer
        buttleData = ButtleDataSingleton().get()
        buttleData.currentParamNodeChanged.emit()
        buttleData.currentViewerNodeChanged.emit()

    @QtCore.pyqtSlot(int)
    def redoNTimes(self, n):
        """
            Calls the cmdManager to redo n commands.
        """
        cmdManager = CommandManager()
        for i in range(n + 1):
            cmdManager.redo()

        # Emit undo/redo display
        self.emitUndoRedoChanged()

        # If we need to update params or viewer
        buttleData = ButtleDataSingleton().get()
        buttleData.currentParamNodeChanged.emit()
        buttleData.currentViewerNodeChanged.emit()

    @QtCore.pyqtSlot()
    def selectAllNodes(self):
        buttleData = ButtleDataSingleton().get()

        for nodeWrapper in buttleData.graphWrapper.getNodeWrappers():
            buttleData.appendNodeWrapper(nodeWrapper)

    @QtCore.pyqtSlot()
    def undo(self):
        """
            Calls the cmdManager to undo the last command.
        """
        cmdManager = CommandManager()
        cmdManager.undo()

        # Emit undo/redo display
        self.emitUndoRedoChanged()

        # If we need to update params or viewer
        buttleData = ButtleDataSingleton().get()
        buttleData.currentParamNodeChanged.emit()
        buttleData.currentViewerNodeChanged.emit()

    @QtCore.pyqtSlot(int)
    def undoNTimes(self, n):
        """
            Calls the cmdManager to undo n commands.
        """
        cmdManager = CommandManager()
        for i in range(n - 1):
            cmdManager.undo()

        # Emit undo/redo display
        self.emitUndoRedoChanged()

        # If we need to update params or viewer
        buttleData = ButtleDataSingleton().get()
        buttleData.currentParamNodeChanged.emit()
        buttleData.currentViewerNodeChanged.emit()

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getConnectionManager(self):
        return self._connectionManager

    def getNodeManager(self):
        return self._nodeManager

    def getUndoRedoStack(self):
        listOfCommand = QObjectListModel(self)

        for cmd in CommandManager().getCommands():
            listOfCommand.append(str(CommandManager().getCommands().index(cmd)) + " : " + cmd.getLabel())
        return listOfCommand

    def getViewerManager(self):
        return self._viewerManager

    # ## Others ## #

    def canRedo(self):
        """
            Calls the cmdManager to return if we can redo or not.
        """
        cmdManager = CommandManager()
        return cmdManager.canRedo()

    def canUndo(self):
        """
            Calls the cmdManager to return if we can undo or not.
        """
        cmdManager = CommandManager()
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


# This class exists just because there are problems when a class extends 2 other class (Singleton and QObject)
class ButtleManagerSingleton(Singleton):

    _buttleManager = ButtleManager()

    def get(self):
        return self._buttleManager
