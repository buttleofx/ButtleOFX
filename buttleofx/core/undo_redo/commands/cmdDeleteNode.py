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
    """

    def __init__(self, graphTarget, nodeName):
        self.graphTarget = graphTarget
        self.nodeName = nodeName
        self.nodeCoord = (50, 20)

    def undoCmd(self):
        """
            Undo the suppression of the node <=> recreate the node.
        """
        print "Undo delete"
        self.graphTarget.getNodes().append(Node(self.nodeName, self.nodeType, self.nodeCoord))
        self.graphTarget.nodesChanged()
        # THINK TO RECREATE CONNECTIONS TOO !!!!!!!!!

    def redoCmd(self):
        """
            Redo the suppression of the node.
        """
        print "Redo delete"
        self.doCmd()

    def doCmd(self):
        """
            Delete a node.
        """
        node = self.graphTarget.getNode(self.nodeName)
        # we store the node type in order to be able to recreate it
        self.nodeType = node.getType()
        # we delete its connections
        self.graphTarget.deleteNodeConnections(self.nodeName)
        # and then we delete the node
        self.graphTarget.getNodes().remove(node)

        self.graphTarget.nodesChanged()
        self.graphTarget.connectionsChanged()
