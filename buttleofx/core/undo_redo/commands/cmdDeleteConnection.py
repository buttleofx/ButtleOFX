# undo_redo
from buttleofx.core.undo_redo.manageTools import UndoableCommand
# core
from buttleofx.core.graph.connection import Connection


class CmdDeleteConnection(UndoableCommand):
    """
        Command that delete a connection between 2 clips.
        Attributes :
        - graphTarget
        - connection : we save the buttle connection because we will need it for the redo
    """

    def __init__(self, graphTarget, connection):
        self._graphTarget = graphTarget
        self._connection = connection

    def undoCmd(self):
        """
            Undo the delete of the connection <=> recreate the connection.
        """
        tuttleNodeSource = self._graphTarget.getNode(self._connection.getClipOut().getNodeName()).getTuttleNode()
        tuttleNodeOutput = self._graphTarget.getNode(self._connection.getClipIn().getNodeName()).getTuttleNode()
        self._graphTarget.getGraphTuttle().connect(tuttleNodeSource, tuttleNodeOutput)
        self._graphTarget.getConnections().append(self._connection)
        self._graphTarget.connectionsChanged()

    def redoCmd(self):
        """
            Redo the delete of the connection.
        """
        self.doCmd()

    def doCmd(self):
        """
            Delete a connection.
        """
        # Function unconnect deletes all the node's connections, we are waiting for the binding of a more adapted function
        self._graphTarget.getGraphTuttle().unconnect(self._graphTarget.getNode(self._connection.getClipOut().getNodeName()).getTuttleNode())
        self._graphTarget.getConnections().remove(self._connection)
        self._graphTarget.connectionsChanged()

