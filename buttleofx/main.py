import os
import sys
import logging

DEV_MODE = os.environ.get("BUTTLEOFX_DEV", False)

logFormat = 'Buttle - %(levelname)s - %(message)s'
if DEV_MODE:
    # Print in console
    logging.basicConfig(format=logFormat, level=logging.DEBUG)
else:
    # Need to set a global level, to allow to use
    # multiple log levels in multiple output handlers.
    logging.getLogger().setLevel(logging.DEBUG)

    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.WARNING)
    fileFormatter = logging.Formatter(logFormat)
    streamHandler.setFormatter(fileFormatter)
    logging.getLogger().addHandler(streamHandler)

    fileHandler = logging.FileHandler('buttle.log')
    fileHandler.setLevel(logging.DEBUG)
    fileFormatter = logging.Formatter('Buttle - %(levelname)s - %(asctime)-15s - %(message)s')
    fileHandler.setFormatter(fileFormatter)
    logging.getLogger().addHandler(fileHandler)


import numpy
import signal
import argparse

from quickmamba.utils import instantcoding

from buttleofx.data import Finder
from buttleofx.gui.viewer import TimerPlayer
from buttleofx.data import globalButtleData
from buttleofx.event import globalButtleEvent
from buttleofx.manager import globalButtleManager
from buttleofx.core.undo_redo.manageTools import globalCommandManager
from buttleofx.gui.browser.browserModel import BrowserModel, globalBrowser, globalBrowserDialog
from buttleofx.gui.browser.actions.browserAction import globalBrowserAction, globalBrowserActionDialog
from buttleofx.gui.browser.actions.browserAction import globalActionManager

from PyQt5 import QtCore, QtGui, QtQml, QtQuick, QtWidgets

# For glViewport
tuttleofx_installed = False
try:
    from pyTuttle import tuttle
    tuttleofx_installed = True
    logging.debug('Use TuttleOFX.')
    # if DEV_MODE:
    tuttle.core().getFormatter().setLogLevel_int(0)
except Exception as e:
    logging.debug(str(e))
    logging.debug('TuttleFX not installed, use Python Image Library instead.')

if tuttleofx_installed:
    from buttleofx.gui.viewerGL.glviewport_tuttleofx import GLViewport_tuttleofx as GLViewportImpl
else:
    from buttleofx.gui.viewerGL.glviewport_pil import GLViewport_pil as GLViewportImpl


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

# Make sure that SIGINTs actually stop the application event loop (Qt sometimes
# swallows KeyboardInterrupt exceptions):
signal.signal(signal.SIGINT, signal.SIG_DFL)


class EventFilter(QtCore.QObject):
    def __init__(self, app, engine):
        QtCore.QObject.__init__(self)
        self.mainApp = app
        self.mainEngine = engine
        self.buttleData = globalButtleData

    def onSaveDialogButtonClicked(self, fileToSave):
        self.buttleData.urlOfFileToSave = fileToSave
        self.buttleData.saveData(QtCore.QUrl(self.buttleData.urlOfFileToSave))
        QtCore.QCoreApplication.quit()

    def onExitDialogDiscardButtonClicked(self):
        QtCore.QCoreApplication.quit()

    def onExitDialogSaveButtonClicked(self):
        if self.buttleData.urlOfFileToSave:
            self.buttleData.saveData(self.buttleData.urlOfFileToSave)
            QtCore.QCoreApplication.quit()
        else:
            saveDialogComponent = QtQml.QQmlComponent(self.mainEngine)
            saveDialogComponent.loadUrl(QtCore.QUrl(os.path.dirname(os.path.abspath(__file__)) + '/gui/dialogs/BrowserSaveDialog.qml'))
            saveDialog = saveDialogComponent.create()
            saveDialog.saveButtonClicked.connect(self.onSaveDialogButtonClicked)
            saveDialog.show()

    def eventFilter(self, receiver, event):
        if event.type() == QtCore.QEvent.KeyPress:
            # If Alt F4 event ignored
            if event.modifiers() == QtCore.Qt.AltModifier and event.key() == QtCore.Qt.Key_F4:
                event.ignore()
        if event.type() != QtCore.QEvent.Close:
            return QtCore.QObject.eventFilter(self, receiver, event)
        if not isinstance(receiver, QtQuick.QQuickWindow) or not receiver.title() == "ButtleOFX":
            return False

        if not self.buttleData.graphCanBeSaved:
            return False

        exitDialogComponent = QtQml.QQmlComponent(self.mainEngine)
        exitDialogComponent.loadUrl(QtCore.QUrl(os.path.dirname(os.path.abspath(__file__)) + '/gui/dialogs/ExitDialog.qml'))
        exitDialog = exitDialogComponent.create()
        exitDialog.saveButtonClicked.connect(self.onExitDialogSaveButtonClicked)
        exitDialog.discardButtonClicked.connect(self.onExitDialogDiscardButtonClicked)
        exitDialog.show()

        # Don't call the parent class, so we don't close the application
        return True


class ButtleApp(QtWidgets.QApplication):
    def __init__(self, argv):
        QtWidgets.QApplication.__init__(self, argv)

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
                qim = QtGui.QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QtGui.QImage.Format_RGB888)
                return qim
            elif im.shape[2] == 4:
                qim = QtGui.QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QtGui.QImage.Format_RGBA8888) #Format_RGBA32))
                return qim

    raise ValueError("toQImage: case not implemented.")

# For debug purposes
count_thumbnail = 0


