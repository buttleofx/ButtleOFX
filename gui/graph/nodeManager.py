from PySide import QtDeclarative, QtCore
from node import Node
from nodeWrapper import NodeWrapper
from QuickMamba.qobjectlistmodel import QObjectListModel

import shiboken


def wrapInstanceAs(instance, target_class):
    return shiboken.wrapInstance(shiboken.getCppPointer(instance)[0], target_class)


class NodeManager(QtCore.QObject):

    """
        Class NodeManager
        A : coreNode list
        B : nodeWrapper list
        C : nodeItem list
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
        return self.nodeWrappers

    @QtCore.Slot(QtDeclarative.QDeclarativeItem, result="QVariant")
    def getWrapper(self, item):
        return self.itemToWrapper[item]

    @QtCore.Slot(QtDeclarative.QDeclarativeItem)
    def deleteNode(self, item):
        if not item:
            return
        n = self.itemToNode[item]
        nw = self.itemToWrapper[item]
        self.coreNodes.remove(n)
        self.nodeWrappers.removeAt(self.nodeWrappers.indexOf(nw))

        if item == self._currentNode:
            self._currentNode = None
            self.currentNodeChanged.emit()

        self.nodesChanged.emit()
        item.deleteLater()

    @QtCore.Slot()
    def deleteCurrentNode(self):
        self.deleteNode(self._currentNode)

    def getCurrentNode(self):
        return self._currentNode

    def setCurrentNode(self, item):
        if self._currentNode == item:
            return
        self._currentNode = item
        self.currentNodeChanged.emit()

    nodesChanged = QtCore.Signal()
    nodes = QtCore.Property("QVariant", getNodes, notify=nodesChanged)
    currentNodeChanged = QtCore.Signal()
    currentNode = QtCore.Property("QVariant", getCurrentNode, setCurrentNode, notify=currentNodeChanged)
