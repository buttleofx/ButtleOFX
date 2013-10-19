from PyQt5 import QtCore, QtGui
from PyQt5 import QtQuick


class ColorExtended(QtQuick.QQuickItem):

    _color = QtGui.QColor()

    def __init__(self, parent=None):
        QtQuick.QQuickItem.__init__(self, parent)

    # the F at the end of a fonction as color.alphaF() means that the value returns or set is between 0 and 1
    def getColor(self):
        return self._color

    def setColor(self, color):
        self._color = color
        self.colorChanged.emit()

    def getRed(self):
        return self._color.redF()

    def setRed(self, red):
        self._color.setRedF(red)
        self.colorChanged.emit()

    def getGreen(self):
        return self._color.greenF()

    def setGreen(self, green):
        self._color.setGreenF(green)
        self.colorChanged.emit()

    def getBlue(self):
        return self._color.blueF()

    def setBlue(self, blue):
        self._color.setBlueF(blue)
        self.colorChanged.emit()

    # hue
    def getHue(self):
        return self._color.hueF()

    def setHue(self, hueF):
        # setHueF doesn't exist
        saturationF = self._color.saturationF()
        brightnessF = self._color.valueF()
        alphaF = self._color.alphaF()
        self._color.setHsvF(hueF, saturationF, brightnessF, alphaF)
        self.colorChanged.emit()

    # saturation
    def getSaturation(self):
        return self._color.saturationF()

    def setSaturation(self, saturationF):
        # setSaturationF doesn't exist
        hueF = self._color.hueF()
        brightnessF = self._color.valueF()
        alphaF = self._color.alphaF()
        self._color.setHsvF(hueF, saturationF, brightnessF, alphaF)
        self.colorChanged.emit()

    # brightness is the b in hsb model for color (also named hsv, with v for value)
    def getBrightness(self):
        return self._color.valueF()

    def setBrightness(self, brightnessF):
        # setBrightnessF doesn't exist
        hueF = self._color.hueF()
        #print "hue in setBrightness : ", hueF
        saturationF = self._color.saturationF()
        #print "saturation : ", saturationF
        alphaF = self._color.alphaF()
        #print "alpha : ", alphaF
        self._color.setHsvF(hueF, saturationF, brightnessF, alphaF)
        #print "new brightness : ", self._color.valueF()
        self.colorChanged.emit()

    # alpha
    def getAlpha(self):
        return self._color.alphaF()

    def setAlpha(self, alphaF):
        self._color.setAlphaF(alphaF)
        self.colorChanged.emit()

    colorChanged = QtCore.pyqtSignal()

    # QColor (contains all information on the color)
    entireColor = QtCore.pyqtProperty(QtGui.QColor, getColor, setColor, notify=colorChanged)

    # rgb (between 0 and 1)
    red = QtCore.pyqtProperty(float, getRed, setRed, notify=colorChanged)
    green = QtCore.pyqtProperty(float, getGreen, setGreen, notify=colorChanged)
    blue = QtCore.pyqtProperty(float, getBlue, setBlue, notify=colorChanged)

    # hsba (also named hsva) (between 0 and 1)
    hue = QtCore.pyqtProperty(float, getHue, setHue, notify=colorChanged)
    saturation = QtCore.pyqtProperty(float, getSaturation, setSaturation, notify=colorChanged)
    brightness = QtCore.pyqtProperty(float, getBrightness, setBrightness, notify=colorChanged)
    alpha = QtCore.pyqtProperty(float, getAlpha, setAlpha, notify=colorChanged)
