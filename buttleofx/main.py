from PySide import QtGui, QtDeclarative
import os
# data
from buttleofx.datas import ButtleData
#connections
from buttleofx.gui.graph.connection import LineItem
# paramEditor
from buttleofx.gui.paramEditor.wrappers import ParamEditorWrapper
# undo_redo
from buttleofx.core.undo_redo.manageTools import CommandManager

currentFilePath = os.path.dirname(os.path.abspath(__file__))


def main(argv):
    # add new QML type
    QtDeclarative.qmlRegisterType(LineItem, "ConnectionLineItem", 1, 0, "ConnectionLine")

    # create undo_redo contexts
    cmdManager = CommandManager()
    cmdManager.setActive()
    cmdManager.clean()

    # create QApplication
    QApplication = QtGui.QApplication(argv)
    view = QtDeclarative.QDeclarativeView()
    view.setWindowTitle("ButtleOFX")

    # data
    buttleData = ButtleData().init(view)
    paramList = []
    paramsW = ParamEditorWrapper(view, paramList)

    # expose data to QML
    rc = view.rootContext()
    rc.setContextProperty("_buttleData", buttleData)
    rc.setContextProperty('_paramList', paramsW)

    # launch QApplication
    view.setSource(os.path.join(currentFilePath, "MainWindow.qml"))
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
    view.show()
    QApplication.exec_()
