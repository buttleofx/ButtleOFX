from PySide import QtGui, QtDeclarative, QtCore

from OpenGL import GL

import numpy


def nbChannelsToGlPixelType(nbChannels):
    if nbChannels == 1:
        return GL.GL_LUMINANCE
    elif nbChannels == 3:
        return GL.GL_RGB
    elif nbChannels == 4:
        return GL.GL_RGBA
    else:
        raise NotImplementedError("load_texture: Unsupported pixel type, nb channels is " + str(nbChannels) + ".")


def numpyValueTypeToGlType(valueType):
    if valueType == numpy.uint8:
        return GL.GL_UNSIGNED_BYTE
    elif valueType == numpy.uint16:
        return GL.GL_UNSIGNED_SHORT
    elif valueType == numpy.float32:
        return GL.GL_FLOAT
    else:
        raise NotImplementedError("load_texture: Unsupported image value type: " + str(valueType))


def load_texture(array, width, height):
    #print('loading texture')
    #print('shape:', array.shape)
    #print('array.ndim', array.ndim)
    #print('array.dtype', array.dtype)

    array_type = numpyValueTypeToGlType(array.dtype)

    if array.ndim == 2:
        # linear array of pixels
        size, channels = array.shape
        #print('size:%d, channels:%d' % (size, channels))
        array_channelGL = nbChannelsToGlPixelType(channels)
        return GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, width, height, 0, array_channelGL, array_type, array)
    elif array.ndim == 3:
        # 2D array of pixels
        array_height, array_width, channels = array.shape
        #print('width:%d, height:%d, channels:%d' % (width, height, channels))
        array_channelGL = nbChannelsToGlPixelType(channels)
        return GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, array_width, array_height, 0, array_channelGL, array_type, array)

    # if you get here, it means a case was missed
    raise NotImplementedError("load_texture: Unsupported image type, ndim is " + str(array.ndim) + ".")


def loadTextureFromImage(imgBounds, img_data):
    texture = GL.glGenTextures(1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
    GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)

    # Texture parameters are part of the texture object, so you need to
    # specify them only once for a given texture object.
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP)
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP)
    # GL_TEXTURE_MAG_FILTER: a surface is bigger than the texture being applied (near objects)
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
    # GL_TEXTURE_MIN_FILTER: a surface is rendered with smaller dimensions than its corresponding texture bitmap (far away objects)
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)  # GL.GL_LINEAR_MIPMAP_LINEAR) #GL.GL_NEAREST)
    #GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, imgBounds.width(), imgBounds.height(), 0, GL.GL_RGB, GL.GL_UNSIGNED_BYTE, img_data)

    load_texture(img_data, imgBounds.width(), imgBounds.height())
    return texture


