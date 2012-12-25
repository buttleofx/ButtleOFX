from PySide import QtGui, QtDeclarative, QtCore, QtOpenGL
from OpenGL import GL, GLU

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
        QtDeclarative.QDeclarativeItem.__init__(self, parent)
        self.initGL()
        
        # Enable paint method calls
        self.setFlag(QtGui.QGraphicsItem.ItemHasNoContents, False)
        self.loadImageFile("input.jpg")
        self.tex = None
        
    def initGL(self):
        GL.glEnable(GL.GL_LINE_SMOOTH)
        
    def loadImageFile(self, filename):
        print "loadImageFile: ", filename
        import Image
        import numpy
        self.img = Image.open(filename)
        self.img_data = numpy.array(self.img.getdata(), numpy.uint8)
        print "image size: ", self.img.size[0], "x", self.img.size[1]

    def updateTextureFromImage(self):
        print "updateTextureFromImage begin"
        self.tex = loadTextureFromImage( self.img, self.img_data )
        print "updateTextureFromImage end"
        
    def paint(self, painter, option, widget):
        print "GLViewport.paint"
        print "width:", self.width()
        print "height:", self.height()
        
        painter.beginNativePainting();
        
        if self.tex is None:
            self.updateTextureFromImage()
        
        GL.glViewport(0, 0, int(self.width()), int(self.height()))
        GL.glClearDepth(1) # just for completeness
        GL.glClearColor( self._bgColorValue.red(), self._bgColorValue.green(), self._bgColorValue.blue(), self._bgColorValue.alpha() )
        print "clearColor:", self._bgColorValue.red(), self._bgColorValue.green(), self._bgColorValue.blue(), self._bgColorValue.alpha()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        #GL.glOrtho(0, 1, 0, 1, -1, 1)
        GL.glMatrixMode(GL.GL_MODELVIEW);
        GL.glLoadIdentity()
        
        GL.glEnable(GL.GL_TEXTURE_2D)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.tex)
        
        imgRatio = float(self.img.size[0]) / float(self.img.size[1])
        winRatio = float(self.width()) / float(self.height())
        print "self.img.size[0]:", self.img.size[0]
        print "self.img.size[1]:", self.img.size[1]
        print "imgRatio:", imgRatio
        
        v = winRatio / imgRatio
        scale = 1.
        if v >= 1.:
            scale = 1. / v
        posX = [-scale, scale]
        posY = [-scale*v, scale*v]
        
        GL.glColor3f( 1.0, 1.0, 1.0 )
        GL.glBegin(GL.GL_QUADS)
        GL.glTexCoord2f(0.0,0.0)
        GL.glVertex2d(posX[0],posY[1])
        GL.glTexCoord2f(0.0, 1.0)
        GL.glVertex2d(posX[0],posY[0])
        GL.glTexCoord2f(1.0,1.0)
        GL.glVertex2d(posX[1],posY[0])
        GL.glTexCoord2f(1.0, 0.0)
        GL.glVertex2d(posX[1],posY[1])
        GL.glEnd()
        
        GL.glLineWidth(3);
        GL.glColor3f( 1., 1., 1. )
        
        GL.glEnable(GL.GL_LINE_STIPPLE)
        #GL.glLineStipple(3, 0x00FF)
        GL.glLineStipple(1, 0xAAAA)
        
        rodTL = self._rodValue.topLeft()
        rodBR = self._rodValue.bottomRight()
        
        GL.glBegin(GL.GL_LINE_LOOP)
        GL.glColor3f( 1., 1., 1. )
        GL.glVertex2d(rodTL.x(), rodTL.y())
        GL.glVertex2d(rodBR.x(), rodTL.y())
        GL.glVertex2d(rodBR.x(), rodBR.y())
        GL.glVertex2d(rodTL.x(), rodBR.y())
        GL.glEnd()
        GL.glDisable(GL.GL_LINE_STIPPLE)
        
        painter.endNativePainting()

    def geometryChanged(self, new, old):
        print "GLViewport.geometryChanged"
        QtDeclarative.QDeclarativeItem.geometryChanged(self, new, old)

    def mousePressEvent(self, event):
        print "GLViewport.mousePressEvent"


    def getBgColor(self):
        return self._bgColorValue
    def setBgColor(self, color):
        self._bgColorValue = color
    bgColorChanged = QtCore.Signal()
    _bgColorValue = QtGui.QColor(0, 0, 0)
    bgColor = QtCore.Property(QtGui.QColor, getBgColor, setBgColor, notify=bgColorChanged)


    def getRegionOfDefinition(self):
        return self._rodValue
    def setRegionOfDefinition(self, rod):
        self._rodValue = rod
    rodChanged = QtCore.Signal()
    _rodValue = QtCore.QRectF(-.5, -.3, .5, .3)
    rod = QtCore.Property(QtCore.QRectF, getRegionOfDefinition, setRegionOfDefinition, notify=rodChanged)


