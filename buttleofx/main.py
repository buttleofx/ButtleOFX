from PySide import QtGui, QtDeclarative, QtOpenGL
import os, sys
from OpenGL import GL

# data
from buttleofx.datas import ButtleData
#connections
from buttleofx.gui.graph.connection import LineItem
# undo_redo
from buttleofx.core.undo_redo.manageTools import CommandManager
# quickmamba
from quickmamba.utils import QmlInstantCoding

currentFilePath = os.path.dirname(os.path.abspath(__file__))


class ButtleApp(QtGui.QApplication):
    def __init__(self, argv):
        super(ButtleApp, self).__init__(argv)

    def notify(self, receiver, event):
        try:
            #print("QApp notify")
            return QtGui.QApplication.notify(self, receiver, event)
        except Exception as e:
            print("QApp notify exception: " + str(e))


def main(argv):
    # add new QML type
    QtDeclarative.qmlRegisterType(LineItem, "ConnectionLineItem", 1, 0, "ConnectionLine")

    # init undo_redo contexts
    cmdManager = CommandManager()
    cmdManager.setActive()
    cmdManager.clean()

    # create QApplication
    app = ButtleApp(argv)
    # create the declarative view
    view = QtDeclarative.QDeclarativeView()
    view.setViewport(QtOpenGL.QGLWidget())
    view.setViewportUpdateMode(QtDeclarative.QDeclarativeView.FullViewportUpdate)

    view.setWindowTitle("ButtleOFX")
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

    # data
    buttleData = ButtleData().init(view)

    # expose data to QML
    rc = view.rootContext()
    rc.setContextProperty("_buttleData", buttleData)

    # set the view
    view.setSource(os.path.join(currentFilePath, "MainWindow.qml"))

    # Declare we are using instant coding tool on this view
    qic = QmlInstantCoding(view, verbose=True)
    # Add any source file (.qml and .js by default) in current working directory
    qic.addFilesFromDirectory(os.getcwd(), recursive=True)

    view.show()
    app.exec_()
