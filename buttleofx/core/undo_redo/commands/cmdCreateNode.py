#!/usr/bin/env python
# -*-coding:utf-8-*

#from buttleofx.gui.graph.node import nodeWrapper
from buttleofx.core.undo_redo.manageTools import UndoableCommand
from buttleofx.gui.graph.node import Node


class CmdCreateNode(UndoableCommand):
    """
        Command that moves a node
    """

    def __init__(self, graphTarget, nodeType):
        """
            Initializes the member variables :
            graphTarget  is the graph in which the node will be created.
            nodeType is the type of the node we want to create.
       """

        self.graphTarget = graphTarget
        self.nodeType = nodeType
        self.nodeName = " "
        self.nodeCoord = (50, 20)

    def undoCmd(self):
        """
            Undo the creation of the node.
        """
        print "Undo creation "
        self.graphTarget.deleteNode(self.nodeName)

    def redoCmd(self):
        """
            Redo the creation of the node
        """
        print "Redo creation"
        self.doCmd()

    def doCmd(self):
        """
            Create a node
        """
        self.graphTarget._nbNodesCreated += 1
        self.nodeName = str(self.nodeType) + "_" + str(self.graphTarget._nbNodesCreated)

        self.graphTarget._nodes.append(Node(self.nodeName, self.nodeType, self.nodeCoord))
        self.graphTarget.nodesChanged()
