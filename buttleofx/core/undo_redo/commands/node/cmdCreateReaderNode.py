# undo_redo
from buttleofx.core.undo_redo.manageTools import UndoableCommand
from buttleofx.core.undo_redo.commands.node import CmdCreateNode


class CmdCreateReaderNode(CmdCreateNode):
    """
        Command that creates a node and sets its filename. It's the case when an image is dropped in the graph.
        We can't use a group of commands because we need the tuttle node to set the value, and this tuttle node is created in the function doCmd() of the cmdCreateNode.!
        Then we need a separate class CmdCreateReaderNode.
        This class inherits CmdCreateNode and reuses its commands.

        Attributes :
        - graphTarget : the graph in which the node will be created.
        - node : we save the node's data because we will need it for the redo
        - nodeName
        - nodeType
        - nodeCoord
        - filename
    """

    def __init__(self, graphTarget, nodeType, x, y, filename):
        CmdCreateNode.__init__(self, graphTarget, nodeType, x, y)
        self._filename = filename

    def undoCmd(self):
        """
            Undoes the creation of the node.
            Just calls the function undoCmd() of the class CmdCreateNode.
        """
        CmdCreateNode.undoCmd(self)

    def redoCmd(self):
        """
            Redoes the creation of the node.
            Just calls the function redoCmd() of the class CmdCreateNode.
        """
        CmdCreateNode.redoCmd(self)

    def doCmd(self):
        """
            Creates a node by calling the function doCmd() of the class CmdCreateNode.
            Then sets the value of the param 'filename'.
        """
        CmdCreateNode.doCmd(self)
        self._node.getTuttleNode().getParam('filename').setValue(str(self._filename))
        self._graphTarget.nodesChanged()
