import os, sys
from OpenGL import GL
# PySide
from PySide import QtGui, QtDeclarative, QtOpenGL, QtCore

# Logging (see console.log)
import logging
# fix thow to display our info
    # from the lowest to the highest level : DEBUG - INFO - WARNING - ERROR - CRITICAL (default = WARNING)
    # to use it :
        # logging.debug("debug message")
        # logging.info("info message")
        # logging.warning("warning message")
        # logging.error("error message")
        # logging.critical("critical message")
# print in a file
logging.basicConfig(format='Buttle - %(levelname)s - %(message)s', filename='console.log', filemode='w', level=logging.DEBUG)
# print in console
#logging.basicConfig(format='Buttle - %(levelname)s - %(message)s', level=logging.DEBUG)

# Tuttle
from pyTuttle import tuttle
# quickmamba
from quickmamba.models import QObjectListModel
from quickmamba.utils import QmlInstantCoding
# PyCheck
#import pychecker.checker

# for glViewport
tuttleofx_installed = False
try:
    import pyTuttle
    tuttleofx_installed = True
    logging.debug('Use TuttleOFX.')
except:
    logging.debug('TuttleFX not installed, use Python Image Library instead.')

if tuttleofx_installed:
    from buttleofx.gui.viewerGL.glviewport_tuttleofx import GLViewport_tuttleofx
else:
    from buttleofx.gui.viewerGL.glviewport_pil import GLViewport_pil

# data
from buttleofx.data import ButtleDataSingleton
# manager
from buttleofx.manager import ButtleManagerSingleton
# event
from buttleofx.event import ButtleEventSingleton
# new QML type
from buttleofx.gui.paramEditor import Finder
# undo_redo
from buttleofx.core.undo_redo.manageTools import CommandManager


currentFilePath = os.path.dirname(os.path.abspath(__file__))


class ButtleApp(QtGui.QApplication):
    def __init__(self, argv):
        super(ButtleApp, self).__init__(argv)

    def notify(self, receiver, event):
        try:
            #logging.info("QApp notify")
            return QtGui.QApplication.notify(self, receiver, event)
        except Exception as e:
            logging.exception("QApp notify exception: " + str(e))
            import traceback
            traceback.print_exc()
            return False


def main(argv):

    #preload Tuttle
    tuttle.core().preload()

    # add new QML type
    QtDeclarative.qmlRegisterType(Finder, "FolderListViewItem", 1, 0, "FolderListView")
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
    buttleData = ButtleDataSingleton().get().init(view, currentFilePath)
    # manager
    buttleManager = ButtleManagerSingleton().get().init()
    # event
    buttleEvent = ButtleEventSingleton().get()


    # expose data to QML
    rc = view.rootContext()
    rc.setContextProperty("_buttleApp", app)
    rc.setContextProperty("_buttleData", buttleData)
    rc.setContextProperty("_buttleManager", buttleManager)
    rc.setContextProperty("_buttleEvent", buttleEvent)

    # set the view
    view.setSource(os.path.join(currentFilePath, "MainWindow.qml"))
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
    view.setWindowTitle("ButtleOFX")
    view.setWindowIcon(QtGui.QIcon("blackMosquito.png"))
    view.setWindowIconText("ButtleOFX")

    # Declare we are using instant coding tool on this view
    qic = QmlInstantCoding(view, verbose=True)
    # Add any source file (.qml and .js by default) in current working directory
    qic.addFilesFromDirectory(os.getcwd(), recursive=True)

    view.show()
    app.exec_()

