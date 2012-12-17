from node import Node
from nodeWrapper import NodeWrapper
from QuickMamba.qobjectlistmodel import QObjectListModel

from PySide import QtDeclarative, QtCore
import shiboken

import os


def wrapInstanceAs(instance, target_class):
    return shiboken.wrapInstance(shiboken.getCppPointer(instance)[0], target_class)


class NodeManager(QtCore.QObject):

    """
        Class NodeManager defined by :
        - A : coreNode list
        - B : nodeWrapper list
        - C : nodeItem list
        - itemToWrapper Map
        - itemToNode Map
        - _currentNode : the current selected node
        When a modification is made, changes are directly applied to A, then B and C are automatically updated.
    """

    def __init__(self, view):
        super(NodeManager, self).__init__()
        self.engine = view.engine()
        self.rootObject = view.rootObject()
        self.nodeItemFactory = None
        self.rootItem = None

        self._currentNode = None
        self._zMax = 2

        # A : coreNode list
        self.coreNodes = []
        # B : nodeWrapper ListModel
        self.nodeWrappers = QObjectListModel(self)
        # C : nodeItem list
        self.nodeItems = []
        # Maps
        self.itemToWrapper = {}
        self.itemToNode = {}

    @QtCore.Slot(result="double")
    def getZMax(self):
        return self._zMax

    @QtCore.Slot()
    def setZMax(self):
        self._zMax += 1

    def createNode(self, nodeType):
        """
            Create and return a core Node from a type of node.
        """
        nbNodes = len(self.coreNodes)
        return Node(str(nodeType), nbNodes, ((nbNodes + 1) * 30, (nbNodes + 5) * 10))

    @QtCore.Slot(str)
    def addNode(self, nodeType):

        """
            Create all needed instances of a node from the type of node : the core node, the wrapped node and the QML node.
            The function doesn't return anything but changes the current selected node as the new node.
        """

        if not self.nodeItemFactory:
            self.nodeItemFactory = QtDeclarative.QDeclarativeComponent(self.engine, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'qml/Node.qml'))
        if not self.rootItem:
            self.rootItem = wrapInstanceAs(self.rootObject, QtDeclarative.QDeclarativeItem)

        # Create coreNode
        n = self.createNode(nodeType)
        # Create nodeWrapper
        nw = NodeWrapper(n)
        # Append to respective lists
        self.coreNodes.append(n)
        self.nodeWrappers.append(nw)

        # Begin create nodeItem
        nodeItem = self.nodeItemFactory.beginCreate(self.engine.rootContext())
        # Add to maps
        self.itemToWrapper[nodeItem] = nw
        self.itemToNode[nodeItem] = n
        # Complete create
        self.nodeItemFactory.completeCreate()
        # Set parent view
        nodeItem.setParentItem(self.rootItem)
        self.nodesChanged.emit()
        # Update current node
        self.setCurrentNode(nodeItem)
        self.currentNodeChanged.emit()

    def getNodes(self):
        """
            Return the nodeWrapper ListModel
        """
        return self.nodeWrappers

    @QtCore.Slot(QtDeclarative.QDeclarativeItem, result="QVariant")
    def getWrapper(self, item):
        """
            Return the right wrapped node from the node's item.
        """
        return self.itemToWrapper[item]

    @QtCore.Slot(QtDeclarative.QDeclarativeItem)
    def deleteNode(self, item):

        """
            Delete all the corresponding instances of the QML node.

        """

        if not item:
            return
        n = self.itemToNode[item]
        nw = self.itemToWrapper[item]
        # Delete the core node
        self.coreNodes.remove(n)
        # Delete the nodeWrapper
        self.nodeWrappers.removeAt(self.nodeWrappers.indexOf(nw))

        # Change the current selected node to None if the deleted node was selected
        if item == self._currentNode:
            self._currentNode = None
            self.currentNodeChanged.emit()

        # Emit the modifications
        self.nodesChanged.emit()
        # Delete the QML node
        item.deleteLater()

    @QtCore.Slot()
    def deleteCurrentNode(self):
        """
            Delete the current selected node by calling the deleteNode() function.
        """
        self.deleteNode(self._currentNode)

    def getCurrentNode(self):
        """
            Return the item of the current selected node.
        """
        return self._currentNode

    def setCurrentNode(self, item):
        """
            Change the current selected node and emit the change.
        """
        if self._currentNode == item:
            return
        self._currentNode = item
        self.currentNodeChanged.emit()

    nodesChanged = QtCore.Signal()
    nodes = QtCore.Property("QVariant", getNodes, notify=nodesChanged)
    currentNodeChanged = QtCore.Signal()
    currentNode = QtCore.Property("QVariant", getCurrentNode, setCurrentNode, notify=currentNodeChanged)
