import sys
from PySide import QtGui, QtDeclarative
from gui.graph.graph.graph import Graph
from gui.graph.graph.graphWrapper import GraphWrapper
from QuickMamba.quickmamba.patterns.signalEvent import Signal

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()

    graph = Graph()
    graphWrapper = GraphWrapper(graph, view)
    graph.createNode("test")
    graph.createNode("test3")
    graphWrapper.__str__()

    view.rootContext().setContextProperty("_graphWrapper", graphWrapper)
    view.rootContext().setContextProperty("_wrappers", graphWrapper.getWrappers())
    view.setWindowTitle("Graph editor")
    view.setSource("qml/GraphEditor.qml")
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

    view.show()
    app.exec_()