import sys
from PySide import QtGui, QtDeclarative
from nodeManager import NodeManager


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()
    view.setWindowTitle("Graph editor")
    view.setSource("qml/window.qml")
    rc = view.rootContext()

    nodeManager = NodeManager(view)
    rc.setContextProperty('_nodeManager', nodeManager)

    view.show()
    app.exec_()
