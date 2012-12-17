import sys
from PySide import QtGui, QtDeclarative
from gui.graph.graph import *
from gui.paramEditor.paramEditor import *

def main():
    QApplication = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()
    view.setWindowTitle("ButtleOFX")
    view.setSource("buttleApp.qml")
    rc = view.rootContext()

    # for the GraphEditor
    nodeManager = NodeManager(view)
    rc.setContextProperty('_nodeManager', nodeManager)

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


    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
    view.show()
    QApplication.exec_()


if __name__ == '__main__':
    main()
