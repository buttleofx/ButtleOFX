from glviewport import *

tuttleofx_installed = False
try:
    import pyTuttle
    from buttleOverlayInteract import ButtleOverlayInteract
    tuttleofx_installed = True
    print('Use TuttleOFX.')
except:
    import Image
    print('TuttleFX not installed, use Python Image Library instead.')

class ButtleGLViewport(GLViewport):
    def __init__(self, parent=None):
        super(ButtleGLViewport, self).__init__(parent)
        
        if tuttleofx_installed:
            self.init_tuttle()
    
    def init_tuttle(self):
        from pyTuttle import tuttle
        tuttle.core().preload()
        self.tuttleGraph = tuttle.Graph()
        self.tuttleReaderNode = self.tuttleGraph.createNode("tuttle.jpegreader")
        self.tuttleReaderNodeOverlay = ButtleOverlayInteract(self.tuttleReaderNode)
        
    def loadImageFile_tuttle(self, filename):
        from pyTuttle import tuttle
        self.tuttleReaderNode.getParam("filename").setValue(str(filename))
        outputCache = tuttle.MemoryCache()
        self.tuttleGraph.compute(outputCache)
        imgRes = outputCache.get(0);
        print 'type imgRes:', type( imgRes )
        print 'imgRes:', dir( imgRes )
        print 'FullName:', imgRes.getFullName()
        print 'MemorySize:', imgRes.getMemorySize()
        #print 'Bounds:', imgRes.getBounds()
        
        self.img_data = imgRes.getNumpyArray()
        
        bounds = imgRes.getBounds()
        #self.getVoidPixelData()
        width = bounds.x2 - bounds.x1
        height = bounds.y2 - bounds.y1
        
        self.setImageBounds( QtCore.QRect(bounds.x1, bounds.y1, width, height) )
    
    def loadImageFile_pil(self, filename):
        self.img = Image.open(filename)
        self.img_data = numpy.array(self.img.getdata(), numpy.uint8)
        self.setImageBounds( QtCore.QRect(0, 0, self.img.size[0], self.img.size[1]) )
        print "image size: ", self._imageBoundsValue.width(), "x", self._imageBoundsValue.height()
        
    def loadImageFile(self, filename):
        print "loadImageFile: ", filename
        self.img_data = None
        self.tex = None
        
        try:
            if tuttleofx_installed:
                self.loadImageFile_tuttle(filename)
                print('Tuttle img_data:', self.img_data)
            else:
                self.loadImageFile_pil(filename)
                print('PIL img_data:', self.img_data)
        except Exception as e:
            print 'Error while loading image file "%s".\nError: "%s"' % (filename, str(e))
            self.img_data = None
            self.setImageBounds( QtCore.QRect() )
        
        if self._fittedModeValue:
            self.fitImage()



