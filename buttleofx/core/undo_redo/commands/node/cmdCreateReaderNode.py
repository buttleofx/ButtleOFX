# undo_redo
from buttleofx.core.undo_redo.manageTools import UndoableCommand
from buttleofx.core.undo_redo.commands.node import CmdCreateNode


class CmdCreateReaderNode(UndoableCommand, CmdCreateNode):
    """
        Command that create a node and set its filename. It's the case when an image is dropped in the graph.
        We can't use a group of commands because we need the tuttle node to set the value, and this tuttle node is created in the function doCmd() of the cmdCreateNode.!
        Then we need a separate class CmdCreateReaderNode.
        This class inherits CmdCreateNode and reuse its commands.

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

    def doCmd(self):
        """
            Create a node.
        """
        CmdCreateNode.doCmd(self)
        self._node.getTuttleNode().getParam('filename').setValue(str(self._filename))
        self._graphTarget.nodesChanged()