class GLViewport(QtDeclarative.QDeclarativeItem):
    _glGeometry = QtCore.QRect()

    def __init__(self, parent=None):
        super(GLViewport, self).__init__(parent)

        self.img_data = None
        self.tex = None

        # Enable paint method calls
        self.setFlag(QtGui.QGraphicsItem.ItemHasNoContents, False)

    def initializeGL(self):
        GL.glClearColor(0.0, 0.0, 0.0, 0.0)  # We assign a black background
        GL.glShadeModel(GL.GL_FLAT)  # We applied a flat shading mode
        GL.glEnable(GL.GL_LINE_SMOOTH)

    def updateTextureFromImage(self):
        #print "updateTextureFromImage begin"
        if self.img_data is not None:
            self.tex = loadTextureFromImage(self._imageBoundsValue, self.img_data)
        else:
            self.tex = None
        #print "updateTextureFromImage end"

    @QtCore.Slot()
    def fitImage(self):
        widthRatio = self.width() / float(self.getImageBounds().width()) if self.getImageBounds().width() else 1.0
        heightRatio = self.height() / float(self.getImageBounds().height()) if self.getImageBounds().height() else 1.0
        self.setScale(min(widthRatio, heightRatio))

        imgCenter = self.getImageBounds().center()
        self.setOffset_xy(
            -(self.width() * .5 / self._scaleValue - imgCenter.x()),
            -(self.height() * .5 / self._scaleValue - imgCenter.y()))

    def prepareGL(self, widget):

        GL.glViewport(int(self._glGeometry.left()), int(widget.height() - self._glGeometry.bottom()), int(self._glGeometry.width()), int(self._glGeometry.height()))

        #GL.glClearDepth(1) # just for completeness
        #GL.glClearColor( self._bgColorValue.red(), self._bgColorValue.green(), self._bgColorValue.blue(), self._bgColorValue.alpha() )
        #GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()

        # glOrtho( left, right, bottom, top, near, far )
        #GL.glOrtho(0, self.width(), 0, self.height(), -1, 1)
        GL.glOrtho(
            self._offsetValue.x(), self._offsetValue.x() + self.width() / self._scaleValue,
            self._offsetValue.y(), self._offsetValue.y() + self.height() / self._scaleValue,
            -1, 1)

        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

        GL.glColor3d(1.0, 1.0, 1.0)

    def drawImage(self):
        #print "GLViewport.drawImage"
        #print "widget size:", self.width(), "x", self.height()
        #print "image size:", self.getImageBounds().width(), "x", self.getImageBounds().height()

        if self.img_data is not None and self.tex is None:
            self.updateTextureFromImage()

        if self.tex is None:
            return

        GL.glEnable(GL.GL_TEXTURE_2D)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.tex)

        imgRect = QtCore.QRectF(self.getImageBounds())

        GL.glColor3d(1.0, 1.0, 1.0)
        GL.glBegin(GL.GL_QUADS)
        GL.glTexCoord2d(0.0, 1.0)
        GL.glVertex2d(imgRect.left(), imgRect.top())
        GL.glTexCoord2d(1.0, 1.0)
        GL.glVertex2d(imgRect.right(), imgRect.top())
        GL.glTexCoord2d(1.0, 0.0)
        GL.glVertex2d(imgRect.right(), imgRect.bottom())
        GL.glTexCoord2d(0.0, 0.0)
        GL.glVertex2d(imgRect.left(), imgRect.bottom())
        GL.glEnd()

    def drawRegions(self):
        GL.glLineWidth(3)
        GL.glEnable(GL.GL_LINE_STIPPLE)
        GL.glLineStipple(1, 0xAAAA)

        GL.glColor3d(1., 0., 0.)
        self.drawRect(self._rodValue)  # RoD

        GL.glColor3d(1., 1., 1.)
        self.drawRect(self._rowValue)  # RoW

        GL.glDisable(GL.GL_LINE_STIPPLE)

        #self.tuttleReaderNode

    def internPaintGL(self, widget):
        if self.img_data is not None:
            self.prepareGL(widget)
            self.drawImage()
            #self.drawRegions()

    def paint(self, painter, option, widget):
        #def paint(self, painter, widget):
        #print "GLViewport.paint"

        painter.beginNativePainting()
        self.internPaintGL(widget)
        painter.endNativePainting()

    def drawRect(self, rect):
        GL.glBegin(GL.GL_LINE_LOOP)
        GL.glVertex2d(rect.left(), rect.top())
        GL.glVertex2d(rect.right(), rect.top())
        GL.glVertex2d(rect.right(), rect.bottom())
        GL.glVertex2d(rect.left(), rect.bottom())
        GL.glEnd()

    def geometryChanged(self, new, old):
        #print "GLViewport.geometryChanged"
        #print "new:", new.x(), new.y(), new.width(), new.height()
        #print "old:", old.x(), old.y(), old.width(), old.height()

        self._localGeometry = new
        self._glGeometry = self.sceneTransform().mapRect(new)

        if self._fittedModeValue:
            self.fitImage()
        QtDeclarative.QDeclarativeItem.geometryChanged(self, new, old)

    def mousePressEvent(self, event):
        #print "GLViewport.mousePressEvent"
        QtDeclarative.QDeclarativeItem.mousePressEvent(self, event)

    def getBgColor(self):
        return self._bgColorValue

    def setBgColor(self, color):
        self._bgColorValue = color
        self.update()
        self.bgColorChanged.emit()
    bgColorChanged = QtCore.Signal()
    _bgColorValue = QtGui.QColor(255, 0, 0)
    bgColor = QtCore.Property(QtGui.QColor, getBgColor, setBgColor, notify=bgColorChanged)

    def getImageBounds(self):
        return self._imageBoundsValue

    def setImageBounds(self, imgSize):
        self._imageBoundsValue = imgSize
        self.update()
        self.imageBoundsChanged.emit()
    imageBoundsChanged = QtCore.Signal()
    _imageBoundsValue = QtCore.QRect(0, 0, 800, 600)
    imageSize = QtCore.Property(QtCore.QSize, getImageBounds, setImageBounds, notify=imageBoundsChanged)

    def getRegionOfDefinition(self):
        return self._rodValue

    def setRegionOfDefinition(self, rod):
        self._rodValue = rod
        self.update()
        self.rodChanged.emit()
    rodChanged = QtCore.Signal()
    _rodValue = QtCore.QRectF(-50., -100., 900., 500.)
    rod = QtCore.Property(QtCore.QRectF, getRegionOfDefinition, setRegionOfDefinition, notify=rodChanged)

    def getRegionOfWork(self):
        return self._rowValue

    def setRegionOfWork(self, row):
        self._rowValue = row
        self.update()
        self.rowChanged.emit()
    rowChanged = QtCore.Signal()
    _rowValue = QtCore.QRectF(0., 0., 720., 576.)
    row = QtCore.Property(QtCore.QRectF, getRegionOfWork, setRegionOfWork, notify=rowChanged)

    def getFittedMode(self):
        return self._fittedModeValue

    def setfittedMode(self, fittedMode):
        self._fittedModeValue = fittedMode
        self.fittedModeChanged.emit()
    fittedModeChanged = QtCore.Signal()
    _fittedModeValue = False
    fittedMode = QtCore.Property(bool, getFittedMode, setfittedMode, notify=fittedModeChanged)

    def getOffset(self):
        return self._offsetValue

    def setOffset(self, offset):
        #print "setOffset:", offset
        self._offsetValue = offset
        self.update()
        self.offsetChanged.emit()
    offsetChanged = QtCore.Signal()
    _offsetValue = QtCore.QPointF(0., 0.)
    offset = QtCore.Property(QtCore.QPointF, getOffset, setOffset, notify=offsetChanged)

    @QtCore.Slot(float, float)
    def setOffset_xy(self, x, y):
        self.setOffset(QtCore.QPointF(x, y))

    def getScale(self):
        return self._scaleValue

    def setScale(self, scale):
        #print "setScale:", self._scaleValue, " => ", scale
        minValue = 0.001
        self._scaleValue = scale if scale > minValue else minValue
        self.update()
        self.scaleChanged.emit()

    @QtCore.Slot(float, float, float)
    def setScaleAtPos_viewportCoord(self, scale, x, y):
        '''
        scale: the new scale value
        pos_viewportTLCoord: the position in Viewport coordinates which should stay unchanged
        '''
        pos_viewportCoord = QtCore.QPointF(x, y)
        oldScale = self._scaleValue
        oldOffset = self._offsetValue
        minValue = 0.001
        newScale = scale if scale > minValue else minValue
        scaleRatio = newScale / oldScale
        # position relative to the viewport but in root scale
        pos_viewport_rootScale = (pos_viewportCoord / oldScale)
        pos_rootCoord = oldOffset + pos_viewport_rootScale
        newOffset = pos_rootCoord - (pos_viewport_rootScale / scaleRatio)

        self._offsetValue = newOffset
        self._scaleValue = newScale
        self.update()
        self.offsetChanged.emit()
        self.scaleChanged.emit()
    scaleChanged = QtCore.Signal()
    _scaleValue = 1.
    imgScale = QtCore.Property(float, getScale, setScale, notify=scaleChanged)
