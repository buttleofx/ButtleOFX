from PySide import QtCore
# core
from buttleofx.core.graph.node import Node
from buttleofx.core.graph.connection import Connection
#undo_redo
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands import CmdCreateNode, CmdDeleteNode, CmdCreateConnection
# quickmamba
from quickmamba.patterns import Signal


class Graph(object):
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

        self.nodesChanged = Signal()
        self.connectionsChanged = Signal()

    def getNodes(self):
        """
            Returns the node List.
        """
        return self._nodes

    def getNode(self, nodeName):
        for node in self._nodes:
            if node.getName() == nodeName:
                return node
        return None

    def getConnections(self):
        """
            Returns the connection List.
        """
        return self._connections

    def createNode(self, nodeType, cmdManager):
        """
            Adds a node from the node list when a node is created.
        """
        print "createNode"
        cmdCreateNode = CmdCreateNode(self, nodeType, cmdManager)
        cmdManager.push(cmdCreateNode)

    def deleteNode(self, nodeName, cmdManager):
        """
            Removes a node in the node list when a node is deleted.
        """
        print "deleteNode"
        cmdDeleteNode = CmdDeleteNode(self, nodeName, cmdManager)
        cmdManager.push(cmdDeleteNode)

    def createConnection(self, clipOut, clipIn, cmdManager):
        """
            Adds a connection in the connection list when a connection is created.
        """
        print "createConnection"
        cmdCreateConnection = CmdCreateConnection(self, clipOut, clipIn)
        cmdManager.push(cmdCreateConnection)

    def deleteConnection(self, connection):
        """
            Delete a connection.
        """
        print "DELETE CONNECTION."
        self._connections.remove(connection)

    def deleteNodeConnections(self, nodeName):
        """
            Delete all the connections of the node.
        """
        print "begin suppression connections :"
        for connection in self._connections:
            if connection.getClipOut().getNodeName() == nodeName or connection.getClipIn().getNodeName() == nodeName:
                self.deleteConnection(connection)
        print "end suppression connections :"
        self.connectionsChanged()

    def contains(self, clip):
        """
            Returns True if the clip is already connected, else False.
        """
        for connection in self._connections:
            if (clip == connection.getClipOut() or clip == connection.getClipIn()):
                return True
        return False

    def nodesConnected(self, clipOut, clipIn):
        """
            Returns True if the nodes containing the clips are already connected (in the other direction).
        """
        for connection in self._connections:
            if (clipOut.getNodeName() == connection.getClipIn().getNodeName() and clipIn.getNodeName() == connection.getClipOut().getNodeName()):
                return True
        return False
