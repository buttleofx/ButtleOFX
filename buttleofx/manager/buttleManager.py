from PySide import QtCore, QtGui
# Tuttle
from pyTuttle import tuttle
# quickmamba
from quickmamba.patterns import Singleton, Signal
# 'little' manager
from nodeManager import NodeManager
from connectionManager import ConnectionManager
from viewerManager import ViewerManager
# undo_redo
from buttleofx.core.undo_redo.manageTools import CommandManager
# data
from buttleofx.data import ButtleDataSingleton


class ButtleManager(QtCore.QObject):
    """
        This class catches events from QML, and manages them by call the right manager or the right methods in core.
        It's like the front manager, which delegate to other manager.
    """

    def init(self, view):
        self._view = view
        self._nodeManager = NodeManager()
        self._connectionManager = ConnectionManager()

        return self

    ############### NodeManager ###############

    @QtCore.Slot(str, int, int)
    def creationNode(self, nodeType, x, y):
        """
            Function called when we want to create a node from the QML.
        """
        self._nodeManager.creationNode(nodeType, x, y)
        self.undoRedoChanged.emit()

    @QtCore.Slot()
    def destructionNodes(self):
        """
            Function called when we want to delete a node from the QML.
        """
        self._nodeManager.destructionNodes()
        self.undoRedoChanged.emit()

    @QtCore.Slot()
    def cutNode(self):
        """
            Function called from the QML when we want to cut a node.
        """
        self._nodeManager.cutNode()
        self.undoRedoChanged.emit()

    @QtCore.Slot()
    def copyNode(self):
        """
            Function called from the QML when we want to copy a node.
        """
        self._nodeManager.copyNode()
        self.undoRedoChanged.emit()

    @QtCore.Slot()
    def pasteNode(self):
        """
            Function called from the QML when we want to paste a node.
        """
        self._nodeManager.pasteNode()
        self.undoRedoChanged.emit()

    @QtCore.Slot()
    def duplicationNode(self):
        """
            Function called from the QML when we want to duplicate a node.
        """
        self._nodeManager.duplicationNode()
        self.undoRedoChanged.emit()

    @QtCore.Slot(str, int, int)
    def dropReaderNode(self, url, x, y):
        """
            Function called when an image is dropped in the graph.
        """
        self._nodeManager.dropReaderNode(url, x, y)
        self.undoRedoChanged.emit()

    @QtCore.Slot(str, int, int)
    def nodeMoved(self, nodeName, x, y):
        """
            Fonction called when a node has moved.
        """
        self._nodeManager.nodeMoved(nodeName, x, y)
        self.undoRedoChanged.emit()

    @QtCore.Slot(str, int, int)
    def nodeIsMoving(self, nodeName, x, y):
        """
            Fonction called when a node is moving.
        """
        self._nodeManager.nodeIsMoving(nodeName, x, y)
        self.undoRedoChanged.emit()

    ############### ConnectionManager ###############

    @QtCore.Slot(QtCore.QObject, int)
    def connectionDragEvent(self, clip, clipNumber):
        """
            Function called when a clip is pressed (but not released yet).
            The function send mimeData to identify the clip.
        """
        mimeData = QtCore.QMimeData()
        mimeData.setText("clip/" + str(clip.getNodeName()) + "/" + str(clip.getName()) + "/" + str(clipNumber))

        drag = QtGui.QDrag(self._view)
        drag.setMimeData(mimeData)

        drag.exec_(QtCore.Qt.MoveAction)

    @QtCore.Slot(str, QtCore.QObject, int)
    def connectionDropEvent(self, dataTmpClip, clip, clipNumber):
        """
            Function called when a clip is released (after pressed).
        """
        self._connectionManager.connectionDropEvent(dataTmpClip, clip, clipNumber)
        self.undoRedoChanged.emit()

    ############### UNDO & REDO ###############

    @QtCore.Slot()
    def undo(self):
        """
            Calls the cmdManager to undo the last command.
        """
        cmdManager = CommandManager()
        cmdManager.undo()
        self.undoRedoChanged.emit()

        # if we need to update params or viewer
        buttleData = ButtleDataSingleton().get()
        buttleData.currentParamNodeChanged.emit()
        buttleData.currentViewerNodeChanged.emit()

    @QtCore.Slot()
    def redo(self):
        """
            Calls the cmdManager to redo the last command.
        """
        cmdManager = CommandManager()
        cmdManager.redo()
        self.undoRedoChanged.emit()

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

    ############### ViewerManager ###############

    @QtCore.Slot()
    def mosquitoDragEvent(self):
        """
            Function called when the viewer's mosquito is dragged.
            The function send the mimeData and launch a drag event.
        """

        mimeData = QtCore.QMimeData()
        mimeData.setText("mosquito_of_the_dead")

        drag = QtGui.QDrag(self._view)
        drag.setMimeData(mimeData)

        drag.exec_(QtCore.Qt.MoveAction)

    ################################################## DATA EXPOSED TO QML ##################################################

    # undo redo
    undoRedoChanged = QtCore.Signal()
    canUndo = QtCore.Property(bool, canUndo, notify=undoRedoChanged)
    canRedo = QtCore.Property(bool, canRedo, notify=undoRedoChanged)


# This class exists just because thre are problems when a class extends 2 other class (Singleton and QObject)
class ButtleManagerSingleton(Singleton):

    _buttleManager = ButtleManager()

    def get(self):
        return self._buttleManager
