# Tuttle
from pyTuttle import tuttle

# undo_redo
from buttleofx.core.undo_redo.manageTools import UndoableCommand
# core
from buttleofx.core.graph.node import Node


class CmdCreateNode(UndoableCommand):
    """
        Command that create a node.
        Attributes :
        - graphTarget : the graph in which the node will be created.
        - nodeType
        - nodeCoord
        - nodeName
    """

    def __init__(self, graphTarget, nodeType, x, y):
        self.graphTarget = graphTarget
        self.nodeName = str(nodeType) + "_" + str(graphTarget._nbNodesCreated)
        self.nodeType = nodeType
        self.nodeCoord = (x, y)

    def undoCmd(self):
        """
            Undo the creation of the node.
        """
        node = self.graphTarget.getNode(self.nodeName)
        self.graphTarget.getGraphTuttle().deleteNode(self.graphTarget.getGraphTuttle().getNode(str(self.nodeName)))
        self.graphTarget.getNodes().remove(node)
        self.graphTarget.nodesChanged()

    def redoCmd(self):
        """
            Redo the creation of the node.
        """
        tuttleNode = self.graphTarget.getGraphTuttle().createNode(str(self.nodeType))
        self.graphTarget.getNodes().append(Node(self.nodeName, self.nodeType, self.nodeCoord, tuttleNode))
        self.graphTarget.nodesChanged()
        # We don't have to recreate the connections because when a node is created, it can't have connections !
        # But maybe we should delete the (hypothetical) connections anyway ??

    def doCmd(self):
        """
            Create a node.
        """

        # New Tuttle node
        tuttleNode = self.graphTarget.getGraphTuttle().createNode(str(self.nodeType))
        #self.graphTarget.getGraphTuttle().addNode(tuttleNode)
        print "TuttleNode name : ", tuttleNode.getName()
        self.graphTarget.getGraphTuttle().renameNode(tuttleNode, str(self.nodeName))
        print "TuttleNode rename : ", tuttleNode.getName()
        print "TuttleNode : ", self.graphTarget.getGraphTuttle().getNode(str(self.nodeName))
        # New Buttle node
        self.graphTarget._nbNodesCreated += 1
        self.graphTarget._nodes.append(Node(self.nodeName, self.nodeType, self.nodeCoord, tuttleNode))
        self.graphTarget.nodesChanged()
