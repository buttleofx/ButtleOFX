from buttleofx.core.undo_redo.manageTools import UndoableCommand


class CmdSetCoord(UndoableCommand):
    """
        Command that moves a node.
        Attributes :
        - graphTarget
        - nodeTargetName : the name of the target node wich will be changed by the movement
        - newCoord : the coordinate wich will be mofidy in the target
        - coordOld : the old coordinate of the target node, wich will be used for reset the target in case of undo command
    """

    def __init__(self, graphTarget, nodeTargetName, newCoord):
        self.graphTarget = graphTarget
        self.nodeTargetName = nodeTargetName
        self.oldCoord = graphTarget.getNode(nodeTargetName).getOldCoord()
        self.newCoord = newCoord

    def undoCmd(self):
        """
            Undoes the movement of the node.
            The target node is reset with the old coordinates.
        """
        node = self.graphTarget.getNode(self.nodeTargetName)
        node.setCoord(self.oldCoord[0], self.oldCoord[1])
        node.setOldCoord(self.oldCoord[0], self.oldCoord[1])

    def redoCmd(self):
        """
            Redoes the movement of the node.
            Just calls the doCmd() function.
        """
        return self.doCmd()

    def doCmd(self):
        """
            Executes the movement of the node.
        """
        node = self.graphTarget.getNode(self.nodeTargetName)
        node.setCoord(self.newCoord[0], self.newCoord[1])
        node.setOldCoord(self.newCoord[0], self.newCoord[1])

    def getLabel(self):
        return self.nodeTargetName