from buttleofx.gui.graph.graph.graph import Graph
from buttleofx.gui.graph.node.nodeWrapper import NodeWrapper

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
        - _zMax : to manage the depth of the graph (in QML)
        - _graph : the data of the graph (python objects, the core data : the nodes and the connections)

        Creates a QObject from a given python object Graph.
    """

    def __init__(self, graph, view):
        super(GraphWrapper, self).__init__()

        self._engine = view.engine()
        self._rootObject = view.rootObject()

        self._nodeWrappers = QObjectListModel(self)
        self.connectionWrappers = []

        self._currentNode = None
        self._zMax = 2

        self._graph = graph

        # the links between the graph and this graphWrapper
        graph.nodeCreated.connect(self.createNodeWrapper)
        graph.nodeCreated.connect(self.setCurrentNode)
        graph.nodeDeleted.connect(self.deleteNodeWrapper)
        graph.nodeDeleted.connect(self.deleteCurrentNode)

    def __str__(self):
        """
            Display on terminal the nodeWrapper list and the node list.
            Usefull to debug the class.
        """
        print("---- The id of all nodeWrappers ----")
        for wrapper in self._nodeWrappers:
            print  wrapper._id

        print("---- The id of all nodes ----")
        for node in self._graph._nodes:
            print node._id

    def getGraph(self):
        """
            Return the graph (the node list and the connection list).
        """
        return self._graph

    @QtCore.Slot()
    def getWrappers(self):
        """
            Return the nodeWrapper list.
        """
        return self._nodeWrappers

    @QtCore.Slot(QtCore.QObject)
    def getWrapper(self, nodeWrapper):
        """
            Return a nodeWrapper of the list.
        """
        return self._nodeWrappers[nodeWrapper.getId()]

    @QtCore.Slot(str)
    def creationProcess(self, nodeType):
        """
            Function called when we want to create a node from the QML.
        """
        self._graph.createNode(nodeType)
        # debug
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
                wrapper = NodeWrapper(node)
                self._nodeWrappers.append(wrapper)
        #self._currentNode = wrapper
        # commandManager.doCmd( CmdCreateNodeWrapper(nodeId) )

    @QtCore.Slot()
    def destructionProcess(self):
        """
            Function called when we want to delete a node from the QML.
        """
        # if at least one node in the graph
        if len(self._nodeWrappers) > 0 and len(self._graph._nodes) > 0:
            self._graph.deleteNode(self._currentNode)
        # debug
        self.__str__()

    def deleteNodeWrapper(self, nodeId):
        print "deleteNodeWrapper"
        self._nodeWrappers.removeAt(0)
        # commandManager.doCmd( CmdDeleteNodeWrapper(nodeId) )

    def getCurrentNode(self):
        """
            Return the item of the current selected node (in QML).
        """
        return self._currentNode

    @QtCore.Slot(int)
    def setCurrentNode(self, nodeId):
        """
            Change the current selected node and emit the change.
        """
        print "setCurrentNode"
        if self._currentNode == nodeId:
            return
        self._currentNode = nodeId
        self.currentNodeChanged.emit()

    def deleteCurrentNode(self, nodeId):
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
