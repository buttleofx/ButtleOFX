import sys
from PySide import QtGui, QtDeclarative
import shiboken
from node import Node
from wrappers.mainWrapper import MainWrapper


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


# List of the graph nodes
nodeList = [
    # Arguments : name, xCoord, yCoord, r, v, b, nbInput
    Node('Node1', 150, 100, 221, 54, 138, 1),
    Node('Node2', 300, 200, 58, 174, 206, 3),
    Node('Node3', 500, 80, 20, 200, 120, 3),
    Node('Node3', 500, 80, 20, 200, 120, 3),
]

QMLMap = []

nodeSelected = 0

if __name__ == '__main__':

    # Initialisation
    app = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()

    mainWrapperNodes = MainWrapper(view, nodeList)
    rc = view.rootContext()
    rc.setContextProperty('nodeListModel', mainWrapperNodes)
    rc.setContextProperty('nodeCount', Node.count)
    view.setWindowTitle("Graph editor")
    view.setSource("qml/window.qml")
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

    rc.setContextProperty('nodeSelected', nodeSelected)
    createNode.count = 0

    # "Cast" the rootObject as a QDeclarativeItem
    rootItem = wrapInstanceAs(view.rootObject(), QtDeclarative.QDeclarativeItem)

    # Create the QML objects corresponding
    for element in nodeList:
        createNode(view, rootItem, QMLMap)

    # Connect the functions we need in the QML files
    rootItem.addNode.connect(lambda: createNode(view, rootItem, QMLMap))
    rootItem.deleteNode.connect(lambda index: deleteNode(QMLMap, QMLMap[index]))
    #rootItem.selectNode.connect(lambda node : nodeSelected = node))

    view.show()
    app.exec_()
