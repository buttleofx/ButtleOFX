import sys
from PySide import QtGui, QtCore, QtDeclarative
import shiboken
import Node
import NodeWrapper
import QObjectListModel


def wrapInstanceAs(instance, target_class):
    return shiboken.wrapInstance(shiboken.getCppPointer(instance)[0], target_class)


def createNode(view, view_root, nodeItemMap):
    nodeComponentFactory = QtDeclarative.QDeclarativeComponent(view.engine(), 'qml/Node.qml')
    nodeComponent = nodeComponentFactory.create()

    # "Cast" the created QDeclarativeComponent
    nodeItem = wrapInstanceAs(nodeComponent, QtDeclarative.QDeclarativeItem)
    nodeItem.setParentItem(view_root)

    nodeItemMap.append(nodeItem)

    createNode.count += 1

    print "len:" + str(len(nodeItemMap))


def deleteNode(nodeItemMap, nodeItem):
    nodeItem.deleteLater()
    nodeItemMap.remove(nodeItem)
    print "len:" + str(len(nodeItemMap))


class MainWrapper(QtCore.QObject):
    def __init__(self, parent):
        super(MainWrapper, self).__init__(parent)
        self._clips = QObjectListModel.QObjectListModel(self)
        #self._clips.setObjectList([NodeWrapper.NodeWrapper(Node.Node(1, 150, 100, 221, 54, 138, 1)), NodeWrapper.NodeWrapper(Node.Node(2, 300, 200, 58, 174, 206, 3))])

    def getClips(self):
        return self._clips

    modelChanged = QtCore.Signal()
    clips = QtCore.Property("QVariant", getClips, notify=modelChanged)


# Controller
class Controller(QtCore.QObject):
    @QtCore.Slot(QtCore.QObject)
    def nodeSelected(self, listElement):
        print 'Node : ', listElement.element.name

# List of the graph nodes
nodes = [
    # Arguments : name, xCoord, yCoord, r, v, b, nbInput
    Node.Node('Node1', 150, 100, 221, 54, 138, 1),
    Node.Node('Node2', 300, 200, 58, 174, 206, 3),
    Node.Node('Node3', 500, 80, 20, 200, 120, 3),
    Node.Node('Node3', 500, 80, 20, 200, 120, 3),
]

QMLMap = []

nodeSelected = 0

if __name__ == '__main__':

    # Initialisation
    app = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()

    mw = MainWrapper(view)
    rc = view.rootContext()
    rc.setContextProperty('MainWrapper', mw)
    rc.setContextProperty('nodeList', nodes)
    rc.setContextProperty('nodeCount', Node.Node.count)
    view.setWindowTitle("Graph editor")
    view.setSource("qml/window.qml")
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

    controller = Controller()
    rc.setContextProperty('controller', controller)
    rc.setContextProperty('nodeSelected', nodeSelected)
    createNode.count = 0

    # "Cast" the rootObject as a QDeclarativeItem
    rootItem = wrapInstanceAs(view.rootObject(), QtDeclarative.QDeclarativeItem)

    # "Wrap" the nodes and add them to the wrapperList
    wrapperList = [NodeWrapper.NodeWrapper(element) for element in nodes]

    # Create the QML objects corresponding
    for element in nodes:
        createNode(view, rootItem, QMLMap)

    # Connect the functions we need in the QML files
    rootItem.addNode.connect(lambda: createNode(view, rootItem, QMLMap))
    rootItem.deleteNode.connect(lambda: deleteNode(QMLMap, QMLMap[nodeSelected]))

    view.show()
    app.exec_()
