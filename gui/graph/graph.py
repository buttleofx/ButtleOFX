from PySide import QtGui, QtCore, QtDeclarative
import shiboken


def wrapInstanceAs(instance, target_class):
    return shiboken.wrapInstance(shiboken.getCppPointer(instance)[0], target_class)


def createNode(view, view_root, nodeItemMap):
    nodeComponentFactory = QtDeclarative.QDeclarativeComponent(view.engine(), 'qml/Node.qml')
    nodeComponent = nodeComponentFactory.create()

    # "Cast" the created QDeclarativeComponent
    nodeItem = wrapInstanceAs(nodeComponent, QtDeclarative.QDeclarativeItem)
    nodeItem.setParentItem(view_root)

    nodeItemMap.append(nodeItem)

    print "len:" + str(len(nodeItemMap))


#def createConnection(view, view_root):
 #   nodeComponentFactory = QtDeclarative.QDeclarativeComponent(view.engine(), 'qml/Connection.qml')
  #  nodeComponent = nodeComponentFactory.create()

    # "Cast" the created QDeclarativeComponent
   # connectionItem = wrapInstanceAs(nodeComponent, QtDeclarative.QDeclarativeItem)
    #connectionItem.setParentItem(view_root)

def deleteNode(nodeItemMap, nodeItem):
    nodeItem.deleteLater()
    nodeItemMap.remove(nodeItem)
    print "len:" + str(len(nodeItemMap))


if __name__ == '__main__':

    app = QtGui.QApplication("")
    view = QtDeclarative.QDeclarativeView()
    view.setWindowTitle("Graph editor")
    view.setSource("qml/window.qml")
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
    rc = view.rootContext()

    # "Cast" the rootObject as a QDeclarativeItem
    rootItem = wrapInstanceAs(view.rootObject(), QtDeclarative.QDeclarativeItem)
    # print "Classic rootObject class : ", view.rootObject().__class__
    # print "After wrapping : ", rootItem.__class__

    nodeItemMap = []

    rootItem.addNode.connect(lambda: createNode(view, rootItem, nodeItemMap))
    rootItem.deleteNode.connect(lambda: deleteNode(nodeItemMap, nodeItemMap[-1]))
    #createNode(view, rootItem)
    #createNode(view, rootItem)

    #createConnection(view, rootItem)

    view.show()
    app.exec_()
