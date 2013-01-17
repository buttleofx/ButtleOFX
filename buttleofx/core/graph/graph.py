from buttleofx.core.graph.node import Node
from buttleofx.core.graph.connection import Connection

from quickmamba.patterns import Signal

from PySide import QtCore, QtGui

#undo_redo
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands import CmdCreateNode
from buttleofx.core.undo_redo.commands import CmdDeleteNode


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

    def createConnection(self, clipOut, clipIn):
        """
            Adds a connection in the connection list when a connection is created.
        """
        print "createConnection"
        self._connections.append(Connection(clipOut, clipIn))
        self.connectionCreated(clipOut, clipIn)
