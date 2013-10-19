# data
from buttleofx.datas import ButtleData
# undo_redo
from buttleofx.core.undo_redo.manageTools import CommandManager
#connections
from buttleofx.gui.graph.connection import LineItem

from PyQt5 import QtCore, QtWidgets, QtQuick, QtQml

import sys
import os


currentFilePath = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    QtQml.qmlRegisterType(LineItem, "ConnectionLineItem", 1, 0, "ConnectionLine")

    app = QtWidgets.QApplication(sys.argv)
    view = QtQuick.QQuickView()

    rc = view.rootContext()

    # create undo-redo context
    cmdManager = CommandManager()
    cmdManager.setActive()
    cmdManager.clean()

    # data
    buttleData = ButtleData().init(view)

    # expose to QML
    rc.setContextProperty("_buttleData", buttleData)

    view.setWindowTitle("Graph editor")
    view.setSource(QtCore.QUrl(os.path.join(currentFilePath, "qml/GraphEditor.qml")))
    view.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)

    view.show()
    app.exec_()
