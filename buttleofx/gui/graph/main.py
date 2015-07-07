import sys
import os
from buttleofx.data import globalButtleData
from PyQt5 import QtCore, QtWidgets, QtQuick, QtQml
from buttleofx.gui.graph.connection import LineItem
from buttleofx.core.undo_redo.manageTools import globalCommandManager


currentFilePath = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    QtQml.qmlRegisterType(LineItem, "ConnectionLineItem", 1, 0, "ConnectionLine")

    app = QtWidgets.QApplication(sys.argv)
    view = QtQuick.QQuickView()

    rc = view.rootContext()

    # Create undo-redo context
    cmdManager = globalCommandManager
    cmdManager.setActive()
    cmdManager.clean()

    # Data
    globalButtleData.init(view)

    # Expose to QML
    rc.setContextProperty("_buttleData", globalButtleData)

    view.setWindowTitle("Graph editor")
    view.setSource(QtCore.QUrl(os.path.join(currentFilePath, "qml/GraphEditor.qml")))
    view.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)

    view.show()
    app.exec_()
