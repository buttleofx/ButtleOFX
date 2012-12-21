from PySide import QtDeclarative, QtCore

from gui.graph.node.nodeWrapper import NodeWrapper
from QuickMamba.qobjectlistmodel import QObjectListModel
from QuickMamba.quickmamba.patterns.signalEvent import Signal

from gui.graph.graph.graph import Graph

class GraphWrapper(QtCore.QObject):

    """
        Class GraphWrapper defined by:
        - _engine : to have the view engine
        - _rootObject : to have the root object
        - _nodeWrappers : list of node wrappers (the python objects we use to communicate with the QML)
        - _connectionWrappers : list of connections wrappers (the python objects we use to communicate with the QML)
        - _currentNode : the current selected node (in QML)
        - _zMax : to manage the depth of the graph (in QML)
        - _graph : the data of the graph (python objects, the core data : the nodes and the connections)

        Creates a QObject from a given python object Graph.
    """

    def __init__(self, graph, view):
        super(GraphWrapper, self).__init__()

        self._graph = graph

        # the links between the graph and this graphWrapper
        graph.nodeCreated.connect(self.createNodeWrapper)
        graph.nodeDeleted.connect(self.deleteNodeWrapper)

        self._engine = view.engine()
        self._rootObject = view.rootObject()

        self._nodeWrappers = QObjectListModel(self)
        self.connectionWrappers = []

        self._currentNode = None
        self._zMax = 2

    def __str__(self):
        """
            To debug the class.
        """
        print("The id of all nodeWrappers")
        for wrapper in self._nodeWrappers:
            print "id : " + str(wrapper._id) + " Name : " + str(wrapper._name)

        print("The id of all nodes")
        for node in self._graph._nodes:
            print "id : " + str(node._id) + " Name : " + str(node._name)

    def getGraph(self):
        """
            Return the graph (the node list and the connection list)
        """
        return self._graph

    @QtCore.Slot()
    def getWrappers(self):
        """
            Return the nodeWrapper list
        """
        return self._nodeWrappers

    @QtCore.Slot(QtCore.QObject)
    def getWrapper(self, nodeWrapper):
        """
            Return a nodeWrapper of the list
        """
        return self._nodeWrappers[nodeWrapper.getId()]

    @QtCore.Slot(str)
    def creation(self, nodeType):
        self._graph.createNode(nodeType)
        # debug
        self.__str__()

    def createNodeWrapper(self, nodeId):
        print "createNodeWrapper"
        wrapper = NodeWrapper(self._graph._nodes[nodeId])
        self._nodeWrappers.append(wrapper)
        self._currentNode = wrapper
        # commandManager.doCmd( CmdCreateNodeWrapper(nodeId) )

    @QtCore.Slot(str)
    def destruction(self, nodeId):
        self._graph.deleteNode(nodeId)
        # debug
        self.__str__()

    @QtCore.Slot(str)
    def deleteNodeWrapper(self, nodeId):
        print "deleteNodeWrapper"
        self._nodeWrappers.removeAt(nodeId)
        # commandManager.doCmd( CmdDeleteNodeWrapper(nodeId) )

    def getCurrentNode(self):
        """
            Return the item of the current selected node (in QML).
        """
        return self._currentNode

    @QtCore.Slot()
    def deleteCurrentNode(self):
        """
            Delete the current selected node by calling the deleteNode() function.
        """
        nodeId = self._currentNode.getId()
        self.deleteNodeWrapper(nodeId)
        self._graph.deleteNode(nodeId)

    def setCurrentNode(self, nodeWrapper):
        """
            Change the current selected node and emit the change.
        """
        if self._currentNode == nodeWrapper:
            return
        self._currentNode = nodeWrapper
        self.currentNodeChanged.emit()

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