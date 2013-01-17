from PySide import QtDeclarative, QtCore
# core : graph
from buttleofx.core.graph import Graph
# gui : graphWrapper
from buttleofx.gui.graph import GraphWrapper
# undo redo
from buttleofx.core.undo_redo.manageTools import CommandManager
#quickmamba
from quickmamba.patterns import Singleton

class ButtleData(QtCore.QObject, Singleton):
    """
        Class ButtleData defined by:
        - _graph
        - _graphWrapper

        This class containts all data we need to manage the application.
        Emit signal when modifications happen
    """
    def init(self, view):
        self._graph = Graph()
        self._graphWrapper = GraphWrapper(self._graph, view)
        return self

    def getGraph(self):
        return self._graph

    @QtCore.Slot(result=GraphWrapper)
    def getGraphWrapper(self):
        return self._graphWrapper

    @QtCore.Slot()
    def undo(self):
        cmdManager = CommandManager()
        cmdManager.undo()

    @QtCore.Slot()
    def redo(self):
        cmdManager = CommandManager()
        cmdManager.redo()

