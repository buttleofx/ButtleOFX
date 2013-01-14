#from buttleofx.gui.graph.node import nodeWrapper
from buttleofx.core.undo_redo.manageTools import UndoableCommand
from buttleofx.gui.graph.node import Node


class CmdDeleteNode(UndoableCommand):
    """
        Command that delete a node.
    """

    def __init__(self, graphTarget, nodeName, cmdManager):
        """
            Initializes the member variables :
            graphTarget  is the graph in which the node will be deleted.
            nodeName is the name of the node we want to create.
       """
        self.graphTarget = graphTarget
        self.cmdManager = cmdManager
        self.nodeName = nodeName
        self.nodeCoord = (50, 20)

    def undoCmd(self):
        """
            Undo the delete of the node.
        """
        print "Undo delete"
        self.graphTarget.createNode(self.nodeType, self.cmdManager)

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
        self.graphTarget._nbNodesCreated -= 1
        # we search the right node to delete
        indexWrapper = 0
        for node in self.graphTarget._nodes:
            if node.getName() == self.nodeName:
                self.nodeType = node.getType()
                self.graphTarget._nodes.remove(node)
                break
            indexWrapper += 1
        self.graphTarget.nodeDeleted(indexWrapper)
