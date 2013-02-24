# undo_redo
from buttleofx.core.undo_redo.manageTools import UndoableCommand
# core
from buttleofx.core.graph.connection import Connection


class CmdCreateConnection(UndoableCommand):
    """
        Command that create a connection between 2 clips
        Attributes :
        - graphTarget
        - connection : we save the buttle connection because we will need it for the redo
        - clipOut
        - clipIn
    """

    def __init__(self, graphTarget, clipOut, clipIn):
        self._graphTarget = graphTarget
        self._connection = None
        self._clipOut = clipOut
        self._clipIn = clipIn

    def undoCmd(self):
        """
            Undo the creation of the connection.
        """
        # Get the output clip and the source clip of the tuttle connection
        tuttleNodeSource = self._graphTarget.getNode(self._connection.getClipOut().getNodeName()).getTuttleNode()
        tuttleNodeOutput = self._graphTarget.getNode(self._connection.getClipIn().getNodeName()).getTuttleNode()
        outputClip = tuttleNodeSource.getClip("Output")
        srcClip = tuttleNodeOutput.getClip("Source")

        # Delete the tuttle connection
        self._graphTarget.getGraphTuttle().unconnect(outputClip, srcClip)

        # Delete the buttle connection
        self._graphTarget.getConnections().remove(self._graphTarget.getConnectionByClips(self._clipOut, self._clipIn))
        self._graphTarget.connectionsChanged()
        #print "Undo create connection : ", self._graphTarget.getGraphTuttle()

    def redoCmd(self):
        """
            Redo the creation of the connection.
        """
        # Creation of the tuttle connection
        tuttleNodeSource = self._graphTarget.getNode(self._clipOut.getNodeName()).getTuttleNode()
        tuttleNodeOutput = self._graphTarget.getNode(self._clipIn.getNodeName()).getTuttleNode()
        self._graphTarget.getGraphTuttle().connect(tuttleNodeSource, tuttleNodeOutput)

        # Creation of the buttle connection
        self._graphTarget.getConnections().append(self._connection)
        self._graphTarget.connectionsChanged()

    def doCmd(self):
        """
            Create a connection.
        """
        # Creation of the tuttle connection
        tuttleNodeSource = self._graphTarget.getNode(self._clipOut.getNodeName()).getTuttleNode()
        tuttleNodeOutput = self._graphTarget.getNode(self._clipIn.getNodeName()).getTuttleNode()
        outputClip = tuttleNodeSource.getClip("Output")
        srcClip = tuttleNodeOutput.getClip(str(self._clipIn.getName()))
        tuttleConnection = self._graphTarget.getGraphTuttle().connect(outputClip, srcClip)

        # Creation of the buttle connection
        self._connection = Connection(self._clipOut, self._clipIn, tuttleConnection)
        self._graphTarget.getConnections().append(self._connection)
        self._graphTarget.connectionsChanged()
        #print "Create connection : ", self._graphTarget.getGraphTuttle()

        # return the buttle connection
        return self._connection
