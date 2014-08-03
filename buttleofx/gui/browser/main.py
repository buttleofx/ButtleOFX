import os
import sys

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtQuick


currentFilePath = os.path.dirname(os.path.abspath(__file__))
quickmambaPath = os.path.join(currentFilePath, '../../../QuickMamba')
sys.path.append(quickmambaPath)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    view = QtQuick.QQuickView()

    rc = view.rootContext()

    view.setWindowTitle("Browser")
    view.setSource(QtCore.QUrl(os.path.join(currentFilePath, "qml/Browser.qml")))
    view.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)

    view.show()
    app.exec_()
