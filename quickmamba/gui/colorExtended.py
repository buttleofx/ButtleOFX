from PySide import QtCore, QtGui
from PySide import QtDeclarative


class ColorExtended(QtDeclarative.QDeclarativeItem):

    _color = QtGui.QColor()
	
    def __init__(self, parent=None):
        QtDeclarative.QDeclarativeItem.__init__(self, parent)


    def getColor(self):
        return self._color

    def setColor(self, color):
        self._color = color
        self.colorChanged.emit()

    def getRed(self):
        return self._color.red()

    def setRed(self, red):
        self._color.setRed(red)
        self.colorChanged.emit()

    def getGreen(self):
        return self._color.green()

    def setGreen(self, green):
        self._color.setGreen(green)
        self.colorChanged.emit()

    def getBlue(self):
        return self._color.blue()

    def setBlue(self, blue):
        self._color.setBlue(blue)
        self.colorChanged.emit()

    def getHue(self):
        return self._color.hue()

    def setHue(self, hue):
        self._color.setHue(hue)
        self.colorChanged.emit()

    #saturation
    def getSaturation(self):
        print "GET SATURATION"
        return self._color.saturationF()

    def setSaturation(self, saturationF):
        print "SET SATURATION :", saturationF
        # setValueF doesn't exist
        hueF = self._color.hueF()
        #print "hue : ", hueF
        valueF = self._color.valueF()
        #print "saturation : ", saturationF
        alphaF = self._color.alphaF()
        #print "alpha : ", alphaF
        # I would use setHslF but for unknown reason (bug ?), it doesn't modify the saturation
        self._color.setHsvF(hueF, saturationF, valueF, alphaF)
        print "self._color.saturation :", self._color.saturationF()
        #print "new ligthness : ", self._color.lightnessF()
        self.colorChanged.emit()

    # brightness (corresponds to lightness for the moment)
    def getBrightness(self):
        print "GET BRIGHTNESS"
        return self._color.lightnessF()

    def setBrightness(self, brightnessF):
        print "SET BRIGHTNESS"
        # setValueF doesn't exist
        hueF = self._color.hueF()
        #print "hue : ", hueF
        saturationF = self._color.saturationF()
        #print "saturation : ", saturationF
        alphaF = self._color.alphaF()
        #print "alpha : ", alphaF
        self._color.setHslF(hueF, saturationF, brightnessF, alphaF)
        #print "new ligthness : ", self._color.lightnessF()
        self.colorChanged.emit()

    # alpha
    def getAlpha(self):
        # alpha returns the value of alpha between 0 and 255 and alphaF between 0 and 1
        return self._color.alphaF()

    def setAlpha(self, alphaF):
        self._color.setAlphaF(alphaF)
        self.colorChanged.emit()

    # value (for v in hsva)
    def getValue(self):
        print "passed in getValue test ColorSlider", self._color.valueF()
        return self._color.valueF()

    def setValue(self, valueF):
        # setValueF doesn't exist
        hueF = self._color.hueF()
        #print "hue : ", hueF
        saturationF = self._color.saturationF()
        #print "saturation : ", saturationF
        alphaF = self._color.alphaF()
        #print "alpha : ", alphaF
        #print "value : ", self._color.valueF()
        self._color.setHsvF(hueF, saturationF, valueF, alphaF)
        #print "new value : ", self._color.valueF()
        self.colorChanged.emit()

    colorChanged = QtCore.Signal()
    #QColor (contains all information on the color)
    entireColor = QtCore.Property(QtGui.QColor, getColor, setColor, notify=colorChanged)
    #rgb
    red = QtCore.Property(float, getRed, setRed, notify=colorChanged)
    green = QtCore.Property(float, getGreen, setGreen, notify=colorChanged)
    blue = QtCore.Property(float, getBlue, setBlue, notify=colorChanged)
    # hsva
    hue = QtCore.Property(float, getHue, setHue, notify=colorChanged)
    saturation = QtCore.Property(float, getSaturation, setSaturation, notify=colorChanged)
    # brightness corresponds to lightness for the moment
    brightness = QtCore.Property(float, getBrightness, setBrightness, notify=colorChanged)
    alpha = QtCore.Property(float, getAlpha, setAlpha, notify=colorChanged)
    value = QtCore.Property(float, getValue, setValue, notify=colorChanged)

