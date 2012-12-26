# graph
from buttleofx.gui.graph import Graph
from buttleofx.gui.graph import GraphWrapper
# paramEditor
from buttleofx.gui.paramEditor.params import ParamInt
from buttleofx.gui.paramEditor.params import ParamString
from buttleofx.gui.paramEditor.wrappers import MainWrapper


from PySide import QtGui, QtDeclarative

import os

currentFilePath = os.path.dirname(os.path.abspath(__file__))


def main(argv):
    QApplication = QtGui.QApplication(argv)
    view = QtDeclarative.QDeclarativeView()
    view.setWindowTitle("ButtleOFX")
    rc = view.rootContext()

    # for the GraphEditor
    graph = Graph()
    graphWrapper = GraphWrapper(graph, view)
    rc.setContextProperty("_graphWrapper", graphWrapper)
    rc.setContextProperty("_nodeWrappers", graphWrapper.getNodeWrappers())

    #connexionList = []
    #connectionManager = ConnectionManager()
    #rc.setContextProperty('_connectionManager', connectionManager)

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

    view.setSource(os.path.join(currentFilePath, "MainWindow.qml"))
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
    view.show()
    QApplication.exec_()

