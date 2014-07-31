from PyQt5 import QtCore
from buttleofx.event import ButtleEventSingleton
from buttleofx.core.graph.connection import Connection
from buttleofx.core.undo_redo.manageTools import UndoableCommand


class CmdCreateConnection(UndoableCommand):
    """
        Command that creates a connection between 2 clips
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

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getLabel(self):
        return "Create connection between '{0}' and '{1}'".format(self.getOut_clipNodeName(), self.getIn_clipNodeName())

    def getIn_clipNodeName(self):
        return self._connection.getClipIn().getNodeName()

    def getOut_clipNodeName(self):
        return self._connection.getClipOut().getNodeName()

    # ## Others ## #

    def doCmd(self):
        """
            Creates a connection.
        """
        # Creation of the tuttle connection
        tuttleNodeSource = self._graphTarget.getNode(self._clipOut.getNodeName()).getTuttleNode()
        tuttleNodeOutput = self._graphTarget.getNode(self._clipIn.getNodeName()).getTuttleNode()
        outputClip = tuttleNodeSource.getClip("Output")
        srcClip = tuttleNodeOutput.getClip(str(self._clipIn.getClipName()))
        tuttleConnection = self._graphTarget.getGraphTuttle().connect(outputClip, srcClip)

        # Creation of the buttle connection
        self._connection = Connection(self._clipOut, self._clipIn, tuttleConnection)
        self._graphTarget.getConnections().append(self._connection)
        self._graphTarget.connectionsChanged()

        # return the buttle connection
        return self._connection

    def redoCmd(self):
        """
            Redoes the creation of the connection.
        """
        # Creation of the tuttle connection
        tuttleNodeSource = self._graphTarget.getNode(self._clipOut.getNodeName()).getTuttleNode()
        tuttleNodeOutput = self._graphTarget.getNode(self._clipIn.getNodeName()).getTuttleNode()
        self._graphTarget.getGraphTuttle().connect(tuttleNodeSource, tuttleNodeOutput)

        # Creation of the buttle connection
        self._graphTarget.getConnections().append(self._connection)
        self._graphTarget.connectionsChanged()

    def undoCmd(self):
        """
            Undoes the creation of the connection.
        """
        # Get the output clip and the source clip of the tuttle connection
        tuttleNodeSource = self._graphTarget.getNode(self._connection.getClipOut().getNodeName()).getTuttleNode()
        tuttleNodeOutput = self._graphTarget.getNode(self._connection.getClipIn().getNodeName()).getTuttleNode()
        outputClip = tuttleNodeSource.getClip("Output")
        srcClip = tuttleNodeOutput.getClip(str(self._clipIn.getClipName()))

        # Delete the tuttle connection
        self._graphTarget.getGraphTuttle().unconnect(outputClip, srcClip)

        # Delete the buttle connection
        self._graphTarget.getConnections().remove(self._graphTarget.getConnectionByClips(self._clipOut, self._clipIn))
        self._graphTarget.connectionsChanged()

    # ############################################# Data exposed to QML ############################################# #

    in_clipNodeName = QtCore.pyqtProperty(str, getIn_clipNodeName, constant=True)
    out_clipNodeName = QtCore.pyqtProperty(str, getOut_clipNodeName, constant=True)
