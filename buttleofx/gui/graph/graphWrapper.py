from PySide import QtCore
import logging
# gui
from buttleofx.gui.graph.node import NodeWrapper
from buttleofx.gui.graph.connection import ConnectionWrapper
# quickmamba
from quickmamba.models import QObjectListModel


class GraphWrapper(QtCore.QObject):
    """
        Class GraphWrapper defined by:
        - _view : to have the view object
        - _rootObject : to have the root object

        - _nodeWrappers : list of node wrappers (the python objects we use to communicate with the QML)
        - _connectionWrappers : list of connections wrappers (the python objects we use to communicate with the QML)

        - _zMax : to manage the depth of the graph (in QML)

        - _graph : the name of the graph mapped by the instance of this class.

        This class is a view, a map, of a graph.
    """

    def __init__(self, graph, view):
        super(GraphWrapper, self).__init__(view)

        self._view = view
        self._rootObject = view.rootObject()

        self._nodeWrappers = QObjectListModel(self)
        self._connectionWrappers = QObjectListModel(self)

        self._zMax = 2

        self._graph = graph

        # the links between the graph and this graphWrapper
        self._graph.nodesChanged.connect(self.updateNodeWrappers)
        self._graph.connectionsChanged.connect(self.updateConnectionWrappers)
        self._graph.connectionsCoordChanged.connect(self.updateConnectionsCoord)

        logging.info("Gui : GraphWrapper created")

    def __str__(self):
        """
            Displays on terminal some data.
            Usefull to debug the class.
        """
        logging.info("=== Graph Buttle Wrapper ===")
        logging.info("---- all nodeWrappers ----")
        for nodeWrapper in self._nodeWrappers:
            nodeWrapper.__str__()

        logging.info("---- all connectionWrappers ----")
        for con in self._connectionWrappers:
            con.__str__()

        self.getGraphMapped().__str__()

    ################################################## ACCESSORS ##################################################

    #################### getters ####################

    def getGraphMapped(self):
        """
            Returns the graph (the node list and the connection list), mapped by this graphWrapper.
        """
        return self._graph

    def getNodeWrappers(self):
        """
            Returns the nodeWrapper list.
        """
        return self._nodeWrappers

    def getNodeWrapper(self, nodeName):
        """
            Returns the right nodeWrapper, identified with its nodeName.
        """
        for nodeWrapper in self._nodeWrappers:
            if nodeWrapper.getName() == nodeName:
                return nodeWrapper
        return None  # QtCore.QObject(self)

    def getConnectionWrappers(self):
        """
            Returns the connectionWrapper list.
        """
        return self._connectionWrappers

    def getConnectionWrapper(self, connectionId):
        """
            Returns a connectionWrapper given a connection id.
        """
        for connection in self._connectionWrappers:
            if connection.getId() == connectionId:
                return connection
        return None

    @QtCore.Slot(result=QtCore.QObject)
    def getLastCreatedNodeWrapper(self):
        return self._nodeWrappers[-1]

    def getZMax(self):
        return self._zMax

    def setZMax(self, zMax):
        self._zMax = zMax

    ################################################## CREATIONS ##################################################

    def createNodeWrapper(self, nodeName):
        """
            Creates a node wrapper and add it to the nodeWrappers list.
        """
        # search the right node in the node list
        node = self._graph.getNode(nodeName)
        if node:
            nodeWrapper = NodeWrapper(node, self._view)
            self._nodeWrappers.append(nodeWrapper)

    def createConnectionWrapper(self, connection):
        """
            Creates a connection wrapper and add it to the connectionWrappers list.
        """
        conWrapper = ConnectionWrapper(connection, self._view)
        self._connectionWrappers.append(conWrapper)

    ################################################## CONNECTIONS MANAGEMENT ##################################################

    def getPositionClip(self, nodeName, clipName, clipNumber):
        """
            Function called when a new idClip is created.
            Returns the position of the clip.
            The calculation is the same as in the QML file (Node.qml).
        """
        node = self.getNodeWrapper(nodeName)

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

    def getConnectionByClips(self, clipOut, clipIn):
        """
            Return the connection, from a clipIn and a clipOut.
        """
        for connection in self.getGraphMapped().getConnections():
            if connection.getClipOut() == clipOut and connection.getClipIn() == clipIn:
                return connection
        return None

    def canConnect(self, clip1, clip2):
        """
            Returns True if the connection between the nodes is possible, else False.
            A connection is possible if the clip isn't already taken, and if the clips are from 2 different nodes, not already connected.
        """

        # if the clips are from the same node : False
        if (clip1.getNodeName() == clip2.getNodeName()):
            return False

        # if the clips are 2 inputs or 2 outputs : False
        if (clip1.getName() == "Output" and clip2.getName() == "Output") or (clip1.getName() != "Output" and clip2.getName() != "Output"):
            return False

        # if the input clip is already taken : False
        if (clip1.getName() != "Output" and self._graph.contains(clip1)) or (clip2.getName() != "Output" and self._graph.contains(clip2)):
            return False

        # if the nodes containing the clips are already connected : False
        if(self._graph.nodesConnected(clip2, clip1)):
            return False

        return True

    ################################################## UPDATE ##################################################

    def updateNodeWrappers(self):
        """
            Updates the nodeWrappers when the signal nodesChanged has been emitted.
        """
        # we clear the list
        self._nodeWrappers.clear()
        # and we fill with the new data
        for node in self._graph.getNodes():
            self.createNodeWrapper(node.getName())

    def updateConnectionWrappers(self):
        """
            Updates the connectionWrappers when the signal connectionsChanged has been emitted.
        """
        # we clear the list
        self._connectionWrappers.clear()
        # and we fill with the new data
        for connection in self._graph.getConnections():
            self.createConnectionWrapper(connection)

    @QtCore.Slot()
    def updateConnectionsCoord(self):
        for connection in self._graph.getConnections():
            clipOut = connection.getClipOut()
            clipIn = connection.getClipIn()
            clipOut.setCoord(self.getPositionClip(clipOut.getNodeName(), clipOut.getPort(), clipOut.getClipNumber()))
            clipIn.setCoord(self.getPositionClip(clipIn.getNodeName(), clipIn.getPort(), clipIn.getClipNumber()))
        self.updateConnectionWrappers()

    ################################################## DATA EXPOSED TO QML ##################################################

    @QtCore.Signal
    def changed(self):
        pass

    # nodes changed
    nodesChanged = QtCore.Signal()
    nodes = QtCore.Property(QtCore.QObject, getNodeWrappers, notify=nodesChanged)

    # connections changed
    connectionWrappersChanged = QtCore.Signal()
    connections = QtCore.Property(QtCore.QObject, getConnectionWrappers, notify=connectionWrappersChanged)

    # nodeWrappers and connectionWrappers
    nodeWrappers = QtCore.Property(QtCore.QObject, getNodeWrappers, constant=True)
    connectionWrappers = QtCore.Property(QtCore.QObject, getConnectionWrappers, constant=True)

    # z index for QML
    zMaxChanged = QtCore.Signal()
    zMax = QtCore.Property(int, getZMax, setZMax, notify=zMaxChanged)
