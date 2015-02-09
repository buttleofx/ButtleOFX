#! /usr/bin/env python3
import os
import numpy
import logging
from pyTuttle import tuttle
from PyQt5 import QtGui, QtQuick

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
                qim = QtGui.QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QtGui.QImage.Format_ARGB32)
                return qim
    raise ValueError("toQImage: case not implemented.")


class ImageProvider(QtQuick.QQuickImageProvider):
    def __init__(self):
        QtQuick.QQuickImageProvider.__init__(self, QtQuick.QQuickImageProvider.Image)
        self.thumbnailCache = tuttle.ThumbnailDiskCache()
        self.thumbnailCache.setRootDir(os.path.join(tuttle.core().getPreferences().getTuttleHomeStr(),
                                                    "thumbnails_cache"))

    def requestImage(self, id, size):
        """
        Compute the image using TuttleOFX
        """
        logging.debug("Tuttle ImageProvider: file='%s'" % id)
        try:
            img = self.thumbnailCache.getThumbnail(id)
            numpyImage = img.getNumpyArray()
            # Convert numpyImage to QImage
            qtImage = toQImage(numpyImage)
            return qtImage.copy(), qtImage.size()

        except Exception as e:
            logging.debug("Tuttle ImageProvider: file='%s' => error: {0}".format(id, str(e)))
            qtImage = QtGui.QImage()
            return qtImage, qtImage.size()
