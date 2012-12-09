import sys
from PySide import QtGui, QtDeclarative
from gui.graph.graph import *


def main():
    QApplication = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()
    view.setWindowTitle("ButtleOFX")
    view.setSource("buttleApp.qml")
    rc = view.rootContext()

    # for the GraphEditor
    nodeManager = NodeManager(view)
    rc.setContextProperty('_nodeManager', nodeManager)

    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
    view.show()
    QApplication.exec_()

if __name__ == '__main__':
    main()
