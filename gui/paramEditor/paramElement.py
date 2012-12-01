import sys

from PySide import QtGui, QtDeclarative
from paramInt import ParamInt
from paramString import ParamString
from wrappers.mainWrapper import MainWrapper
from wrappers.intWrapper import IntWrapper
from wrappers.stringWrapper import StringWrapper


def main():
    app = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()

    paramListTmp = [
            ParamInt(1.5, 5, 52),
            ParamInt(defaultValue=2.5, minimum=5, maximum=52, text="truc oh oh oh"),
            ParamInt(defaultValue=5.5, minimum=5, maximum=52),
            ParamString(defaultValue="plop.jpg", stringType="filename"),
            ParamInt(defaultValue=7.5, minimum=5, maximum=52),
            ParamString(defaultValue="plop.jpg", stringType="filename")
    ]

    mapTypeToWrapper = {
        ParamInt: IntWrapper,
        ParamString: StringWrapper
    }

    paramList = [mapTypeToWrapper[paramElt.__class__](paramElt) for paramElt in paramListTmp]
    paramListModel = MainWrapper(view, paramList)

    rc = view.rootContext()
    rc.setContextProperty('_paramListModel', paramListModel)

    view.setSource('qml/paramElement.qml')
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

    view.show()

    app.exec_()

if __name__ == '__main__':
    main()
