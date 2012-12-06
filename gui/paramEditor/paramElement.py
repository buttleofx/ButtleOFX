import sys

from PySide import QtGui, QtDeclarative
from paramInt import ParamInt
from paramString import ParamString
from wrappers.mainWrapper import MainWrapper


def main():
    app = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()

    paramList = [
            ParamInt(60, 5, 128),
            ParamInt(defaultValue=8, minimum=5, maximum=500, text="something"),
            ParamInt(defaultValue=50, minimum=1, maximum=52, text=""),
            ParamString(defaultValue="something.jpg", stringType="filename"),
            ParamInt(defaultValue=7, minimum=5, maximum=12),
            ParamString(defaultValue="somethingelse.jpg", stringType="filename")
    ]

    mw = MainWrapper(view, paramList)
    view.rootContext().setContextProperty('_paramListModel', mw)

    view.setSource('qml/ParamElement.qml')
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

    view.show()

    app.exec_()

if __name__ == '__main__':
    main()
