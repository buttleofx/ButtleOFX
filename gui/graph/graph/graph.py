from PySide import QtDeclarative, QtCore

from gui.graph.node.node import Node
from QuickMamba.quickmamba.patterns.signalEvent import Signal

class Graph:

    """
        Class Graph contains
        - _nodes : list of nodes (python objects, the core nodes)
        - _connections : list of connections (python objects, the core connections)
        - changed : the signal emited to the wrapper layer
    """

    def __init__(self):
        #super(Graph, self).__init__()

        self._nodes = []
        self._connections = []

        self.nodeCreated = Signal()
        self.nodeDeleted = Signal()

    def getNodes(self):

        """
            Returns the node List.
        """
        return self._nodes

    def getConnexions(self):

        """
            Returns the connection List.
        """
        return self._connections

    #@QtCore.Slot(str)
    def createNode(self, nodeType):

        """
            Adds a node from the node list when a node is created.
        """
        #
        print "createNode"
        nodeId = len(self._nodes) # need idNode module
        self._nodes.append(Node(nodeId, "Noeud n : " + str(nodeId) + " - " + str(nodeType), str(nodeType), ((nodeId + 1) * 30, (nodeId + 5) * 10)))
        self.nodeCreated(nodeId)
        # commandManager.doCmd( CmdCreateNode(nodeType) )

    #@QtCore.Slot(QtDeclarative.QDeclarativeItem)
    def deleteNode(self, nodeId):

        """
            Removes a node from the node list when a node is deleted.
        """
        print "deleteNode"
        #
        self._nodes.remove(self._nodes[nodeId])
        self.nodeDeleted(nodeId)
        # commandManager.doCmd( CmddeleteNode(nodeid) )