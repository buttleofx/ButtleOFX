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
#logging.basicConfig(format='Buttle - %(levelname)s - %(asctime)-15s - %(message)s', filename='console.log', filemode='w', level=logging.DEBUG)
# print in console
logging.basicConfig(format='Buttle - %(levelname)s - %(message)s', level=logging.DEBUG)

# Tuttle
from pyTuttle import tuttle
import getBestPlugin
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
    from buttleofx.gui.viewerGL.glviewport_tuttleofx import GLViewport_tuttleofx as GLViewportImpl
else:
    from buttleofx.gui.viewerGL.glviewport_pil import GLViewport_pil as GLViewportImpl

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
#FileModelBrowser
from buttleofx.gui.browser import FileModelBrowser,FileModelBrowserSingleton
# undo_redo
from buttleofx.core.undo_redo.manageTools import CommandManager
# Menu
from buttleofx.gui.graph.menu import MenuWrapper

# PyQt5
from PyQt5 import QtCore, QtGui, QtQml, QtQuick, QtWidgets
from PyQt5.QtWidgets import QWidget, QFileDialog, QApplication, QMessageBox

import numpy

import argparse
import os
import sys

osname = os.name.lower()
sysplatform = sys.platform.lower()
windows = osname == "nt" and sysplatform.startswith("win")
macos = sysplatform.startswith("darwin")
linux = not windows and not macos
unix = not windows

# Path of this file
currentFilePath = os.path.dirname(os.path.abspath(__file__))
if windows:
    currentFilePath = currentFilePath.replace("\\", "/")


class EventFilter(QtCore.QObject):
    def eventFilter(self, receiver, event):
        buttleData = ButtleDataSingleton().get()
        browser = FileModelBrowserSingleton().get()
        if event.type() == QtCore.QEvent.KeyPress :
            # if alt f4 event ignored
            if event.modifiers() == QtCore.Qt.AltModifier and event.key() == QtCore.Qt.Key_F4 :
                event.ignore()
        if event.type() != QtCore.QEvent.Close :
            return super(EventFilter,self).eventFilter(receiver, event)
        if not isinstance(receiver,QtQuick.QQuickWindow) or not receiver.title() =="ButtleOFX" :
            return False
        if not buttleData.graphCanBeSaved :
            return False
        msgBox = QMessageBox()
        msgBox.setText("The graph has been modified.")
        msgBox.setModal(True)
        msgBox.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        msgBox.setInformativeText("Do you want to save your changes?")
        msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Abort)
        msgBox.setDefaultButton(QMessageBox.Save)
        ret = msgBox.exec_()
        if ret == QMessageBox.Save:
            if buttleData.urlOfFileToSave:
                # Save on the already existing file
                buttleData.saveData(buttleData.urlOfFileToSave)
                # Close the application
                return super(EventFilter,self).eventFilter(receiver, event)
            # This project has never been saved, so ask the user on which file to save.
            dialog = QFileDialog()
            fileToSave = dialog.getSaveFileName(None, "Save the graph", browser.getFirstFolder())[0]
            if not (fileToSave.endswith(".bofx")):
                fileToSave += ".bofx"
            buttleData.urlOfFileToSave = fileToSave
            buttleData.saveData(fileToSave)
            # Close the application
            return super(EventFilter,self).eventFilter(receiver, event)
        if ret == QMessageBox.Discard :
            # Close the application
            return super(EventFilter,self).eventFilter(receiver, event)
        # Don't call the parent class, so we don't close the application
        return True


class ButtleApp(QtWidgets.QApplication):
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


gray_color_table = [QtGui.qRgb(i, i, i) for i in range(256)]

def toQImage(im):
    if im is None:
        return QtGui.QImage()

    if im.dtype == numpy.uint8:
        if len(im.shape) == 2:
            qim = QtGui.QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QtGui.QImage.Format_Indexed8)
            qim.setColorTable(gray_color_table)
            return qim

        elif len(im.shape) == 3:
            if im.shape[2] == 3:
                qim = QtGui.QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QtGui.QImage.Format_RGB888);
                return qim
            elif im.shape[2] == 4:
                qim = QtGui.QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QtGui.QImage.Format_ARGB32);
                return qim

    raise ValueError("toQImage: case not implemented.")


