from PySide import QtCore
from QuickMamba.qobjectlistmodel import QObjectListModel
from nodeWrapper import NodeWrapper


class MainWrapper(QtCore.QObject):
    def __init__(self, parent, nodeList):
        super(MainWrapper, self).__init__(parent)
        self._nodes = QObjectListModel(self)
        self._nodes.setObjectList([NodeWrapper(node) for node in nodeList])

    def getNodes(self):
        return self._nodes

    modelChanged = QtCore.Signal()
    nodes = QtCore.Property("QVariant", getNodes, notify=modelChanged)
    