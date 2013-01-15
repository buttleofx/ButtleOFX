from glviewport import *

import Image


class GLViewport_pil(GLViewport):
    def __init__(self, parent=None):
        super(GLViewport_pil, self).__init__(parent)

    def loadImageFile_pil(self, filename):
        self.img = Image.open(filename)
        self.img_data = numpy.array(self.img.getdata(), numpy.uint8)
        self.setImageBounds( QtCore.QRect(0, 0, self.img.size[0], self.img.size[1]) )
        self.tuttleOverlay = None
        self.recomputeOverlay = False
        print "image size: ", self._imageBoundsValue.width(), "x", self._imageBoundsValue.height()
        
    def loadImageFile(self, filename):
        print "loadImageFile: ", filename
        self.img_data = None
        self.tex = None
        
        try:
            self.loadImageFile_pil(filename)
            print('PIL img_data:', self.img_data)
        except Exception as e:
            print 'Error while loading image file "%s".\nError: "%s"' % (filename, str(e))
            self.img_data = None
            self.setImageBounds( QtCore.QRect() )
        
        if self._fittedModeValue:
            self.fitImage()
