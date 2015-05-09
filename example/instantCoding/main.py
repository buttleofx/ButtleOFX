import sys
sys.path.append("../..")

from quickmamba.utils import QmlInstantCoding

from PyQt5 import QtCore, QtWidgets, QtQuick

import os


def main():
    app = QtWidgets.QApplication(sys.argv)
    view = QtQuick.QQuickView()
    view.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)

    # Create a declarative view
    view.setSource(QtCore.QUrl("source.qml"))
    # Declare we are using instant coding tool on this view
    qic = QmlInstantCoding(view, verbose=True)
    # Add any source file (.qml and .js by default) in current working directory
    qic.addFilesFromDirectory(os.getcwd())

    view.show()
    app.exec_()

if __name__ == '__main__':
    main()
