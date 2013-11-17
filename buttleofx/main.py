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
logging.basicConfig(format='Buttle - %(levelname)s - %(asctime)-15s - %(message)s', filename='console.log', filemode='w', level=logging.DEBUG)
# print in console
#logging.basicConfig(format='Buttle - %(levelname)s - %(message)s', level=logging.DEBUG)

# Tuttle
from pyTuttle import tuttle
# quickmamba
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
from buttleofx.data import Finder
#TimerPlayer
from buttleofx.gui.viewer import TimerPlayer
# undo_redo
from buttleofx.core.undo_redo.manageTools import CommandManager
# Menu
from buttleofx.gui.graph.menu import MenuWrapper

# PyQt5
from PyQt5 import QtCore, QtGui, QtQml

import os


# Path of this file
currentFilePath = os.path.dirname(os.path.abspath(__file__))


class ButtleApp(QtGui.QGuiApplication):
    def __init__(self, argv):
        super(ButtleApp, self).__init__(argv)

#    def notify(self, receiver, event):
#        try:
#            logging.info("QApp notify")
#            return super(ButtleApp, self).notify(receiver, event)
#        except Exception as e:
#            logging.exception("QApp notify exception: " + str(e))
#            import traceback
#            traceback.print_exc()
#            return False


def main(argv, app):

    #preload Tuttle
    tuttle.core().preload()

    # give to QML acces to TimerPlayer defined in buttleofx/gui/viewer
    QtQml.qmlRegisterType(TimerPlayer, "TimerPlayer", 1, 0, "TimerPlayer")
    # add new QML type
    QtQml.qmlRegisterType(Finder, "FolderListViewItem", 1, 0, "FolderListView")
    if tuttleofx_installed:
        QtQml.qmlRegisterType(GLViewport_tuttleofx, "Viewport", 1, 0, "GLViewport")
    else:
        QtQml.qmlRegisterType(GLViewport_pil, "Viewport", 1, 0, "GLViewport")

    # init undo_redo contexts
    cmdManager = CommandManager()
    cmdManager.setActive()
    cmdManager.clean()

    # create the declarative view
    engine = QtQml.QQmlEngine(app)
    #view = QtQuick.QQuickView()
    #view.setViewport(QtOpenGL.QGLWidget())
    #view.setViewportUpdateMode(QtQml.QQuickView.FullViewportUpdate)

    # data
    buttleData = ButtleDataSingleton().get().init(engine, currentFilePath)
    # manager
    buttleManager = ButtleManagerSingleton().get().init()
    # event
    buttleEvent = ButtleEventSingleton().get()
    # Menus
    #fileMenu = MenuWrapper("file", 0, component, app)
    #editMenu = MenuWrapper("edit", 0, view, app)
    #addMenu = MenuWrapper("buttle/", 1, view, app)

    # expose data to QML
    rc = engine.rootContext()
    rc.setContextProperty("_buttleApp", app)
    rc.setContextProperty("_buttleData", buttleData)
    rc.setContextProperty("_buttleManager", buttleManager)
    rc.setContextProperty("_buttleEvent", buttleEvent)
    #rc.setContextProperty("_fileMenu", fileMenu)
    #rc.setContextProperty("_editMenu", editMenu)
    #rc.setContextProperty("_addMenu", addMenu)

    mainFilepath = os.path.join(currentFilePath, "MainWindow.qml")
    component = QtQml.QQmlComponent(engine)
    component.loadUrl(QtCore.QUrl(mainFilepath))

    topLevel = component.create()
#    topLevel = component.beginCreate(rc)
#    component.completeCreate()
#    print("Component errors:", component.errors())

    # Declare we are using instant coding tool on this view
    qic = QmlInstantCoding(component, verbose=True)

    # Add any source file (.qml and .js by default) in current working directory
    parentDir = os.path.dirname(currentFilePath)
    print("Watch directory:", parentDir)
    qic.addFilesFromDirectory(parentDir, recursive=True)

    #add._menu.popup(view.mapToGlobal(QtCore.QPoint(0, 0)))

    if topLevel is not None:
        topLevel.show()
    else:
        print("ERRORS")
        # Print all errors that occurred.
        for error in component.errors():
            print(error.toString())

