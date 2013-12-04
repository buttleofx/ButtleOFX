from PyQt5 import QtCore, QtWidgets, QtQuick, QtQml

import sys
import os

currentFilePath = os.path.dirname(os.path.abspath(__file__))
quickmambaPath = os.path.join(currentFilePath, '../../../QuickMamba')
sys.path.append(quickmambaPath)

import fileModelBrowser


if __name__ == '__main__':
    QtQml.qmlRegisterType(fileModelBrowser.FileModelBrowser, "ButtleFileModel", 1, 0, "FileModelBrowser")

    app = QtWidgets.QApplication(sys.argv)
    view = QtQuick.QQuickView()

    rc = view.rootContext()

    view.setSource(QtCore.QUrl(os.path.join(currentFilePath, "qml/Browser.qml")))
    view.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)

    view.show()
    app.exec_()
