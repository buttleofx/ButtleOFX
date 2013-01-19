# undo_redo
from buttleofx.core.undo_redo.manageTools import UndoableCommand
# core
from buttleofx.core.graph.connection import Connection


class CmdDeleteConnection(UndoableCommand):
    """
        Command that delete a connection between 2 clips.
    """

    def __init__(self, graph, connection):
        self._graph = graph
        self._connection = connection

    def undoCmd(self):
        """
            Undo the delete of the connection <=> recreate the connection.
        """
        self._graph.getConnections().append(self._connection)
        self._graph.connectionsChanged()

    def redoCmd(self):
        """
            Redo the delete of the connection.
        """
        self.doCmd()

    def doCmd(self):
        """
            Delete a connection.
        """
        self._graph.getConnections().remove(self._connection)
        self._graph.connectionsChanged()
