from PySide import QtDeclarative, QtCore
from node import Node
from nodeWrapper import NodeWrapper
from QuickMamba.qobjectlistmodel import QObjectListModel

import shiboken


def wrapInstanceAs(instance, target_class):
    """
        Cast the instance as a shiboken object.
    """
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

        # A : coreNode list
        self.coreNodes = []
        # B : nodeWrapper ListModel
        self.nodeWrappers = QObjectListModel(self)
        # C : nodeItem list
        self.nodeItems = []
        # Maps
        self.itemToWrapper = {}
        self.itemToNode = {}

    def createNode(self, nodeType):

        """
            Create and return a core Node from a type of node.
        """

        if str(nodeType) == "Blur":
            r = 58
            g = 174
            b = 206
            nbInput = 1
        elif str(nodeType) == "Gamma":
            r = 221
            g = 54
            b = 138
            nbInput = 2
        elif str(nodeType) == "Invert":
            r = 90
            g = 205
            b = 45
            nbInput = 3
        else:
            r = 187
            g = 187
            b = 187
            nbInput = 1
        return Node(str(nodeType) + str(len(self.coreNodes)), (len(self.coreNodes) + 1) * 30, (len(self.coreNodes) + 5) * 10, r, g, b, nbInput)

    @QtCore.Slot(str)
    def addNode(self, nodeType):

        """
            Create all needed instances of a node from the type of node : the core node, the wrapped node and the node item (QML object).
            The function doesn't return anything but change the current selected node as the new node.
        """

        if not self.nodeItemFactory:
            self.nodeItemFactory = QtDeclarative.QDeclarativeComponent(self.engine, 'qml/Node.qml')
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
            Return the right wrapped node from the node item.
        """
        return self.itemToWrapper[item]

    @QtCore.Slot(QtDeclarative.QDeclarativeItem)
    def deleteNode(self, item):

        """
            Delete all the corresponding instances of the node item.

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
