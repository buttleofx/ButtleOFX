import logging
from PyQt5 import QtCore
from pyTuttle import tuttle
from .glviewport import GLViewport
from buttleofx.data import ButtleDataSingleton
from buttleofx.event import ButtleEventSingleton
from buttleofx.manager import ButtleManagerSingleton
# from .tuttleOverlayInteract import TuttleOverlayInteract


class GLViewport_tuttleofx(GLViewport):
    def __init__(self, parent=None):
        super(GLViewport_tuttleofx, self).__init__(parent)

        self.tuttleOverlay = None
        self.recomputeOverlay = False

        self._timeHasChanged = False
        self._time = 0
        self._frame = 0
        self._frameHasChanged = False

        self.connectToButtleEvent()

    # ######################################## Methods exposed to QML ####################################### #

    @QtCore.pyqtSlot()
    def unconnectToButtleEvent(self):
        buttleEvent = ButtleEventSingleton().get()
        # disconnect : load image when the viewer changed
        buttleEvent.viewerChangedSignal.disconnect(self.loadImage)
        # disconnect : load image when one param changed
        buttleEvent.oneParamChangedSignal.disconnect(self.loadImage)

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    # Frame management
    def getFrame(self):
        return self._frame

    # ## Setters ## #

    def setFrame(self, currentFrame):
        self._frameHasChanged = True
        self._frame = currentFrame
        self.loadImage()
        self.frameChanged.emit()
        self.update()

    # ## Others ## #

    def clearMapOfImageAlreadyCalculated(self):
        buttleData = ButtleDataSingleton().get()
        buttleData._mapNodeNameToComputedImage.clear()

    def connectToButtleEvent(self):
        buttleEvent = ButtleEventSingleton().get()
        # connect : load image when the viewer changed
        buttleEvent.viewerChangedSignal.connect(self.loadImage)
        # connect : load image when one param changed
        buttleEvent.oneParamChangedSignal.connect(self.loadImage)

    def internPaintGL(self):
        super(GLViewport_tuttleofx, self).internPaintGL()
        pixelScale = tuttle.OfxPointD()
        pixelScale.x = self.getScale()
        pixelScale.y = pixelScale.x
        if self.img_data is not None and self.tuttleOverlay:
            self.tuttleOverlay.draw(pixelScale)

    def loadImage(self):
        # print("glviewport_tuttleofx.loadImage")
        self.img_data = None
        self.tex = None

        try:
            self.loadImage_tuttle()
            # print('Tuttle img_data:', self.img_data)
        except Exception as e:
            logging.debug('Error while loading image file.\nError: "%s"' % str(e))
            self.img_data = None
            self.setImageBounds(QtCore.QRect())
            # raise

        if self._fittedModeValue:
            self.fitImage()

    def loadImage_tuttle(self):
        buttleManager = ButtleManagerSingleton().get()
        logging.debug("retrieveImage start")
        imgRes = buttleManager.getViewerManager().retrieveImage(self._frame, self._frameHasChanged)
        logging.debug("retrieveImage end")
        self._frameHasChanged = False
        self.img_data = imgRes.getNumpyArray()

        bounds = imgRes.getBounds()
        width = bounds.x2 - bounds.x1
        height = bounds.y2 - bounds.y1

        self.setImageBounds(QtCore.QRect(bounds.x1, bounds.y1, width, height))

    # ############################################# Data exposed to QML ############################################## #

    frameChanged = QtCore.pyqtSignal()
    frame = QtCore.pyqtProperty(int, getFrame, setFrame, notify=frameChanged)
