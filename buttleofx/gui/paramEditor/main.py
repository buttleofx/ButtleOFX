# garph
from buttleofx.core.graph import Graph
from buttleofx.gui.graph import GraphWrapper
# undo_redo
from buttleofx.core.undo_redo.manageTools import CommandManager
# params
from buttleofx.gui.paramEditor.params import ParamInt
from buttleofx.gui.paramEditor.params import ParamString
from buttleofx.gui.paramEditor.wrappers import ParamEditorWrapper

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

    # data
    # graph and graphWrapper
    graph = Graph()
    graphWrapper = GraphWrapper(graph, view)

    # test node creation
    graph.createNode("Blur", cmdManager)
    graphWrapper.__str__()

    # params
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

    view.setSource(os.path.join(currentFilePath, 'qml/ParamEditor.qml'))
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

    view.show()

    app.exec_()
