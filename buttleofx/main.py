# graph
from buttleofx.gui.graph import Graph
from buttleofx.gui.graph import GraphWrapper
from buttleofx.datas import ButtleData
# paramEditor
from buttleofx.gui.paramEditor.params import ParamInt
from buttleofx.gui.paramEditor.params import ParamString
from buttleofx.gui.paramEditor.wrappers import MainWrapper
#undo_redo
from buttleofx.core.undo_redo.manageTools import CommandManager

from PySide import QtGui, QtDeclarative

import os

currentFilePath = os.path.dirname(os.path.abspath(__file__))


def main(argv):
    # data
    buttleData = ButtleData()

    # create undo-redo context
    cmdManager = CommandManager()
    cmdManager.setActive()
    cmdManager.clean()

    # create application
    QApplication = QtGui.QApplication(argv)
    view = QtDeclarative.QDeclarativeView()
    view.setWindowTitle("ButtleOFX")
    rc = view.rootContext()

    # for the GraphEditor
    graph = Graph()
    graphWrapper = GraphWrapper(graph, view)
    buttleData.setGraph(graph)
    buttleData.setGraphWrapper(graphWrapper)
    graph.drawConnections(view)

    rc.setContextProperty("_graphWrapper", buttleData.getGraphWrapper())
    rc.setContextProperty("_nodeWrappers", buttleData.getGraphWrapper().getNodeWrappers())
    rc.setContextProperty("_cmdManager", cmdManager)

    # for the ParamEditor
    paramList = [
            ParamInt(20, 5, 128),
            ParamInt(defaultValue=11, minimum=5, maximum=500, text="something"),
            ParamInt(defaultValue=50, minimum=1, maximum=52, text="truc"),
            ParamString(defaultValue="something.jpg", stringType="filename"),
            ParamInt(defaultValue=7, minimum=5, maximum=12),
            ParamString(defaultValue="somethingelse.jpg", stringType="type2")
    ]
    mainWrapper = MainWrapper(view, paramList)
    rc.setContextProperty('_paramListModel', mainWrapper)

    # launch QML
    view.setSource(os.path.join(currentFilePath, "MainWindow.qml"))
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
    view.show()
    QApplication.exec_()
