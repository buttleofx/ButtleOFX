import sys
sys.path.append("../..")

import os
from PySide import QtGui, QtDeclarative
from quickmamba.utils import QmlInstantCoding


def main():
    app = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

    # Create a declarative view
    view.setSource("source.qml")
    # Declare we are using instant coding tool on this view
    qic = QmlInstantCoding(view, verbose=True)
    # Add any source file (.qml and .js by default) in current working directory
    qic.addFilesFromDirectory(os.getcwd())

    view.show()
    app.exec_()

if __name__ == '__main__':
    main()
