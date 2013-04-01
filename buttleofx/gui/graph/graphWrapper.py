from PySide import QtCore
import logging
# quickmamba
from quickmamba.models import QObjectListModel
# gui
from buttleofx.gui.graph.node import NodeWrapper
from buttleofx.gui.graph.connection import ConnectionWrapper


class GraphWrapper(QtCore.QObject):
    """
        Class GraphWrapper defined by:
            - _view : to have the view object
            - _rootObject : to have the root object

            - _nodeWrappers : list of node wrappers (the python objects we use to communicate with the QML)
            - _connectionWrappers : list of connections wrappers (the python objects we use to communicate with the QML)

            - _zMax : to manage the depth of the graph (in QML)

            - _graph : the name of the graph mapped by the instance of this class.

        This class is a view (= a map) of a graph.
    """

    def __init__(self, graph, view):
        super(GraphWrapper, self).__init__(view)

        self._view = view
        self._rootObject = view.rootObject()

        self._nodeWrappers = QObjectListModel(self)
        self._connectionWrappers = QObjectListModel(self)

        self._zMax = 2

        self._graph = graph

        # links core signals to wrapper layer
        self._graph.nodesChanged.connect(self.updateNodeWrappers)
        self._graph.connectionsCoordChanged.connect(self.updateConnectionsCoord)
        self._graph.connectionsChanged.connect(self.updateConnectionWrappers)

        logging.info("Gui : GraphWrapper created")

    def __str__(self):
        """
            Displays on terminal some data.
            Usefull to debug the class.
        """
        str_list = []

        str_list.append("=== Graph Buttle Wrapper === \n")
        str_list.append("---- all nodeWrappers ---- \n")

        for nodeWrapper in self._nodeWrappers:
            str_list.append(nodeWrapper.__str__())
            str_list.append("\n")

        str_list.append("---- all connectionWrappers ---- \n")
        for con in self._connectionWrappers:
            str_list.append(con.__str__())
            str_list.append("\n")

        str_list.append((self.getGraphMapped()).__str__())

        return ''.join(str_list)

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
        """
            Returns the wrapper of the last node created.
        """
        return self._nodeWrappers[-1]

    def getZMax(self):
        """
            Returns the depth of the QML graph
        """
        return self._zMax

    def getPositionClip(self, nodeName, clipName, clipIndex):
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
        inputTopMargin = node.getInputTopMargin()
        outputTopMargin = node.getOutputTopMargin()

        if (clipName == "Output"):
            xClip = nodeCoord.x() + widthNode + clipSize / 2
            yClip = nodeCoord.y() + outputTopMargin + clipSize / 2
        else:
            xClip = nodeCoord.x() - clipSize / 2
            yClip = nodeCoord.y() + inputTopMargin + int(clipIndex) * (clipSpacing + clipSize) + clipSize / 2
        return (xClip, yClip)

    #################### setters ####################

    def setZMax(self, zMax):
        """
            Sets the depth of the QML graph
        """
        self._zMax = zMax

    ################################################## CREATIONS ##################################################

    def createNodeWrapper(self, nodeName):
        """
            Creates a node wrapper and add it to the nodeWrappers list.
        """
        # we search the right node in the node list
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

    ################################################ UPDATE WRAPPER LAYER ################################################

    def updateNodeWrappers(self):
        """
            Updates the nodeWrappers when the signal nodesChanged has been emitted.
        """
        # we clear the list
        self.getNodeWrappers().clear()
        # and we fill with the new data
        for node in self._graph.getNodes():
            self.createNodeWrapper(node.getName())

    def updateConnectionWrappers(self):
        """
            Updates the connectionWrappers when the signal connectionsChanged has been emitted.
        """
        # we clear the list
        self.getConnectionWrappers().clear()
        # and we fill with the new data
        for connection in self._graph.getConnections():
            self.createConnectionWrapper(connection)

    @QtCore.Slot(QtCore.QObject)
    def updateConnectionsCoord(self, node):
        """
            Updates the coordinates of the connections when a node is beeing moved.
            This update just affects the connections of the moving node.
        """
        # for each connection of the graph
        for connection in self._graph.getConnections():
            # if the connection concerns the node we're moving
            if node.getName() in connection.getConcernedNodes():
                clipOut = connection.getClipOut()
                clipIn = connection.getClipIn()
                if self.getNodeWrapper(clipOut.getNodeName()) != None:
                    # update clipOut coords
                    clipOut.setCoord(self.getPositionClip(clipOut.getNodeName(), clipOut.getClipName(), clipOut.getClipIndex()))
                if self.getNodeWrapper(clipIn.getNodeName()) != None:
                    # update clipIn coords
                    clipIn.setCoord(self.getPositionClip(clipIn.getNodeName(), clipIn.getClipName(), clipIn.getClipIndex()))
        self.updateConnectionWrappers()

    ################################################## DATA EXPOSED TO QML ##################################################

    # nodeWrappers and connectionWrappers
    nodeWrappers = QtCore.Property(QtCore.QObject, getNodeWrappers, constant=True)
    connectionWrappers = QtCore.Property(QtCore.QObject, getConnectionWrappers, constant=True)

    # z index for QML (good superposition of nodes in the graph)
    zMaxChanged = QtCore.Signal()
    zMax = QtCore.Property(int, getZMax, setZMax, notify=zMaxChanged)
