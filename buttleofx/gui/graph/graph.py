from buttleofx.gui.graph.node import Node
from buttleofx.gui.graph.connection import Connection

from quickmamba.patterns import Signal


class Graph:
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
        self._nbNodesCreated = 0

        self.nodeCreated = Signal()
        self.nodeDeleted = Signal()
        self.connectionCreated = Signal()
        self.connectionDeleted = Signal()

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

        print "createNode"
        self._nbNodesCreated += 1
        nodeName = str(nodeType) + "_" + str(self._nbNodesCreated)
        nodeCoord = (50, 20)
        #nodeId = IdNode(nodeName, nodeType, nodeCoord[0], nodeCoord[1])

        self._nodes.append(Node(nodeName, nodeType, nodeCoord))

        self.nodeCreated(nodeName)
        # commandManager.doCmd( CmdCreateNode(nodeType) )

    def deleteNode(self, nodeName):
        """
            Removes a node in the node list when a node is deleted.
        """
        print "deleteNode"

        # we search the right node to delete
        indexWrapper = 0
        for node in self._nodes:
            if node.getName() == nodeName:
                self._nodes.remove(node)
                break
            indexWrapper += 1
        self.nodeDeleted(indexWrapper)
        # commandManager.doCmd( CmddeleteNode(nodeid) )

    def createConnection(self, clipOut, clipIn):
        """
            Adds a connection in the connection list when a connection is created.
        """

        print "createConnection"
        self._connections.append(Connection(clipOut, clipIn))
        self.connectionCreated(clipOut, clipIn)
