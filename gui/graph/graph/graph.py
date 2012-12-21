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
        nodeId = len(self._nodes) # need idNode module
        self._nodes.append(Node(nodeId, "Noeud n : " + str(nodeId) + " - " + str(nodeType), str(nodeType), ((nodeId + 1) * 30, (nodeId + 5) * 10)))
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