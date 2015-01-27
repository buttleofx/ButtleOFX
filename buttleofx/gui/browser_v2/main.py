#! /usr/bin/env python3

'''
    # How to run browser_v2 in standalone mode ?
    copy/paste those lines to the run_buttleofx.sh

    ## Add QML2 env. var. to run browser_v2
    export QML2_IMPORT_PATH=$QT_DIR/qml

    ## Run browser_v2 in standalone mode (comment original run)
    $PYTHONHOME/bin/python $BUTTLE_TOP_DIR/ButtleOFX/buttleofx/gui/browser_v2/main.py

'''

import os
import sys
from PyQt5.QtQml import qmlRegisterType

from pyTuttle import tuttle
from buttleofx.gui.browser_v2.browserModel import BrowserModel
from buttleofx.gui.browser_v2.standaloneUtils import *
# To prevent drivers conflicts between Mesa-utils and NVIDIA drivers on Ubuntu
from OpenGL import GL
from pySequenceParser import sequenceParser

currentFilePath = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':

    tuttle.core().preload()
    b = sequenceParser.browse("/home/alex/Bureau/tmp/")
    b = BrowserModel(path="/home/alex/Bureau/tmp")
    for a in b.getItems():
        print(a.getPath(), a.getWeightFormatted())
    app = QtWidgets.QApplication(sys.argv)
    engine = QtQml.QQmlEngine(app)
    engine.quit.connect(app.quit)
    engine.addImageProvider("buttleofx", ImageProvider())

    view = QtQuick.QQuickView(engine, None)
    rc = view.rootContext()

    qmlRegisterType(BrowserModel, 'BrowserModel', 1, 0, 'BrowserModel')
    qmlFilePath = os.path.join(currentFilePath, "qml/Browser.qml")

    view.setSource(QtCore.QUrl(qmlFilePath))
    view.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)

    view.show()
    app.exec_()
