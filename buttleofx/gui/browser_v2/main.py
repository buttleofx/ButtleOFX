'''
    # How to run browser_v2 in standalone mode ?
    copy/paste those lines to the run_buttleofx.sh

    ## Add QML2 env. var. to run browser_v2
    export QML2_IMPORT_PATH=$QT_DIR/qml

    ## Run browser_v2 in standalone mode (remove the )
    $PYTHONHOME/bin/python $BUTTLE_TOP_DIR/ButtleOFX/buttleofx/gui/browser_v2/main.py

'''


import os
import sys

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtQuick
from PyQt5.QtQml import qmlRegisterType


class Browser(QtCore.QObject):

    def __init__(self, parent=None):
        super(Browser, self).__init__(parent)
        self._title = "Browser standalone"
        self._counter = 0

    @QtCore.pyqtSlot()
    def greeting(self, name="world!"):
        print("Hello " + name)

    # Expose property to QML
    def getTitle(self):
        return self._title

    def setTitle(self, title):
        self._title = title
        print("Plop")
        self.titleChange.emit()

    titleChange = QtCore.pyqtSignal()
    title = QtCore.pyqtProperty(str, getTitle, setTitle, notify=titleChange)





currentFilePath = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    view = QtQuick.QQuickView()
    rc = view.rootContext()

    b = Browser()
    rc.setContextProperty("_browser", b)

    qmlRegisterType(Browser, 'Browser', 1, 0, 'Browser')

#    view.setWindowTitle("Browser")
    qmlFilePath = os.path.join(currentFilePath, "Browser.qml")
#    print(qmlFilePath)
    view.setSource(QtCore.QUrl(qmlFilePath))
    view.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)

    view.show()
    app.exec_()