class TuttleImageProvider(QtQuick.QQuickImageProvider):
    def __init__(self):
        logging.debug("TuttleImageProvider constructor")
        QtQuick.QQuickImageProvider.__init__(self, QtQuick.QQuickImageProvider.Image)
        self.thumbnailCache = tuttle.ThumbnailDiskCache()
        self.thumbnailCache.setRootDir(os.path.join(tuttle.core().getPreferences().getTuttleHomeStr(),
                                                    "thumbnails_cache"))

    def requestImage(self, idImg, size):
        """
        Compute the image using TuttleOFX: old way. Now the thumbnail build is wrapped inside a python process
        """
        logging.debug("TuttleImageProvider: file='%s'", idImg)
        try:
            img = self.thumbnailCache.getThumbnail(idImg)
            numpyImage = img.getNumpyArray()

            # Convert numpyImage to QImage
            qtImage = toQImage(numpyImage)

            # For debug purposes:
            # global count_thumbnail
            # qtImage.save("/tmp/buttle/thumbnail_{0}.png".format(str(count_thumbnail)))
            # count_thumbnail += 1

            return qtImage.copy(), qtImage.size()
        except Exception as e:
            logging.debug("TuttleImageProvider: file='{file}' => error: {error}".format(file=idImg, error=str(e)))
            qtImage = QtGui.QImage()
            return qtImage, qtImage.size()


def main(argv, app):

    # Preload Tuttle
    # Don't use the Plugin cache, to avoid multithreading troubles.
    tuttle.core().preload(False)

    # Give to QML acces to TimerPlayer defined in buttleofx/gui/viewer
    QtQml.qmlRegisterType(TimerPlayer, "TimerPlayer", 1, 0, "TimerPlayer")
    # Give to QML access to BrowserModel defined in buttleofx/gui/browser
    QtQml.qmlRegisterType(BrowserModel, "BrowserModel", 1, 0, "BrowserModel")
    # Add new QML type
    QtQml.qmlRegisterType(Finder, "FolderListViewItem", 1, 0, "FolderListView")

    QtQml.qmlRegisterType(GLViewportImpl, "Viewport", 1, 0, "GLViewport")

    # Init undo_redo contexts
    cmdManager = globalCommandManager
    cmdManager.setActive()
    cmdManager.clean()

    # Create the QML engine
    engine = QtQml.QQmlEngine(app)
    engine.quit.connect(app.quit)
    engine.addImageProvider("buttleofx", TuttleImageProvider())

    # Data
    globalButtleData.init(engine, currentFilePath)
    # Manager
    buttleManager = globalButtleManager.init()

    parser = argparse.ArgumentParser(description=('A command line to execute ButtleOFX, an opensource compositing '
                                                  'software. If you pass a folder as an argument, ButtleOFX will '
                                                  'start at this path.'))
    parser.add_argument('folder', nargs='?', help='Folder to browse')
    args = parser.parse_args()

    globalBrowser.setCurrentPath(os.path.abspath(args.folder) if args.folder else globalBrowser.getHomePath())
    # Expose data to QML
    rc = engine.rootContext()
    rc.setContextProperty("_buttleApp", app)
    rc.setContextProperty("_buttleData", globalButtleData)
    rc.setContextProperty("_buttleManager", buttleManager)
    rc.setContextProperty("_buttleEvent", globalButtleEvent)
    rc.setContextProperty("_browser", globalBrowser)
    rc.setContextProperty("_browserDialog", globalBrowserDialog)
    rc.setContextProperty("_browserAction", globalBrowserAction)
    rc.setContextProperty("_browserActionDialog", globalBrowserActionDialog)
    rc.setContextProperty("_actionManager", globalActionManager)

    iconPath = os.path.join(currentFilePath, "../blackMosquito.png")
    # iconPath = QtCore.QUrl("file:///" + iconPath)
    app.setWindowIcon(QtGui.QIcon(iconPath))

    mainFilepath = os.path.join(currentFilePath, "MainWindow.qml")
    if windows:
        mainFilepath = mainFilepath.replace('\\', '/')

    component = QtQml.QQmlComponent(engine)
    qmlFile = QtCore.QUrl("file:///" + mainFilepath)
    component.loadUrl(qmlFile)
    topLevelItem = component.create()
    # engine.load(QtCore.QUrl("file:///" + mainFilepath))
    # topLevelItem = engine.rootObjects()[0]

    if not topLevelItem:
        logging.error("Errors while loading QML file:")

        for error in component.errors():
            logging.error(error.toString())
        return -1
    topLevelItem.setIcon(QtGui.QIcon(iconPath))

    if DEV_MODE:
        # Declare we are using instant coding tool on this view
        qic = instantcoding.QmlInstantCoding(
            engine,
            instantcoding.ReloadComponent(qmlFile, component, topLevelItem),
            verbose=True)
        # qic = instantcoding.QmlInstantCoding(engine, instantcoding.AskQmlItemToReload(topLevelItem), verbose=True)

        # Add any source file (.qml and .js by default) in current working directory
        parentDir = os.path.dirname(currentFilePath)
        logging.debug("Watch directory: %s", parentDir)
        qic.addFilesFromDirectory(parentDir, recursive=True)

    aFilter = EventFilter(app, engine)
    app.installEventFilter(aFilter)

    globalBrowser.loadData()
    globalBrowserDialog.loadData()

    with globalActionManager:
        topLevelItem.show()
        exitCode = app.exec_()
        sys.exit(exitCode)