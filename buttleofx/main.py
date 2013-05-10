import os
# PySide
from PySide import QtGui, QtDeclarative, QtOpenGL

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
# undo_redo
from buttleofx.core.undo_redo.manageTools import CommandManager
# Menu
from buttleofx.gui.graph.menu import MenuWrapper

# Path of this file
currentFilePath = os.path.dirname(os.path.abspath(__file__))

from PySide import QtCore
from PySide.QtCore import *
from PySide.QtGui import *
#import shiboken

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

    # Preload Tuttle
    tuttle.core().preload()

    # init undo_redo contexts
    cmdManager = CommandManager()
    cmdManager.setActive()
    cmdManager.clean()

    # data
    buttleData = ButtleDataSingleton().get()
    # manager
    buttleManager = ButtleManagerSingleton().get().init()
    # event
    buttleEvent = ButtleEventSingleton().get()


    QApplication.setGraphicsSystem("opengl")
    # Create QApplication
    app = ButtleApp(argv)

    # Create QDDeclarativeEngine and QDeclarativeComonent
    engine = QtDeclarative.QDeclarativeEngine(app)

    # add new QML type
    QtDeclarative.qmlRegisterType(Finder, "FolderListViewItem", 1, 0, "FolderListView")
    if tuttleofx_installed:
        QtDeclarative.qmlRegisterType(GLViewport_tuttleofx, "Viewport", 1, 0, "GLViewport")
    else:
        QtDeclarative.qmlRegisterType(GLViewport_pil, "Viewport", 1, 0, "GLViewport")

    # Set context
    rc = engine.rootContext()
    rc.setContextProperty("_buttleApp", app)
    rc.setContextProperty("_buttleData", buttleData)
    rc.setContextProperty("_buttleManager", buttleManager)
    rc.setContextProperty("_buttleEvent", buttleEvent)

    component = QtDeclarative.QDeclarativeComponent(engine, QUrl.fromLocalFile(os.path.join(currentFilePath, "MainWindow.qml")))
    print "A:", component.errors()
    myObject = component.beginCreate(rc)
    print "B:", component.errors()
    buttleData.init(myObject, currentFilePath)
    component.completeCreate()
    print "C:", component.errors()
    #myObject = component.create()


    # expose data to QML
    # rc = engine.rootContext()
    # rc.setContextProperty("_buttleApp", app)
    # rc.setContextProperty("_buttleData", buttleData)
    # rc.setContextProperty("_buttleManager", buttleManager)
    # rc.setContextProperty("_buttleEvent", buttleEvent)
    # # rc.setContextProperty("_fileMenu", fileMenu)
    # # rc.setContextProperty("_editMenu", editMenu)
    # # rc.setContextProperty("_renderMenu", renderMenu)
    # # rc.setContextProperty("_windowMenu", windowMenu)
    # # rc.setContextProperty("_helpMenu", helpMenu)
    # # rc.setContextProperty("_addMenu", addMenu)


    # Declare we are using instant coding tool on this view
    #qic = QmlInstantCoding(engine, verbose=True)

    # Add any source file (.qml and .js by default) in current working directory
    #qic.addFilesFromDirectory(os.getcwd(), recursive=True)

    #add._menu.popup(view.mapToGlobal(QtCore.QPoint(0, 0)))

#    # create the declarative view
#    view = QtDeclarative.QDeclarativeView()
#    view.setViewport(QtOpenGL.QGLWidget())
#    view.setViewportUpdateMode(QtDeclarative.QDeclarativeView.FullViewportUpdate)

#    scene = QtGui.QGraphicsScene()
#    componentPtr = long(shiboken.getCppPointer(component)[0])
#    item = shiboken.wrapInstance(componentPtr, QtGui.QGraphicsItem)
#    item.setPos(10,500)
#    scene.addItem(item)
#    view.setScene(scene)
#    view.show()
#    view.resize(1024, 2000)

    app.exec_()
