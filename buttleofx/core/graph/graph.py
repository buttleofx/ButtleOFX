from PySide import QtCore
# core
from buttleofx.core.graph.node import Node
from buttleofx.core.graph.connection import Connection
#undo_redo
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands import CmdCreateNode, CmdDeleteNode, CmdCreateConnection, CmdDeleteConnection
# quickmamba
from quickmamba.patterns import Signal


class Graph(object):
    """
        Class Graph contains
        - _nodes : list of nodes (python objects, the core nodes)
        - _connections : list of connections (python objects, the core connections)
        - nodesChanged : the signal emited to the wrapper layer to update nodeWrappers
        - connectionsChanged : the signal emited to the wrapper layer to update connectionWrappers
    """

    def __init__(self):
        self._nodes = []
        self._connections = []
        self._nbNodesCreated = 0

        self.nodesChanged = Signal()
        self.connectionsChanged = Signal()
        self.connectionsCoordChanged = Signal()

    ################################################## ACCESSORS ##################################################

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

    ################################################## CREATION & DESTRUCTION ##################################################

    def createNode(self, nodeType):
        """
            Adds a node from the node list when a node is created.
        """
        cmdCreateNode = CmdCreateNode(self, nodeType)
        cmdManager = CommandManager()
        cmdManager.push(cmdCreateNode)

    def deleteNode(self, nodeName):
        """
            Removes a node in the node list when a node is deleted.
        """
        cmdDeleteNode = CmdDeleteNode(self, nodeName)
        cmdManager = CommandManager()
        cmdManager.push(cmdDeleteNode)

    def createConnection(self, clipOut, clipIn):
        """
            Adds a connection in the connection list when a connection is created.
        """
        cmdCreateConnection = CmdCreateConnection(self, clipOut, clipIn)
        cmdManager = CommandManager()
        cmdManager.push(cmdCreateConnection)

    def deleteConnection(self, connection):
        """
            Removes a connection.
        """
        cmdDeleteConnection = CmdDeleteConnection(self, connection)
        cmdManager = CommandManager()
        cmdManager.push(cmdDeleteConnection)

    def deleteNodeConnections(self, nodeName):
        """
            Removes all the connections of the node.
        """
        # We can't use a for loop. We have to rebuild the list, based on the current values.
        self._connections = [connection for connection in self._connections if not (connection.getClipOut().getNodeName() == nodeName or connection.getClipIn().getNodeName() == nodeName)]
        self.connectionsChanged()

    ################################################## FLAGS ##################################################

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
