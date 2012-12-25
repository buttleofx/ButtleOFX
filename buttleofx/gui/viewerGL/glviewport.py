from PySide import QtGui, QtDeclarative, QtCore
from OpenGL import GL

def loadTextureFromImage(img, img_data):
    texture = GL.glGenTextures(1)
    GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT,1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture)

    # Texture parameters are part of the texture object, so you need to 
    # specify them only once for a given texture object.
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP)
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP)
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, img.size[0], img.size[1], 0, GL.GL_RGB, GL.GL_UNSIGNED_BYTE, img_data)
    return texture

class GLViewport(QtDeclarative.QDeclarativeItem):
    def __init__(self, parent=None):
        super(GLViewport, self).__init__(parent)
        
        # Enable paint method calls
        self.setFlag(QtGui.QGraphicsItem.ItemHasNoContents, False)
        self.loadImageFile("input.jpg")
        self.tex = None
        
    def initializeGL(self):
        GL.glClearColor(0.0,0.0,0.0,0.0) # We assign a black background
        GL.glShadeModel(GL.GL_FLAT) # We applied a flat shading mode
        GL.glEnable(GL.GL_LINE_SMOOTH)
    
    def loadImageFile(self, filename):
        print "loadImageFile: ", filename
        import Image
        import numpy
        self.img = Image.open(filename)
        self.img_data = numpy.array(self.img.getdata(), numpy.uint8)
        self.setImageSize( QtCore.QSize(self.img.size[0], self.img.size[1]) )
        print "image size: ", self.img.size[0], "x", self.img.size[1]

    def updateTextureFromImage(self):
        print "updateTextureFromImage begin"
        self.tex = loadTextureFromImage( self.img, self.img_data )
        print "updateTextureFromImage end"
        
    def fitImage(self):
        self.setScale( min( self.width()/float(self.getImageSize().x()), self.height()/float(self.getImageSize().y()) ) )

    def prepareGL(self):
        
        GL.glViewport(0, 0, int(self.width()), int(self.height()))
        GL.glClearDepth(1) # just for completeness
        GL.glClearColor( self._bgColorValue.red(), self._bgColorValue.green(), self._bgColorValue.blue(), self._bgColorValue.alpha() )
        print "clearColor:", self._bgColorValue.red(), self._bgColorValue.green(), self._bgColorValue.blue(), self._bgColorValue.alpha()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        # glOrtho( left, right, bottom, top, near, far )
        #GL.glOrtho(0, 1, 0, 1, -1, 1)
        #GL.glOrtho(0, self.width(), 0, self.height(), -1, 1)
        GL.glMatrixMode(GL.GL_MODELVIEW);
        GL.glLoadIdentity()
        
        GL.glColor3f(1.0, 1.0, 1.0)
        
    def drawImage(self):
        print "GLViewport.drawImage"
        print "widget size:", self.width(), "x", self.height()
        print "image size:", self.getImageSize().width(), "x", self.getImageSize().height()
        
        if self.tex is None:
            self.updateTextureFromImage()
        
        GL.glEnable(GL.GL_TEXTURE_2D)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.tex)
        
        imgRatio = float(self.img.size[0]) / float(self.img.size[1])
        winRatio = float(self.width()) / float(self.height())
        print "self.img.size[0]:", self.img.size[0]
        print "self.img.size[1]:", self.img.size[1]
        print "imgRatio:", imgRatio
        
        v = winRatio / imgRatio
        scale = self._scaleValue
        if v >= 1.:
            scale = 1. / v
        
        tl = QtCore.QPointF(-scale, -scale*v)
        br = QtCore.QPointF(scale, scale*v)
        
        GL.glColor3f( 1.0, 1.0, 1.0 )
        GL.glBegin(GL.GL_QUADS)
        GL.glTexCoord2f(0.0, 1.0); GL.glVertex2d(tl.x(), tl.y())
        GL.glTexCoord2f(1.0, 1.0); GL.glVertex2d(br.x(), tl.y())
        GL.glTexCoord2f(1.0, 0.0); GL.glVertex2d(br.x(), br.y())
        GL.glTexCoord2f(0.0, 0.0); GL.glVertex2d(tl.x(), br.y())
        GL.glEnd()
        
    def drawRegions(self):
        GL.glLineWidth(3);
        GL.glEnable(GL.GL_LINE_STIPPLE)
        GL.glLineStipple(1, 0xAAAA)
        
        GL.glColor3f( 1., 0., 0. )
        self.drawRect( self._rodValue ) # RoD
        
        GL.glColor3f( 0., 1., 0. )
        self.drawRect( self._rowValue ) # RoW
        
        GL.glDisable(GL.GL_LINE_STIPPLE)
        
    def internPaintGL(self):
        self.prepareGL()
        self.drawImage()
        self.drawRegions()
    
    def paint(self, painter, option, widget):
        painter.beginNativePainting();
        self.internPaintGL()
        painter.endNativePainting()

    def drawRect(self, rect):
        tl = rect.topLeft()
        br = rect.bottomRight()
        
        GL.glBegin(GL.GL_LINE_LOOP)
        GL.glVertex2d(tl.x(), tl.y())
        GL.glVertex2d(br.x(), tl.y())
        GL.glVertex2d(br.x(), br.y())
        GL.glVertex2d(tl.x(), br.y())
        GL.glEnd()

    def geometryChanged(self, new, old):
        print "GLViewport.geometryChanged"
        QtDeclarative.QDeclarativeItem.geometryChanged(self, new, old)

    def mousePressEvent(self, event):
        print "GLViewport.mousePressEvent"


    def getBgColor(self):
        return self._bgColorValue
    def setBgColor(self, color):
        self._bgColorValue = color
        self.bgColorChanged.emit()
    bgColorChanged = QtCore.Signal()
    _bgColorValue = QtGui.QColor(0, 0, 0)
    bgColor = QtCore.Property(QtGui.QColor, getBgColor, setBgColor, notify=bgColorChanged)


    def getImageSize(self):
        return self._imageSizeValue
    def setImageSize(self, imgSize):
        self._imageSizeValue = imgSize
        self.imageSizeChanged.emit()
    imageSizeChanged = QtCore.Signal()
    _imageSizeValue = QtCore.QSize(800, 600)
    imageSize = QtCore.Property(QtCore.QSize, getImageSize, setImageSize, notify=imageSizeChanged)


    def getRegionOfDefinition(self):
        return self._rodValue
    def setRegionOfDefinition(self, rod):
        self._rodValue = rod
        self.rodChanged.emit()
    rodChanged = QtCore.Signal()
    _rodValue = QtCore.QRectF(-50., -100., 900., 500.)
    rod = QtCore.Property(QtCore.QRectF, getRegionOfDefinition, setRegionOfDefinition, notify=rodChanged)


    def getRegionOfWork(self):
        return self._rowValue
    def setRegionOfWork(self, row):
        self._rowValue = row
        self.rowChanged.emit()
    rowChanged = QtCore.Signal()
    _rowValue = QtCore.QRectF(0., 0., 720., 576.)
    row = QtCore.Property(QtCore.QRectF, getRegionOfWork, setRegionOfWork, notify=rowChanged)


    def getScale(self):
        return self._scaleValue
    def setScale(self, scale):
        self._scaleValue = scale
        self.scaleChanged.emit()
    scaleChanged = QtCore.Signal()
    _scaleValue = 1.
    scale = QtCore.Property(float, getScale, setScale, notify=scaleChanged)


