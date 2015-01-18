'''
    # How to run browser_v2 in standalone mode ?
    copy/paste those lines to the run_buttleofx.sh

    ## Add QML2 env. var. to run browser_v2
    export QML2_IMPORT_PATH=$QT_DIR/qml

    ## Run browser_v2 in standalone mode
    $PYTHONHOME/bin/python $BUTTLE_TOP_DIR/ButtleOFX/buttleofx/gui/browser_v2/main.py

'''


import os
import sys

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtQuick
from PyQt5.QtQml import qmlRegisterType
from browserModel import BrowserModel


currentFilePath = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    view = QtQuick.QQuickView()
    rc = view.rootContext()


    # rc.setContextProperty("_browser", b)

    qmlRegisterType(BrowserModel, 'BrowserModel', 1, 0, 'BrowserModel')

#    view.setWindowTitle("Browser")
    qmlFilePath = os.path.join(currentFilePath, "Browser.qml")
#    print(qmlFilePath)
    view.setSource(QtCore.QUrl(qmlFilePath))
    view.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)

    view.show()
    app.exec_()
