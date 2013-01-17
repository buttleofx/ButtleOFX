from buttleofx.core.undo_redo.manageTools import UndoableCommand

class CmdSetCoord(UndoableCommand):
    """
        Command that moves a node
    """

    def __init__(self, nodeTarget, newCoord):
        """
            Initializes the member variables :
            nodeTarget is the target node wich will be changed by the movement
            newCoord are the coordinate wich will be mofidy in the target
            coordOld are the old coordinate of the target node, wich will be used for reset the target in case of undo command

        """
        self.nodeTarget = nodeTarget
        self.coordOld = self.nodeTarget.getCoord()
        self.newCoord = newCoord

    def undoCmd(self):
        """
            Undoes the movement of the node.
            The target node is reset with the old coordinates.
        """
        self.nodeTarget.setCoord(self.coordOld[0], self.coordOld[1])
        return self.nodeTarget

    def redoCmd(self):
        """
            Redoes the movement of the node.
        """
        return self.doCmd()

    def doCmd(self):
        """
            Executes the movement of the node.
        """

        self.nodeTarget.setCoord(self.newCoord[0], self.newCoord[1])
        return self.nodeTarget

    # Attention, il faut utiliser le nom du noeud pour l'identifer dans le ButtleData.
    # Comme ca, lorsqu'on deplace un noeud, puisqu'on le modifie, on est capable de faire deux fois redo.