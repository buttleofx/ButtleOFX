from pyTuttle import tuttle

from PySide import QtGui, QtDeclarative, QtOpenGL, QtCore
import os, sys
from OpenGL import GL

from quickmamba.models import QObjectListModel

# for glViewport
tuttleofx_installed = False
try:
    import pyTuttle
    tuttleofx_installed = True
    print('Use TuttleOFX.')
except:
    print('TuttleFX not installed, use Python Image Library instead.')

if tuttleofx_installed:
    from buttleofx.gui.viewerGL.glviewport_tuttleofx import GLViewport_tuttleofx
else:
    from buttleofx.gui.viewerGL.glviewport_pil import GLViewport_pil


# data
from buttleofx.data import ButtleData
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
            import traceback
            traceback.print_exc()
            return False


def main(argv):

    #preload Tuttle
    tuttle.core().preload()

    # add new QML type
    QtDeclarative.qmlRegisterType(LineItem, "ConnectionLineItem", 1, 0, "ConnectionLine")
    if tuttleofx_installed:
        QtDeclarative.qmlRegisterType(GLViewport_tuttleofx, "Viewport", 1, 0, "GLViewport")
    else:
        QtDeclarative.qmlRegisterType(GLViewport_pil, "Viewport", 1, 0, "GLViewport")

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

    # data
    buttleData = ButtleData().init(view)

    # expose data to QML
    rc = view.rootContext()
    rc.setContextProperty("_buttleData", buttleData)
    rc.setContextProperty("_buttleApp", app)

    # set the view
    view.setSource(os.path.join(currentFilePath, "MainWindow.qml"))
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
    view.setWindowTitle("ButtleOFX")

    # Declare we are using instant coding tool on this view
    qic = QmlInstantCoding(view, verbose=True)
    # Add any source file (.qml and .js by default) in current working directory
    qic.addFilesFromDirectory(os.getcwd(), recursive=True)

    view.show()
    app.exec_()
