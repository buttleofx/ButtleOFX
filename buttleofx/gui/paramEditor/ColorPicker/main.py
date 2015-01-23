
import os
import sys

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtQuick
from PyQt5 import QtQml
from screenPicker.screenPicker import ScreenPicker
from OpenGL import GL




currentFilePath = os.path.dirname(os.path.abspath(__file__))
quickmambaPath = os.path.join(currentFilePath, '../../../../QuickMamba')
sys.path.append(quickmambaPath)


import quickmamba

if __name__ == '__main__':
    quickmamba.qmlRegister()
    print ("quick ok")
    QtQml.qmlRegisterType(ScreenPicker, "ScreenPicker", 1, 0, "ScreenPicker")
    app = QtWidgets.QApplication(sys.argv)
    view = QtQuick.QQuickView()

    view.setTitle("Color Picker")
    view.setSource(QtCore.QUrl(os.path.join(currentFilePath, "qml/ColorWheelTest.qml")))
    view.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)

    view.show()
    app.exec_()