class ImageProvider(QtQuick.QQuickImageProvider):
    def __init__(self):
        QtQuick.QQuickImageProvider.__init__(self, QtQuick.QQuickImageProvider.Image)

    def requestImage(self, id, size):
        # print('requestImage:', 'id: ', id)
        max_size = 200
        try:
            (_, extension) = os.path.splitext(id)
            readerIdentifier = getBestPlugin.getBestReader(extension)
        except Exception as e:
            # print("Tuttle ImageProvider: Unsupported extension '%s'" % extension, str(e))
            # import traceback
            # traceback.print_exc()
            qtImage = QtGui.QImage(max_size, max_size, QtGui.QImage.Format_RGB32)
            qtImage.fill(QtGui.QColor("green"))
            return qtImage, qtImage.size()
        
        try:
            # compute image using TuttleOFX
            outputCache = tuttle.MemoryCache()
            tuttle.compute(
                outputCache,
                [
                    tuttle.NodeInit(readerIdentifier, filename=id, bitDepth="8i"),
                    tuttle.NodeInit("tuttle.resize", keepRatio=True, size=(max_size, max_size)),
                    # tuttle.NodeInit("tuttle.jpegwriter", filename="/tmp/buttleofx_test_thumbnail.jpg"),
                ])
            
            # retrieve graph output
            imgRes = outputCache.get(0)
            numpyImage = imgRes.getNumpyArray()
            
            # convert numpyImage to QImage
            # qtImage = numpy2qimage(numpyImage)
            qtImage = toQImage(numpyImage)
            
            return qtImage, qtImage.size()
        
        except Exception as e:
            print("Error Tuttle ImageProvider: ", str(e))
            # import traceback
            # traceback.print_exc()
            qtImage = QtGui.QImage(max_size, max_size,QtGui.QImage.Format_RGB32)
            qtImage.fill(QtGui.QColor("red"))
            return qtImage, qtImage.size()
    

def main(argv, app):

    #preload Tuttle
    tuttle.core().preload()

    # give to QML acces to TimerPlayer defined in buttleofx/gui/viewer
    QtQml.qmlRegisterType(TimerPlayer, "TimerPlayer", 1, 0, "TimerPlayer")
    # give to QML access to FileModelBrowser defined in buttleofx/gui/browser
    QtQml.qmlRegisterType(FileModelBrowser, "ButtleFileModel", 1, 0, "FileModelBrowser")
    # add new QML type
    QtQml.qmlRegisterType(Finder, "FolderListViewItem", 1, 0, "FolderListView")
    
    QtQml.qmlRegisterType(GLViewportImpl, "Viewport", 1, 0, "GLViewport")

    # init undo_redo contexts
    cmdManager = CommandManager()
    cmdManager.setActive()
    cmdManager.clean()

    # create the declarative view
    engine = QtQml.QQmlEngine(app)
    engine.quit.connect(app.quit)
    #view = QtQuick.QQuickView()
    #view.setViewport(QtOpenGL.QGLWidget())
    #view.setViewportUpdateMode(QtQml.QQuickView.FullViewportUpdate)
    
    engine.addImageProvider("buttleofx", ImageProvider())
    #ImageProviderGUI()

    # data
    buttleData = ButtleDataSingleton().get().init(engine, currentFilePath)
    # manager
    buttleManager = ButtleManagerSingleton().get().init()
    # event
    buttleEvent = ButtleEventSingleton().get()
    #fileModelBrowser
    browser = FileModelBrowserSingleton().get()
    
    parser = argparse.ArgumentParser(description='A command line to execute ButtleOFX, an opensource compositing software. If you pass a folder as an argument, ButtleOFX will start at this path.')
    parser.add_argument('folder', nargs='?', help='Folder to browse')
    args = parser.parse_args()
    if args.folder:
        inputFolder = os.path.abspath(args.folder)
        browser.setFirstFolder(inputFolder)
    else:
        inputFolder = os.path.expanduser("~")
        browser.setFirstFolder(inputFolder)

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
    rc.setContextProperty("_browser", browser)
    #rc.setContextProperty("_fileMenu", fileMenu)
    #rc.setContextProperty("_editMenu", editMenu)
    #rc.setContextProperty("_addMenu", addMenu)

    mainFilepath = os.path.join(currentFilePath, "MainWindow.qml")
    if windows:
      mainFilepath = mainFilepath.replace('\\', '/')
    component = QtQml.QQmlComponent(engine)
    component.loadUrl(QtCore.QUrl("file:///" + mainFilepath))

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
        topLevel.setIcon(QtGui.QIcon(os.path.join(currentFilePath, "../blackMosquito.png")))
        topLevel.show()

    else:
        print("ERRORS")
        # Print all errors that occurred.
        for error in component.errors():
            print(error.toString())

    aFilter = EventFilter()
    app.installEventFilter(aFilter)
    sys.exit(app.exec_())
