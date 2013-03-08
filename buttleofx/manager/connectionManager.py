from PySide import QtCore, QtGui
# quickmamba
from quickmamba.patterns import Signal
# data
from buttleofx.data import ButtleDataSingleton
# event
from buttleofx.event import ButtleEventSingleton
# connection
from buttleofx.core.graph.connection import IdClip


class ConnectionManager(QtCore.QObject):
    """
        This class manages actions about connections.
    """

    def __init__(self):
        super(ConnectionManager, self).__init__()

        self.undoRedoChanged = Signal()

        buttleData = ButtleDataSingleton().get()
        buttleData.getGraph().connectionsCoordChanged.connect(self.updateConnectionsCoord)
        buttleData.getGraph().connectionsChanged.connect(self.updateConnectionWrappers)

    ############### getters & flags ###############

    def getPositionClip(self, nodeName, clipName, clipNumber):
        """
            Function called when a new idClip is created.
            Returns the position of the clip.
            The calculation is the same as in the QML file (Node.qml).
        """
        buttleData = ButtleDataSingleton().get()
        node = buttleData.getGraphWrapper().getNodeWrapper(nodeName)

        nodeCoord = node.getCoord()
        widthNode = node.getWidth()
        clipSpacing = node.getClipSpacing()
        clipSize = node.getClipSize()
        heightNode = node.getHeight()
        inputTopMargin = node.getInputTopMargin()

        if (clipName == "Output"):
            xClip = nodeCoord.x() + widthNode + clipSize / 2
            yClip = nodeCoord.y() + heightNode / 2 + clipSize / 2
        else:
            xClip = nodeCoord.x() - clipSize / 2
            yClip = nodeCoord.y() + inputTopMargin + int(clipNumber) * (clipSpacing + clipSize) + clipSize / 2
        return (xClip, yClip)

    def canConnect(self, clip1, clip2):
        """
            Returns True if the connection between the nodes is possible, else False.
            A connection is possible if the clip isn't already taken, and if the clips are from 2 different nodes, not already connected.
        """
        buttleData = ButtleDataSingleton().get()
        graph = buttleData.getGraph()

        # if the clips are from the same node : False
        if (clip1.getNodeName() == clip2.getNodeName()):
            return False

        # if the clips are 2 inputs or 2 outputs : False
        if (clip1.getClipName() == "Output" and clip2.getClipName() == "Output") or (clip1.getClipName() != "Output" and clip2.getClipName() != "Output"):
            return False

        # if the input clip is already taken : False
        if (clip1.getClipName() != "Output" and graph.contains(clip1)) or (clip2.getClipName() != "Output" and graph.contains(clip2)):
            return False

        # if the nodes containing the clips are already connected : False
        if(graph.nodesConnected(clip2, clip1)):
            return False

        return True

    ############### EVENTS FROM QML ###############

    @QtCore.Slot(QtCore.QObject, int)
    def connectionDragEvent(self, clip, clipNumber):
        """
            Function called when a clip is pressed (but not released yet).
            The function send mimeData to identify the clip.
        """
        mimeData = QtCore.QMimeData()
        mimeData.setText("clip/" + str(clip.getNodeName()) + "/" + str(clip.getClipName()) + "/" + str(clipNumber))

        widget = QtGui.QWidget()

        drag = QtGui.QDrag(widget)
        drag.setMimeData(mimeData)

        drag.exec_(QtCore.Qt.MoveAction)

    @QtCore.Slot(str, QtCore.QObject, int)
    def connectionDropEvent(self, dataTmpClip, clip, clipNumber):
        """
            Create or delete a connection between 2 nodes.
        """
        buttleData = ButtleDataSingleton().get()

        infosTmpClip = dataTmpClip.split("/")

        if infosTmpClip[0] != "clip" or len(infosTmpClip) != 4:
            return
        else:
            tmpClipNodeName, tmpClipName, tmpClipNumber = infosTmpClip[1], infosTmpClip[2], int(infosTmpClip[3])

        positionTmpClip = self.getPositionClip(tmpClipNodeName, tmpClipName, tmpClipNumber)
        tmpClip = IdClip(tmpClipNodeName, tmpClipName, tmpClipNumber, positionTmpClip)

        if tmpClip:
            positionNewClip = self.getPositionClip(clip.getNodeName(), clip.getClipName(), clipNumber)
            newClip = IdClip(clip.getNodeName(), clip.getClipName(), clipNumber, positionNewClip)

            if tmpClip.getClipName() == "Output":
                clipOut = tmpClip
                clipIn = newClip
            else:
                clipOut = newClip
                clipIn = tmpClip

            if self.canConnect(clipOut, clipIn):
                    self.connect(clipOut, clipIn)
                    return

            else:
                connection = buttleData.getGraph().getConnectionByClips(clipOut, clipIn)
                if connection:
                    self.disconnect(buttleData.getGraphWrapper().getConnectionWrapper(connection.getId()))
                    return

        # update undo/redo display
        self.undoRedoChanged()

    ############### CREATION AND DESTRUCTION ###############

    def connect(self, clipOut, clipIn):
        """
            Adds a connection between 2 clips.
        """
        buttleData = ButtleDataSingleton().get()
        connection = buttleData.getGraph().createConnection(clipOut, clipIn)

    @QtCore.Slot(QtCore.QObject)
    def disconnect(self, connectionWrapper):
        """
            Removes a connection between 2 clips.
        """
        buttleData = ButtleDataSingleton().get()
        buttleData.getGraph().deleteConnection(connectionWrapper.getConnection())

    ################################################## WRAPPER LAYER ##################################################

    def updateConnectionWrappers(self):
        """
            Updates the connectionWrappers when the signal connectionsChanged has been emitted.
        """
        buttleData = ButtleDataSingleton().get()
        # we clear the list
        buttleData.getGraphWrapper().getConnectionWrappers().clear()
        # and we fill with the new data
        for connection in buttleData.getGraph().getConnections():
            buttleData.getGraphWrapper().createConnectionWrapper(connection)

    def updateConnectionsCoord(self, node):
        buttleData = ButtleDataSingleton().get()
        # for each connection of the graph
        for connection in buttleData.getGraph().getConnections():
            # if the connection conerns the node we've just moved
            if node.getName() in connection.getConcernedNodes():
                clipOut = connection.getClipOut()
                clipIn = connection.getClipIn()
                # update clipOut and clipIn coords
                clipOut.setCoord(self.getPositionClip(clipOut.getNodeName(), clipOut.getClipName(), clipOut.getClipNumber()))
                clipIn.setCoord(self.getPositionClip(clipIn.getNodeName(), clipIn.getClipName(), clipIn.getClipNumber()))
        self.updateConnectionWrappers()