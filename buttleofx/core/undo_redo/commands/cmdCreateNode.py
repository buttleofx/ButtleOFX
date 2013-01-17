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

    def __init__(self, graphTarget, nodeType):
        self.graphTarget = graphTarget
        self.nodeType = nodeType
        self.nodeCoord = (50, 20)

    def undoCmd(self):
        """
            Undo the creation of the node.
        """
        print "Undo creation "
        #self.graphTarget.deleteNode(self.nodeName)

        node = self.graphTarget.getNode(self.nodeName)
        self.nodeCoord = node.getCoord()
        self.graphTarget.deleteNodeConnections(self.nodeName)
        self.graphTarget.getNodes().remove(node)
        self.graphTarget.nodesChanged()

    def redoCmd(self):
        """
            Redo the creation of the node.
        """
        print "Redo creation"
        self.graphTarget.getNodes().append(Node(self.nodeName, self.nodeType, self.nodeCoord))
        self.graphTarget.nodesChanged()
        # THINK TO RECREATE CONNECTIONS TOO !!!!!!!!!

    def doCmd(self):
        """
            Create a node.
        """
        self.graphTarget._nbNodesCreated += 1
        self.nodeName = str(self.nodeType) + "_" + str(self.graphTarget._nbNodesCreated)
        self.graphTarget._nodes.append(Node(self.nodeName, self.nodeType, self.nodeCoord))
        self.graphTarget.nodesChanged()
