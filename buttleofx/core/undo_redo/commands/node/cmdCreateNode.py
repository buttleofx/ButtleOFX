from PyQt5 import QtCore
# Tuttle
from pyTuttle import tuttle
# undo_redo
from buttleofx.core.undo_redo.manageTools import UndoableCommand
# core
from buttleofx.core.graph.node import Node


class CmdCreateNode(UndoableCommand):
    """
        Command that creates a node.
        Attributes :
        - graphTarget : the graph in which the node will be created.
        - node : we save the node's data because we will need it for the redo
        - nodeName
        - nodeType
        - nodeCoord
    """

    def __init__(self, graphTarget, nodeType, x, y):
        self._graphTarget = graphTarget
        self._node = None
        self._nodeName = None
        self._nodeType = nodeType
        self._nodeCoord = (x, y)

    def getNodeName(self):
        return self._nodeName

    def undoCmd(self):
        """
            Undoes the creation of the node.
        """
        # The tuttle node is not deleted. We keep it so we don't need to recreate it when the redo command is called.
        node = self._graphTarget.getNode(self._nodeName)
        self._graphTarget.getNodes().remove(node)

        # emit nodesChanged signal
        self._graphTarget.nodesChanged()

    def redoCmd(self):
        """
            Redoes the creation of the node.
        """
        # We don't have to recreate the connections because when a node is created, it can't have connections !
        self._graphTarget.getNodes().append(self._node)

        # emit nodesChanged signal
        self._graphTarget.nodesChanged()

    def doCmd(self):
        """
            Creates a node.
        """
        # We create a new Tuttle node and rename it so it has the same name as the Node
        tuttleNode = self._graphTarget.getGraphTuttle().createNode(str(self._nodeType))
        self._nodeName = tuttleNode.getName()

        # New Buttle node
        self._node = Node(self._nodeName, self._nodeType, self._nodeCoord, tuttleNode)
        self._graphTarget._nodes.append(self._node)

        # connect each param to the node
        for param in self._node.getParams():
            if param.paramChanged is not None:
                # warn the node that one of his param just changed
                param.paramChanged.connect(self._node.emitNodeContentChanged)

        # emit nodesChanged signal
        self._graphTarget.nodesChanged()

        # return the buttle node
        return self._node

    nodeName = QtCore.pyqtProperty(str, getNodeName, constant=True)
