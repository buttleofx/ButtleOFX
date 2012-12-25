from buttleofx.gui.graph import Graph
from buttleofx.gui.graph import GraphWrapper
from quickmamba.patterns import Signal

from PySide import QtGui, QtDeclarative

import sys
import os

currentFilePath = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()

    graph = Graph()
    graphWrapper = GraphWrapper(graph, view)

    graph.createNode("test")
    graphWrapper.__str__()

    view.rootContext().setContextProperty("_graphWrapper", graphWrapper)
    view.rootContext().setContextProperty("_wrappers", graphWrapper.getWrappers())
    view.setWindowTitle("Graph editor")
    view.setSource(os.path.join(currentFilePath, "qml/GraphEditor.qml"))
    view.setSource("qml/GraphEditor.qml")
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

    view.show()
    app.exec_()
