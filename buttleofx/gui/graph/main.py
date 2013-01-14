# garph
from buttleofx.gui.graph import Graph
from buttleofx.gui.graph import GraphWrapper
# undo_redo
from buttleofx.core.undo_redo.manageTools import CommandManager

from PySide import QtGui, QtDeclarative

import sys
import os

currentFilePath = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()

    # create undo-redo context
    cmdManager = CommandManager()
    cmdManager.setActive()
    cmdManager.clean()

    # graph and graphWrapper
    graph = Graph()
    graphWrapper = GraphWrapper(graph, view)

    # test node creation
    graph.createNode("test", cmdManager)
    graphWrapper.__str__()

    view.rootContext().setContextProperty("_graphWrapper", graphWrapper)
    view.rootContext().setContextProperty("_nodeWrappers", graphWrapper.getNodeWrappers())
    view.rootContext().setContextProperty("_cmdManager", cmdManager)

    view.setWindowTitle("Graph editor")
    view.setSource(os.path.join(currentFilePath, "qml/GraphEditor.qml"))
    view.setSource("qml/GraphEditor.qml")
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

    view.show()
    app.exec_()
