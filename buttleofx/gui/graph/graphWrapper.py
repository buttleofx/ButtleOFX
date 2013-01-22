from PySide import QtCore
# core
from buttleofx.core.graph.connection import IdClip
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

        - _tmpClipOut : the future connected output clip when a connection is beeing created. It correspounds of the output clip which was beeing clicked and not connected for the moment.
        - _tmpClipIn : the future connected input clip when a connection is beeing created. It correspounds of the input clip which was beeing clicked and not connected for the moment.
        
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

        self._tmpClipIn = None
        self._tmpClipOut = None

        self._zMax = 2

        self._graph = graph

        # the links between the graph and this graphWrapper
        self._graph.nodesChanged.connect(self.updateNodeWrappers)
        self._graph.connectionsChanged.connect(self.updateConnectionWrappers)
        self._graph.connectionsCoordChanged.connect(self.updateConnectionsCoord)

        print "Gui : GraphWrapper created"


    def __str__(self):
        """
            Displays on terminal some data.
            Usefull to debug the class.
        """
        print("---- all nodeWrappers ----")
        for nodeWrapper in self._nodeWrappers:
            print nodeWrapper.getName() + " " + str(nodeWrapper.getCoord())

        print("---- all nodes ----")
        for node in self._graph._nodes:
            print node._name + " " + str(node.getCoord())

        print("---- all connectionWrappers ----")
        for con in self._connectionWrappers:
            con.__str__()

        print("---- all connections ----")
        for con in self._graph._connections:
            con.__str__()

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
        return None

    def getConnectionWrappers(self):
        """
            Returns the connectionWrapper list.
        """
        return self._connectionWrappers

    def getTmpClipOut(self):
        return self._tmpClipOut

    def getTmpClipIn(self):
        return self._tmpClipIn

    def getWidthNode(self):
        return NodeWrapper.widthNode

    def getHeightEmptyNode(self):
        return NodeWrapper.heightEmptyNode

    def getClipSpacing(self):
        return NodeWrapper.clipSpacing

    def getClipSize(self):
        return NodeWrapper.clipSize

    def getNodeInputSideMargin(self):
        return NodeWrapper.inputSideMargin

    @QtCore.Slot(result="QVariant")
    def getLastCreatedNodeWrapper(self):
        return self._nodeWrappers[-1]

    def getZMax(self):
        return self._zMax

    def setZMax(self, zMax):
        self._zMax = zMax

    #################### setters ####################

    def resetTmpClips(self):
        self._tmpClipIn = None
        self._tmpClipOut = None

    def setTmpClipOut(self, idClip):
        self._tmpClipOut = idClip

    def setTmpClipIn(self, idClip):
        self._tmpClipIn = idClip

    ################################################## CREATIONS ##################################################

    def createNodeWrapper(self, nodeName):
        """
            Creates a node wrapper and add it to the nodeWrappers list.
        """
        # search the right node in the node list
        node = self._graph.getNode(nodeName)
        if (node != None):
            nodeWrapper = NodeWrapper(node, self._view)
            self._nodeWrappers.append(nodeWrapper)

    def createConnectionWrapper(self, connection):
        """
            Creates a connection wrapper and add it to the connectionWrappers list.
        """
        conWrapper = ConnectionWrapper(connection, self._view)
        self._connectionWrappers.append(conWrapper)

    ################################################## CONNECTIONS MANAGEMENT ##################################################

    def getPositionClip(self, nodeName, port, clipNumber):
        """
            Function called when a new idClip is created.
            Returns the position of the clip.
            The calculation is the same as in the QML file (Node.qml).
        """
        nodeCoord = self._graph.getNode(nodeName).getCoord()
        widthNode = self.getWidthNode()
        heightEmptyNode = self.getHeightEmptyNode()
        clipSpacing = self.getClipSpacing()
        clipSize = self.getClipSize()
        nbInput = self._graph.getNode(nodeName).getNbInput()
        heightNode = heightEmptyNode + clipSpacing * nbInput
        inputTopMargin = (heightNode - clipSize * nbInput - clipSpacing * (nbInput - 1)) / 2

        if (port == "input"):
            xClip = nodeCoord[0] - clipSize / 2
            yClip = nodeCoord[1] + inputTopMargin + (clipNumber) * (clipSpacing + clipSize) + clipSize / 2
        elif (port == "output"):
            xClip = nodeCoord[0] + widthNode + clipSize / 2
            yClip = nodeCoord[1] + heightNode / 2 + clipSize / 2
        return (xClip, yClip)

    def getConnectionByClips(self, clipOut, clipIn):
        """
            Return the connection, from a clipIn and a clipOut.
        """
        for connection in self.getGraphMapped().getConnections():
            if connection.getClipOut() == clipOut and connection.getClipIn() == clipIn:
                return connection
        return None

    def canConnect(self, clipOut, clipIn):
        """
            Returns True if the connection between the nodes is possible, else False.
            A connection is possible if the clip isn't already taken, and if the clips are from 2 different nodes, not already connected.
        """
        # if the clips are from the same node : False
        if (clipOut.getNodeName() == clipIn.getNodeName()):
            return False
        # if the input clip is already taken : False
        if (self._graph.contains(clipIn)):
            return False
        # if the nodes containing the clips are already connected : False
        if(self._graph.nodesConnected(clipOut, clipIn)):
            return False

        return True

    ################################################## UPDATE ##################################################

    def updateNodeWrappers(self):
        """
            Updates the nodeWrappers when the signal nodesChanged has been emitted.
        """
        print "=> UPDATE NODE WRAPPERS"
        # we clear the list
        self._nodeWrappers.clear()
        # and we fill with the new data
        for node in self._graph.getNodes():
            self.createNodeWrapper(node.getName())
        #self.__str__()

    def updateConnectionWrappers(self):
        """
            Updates the connectionWrappers when the signal connectionsChanged has been emitted.
        """
        print "=> UPDATE CONNECTION WRAPPERS"
        # we clear the list
        self._connectionWrappers.clear()
        # and we fill with the new data
        for connection in self._graph.getConnections():
            self.createConnectionWrapper(connection)
        #self.__str__()

    @QtCore.Slot()
    def updateConnectionsCoord(self):
        print "=> UPDATE CONNECTION COORDS"
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
    nodes = QtCore.Property("QVariant", getNodeWrappers, notify=nodesChanged)

    # connections changed
    connectionWrappersChanged = QtCore.Signal()
    connections = QtCore.Property("QVariant", getConnectionWrappers, notify=connectionWrappersChanged)

    # nodeWrappers and connectionWrappers
    nodeWrappers = QtCore.Property(QtCore.QObject, getNodeWrappers, constant=True)
    connectionWrappers = QtCore.Property(QtCore.QObject, getConnectionWrappers, constant=True)

    # z index for QML
    zMaxChanged = QtCore.Signal()
    zMax = QtCore.Property(int, getZMax, setZMax, notify=zMaxChanged)

    # for a clean display of connection
    widthNode = QtCore.Property(int, getWidthNode, notify=changed)
    heightEmptyNode = QtCore.Property(int, getHeightEmptyNode, notify=changed)
    clipSpacing = QtCore.Property(int, getClipSpacing, notify=changed)
    clipSize = QtCore.Property(int, getClipSize, notify=changed)
    nodeInputSideMargin = QtCore.Property(int, getNodeInputSideMargin, notify=changed)
