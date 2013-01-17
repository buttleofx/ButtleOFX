# undo_redo
from buttleofx.core.undo_redo.manageTools import UndoableCommand
# core
from buttleofx.core.graph.node import Node


class CmdDeleteNode(UndoableCommand):
    """
        Command that delete a node.
    """

    def __init__(self, graphTarget, nodeName):
        """
            Initializes the member variables :
            graphTarget  is the graph in which the node will be deleted.
            nodeName is the name of the node we want to create.
       """
        self.graphTarget = graphTarget
        self.nodeName = nodeName
        self.nodeCoord = (50, 20)

    def undoCmd(self):
        """
            Undo the delete of the node.
        """
        print "Undo delete"
        self.graphTarget.createNode(self.nodeType)

    def redoCmd(self):
        """
            Redo the delete of the node.
        """
        print "Redo creation"
        self.doCmd()

    def doCmd(self):
        """
            Delete a node.
        """
        # we search the right node to delete
        indexWrapper = 0
        for node in self.graphTarget._nodes:
            if node.getName() == self.nodeName:
                self.nodeType = node.getType()
                # delete his connections
                for connection in self.graphTarget._connections:
                    if connection.getClipOut().getNodeName() == self.nodeName or connection.getClipIn().getNodeName() == self.nodeName:
                        self.graphTarget.deleteConnection(connection)
                # delete the node
                self.graphTarget._nodes.remove(node)
                break
            indexWrapper += 1
        self.graphTarget.nodesChanged()
        self.graphTarget.connectionsChanged()
