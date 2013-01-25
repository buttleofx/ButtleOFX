from glviewport import GLViewport

from tuttleOverlayInteract import TuttleOverlayInteract

from pyTuttle import tuttle

from PySide import QtCore


class GLViewport_tuttleofx(GLViewport):
    def __init__(self, parent=None):
        super(GLViewport_tuttleofx, self).__init__(parent)
        
        self.tuttleOverlay = None
        self.recomputeOverlay = False
        self._time = self.getTime()
        self.init_tuttle()
        #self._currenTime.changed(self.emitChanged)
    
    def init_tuttle(self):
        tuttle.core().preload(False)
        #print "Plugins cache:", tuttle.core().getImageEffectPluginCache()
        self.tuttleGraph = tuttle.Graph()
        self.tuttleReaderNode = self.tuttleGraph.createNode("tuttle.ffmpegreader")
        #self.tuttleLensNode = self.tuttleGraph.createNode("tuttle.lensdistort")
        self.tuttleLensNode = self.tuttleGraph.createNode("tuttle.lensdistort",
                    coef1=.5, #outOfImage='transparency',
                    gridOverlay=True, gridCenterOverlay=True) #, debugDisplayRoi=True)
        self.tuttleGraph.connect(self.tuttleReaderNode, self.tuttleLensNode)
        self.tuttleOverlay = TuttleOverlayInteract(self, self.tuttleGraph, self.tuttleLensNode)
        #self.tuttleOverlay.createInstanceAction()
        #self.tuttleOverlay.initOverlayDescriptor(8, True)
        
    def loadImageFile_tuttle(self, filename):
        print 'loadImageFile_tuttle:', str(filename)
        
        self.tuttleReaderNode.getParam("filename").setValue(str(filename))
        outputCache = tuttle.MemoryCache()
        self.tuttleGraph.compute(outputCache, self.tuttleLensNode, tuttle.ComputeOptions(0))
        imgRes = outputCache.get(0);
        #print 'type imgRes:', type( imgRes )
        #print 'imgRes:', dir( imgRes )
        #print 'FullName:', imgRes.getFullName()
        #print 'MemorySize:', imgRes.getMemorySize()
        #print 'Bounds:', imgRes.getBounds()
        
        self.img_data = imgRes.getNumpyArray()
        
        bounds = imgRes.getBounds()
        #self.getVoidPixelData()
        width = bounds.x2 - bounds.x1
        height = bounds.y2 - bounds.y1
        
        self.setImageBounds( QtCore.QRect(bounds.x1, bounds.y1, width, height) )
        
        self.tuttleOverlay.setupGraph()
        
#        self.recomputeOverlay = False
#        if self.recomputeOverlay:
#            print("GLViewport_tuttleofx.loadImageFile_tuttle recomputeOverlay")
#            try:
#                print("GLViewport_tuttleofx.loadImageFile_tuttle recomputeOverlay A")
#                self.tuttleOverlay = None
#                self.tuttleOverlay = TuttleOverlayInteract(self, self.tuttleLensNode)
#                print("GLViewport_tuttleofx.loadImageFile_tuttle recomputeOverlay B")
#                self.tuttleOverlay.createInstanceAction()
#                print("GLViewport_tuttleofx.loadImageFile_tuttle recomputeOverlay C")
#            except Exception as e:
#                print "Exception: ", str(e)
#                self.tuttleOverlay = None
#            self.recomputeOverlay = False
    
    def loadImageFile(self, filename):
        print "loadImageFile: ", filename
        self.img_data = None
        self.tex = None
        
        try:
            self.loadImageFile_tuttle(filename)
            print('Tuttle img_data:', self.img_data)
        except:
            print 'Error while loading image file "%s".' % (filename)
            self.img_data = None
            self.setImageBounds( QtCore.QRect() )
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