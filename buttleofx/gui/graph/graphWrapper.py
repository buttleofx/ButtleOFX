from PySide import QtCore
# core
from buttleofx.core.graph.connection import IdClip
# undo redo
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands import CmdSetCoord
# gui
from buttleofx.gui.graph.node import NodeWrapper
from buttleofx.gui.graph.connection import ConnectionWrapper
# quickmamba
from quickmamba.models import QObjectListModel


class GraphWrapper(QtCore.QObject):
    """
        Class GraphWrapper defined by:
        - _rootObject : to have the root object
        - _nodeWrappers : list of node wrappers (the python objects we use to communicate with the QML)
        - _connectionWrappers : list of connections wrappers (the python objects we use to communicate with the QML)
        - _currentNodeName : the current selected node (in QML). This is just the name of the node.
        - _currentNodeWrapper : the current selected node (in QML). This is a NodeWrapper.
        - _tmpClipOut : the future connected output clip when a connection is beeing created. It correspounds of the output clip which was beeing clicked and not connected for the moment.
        - _tmpClipIn : the future connected input clip when a connection is beeing created. It correspounds of the input clip which was beeing clicked and not connected for the moment.
        - _zMax : to manage the depth of the graph (in QML)
        - _graph : the data of the graph (python objects, the core data : the nodes and the connections)

        Creates a QObject from a given python object Graph.

    """

    def __init__(self, graph, view):
        super(GraphWrapper, self).__init__(view)

        self._view = view
        self._rootObject = view.rootObject()

        self._nodeWrappers = QObjectListModel(self)
        self._connectionWrappers = QObjectListModel(self)

        self._currentParamNodeName = None
        self._currentParamNodeWrapper = None

        self._currentSelectedNodeName = None
        self._currentSelectedNodeWrapper = None

        self._currentViewerNodeName = None
        self._currentViewerNodeWrapper = None

        self._tmpClipIn = None
        self._tmpClipOut = None

        self._zMax = 2

        self._graph = graph

        # the links between the graph and this graphWrapper
        graph.nodesChanged.connect(self.updateNodeWrappers)
        graph.connectionsChanged.connect(self.updateConnectionWrappers)
        graph.connectionsCoordChanged.connect(self.updateConnectionsCoord)


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

    def getGraph(self):
        """
            Returns the graph (the node list and the connection list).
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

    def getCurrentParamNodeName(self):
        """
            Returns the name of the current param node.
        """
        return self._currentParamNodeName

    def getCurrentSelectedNodeName(self):
        """
            Returns the name of the current selected node.
        """
        return self._currentSelectedNodeName

    def getCurrentViewerNodeName(self):
        """
            Returns the name of the current viewer node.
        """
        return self._currentViewerNodeName

    def getCurrentParamNodeWrapper(self):
        """
            Returns the current param nodeWrapper.
        """
        return self.getNodeWrapper(self.getCurrentParamNodeName())

    def getCurrentSelectedNodeWrapper(self):
        """
            Returns the current selected nodeWrapper.
        """
        return self.getNodeWrapper(self.getCurrentSelectedNodeName())

    def getCurrentViewerNodeWrapper(self):
        """
            Returns the current viewer nodeWrapper.
        """
        return self.getNodeWrapper(self.getCurrentViewerNodeName())

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

    def setCurrentParamNodeWrapper(self, nodeWrapper):
        """
            Changes the current param node and emits the change.
        """
        if self._currentParamNodeName == nodeWrapper.getName():
            return
        self._currentParamNodeName = nodeWrapper.getName()
        self.currentParamNodeChanged.emit()

    def setCurrentSelectedNodeWrapper(self, nodeWrapper):
        """
        Changes the current selected node and emits the change.
        """
        if self._currentSelectedNodeName == nodeWrapper.getName():
            return
        self._currentSelectedNodeName = nodeWrapper.getName()
        self.currentSelectedNodeChanged.emit()

    def setCurrentViewerNodeWrapper(self, nodeWrapper):
        """
        Changes the current viewer node and emits the change.
        """
        if self._currentViewerNodeName == nodeWrapper.getName():
            return
        self._currentViewerNodeName = nodeWrapper.getName()
        self.currentViewerNodeChanged.emit()

    def getZMax(self):
        return self._zMax

    def setZMax(self, zMax):
        self._zMax = zMax

    ################################################## CREATION & DESTRUCTION ##################################################

    @QtCore.Slot(str)
    def creationNode(self, nodeType):
        """
            Function called when we want to create a node from the QML.
        """
        self._graph.createNode(nodeType)

    @QtCore.Slot()
    def destructionNode(self):
        """
            Function called when we want to delete a node from the QML.
        """
        # if at least one node in the graph
        if len(self._nodeWrappers) > 0 and len(self._graph.getNodes()) > 0:
            # if a node is selected
            if self._currentSelectedNodeName != None:
                self._graph.deleteNode(self._currentSelectedNodeName)
        self._currentSelectedNodeName = None
        self.currentSelectedNodeChanged.emit()

    def createNodeWrapper(self, nodeName):
        """
            Creates a node wrapper and add it to the nodeWrappers list.
        """
        # search the right node in the node list
        node = self._graph.getNode(nodeName)
        if (node != None):
            nodeWrapper = NodeWrapper(node, self._view)
            self._nodeWrappers.append(nodeWrapper)

    def connect(self, clipOut, clipIn):
        """
            Add a connection between 2 clips.
        """
        self._graph.createConnection(clipOut, clipIn)
        self._tmpClipIn = None
        self._tmpClipOut = None

    def disconnect(self, connection):
        """
            Remove a connection between 2 clips.
        """
        self._graph.deleteConnection(connection)
        self._tmpClipIn = None
        self._tmpClipOut = None

    ################################################## INTERACTIONS ##################################################

    @QtCore.Slot(str, int, int)
    def nodeMoved(self, nodeName, x, y):
        """
            Manage when a node is moved.
        """
        # only push a cmd if the node truly moved
        if self._graph.getNode(nodeName).getOldCoord() != (x, y):
            cmdMoved = CmdSetCoord(self._graph, nodeName, (x, y))
            cmdManager = CommandManager()
            cmdManager.push(cmdMoved)

    @QtCore.Slot(str, int, int)
    def nodeIsMoving(self, nodeName, x, y):
        """
            Manage when a node is moved.
        """
        self._graph.getNode(nodeName).setCoord(x, y)
        self._graph.connectionsCoordChanged()
        # only push a cmd if the node truly moved
        # if self._graph.getNode(nodeName).getCoord() != (x, y):
        #     cmdMoved = CmdSetCoord(self._graph, nodeName, (x, y))
        #     cmdManager = CommandManager()
        #     cmdManager.push(cmdMoved)

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
        for connection in self.getGraph().getConnections():
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

    @QtCore.Slot(str, str, int)
    def clipPressed(self, nodeName, port, clipNumber):
        """
            Function called when a clip is pressed (but not released yet).
            The function replace the tmpClipIn or tmpClipOut.
        """
        position = self.getPositionClip(nodeName, port, clipNumber)
        idClip = IdClip(nodeName, port, clipNumber, position)
        if (port == "input"):
            self._tmpClipIn = idClip
        elif (port == "output"):
            self._tmpClipOut = idClip

    @QtCore.Slot(str, str, int)
    def clipReleased(self, nodeName, port, clipNumber):
        """
            Function called when a clip is released (after pressed).
        """
        if (port == "input"):
            #if there is a tmpNodeOut
            if (self._tmpClipOut != None and self._tmpClipOut._nodeName != nodeName):
                position = self.getPositionClip(nodeName, port, clipNumber)
                idClip = IdClip(nodeName, port, clipNumber, position)
                if self.canConnect(self._tmpClipOut, idClip):
                    self.connect(self._tmpClipOut, idClip)
                elif self._graph.contains(self._tmpClipOut) and self._graph.contains(idClip):
                    self.disconnect(self.getConnectionByClips(self._tmpClipOut, idClip))
                else:
                    print "Unable to connect or delete the nodes."

        elif (port == "output"):
            #if there is a tmpNodeIn
            if (self._tmpClipIn != None and self._tmpClipIn._nodeName != nodeName):
                position = self.getPositionClip(nodeName, port, clipNumber)
                idClip = IdClip(nodeName, port, clipNumber, position)
                if self.canConnect(idClip, self._tmpClipIn):
                    self.connect(idClip, self._tmpClipIn)
                elif self._graph.contains(self._tmpClipIn) and self._graph.contains(idClip):
                    self.disconnect(self.getConnectionByClips(idClip, self._tmpClipIn))
                else:
                    print "Unable to connect or delete the nodes."

    def createConnectionWrapper(self, connection):
        """
            Creates a connection wrapper and add it to the connectionWrappers list.
        """
        conWrapper = ConnectionWrapper(connection, self._view)
        self._connectionWrappers.append(conWrapper)

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
        self.__str__()

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
        self.__str__()

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

    # current param, view, and selected node
    currentParamNodeChanged = QtCore.Signal()
    currentParamNodeWrapper = QtCore.Property(QtCore.QObject, getCurrentParamNodeWrapper, setCurrentParamNodeWrapper, notify=currentParamNodeChanged)
    currentViewerNodeChanged = QtCore.Signal()
    currentViewerNodeWrapper = QtCore.Property(QtCore.QObject, getCurrentViewerNodeWrapper, setCurrentViewerNodeWrapper, notify=currentViewerNodeChanged)
    currentSelectedNodeChanged = QtCore.Signal()
    currentSelectedNodeWrapper = QtCore.Property(QtCore.QObject, getCurrentSelectedNodeWrapper, setCurrentSelectedNodeWrapper, notify=currentSelectedNodeChanged)

    # z index for QML
    zMaxChanged = QtCore.Signal()
    zMax = QtCore.Property(int, getZMax, setZMax, notify=zMaxChanged)

    # for a clean display of connection
    widthNode = QtCore.Property(int, getWidthNode, notify=changed)
    heightEmptyNode = QtCore.Property(int, getHeightEmptyNode, notify=changed)
    clipSpacing = QtCore.Property(int, getClipSpacing, notify=changed)
    clipSize = QtCore.Property(int, getClipSize, notify=changed)
    nodeInputSideMargin = QtCore.Property(int, getNodeInputSideMargin, notify=changed)
