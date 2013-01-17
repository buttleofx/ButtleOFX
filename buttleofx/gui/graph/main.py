from PySide import QtGui, QtDeclarative
import sys
import os
# data
from buttleofx.datas import ButtleData
# undo_redo
from buttleofx.core.undo_redo.manageTools import CommandManager

currentFilePath = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()

    rc = view.rootContext()

    # create undo-redo context
    cmdManager = CommandManager()
    cmdManager.setActive()
    cmdManager.clean()

    # data
    buttleData = ButtleData().init(view)
    #buttleData.getGraph().createNode("Blur", cmdManager)
    rc.setContextProperty("_buttleData", buttleData)
    rc.setContextProperty("_cmdManager", cmdManager)

    view.setWindowTitle("Graph editor")
    view.setSource(os.path.join(currentFilePath, "qml/GraphEditor.qml"))
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

    view.show()
    app.exec_()
