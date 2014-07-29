import sys
import os
from buttleofx.core.graph import Graph
from buttleofx.gui.graph import GraphWrapper
from PyQt5 import QtCore, QtWidgets, QtQuick
from buttleofx.gui.paramEditor.params import ParamInt
from buttleofx.gui.paramEditor.params import ParamString
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.gui.paramEditor.wrappers import ParamEditorWrapper


currentFilePath = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    view = QtQuick.QQuickView()

    paramList = [
        ParamInt(20, 5, 128),
        ParamInt(defaultValue=11, minimum=5, maximum=500, text="something"),
        ParamInt(defaultValue=50, minimum=1, maximum=52, text="truc"),
        ParamString(defaultValue="something.jpg", stringType="filename"),
        ParamInt(defaultValue=7, minimum=5, maximum=12),
        ParamString(defaultValue="somethingelse.jpg", stringType="type2")
    ]

    # Create undo-redo context
    cmdManager = CommandManager()
    cmdManager.setActive()
    cmdManager.clean()

    # Data
    # Graph and graphWrapper
    graph = Graph()
    graphWrapper = GraphWrapper(graph, view)

    # Test node creation
    graph.createNode("Blur", cmdManager)
    graphWrapper.__str__()

    # Params
    paramList = []
    for node in graph.getNodes():
        nodeName = ParamString(defaultValue=node.getName(), stringType="Name")
        nodeType = ParamString(defaultValue=node.getType(), stringType="Type")
        nodeCoord_x = ParamInt(defaultValue=node.getCoord()[0], minimum=0, maximum=1000, text="Coord x")
        nodeCoord_y = ParamInt(defaultValue=node.getCoord()[1], minimum=0, maximum=1000, text="Coord y")

        nodeColor_r = ParamInt(defaultValue=node.getColor().red(), minimum=0, maximum=255, text="Color red")
        nodeColor_g = ParamInt(defaultValue=node.getColor().green(), minimum=0, maximum=255, text="Color green")
        nodeColor_b = ParamInt(defaultValue=node.getColor().blue(), minimum=0, maximum=255, text="Color blue")

        nodeNbInput = ParamInt(defaultValue=node.getNbInput(), minimum=1, maximum=15, text="Nb input")
        nodeImage = ParamString(defaultValue=node.getImage(), stringType="Image file")

        paramList.append(nodeName)
        paramList.append(nodeType)
        paramList.append(nodeCoord_x)
        paramList.append(nodeCoord_y)
        paramList.append(nodeColor_r)
        paramList.append(nodeColor_g)
        paramList.append(nodeColor_b)
        paramList.append(nodeNbInput)
        paramList.append(nodeImage)

    paramsw = ParamEditorWrapper(view, paramList)
    view.rootContext().setContextProperty('_paramListModel', paramsw)

    view.setSource(QtCore.QUrl(os.path.join(currentFilePath, 'qml/ParamEditor.qml')))
    view.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)

    view.show()
    app.exec_()
