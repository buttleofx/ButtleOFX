import sys

from PySide import QtGui, QtDeclarative
from gui.paramEditor.paramInt import ParamInt
from gui.paramEditor.paramString import ParamString
from gui.paramEditor.wrappers.mainWrapper import MainWrapper


def main():
    app = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()

    paramList = [
            ParamInt(20, 5, 128),
            ParamInt(defaultValue=11, minimum=5, maximum=500, text="something"),
            ParamInt(defaultValue=50, minimum=1, maximum=52, text="truc"),
            ParamString(defaultValue="something.jpg", stringType="filename"),
            ParamInt(defaultValue=7, minimum=5, maximum=12),
            ParamString(defaultValue="somethingelse.jpg", stringType="type2")
    ]

    mw = MainWrapper(view, paramList)
    view.rootContext().setContextProperty('_paramListModel', mw)

    view.setSource('qml/ParamEditor.qml')
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

    view.show()

    app.exec_()

if __name__ == '__main__':
    main()
