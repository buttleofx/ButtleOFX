from PySide import QtCore
# tuttle
from pyTuttle import tuttle
# for the viewer
from tuttleOverlayInteract import TuttleOverlayInteract
from glviewport import GLViewport
# data
from buttleofx.data import ButtleDataSingleton
# manager 
from buttleofx.manager import ButtleManagerSingleton
# event 
from buttleofx.event import ButtleEventSingleton


class GLViewport_tuttleofx(GLViewport):
    def __init__(self, parent=None):
        super(GLViewport_tuttleofx, self).__init__(parent)

        self.tuttleOverlay = None
        self.recomputeOverlay = False

        self._timeHasChanged = False
        self._time = 0
        self._frame = 0
        self._frameHasChanged = False

        self.connectToButtleData()

    def connectToButtleData(self):
        # connect viewerChanged to load image
        buttleEvent = ButtleEventSingleton().get()
        buttleEvent.viewerChangedSignal.connect(self.loadImage)
        # connect paramChanged to clearMap and load image
        buttleEvent.paramChangedSignal.connect(self.clearMapOfImageAlreadyCalculated)
        buttleEvent.paramChangedSignal.connect(self.loadImage)

    @QtCore.Slot()
    def unconnectToButtleData(self):
        # connct viewerChanged to load image
        buttleEvent = ButtleEventSingleton().get()
        buttleEvent.viewerChangedSignal.disconnect(self.loadImage)
        # connect paramChanged to clearMap and load image
        buttleEvent.paramChangedSignal.disconnect(self.clearMapOfImageAlreadyCalculated)
        buttleEvent.paramChangedSignal.disconnect(self.loadImage)

    def loadImage_tuttle(self):
        print "--------------------------------- loadImage_tuttle ---------------------------"
        buttleManager = ButtleManagerSingleton().get()
        #imgRes = buttleManager.getViewerManager().computeNode(self._time)

        imgRes = buttleManager.getViewerManager().retrieveImage(self._frame, self._frameHasChanged)
        self._frameHasChanged = False

        self.img_data = imgRes.getNumpyArray()

        bounds = imgRes.getBounds()

        width = bounds.x2 - bounds.x1
        height = bounds.y2 - bounds.y1

        self.setImageBounds(QtCore.QRect(bounds.x1, bounds.y1, width, height))

    def loadImage(self):
        self.img_data = None
        self.tex = None

        try:
            self.loadImage_tuttle()
            print('Tuttle img_data:', self.img_data)
        except:
            print 'Error while loading image file '
            self.img_data = None
            self.setImageBounds(QtCore.QRect())
            #raise

        if self._fittedModeValue:
            self.fitImage()

    def clearMapOfImageAlreadyCalculated(self):
        buttleData = ButtleDataSingleton().get()
        buttleData._mapNodeNameToComputedImage.clear()

    def internPaintGL(self, widget):
        super(GLViewport_tuttleofx, self).internPaintGL(widget)
        pixelScale = tuttle.OfxPointD()
        pixelScale.x = self.getScale()
        pixelScale.y = pixelScale.x
        if self.img_data is not None and self.tuttleOverlay:
            self.tuttleOverlay.draw(pixelScale)

    #time management
    def getTime(self):
        return self._time

    def setTime(self, currentTime):
        self._timeHasChanged = True
        self._time = currentTime
        self.update()
        self.timeChanged.emit()
        self.loadImage()

    timeChanged = QtCore.Signal()
    time = QtCore.Property(float, getTime, setTime, notify=timeChanged)

    #frame management
    def getFrame(self):
        return self._frame

    def setFrame(self, currentFrame):
        self._frameHasChanged = True
        self._frame = currentFrame
        self.update()
        self.frameChanged.emit()
        self.loadImage()

    frameChanged = QtCore.Signal()
    frame = QtCore.Property(int, getFrame, setFrame, notify=frameChanged)
