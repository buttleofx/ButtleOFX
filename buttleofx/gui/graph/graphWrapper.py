from buttleofx.gui.graph.node import idNode

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
        - _currentNode : the current selected node (in QML). This is just the nodeId.
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
        self._tmpClipIn = None
        self._tmpClipOut = None

        self._zMax = 2

        self._graph = graph

        # the links between the graph and this graphWrapper
        graph.nodeCreated.connect(self.createNodeWrapper)
        graph.nodeCreated.connect(self.setCurrentNode)
        graph.nodeDeleted.connect(self.deleteNodeWrapper)
        graph.nodeDeleted.connect(self.deleteCurrentNode)
        graph.connectionCreated.connect(self.createConnectionWrapper)

    def __str__(self):
        """
            Display on terminal the nodeWrapper list and the node list.
            Usefull to debug the class.
        """
        print("---- The id of all nodeWrappers ----")
        for wrapper in self._nodeWrappers:
            print wrapper._id

        print("---- The id of all nodes ----")
        for node in self._graph._nodes:
            print node._id

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
    def getWrappers(self):
        """
            Return the nodeWrapper list.
        """
        return self._nodeWrappers

    @QtCore.Slot(str)
    def creationProcess(self, nodeType):
        """
            Function called when we want to create a node from the QML.
        """
        self._graph.createNode(nodeType)
        # debug
        self.__str__()

    @QtCore.Slot(str, str, int)
    def clipPressed(self, node, port, clip):
        """
            Function called when a clip is pressed (but not released yet).
            The function replace the tmpClipIn or tmpClipOut.
        """
        idClip = IdClip(node, port, clip)
        if (port == "input"):
            print "inputPressed"
            self._tmpClipIn = idClip
            print "Add tmpNodeIn: " + node + " " + port + " " + str(clip)
        elif (port == "output"):
            print "outputPressed"
            self._tmpClipOut = idClip
            print "Add tmpNodeOut: " + node + " " + port + " " + str(clip)

    @QtCore.Slot(str, str, int)
    def clipReleased(self, node, port, clip):

        if (port == "input"):
            #if there is a tmpNodeOut we can connect the nodes
            print "inputReleased"
            if (self._tmpClipOut != None and self._tmpClipOut._node != node):
                idClip = IdClip(node, port, clip)
                self._graph.createConnection(self._tmpClipOut, idClip)
                self._tmpClipIn = None
                self._tmpClipOut = None
                self.__str__()

        elif (port == "output"):
            #if there is a tmpNodeIn we can connect the nodes
            print "inputReleased"
            if (self._tmpClipIn != None and self._tmpClipIn._node != node):
                idClip = IdClip(node, port, clip)
                self._graph.createConnection(idClip, self._tmpClipIn)
                self._tmpClipIn = None
                self._tmpClipOut = None
                self.__str__()

    def createNodeWrapper(self, nodeId):
        """
            Create a node wrapper and add it to the nodeWrapper list.
        """
        print "createNodeWrapper"
        #wrapper = NodeWrapper(self._graph._nodes[nodeId])
        # search the right node in the node list
        for node in self._graph._nodes:
            if node.getId() == nodeId:
                wrapper = NodeWrapper(node, self._view)
                self._nodeWrappers.append(wrapper)
        # commandManager.doCmd( CmdCreateNodeWrapper(nodeId) )

    def createConnectionWrapper(self, clipOut, clipIn):
        """
            Create a connection wrapper and add it to the connectionWrapper list.
        """
        print "createConnectionWrapper"

        conWrapper = ConnectionWrapper(clipOut, clipIn)
        self._connectionWrappers.append(conWrapper)
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
            Return the item of the current selected node (in QML).
        """
        return self._currentNode

    @QtCore.Slot(result="QVariant")
    def getNodeWrapper(self, node):
        """
            Return the item of the current selected node (in QML).
        """
        return self._nodeWrappers(node)

    @QtCore.Slot(result="str")
    def getImageCurrentNode(self):
        for wrapper in self._nodeWrappers:
            if wrapper.getId() == self._currentNode:
                return wrapper.getImage()

    @QtCore.Slot(object)
    def setCurrentNode(self, nodeId):
        """
            Change the current selected node and emit the change.
        """
        print "setCurrentNode"
        if self._currentNode == nodeId:
            return
        self._currentNode = nodeId
        self.currentNodeChanged.emit()

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
    nodes = QtCore.Property("QVariant", getWrappers, notify=nodesChanged)
    currentNodeChanged = QtCore.Signal()
    currentNode = QtCore.Property("QVariant", getCurrentNode, setCurrentNode, notify=currentNodeChanged)
