# undo_redo
from buttleofx.core.undo_redo.manageTools import UndoableCommand
# core
from buttleofx.core.graph.connection import Connection


class CmdCreateConnection(UndoableCommand):
    """
        Command that moves a node
    """

    def __init__(self, graph, clipOut, clipIn):
        self._graph = graph
        self._connection = Connection(clipOut, clipIn)

    def undoCmd(self):
        """
            Undo the creation of the connection.
        """
        print "Undo creation of the connection "
        self._graph.deleteConnection(self._connection)
        self._graph.connectionsChanged()

    def redoCmd(self):
        """
            Redo the creation of the connection.
        """
        print "Redo creation of the connection"
        self.doCmd()

    def doCmd(self):
        """
            Create a connection.
        """
        self._graph.getConnections().append(self._connection)
        self._graph.connectionsChanged()
