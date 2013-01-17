# undo_redo
from buttleofx.core.undo_redo.manageTools import UndoableCommand
# core
from buttleofx.core.graph.node import Node


class CmdDeleteNode(UndoableCommand):
    """
        Command that delete a node.
        Attributes :
        - graphTarget : the graph in which the node will be deleted.
        - nodeName
        - nodeCoord
        - nodeType
        - connections : list of the connections of the node, based on all the connections. We just keep the connections concerning our node.
    """

    def __init__(self, graphTarget, nodeName):
        self.graphTarget = graphTarget
        self.nodeName = nodeName
        self.nodeCoord = (50, 20)
        self.connections = [connection for connection in self.graphTarget.getConnections() if (connection.getClipOut().getNodeName() == nodeName or connection.getClipIn().getNodeName() == nodeName)]

    def undoCmd(self):
        """
            Undo the suppression of the node <=> recreate the node.
        """
        print "Undo delete node"
        # we recreate the node
        self.graphTarget.getNodes().append(Node(self.nodeName, self.nodeType, self.nodeCoord))
        # we recreate all the connections
        for connection in self.connections:
            self.graphTarget.getConnections().append(connection)

        self.graphTarget.nodesChanged()
        self.graphTarget.connectionsChanged()

    def redoCmd(self):
        """
            Redo the suppression of the node.
        """
        print "Redo delete node"
        self.doCmd()

    def doCmd(self):
        """
            Delete a node.
        """
        node = self.graphTarget.getNode(self.nodeName)
        # we store the node type and its coordinates in order to be able to recreate it
        self.nodeType = node.getType()
        self.nodeCoord = node.getCoord()
        # we delete its connections
        self.graphTarget.deleteNodeConnections(self.nodeName)
        # and then we delete the node
        self.graphTarget.getNodes().remove(node)

        self.graphTarget.nodesChanged()
        self.graphTarget.connectionsChanged()
