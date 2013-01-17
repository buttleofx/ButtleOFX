from PySide import QtGui, QtDeclarative

from buttleofx.gui.paramEditor.params import ParamInt
from buttleofx.gui.paramEditor.params import ParamString
from buttleofx.gui.paramEditor.params import ParamBoolean
from buttleofx.gui.paramEditor.wrappers import MainWrapper

import sys
import os

currentFilePath = os.path.dirname(os.path.abspath(__file__))


def main():
    app = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()

    paramList = [
            ParamInt(20, 5, 128),
            ParamInt(defaultValue=11, minimum=5, maximum=500, text="something"),
            ParamInt(defaultValue=50, minimum=1, maximum=52, text="truc"),
            ParamString(defaultValue="something.jpg", stringType="filename"),
            ParamInt(defaultValue=7, minimum=5, maximum=12),
            ParamString(defaultValue="somethingelse.jpg", stringType="type2"),
            ParamBoolean(defaultValue="true", text="lol")
    ]

    mw = MainWrapper(view, paramList)
    view.rootContext().setContextProperty('_paramListModel', mw)

    view.setSource(os.path.join(currentFilePath, 'qml/ParamEditor.qml'))
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

    view.show()

    app.exec_()

if __name__ == '__main__':
    main()
