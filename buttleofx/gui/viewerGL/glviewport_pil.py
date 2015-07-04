import logging

import Image
import numpy

from PyQt5 import QtCore

from glviewport import GLViewport


class GLViewport_pil(GLViewport):

    def __init__(self, parent=None):
        GLViewport.__init__(self, parent)

    # ######################################## Methods private to this class ####################################### #

    def loadImageFile_pil(self, filename):
        self.img = Image.open(filename)
        self.img_data = numpy.array(self.img.getdata(), numpy.uint8)
        self.setImageBounds(QtCore.QRect(0, 0, self.img.size[0], self.img.size[1]))
        self.tuttleOverlay = None
        self.recomputeOverlay = False
        logging.debug("image size: %sx%s" % (self._imageBoundsValue.width(), self._imageBoundsValue.height()))

    def loadImageFile(self, filename):
        logging.debug("loadImageFile: %s" % filename)
        self.img_data = None
        self.tex = None

        try:
            self.loadImageFile_pil(filename)
            logging.debug('PIL img_data: %s' % self.img_data)
        except Exception as e:
            logging.warning('Error while loading image file "%s".\n"%s"' % (filename, str(e)))
            self.img_data = None
            self.setImageBounds(QtCore.QRect())

        if self._fittedModeValue:
            self.fitImage()
