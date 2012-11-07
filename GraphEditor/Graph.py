import sys
import Node
import NodeWrapper
import ListModel
from PySide import QtCore, QtGui, QtDeclarative


# Controller
class Controller(QtCore.QObject):
    @QtCore.Slot(QtCore.QObject)
    def nodeSelected(self, listElement):
        print 'Node : ', listElement._element.name


# Listener
class Listener(QtCore.QObject):

    """
        Class Listener for Nodes defined by :
            - boolean clicked
    """

    def __init__(self):
        QtCore.QObject.__init__(self)
        self._clicked = False

    def get_onClicked(self):
        return self._clicked

    def _addNode(self):
        newNode = Node.Node('Node' + str(len(nodes) + 1), 10, 40, 187, 187, 187, 3)
        nodes.append(newNode)
        elements = [NodeWrapper.NodeWrapper(element) for element in nodes]
        nodeList = ListModel.ListModel(elements)
        rc.setContextProperty('nodeListModel', nodeList)
        for element in nodes:
            print("{}".format(element.name))

    on_clicked = QtCore.Signal()
    addNode = QtCore.Property(float, _addNode, notify=on_clicked)


# List of the graph nodes
nodes = [
    # Arguments : name, xCoord, yCoord, r, v, b, nbInput
    Node.Node('Node1', 150, 100, 221, 54, 138, 1),
    Node.Node('Node2', 300, 200, 58, 174, 206, 3),
    Node.Node('Node3', 500, 80, 20, 200, 120, 3),
]


# QApplication / QDeclarativeView
app = QtGui.QApplication(sys.argv)
view = QtDeclarative.QDeclarativeView()
view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
rc = view.rootContext()


def main():

    elements = [NodeWrapper.NodeWrapper(element) for element in nodes]
    nodeList = ListModel.ListModel(elements)
    controller = Controller()
    listener = Listener()

    rc.setContextProperty('nodeListModel', nodeList)
    rc.setContextProperty('controller', controller)
    rc.setContextProperty('listener', listener)
    view.setWindowTitle("Graph editor")
    view.setSource('graph.qml')

    view.show()
    app.exec_()

if __name__ == '__main__':
    main()
