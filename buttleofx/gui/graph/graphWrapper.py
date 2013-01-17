from PySide import QtDeclarative, QtCore
# core
from buttleofx.core.graph import Graph
from buttleofx.core.graph.connection import IdClip
# undo redo
from buttleofx.core.undo_redo.manageTools import CommandManager
# gui
from buttleofx.gui.graph.node import NodeWrapper
from buttleofx.gui.graph.connection import ConnectionWrapper
# quickmamba
from quickmamba.models import QObjectListModel
from quickmamba.patterns import Signal



class GraphWrapper(QtCore.QObject):
    """
        Class GraphWrapper defined by:
        - _engine : to have the view engine
        - _rootObject : to have the root object
        - _nodeWrappers : list of node wrappers (the python objects we use to communicate with the QML)
        - _connectionWrappers : list of connections wrappers (the python objects we use to communicate with the QML)
        - _currentNode : the current selected node (in QML). This is just the nodeName.
        - _tmpClipOut : the future connected output clip when a connection is beeing created. It correspounds of the output clip which was beeing clicked and not connected for the moment.
        - _tmpClipIn : the future connected input clip when a connection is beeing created. It correspounds of the input clip which was beeing clicked and not connected for the moment.
        - _zMax : to manage the depth of the graph (in QML)
        - _graph : the data of the graph (python objects, the core data : the nodes and the connections)

        Creates a QObject from a given python object Graph.
    """

    def __init__(self, graph, view):
        super(GraphWrapper, self).__init__(view)

        self._view = view
        self._engine = view.engine()
        self._rootObject = view.rootObject()

        self._nodeWrappers = QObjectListModel(self)
        self._connectionWrappers = QObjectListModel(self)

        self._currentNode = None
        self._currentParams = None
        self._currentImage = ""
        self._tmpClipIn = None
        self._tmpClipOut = None

        self._zMax = 2

        self._graph = graph

        # the links between the graph and this graphWrapper
        graph.nodesChanged.connect(self.updateNodeWrappers)
        graph.connectionsChanged.connect(self.updateConnectionWrappers)

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

    @QtCore.Slot(result="QVariant")
    def getNodeWrappers(self):
        """
            Returns the nodeWrapper list.
        """
        return self._nodeWrappers

    @QtCore.Slot(result="QtCore.QObject")
    def getNodeWrapper(self, nodeName):
        """
            Returns the right nodeWrapper, identified with its nodeName.
        """
        for node in self._nodeWrappers:
            if node.getName() == nodeName:
                return node
        return None

    @QtCore.Slot(result="QVariant")
    def getConnectionWrappers(self):
        """
            Return the connectionWrapper list.
        """
        return self._connectionWrappers

    @QtCore.Slot(result="QVariant")
    def getCurrentNode(self):
        """
            Return the name of the current selected node.
        """
        return self._currentNode

    @QtCore.Slot(result="QtCore.QObject")
    def getCurrentNodeWrapper(self):
        """
            Return the name of the current selected node.
        """
        return self.getNodeWrapper(self._currentNode)

    @QtCore.Slot(result="QVariant")
    def getCurrentParams(self):
        """
            Return the params of the current node.
        """
        return self._currentParams

    def getCurrentImage(self):
        """
            Return the url of the current image
        """
        return self._currentImage

    #################### setters ####################

    @QtCore.Slot(str)
    def setCurrentNode(self, nodeName):
        """
            Change the current selected node and emit the change.
        """
        print "setCurrentNode : " + str(nodeName)

        if self._currentNode == nodeName:
            return

        #we search the image of the selected node
        for nodeWrapper in self._nodeWrappers:
            if nodeWrapper.getName() == nodeName:
                self.setCurrentImage(nodeWrapper.getImage())
                self.setCurrentParams(nodeName)

        self._currentNode = nodeName

        self.currentNodeChanged.emit()

    @QtCore.Slot(str)
    def setCurrentParams(self, nodeName):
        """
            Change the current params and emit the change.
        """
        print "setCurrentParams"
        self._currentParams = self.getNodeWrapper(nodeName).getParams().getParamElts()
        self.currentParamsChanged.emit()

    def setCurrentImage(self, urlImage):
        """
            Change the currentImage, displayed in the viewer
        """
        self._currentImage = urlImage
        self.currentImageChanged.emit()

    @QtCore.Slot(result="double")
    def getZMax(self):
        return self._zMax

    @QtCore.Slot()
    def setZMax(self):
        self._zMax += 1

    ################################################## CREATION & DESTRUCTION ##################################################

    @QtCore.Slot(str, CommandManager)
    def creationNode(self, nodeType, cmdManager):
        """
            Function called when we want to create a node from the QML.
        """
        self._graph.createNode(nodeType, cmdManager)
        # debug
        self.__str__()

    def createNodeWrapper(self, nodeName):
        """
            Creates a node wrapper and add it to the nodeWrappers list.
        """
        print "createNodeWrapper"

        # search the right node in the node list
        node = self._graph.getNode(nodeName)
        if (node != None):
            nodeWrapper = NodeWrapper(node, self._view)
            self._nodeWrappers.append(nodeWrapper)

    @QtCore.Slot(CommandManager)
    def destructionNode(self, cmdManager):
        """
            Function called when we want to delete a node from the QML.
        """
        # if at least one node in the graph
        if len(self._nodeWrappers) > 0 and len(self._graph._nodes) > 0:
            # if a node is selected
            if self._currentNode != None:
                self._graph.deleteNode(self._currentNode, cmdManager)
        self._currentNode = None
        # debug
        self.__str__()

    ################################################## CONNECTIONS MANAGEMENT ##################################################

    def getPositionClip(self, nodeName, port, clipNumber):
        """
            Function called when a new idClip is created.
            Returns the position of the clip.
            The calculation is the same as in the QML file (Node.qml).
        """
        nodeCoord = self._graph.getNode(nodeName).getCoord()
        widthNode = 110
        heightEmptyNode = 35
        clipSpacing = 7
        clipSize = 8
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

    def connect(self, clipOut, clipIn, cmdManager):
        """
            Add a connection between 2 clips.
        """
        self._graph.createConnection(clipOut, clipIn, cmdManager)
        self._tmpClipIn = None
        self._tmpClipOut = None
        self.__str__()

    @QtCore.Slot(str, str, int)
    def clipPressed(self, nodeName, port, clipNumber):
        """
            Function called when a clip is pressed (but not released yet).
            The function replace the tmpClipIn or tmpClipOut.
        """
        position = self.getPositionClip(nodeName, port, clipNumber)
        #position = self._graph.getNode(nodeName).getCoord()
        idClip = IdClip(nodeName, port, clipNumber, position)
        if (port == "input"):
            self._tmpClipIn = idClip
        elif (port == "output"):
            self._tmpClipOut = idClip

    @QtCore.Slot(str, str, int, CommandManager)
    def clipReleased(self, nodeName, port, clipNumber, cmdManager):

        if (port == "input"):
            #if there is a tmpNodeOut we can connect the nodes
            if (self._tmpClipOut != None and self._tmpClipOut._nodeName != nodeName):
                position = self.getPositionClip(nodeName, port, clipNumber)
                idClip = IdClip(nodeName, port, clipNumber, position)
                if self.canConnect(self._tmpClipOut, idClip):
                    self.connect(self._tmpClipOut, idClip, cmdManager)
                else:
                    print "Unable to connect the nodes."

        elif (port == "output"):
            #if there is a tmpNodeIn we can connect the nodes
            if (self._tmpClipIn != None and self._tmpClipIn._nodeName != nodeName):
                position = self.getPositionClip(nodeName, port, clipNumber)
                idClip = IdClip(nodeName, port, clipNumber, position)
                if self.canConnect(idClip, self._tmpClipIn):
                    self.connect(idClip, self._tmpClipIn, cmdManager)
                else:
                    print "Unable to connect the nodes."

    def createConnectionWrapper(self, connection):
        """
            Creates a connection wrapper and add it to the connectionWrappers list.
        """
        conWrapper = ConnectionWrapper(connection, self._view)
        self._connectionWrappers.append(conWrapper)

    ################################################## UPDATE ##################################################

    def updateNodeWrappers(self):
        """
            Updates the nodeWrappers when the signal nodesChanged has been emited.
        """
        # we clear the list
        self._nodeWrappers.clear()
        # and we fill with the new data
        for node in self._graph.getNodes():
            self.createNodeWrapper(node.getName())

    def updateConnectionWrappers(self):
        """
            Updates the connectionWrappers when the signal connectionsChanged has been emited.
        """
        print "UPDATE CONNECTIONS WRAPPERS"
        # we clear the list
        self._connectionWrappers.clear()
        # and we fill with the new data
        for connection in self._graph.getConnections():
            self.createConnectionWrapper(connection)

    @QtCore.Slot()
    def updateConnectionsCoord(self):
        print "UPDATE CONNECTIONS COORDS"
        for connection in self._graph.getConnections():
            clipOut = connection.getClipOut()
            clipIn = connection.getClipIn()
            clipOut.setCoord(self.getPositionClip(clipOut.getNodeName(), clipOut.getPort(), clipOut.getClipNumber()))
            clipIn.setCoord(self.getPositionClip(clipIn.getNodeName(), clipIn.getPort(), clipIn.getClipNumber()))
        self.updateConnectionWrappers()

    ################################################## DATA EXPOSED TO QML ##################################################

    nodesChanged = QtCore.Signal()
    nodes = QtCore.Property("QVariant", getNodeWrappers, notify=nodesChanged)
    connectionWrappersChanged = QtCore.Signal()
    connections = QtCore.Property("QVariant", getConnectionWrappers, notify=connectionWrappersChanged)
    currentNodeChanged = QtCore.Signal()
    currentNode = QtCore.Property(str, getCurrentNode, setCurrentNode, notify=currentNodeChanged)
    currentParamsChanged = QtCore.Signal()
    currentParams = QtCore.Property("QVariant", getCurrentParams, setCurrentParams, notify=currentParamsChanged)
    currentImageChanged = QtCore.Signal()
    currentImage = QtCore.Property(str, getCurrentImage, setCurrentImage, notify=currentImageChanged)
