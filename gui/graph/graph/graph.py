from QuickMamba.quickmamba.patterns.signalEvent import Signal
from QuickMamba.quickmamba.patterns.singleton import Singleton

from gui.graph.node.node import Node
from gui.graph.node.idNode import IdNode

class Graph(Singleton):
    """
        Class Graph contains
        - _nodes : list of nodes (python objects, the core nodes)
        - _connections : list of connections (python objects, the core connections)
        - nodeCreated : the signal emited to the wrapper layer when a node is created
        - nodeDeleted : the signal emited to the wrapper layer when a node is deleted
    """

    def __init__(self):
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

    def createNode(self, nodeType):
        """
            Adds a node from the node list when a node is created.
        """
        #
        print "createNode"
        nodeName = "Name = type : " + str(nodeType)
        nodeCoord = (30, 50)
        nodeId = IdNode(nodeName, nodeType, nodeCoord[0], nodeCoord[1])

        self._nodes.append(Node(nodeId, nodeName, nodeType, nodeCoord))

        self.nodeCreated(nodeId)
        # commandManager.doCmd( CmdCreateNode(nodeType) )

    def deleteNode(self, nodeId):
        """
            Removes a node from the node list when a node is deleted.
        """
        print "deleteNode"
        #
        # we search the right node to delete
        for node in self._nodes:
            if node.getId() == nodeId:
                self._nodes.remove(node)
                break
        self.nodeDeleted(nodeId)
        # commandManager.doCmd( CmddeleteNode(nodeid) )