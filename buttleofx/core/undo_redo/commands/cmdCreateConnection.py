# undo_redo
from buttleofx.core.undo_redo.manageTools import UndoableCommand
# core
from buttleofx.core.graph.connection import Connection


class CmdCreateConnection(UndoableCommand):
    """
        Command that create a connection between 2 clips.
    """

    def __init__(self, graphTarget, clipOut, clipIn):
        self._graphTarget = graphTarget
        self._clipOut = clipOut
        self._clipIn = clipIn

    def undoCmd(self):
        """
            Undo the creation of the connection.
        """
        self._graphTarget.getGraphTuttle().unconnect(self._graphTarget.getNode(self._clipOut.getNodeName()).getTuttleNode())
        self._graphTarget.getConnections().remove(self._graphTarget.getConnectionByClips(self._clipOut, self._clipIn))
        self._graphTarget.connectionsChanged()

    def redoCmd(self):
        """
            Redo the creation of the connection.
        """
        self.doCmd()

    def doCmd(self):
        """
            Create a connection.
        """

        tuttleNodeSource = self._graphTarget.getNode(self._clipOut.getNodeName()).getTuttleNode()
        tuttleNodeOutput = self._graphTarget.getNode(self._clipIn.getNodeName()).getTuttleNode()
        tuttleConnection = self._graphTarget.getGraphTuttle().connect(tuttleNodeSource, tuttleNodeOutput)

        self._graphTarget.getGraphTuttle().__str__()

        self._graphTarget.getConnections().append(Connection(self._clipOut, self._clipIn, tuttleConnection))
        self._graphTarget.connectionsChanged()
