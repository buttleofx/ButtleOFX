from buttleofx.gui.graph import Graph
from buttleofx.gui.graph.node import NodeWrapper
from buttleofx.gui.graph.connection import ConnectionWrapper, IdClip

from quickmamba.models import QObjectListModel
from quickmamba.patterns import Signal
from quickmamba.patterns import Singleton

from PySide import QtDeclarative, QtCore


class GraphWrapper(QtCore.QObject, Singleton):
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
        self._currentImage = ""
        self._tmpClipIn = None
        self._tmpClipOut = None

        self._zMax = 2

        self._graph = graph

        # the links between the graph and this graphWrapper
        graph.nodeCreated.connect(self.createNodeWrapper)
        #graph.nodeCreated.connect(self.setCurrentNode)
        graph.nodeDeleted.connect(self.deleteNodeWrapper)
        graph.nodeDeleted.connect(self.deleteCurrentNode)
        graph.connectionCreated.connect(self.createConnectionWrapper)

    def __str__(self):
        """
            Display on terminal some data.
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

    @QtCore.Slot(result="QVariant")
    def getGraph(self):
        """
            Return the graph (the node list and the connection list).
        """
        return self._graph

    @QtCore.Slot(result="QVariant")
    def getNodeWrappers(self):
        """
            Return the nodeWrapper list.
        """
        return self._nodeWrappers

    @QtCore.Slot(result="QVariant")
    def getNode(self, nodeName):
        for node in self._nodeWrappers:
            if node.getName() == nodeName:
                return node

    @QtCore.Slot()
    def getConnectionWrappers(self):
        """
            Return the connectionWrapper list.
        """
        return self._connectionWrappers

    @QtCore.Slot(str)
    def creationProcess(self, nodeType):
        """
            Function called when we want to create a node from the QML.
        """
        self._graph.createNode(nodeType)
        # debug
        self.__str__()

    @QtCore.Slot(str, str, int)
    def clipPressed(self, nodeName, port, clip):
        """
            Function called when a clip is pressed (but not released yet).
            The function replace the tmpClipIn or tmpClipOut.
        """

        # To define with the IdClip info !
        #position = _graph.getNode(nodeName).getCoord[]
        idClip = IdClip(nodeName, port, clip)
        if (port == "input"):
            print "inputPressed"
            self._tmpClipIn = idClip
            print "Add tmpNodeIn: " + nodeName + " " + port + " " + str(clip)
        elif (port == "output"):
            print "outputPressed"
            self._tmpClipOut = idClip
            print "Add tmpNodeOut: " + nodeName + " " + port + " " + str(clip)

    @QtCore.Slot(str, str, int)
    def clipReleased(self, nodeName, port, clip):

        if (port == "input"):
            #if there is a tmpNodeOut we can connect the nodes
            print "inputReleased"
            if (self._tmpClipOut != None and self._tmpClipOut._nodeName != nodeName):
                idClip = IdClip(nodeName, port, clip)
                self._graph.createConnection(self._tmpClipOut, idClip)
                self._tmpClipIn = None
                self._tmpClipOut = None
                self.__str__()

        elif (port == "output"):
            #if there is a tmpNodeIn we can connect the nodes
            print "inputReleased"
            if (self._tmpClipIn != None and self._tmpClipIn._nodeName != nodeName):
                idClip = IdClip(nodeName, port, clip)
                self._graph.createConnection(idClip, self._tmpClipIn)
                self._tmpClipIn = None
                self._tmpClipOut = None
                self.__str__()

    def createNodeWrapper(self, nodeName):
        """
            Create a node wrapper and add it to the nodeWrappers list.
        """
        print "createNodeWrapper"
        #wrapper = NodeWrapper(self._graph._nodes[nodeId])

        # search the right node in the node list
        for node in self._graph._nodes:
            if node.getName() == nodeName:
                nodeWrapper = NodeWrapper(node, self._view)
                self._nodeWrappers.append(nodeWrapper)
                #self.setCurrentNode(nodeWrapper.getName())
        # commandManager.doCmd( CmdCreateNodeWrapper(nodeId) )

    def createConnectionWrapper(self, clipOut, clipIn):
        """
            Create a connection wrapper and add it to the connectionWrappers list.
        """
        print "createConnectionWrapper"

        conWrapper = ConnectionWrapper(clipOut, clipIn)
        print "truc"
        self._connectionWrappers.append(conWrapper)
        print "trac"
        # commandManager.doCmd( CmdCreateConnectionWrapper(clipOut, clipIn) )

    @QtCore.Slot()
    def destructionProcess(self):
        """
            Function called when we want to delete a node from the QML.
        """
        # if at least one node in the graph
        if len(self._nodeWrappers) > 0 and len(self._graph._nodes) > 0:
            # if a node is selected
            if self._currentNode != None:
                self._graph.deleteNode(self._currentNode)
        # debug
        self.__str__()

    def deleteNodeWrapper(self, indiceW):
        print "deleteNodeWrapper"
        self._nodeWrappers.removeAt(indiceW)
        # commandManager.doCmd( CmdDeleteNodeWrapper(indiceW) )

    @QtCore.Slot(result="QVariant")
    def getCurrentNode(self):
        """
            Return the name of the current selected node.
        """
        return self._currentNode

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
            if nodeWrapper.getName() == self._currentNode:
                self.setCurrentImage(nodeWrapper.getImage())
                self.currentImageChanged.emit()
                print(self._currentImage)

        self._currentNode = nodeName
        self.currentNodeChanged.emit()

    def getCurrentImage(self):
        """
            Return the url of the current image
        """
        return self._currentImage

    def setCurrentImage(self, urlImage):
        """
            Change the currentImage, displayed in the viewer
        """
        self._currentImage = urlImage

    def deleteCurrentNode(self, indiceW):
        """
            Delete the current selected node by calling the deleteNode() function.
        """
        print "deleteCurrentNode"
        self._currentNode = None

    @QtCore.Slot(result="double")
    def getZMax(self):
        return self._zMax

    @QtCore.Slot()
    def setZMax(self):
        self._zMax += 1

    nodesChanged = QtCore.Signal()
    nodes = QtCore.Property("QVariant", getNodeWrappers, notify=nodesChanged)
    connectionsChanged = QtCore.Signal()
    connections = QtCore.Property("QVariant", getConnectionWrappers, notify=connectionsChanged)
    currentNodeChanged = QtCore.Signal()
    currentNode = QtCore.Property(str, getCurrentNode, setCurrentNode, notify=currentNodeChanged)
    currentImageChanged = QtCore.Signal()
    currentImage = QtCore.Property(str, getCurrentImage, setCurrentImage, notify=currentImageChanged)
