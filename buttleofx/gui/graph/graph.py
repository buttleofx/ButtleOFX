from buttleofx.gui.graph.node import Node
from buttleofx.gui.graph.connection import Connection

from quickmamba.patterns import Signal

from PySide import QtCore, QtGui

#undo_redo
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands import CmdCreateNode


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

    @QtCore.Slot(str, CommandManager)
    def createNode(self, nodeType, cmdManager):
        """
            Adds a node from the node list when a node is created.
        """

        print "createNode"
        cmdCreateNode = CmdCreateNode(self, nodeType)
        cmdManager.push(cmdCreateNode)
        #CommandManager.doCmd(CmdCreateNode(nodeType))

    def deleteNode(self, nodeName):
        """
            Removes a node in the node list when a node is deleted.
        """
        print "deleteNode"

        # we search the right node to delete
        node = self.getNode(nodeName)
        if (node != None):
            self.deleteNodeConnections(nodeName)
            self._nodes.remove(node)
        self.nodesChanged()
        # commandManager.doCmd( CmddeleteNode(nodeid) )

    def deleteNodeConnections(self, nodeName):
        """
            Delete all the connections of the node.
        """
        for connection in self._connections:
            if connection.getClipOut().getNodeName() == nodeName or connection.getClipIn().getNodeName() == nodeName:
                self._connections.remove(connection)
        self.connectionsChanged()

    def createConnection(self, clipOut, clipIn):
        """
            Adds a connection in the connection list when a connection is created.
        """

        print "createConnection"
        newConnection = Connection(clipOut, clipIn)
        self._connections.append(newConnection)
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
