from glviewport import GLViewport

from tuttleOverlayInteract import TuttleOverlayInteract

from pyTuttle import tuttle

from PySide import QtCore

# data
from buttleofx.data import *


class GLViewport_tuttleofx(GLViewport):
    def __init__(self, parent=None):
        super(GLViewport_tuttleofx, self).__init__(parent)

        self.tuttleOverlay = None
        self.recomputeOverlay = False
        
        buttleData = ButtleDataSingleton().get()
        buttleData.currentViewerNodeChangedPython.connect(self.loadImage)

    def loadImage_tuttle(self):
        print "--------------------------------- loadImage_tuttle ---------------------------"
        buttleData = ButtleDataSingleton().get()
        imgRes = buttleData.computeNode(self._time)

        self._time = 0

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
            raise

        if self._fittedModeValue:
            self.fitImage()

        print "loadImageFile end"

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
        self._time = currentTime
        self.update()
        self.timeChanged.emit()
        self.reloadImage()
        #print "self._time du setTime:", self._time
    
    timeChanged = QtCore.Signal()
    time = QtCore.Property(float, getTime, setTime, notify=timeChanged)
 

 #   def getCurrentTime(self):
 #       return self._currentTime
#
    #def setCurrentTime(self, currentTime):
 #       self._currentTime = currentTime
 #       super.setOffset(self, currentTime)
#
 #   @QtCore.Signal
 #   def changed(self):
 #       pass

 #   def emitChanged(self):
  #      self.changed.emit()

#times signals
    #timeChanged = QtCore.Signal()
    #currentTime = QtCore.Property(QtCore.QObject, getCurrentTime, setCurrentTime, notify = timeChanged)

