from PySide import QtCore


class RGBAWrapper(QtCore.QObject):
    """
        Gui class, which maps a ParamRGBA.
    """

    def __init__(self, param):
        QtCore.QObject.__init__(self)
        self._param = param
        self._param.changed.connect(self.emitChanged)
        self._positionColorSlider = 0
        self._positionAlphaSlider = 0
        self._positionXcolorSelector = 0
        self._positionYcolorSelector = 0

    #################### getters ####################

    def getParamType(self):
        return self._param.getParamType()

    def getDefaultR(self):
        return self._param.getDefaultR()

    def getDefaultG(self):
        return self._param.getDefaultG()

    def getDefaultB(self):
        return self._param.getDefaultB()

    def getDefaultA(self):
        return self._param.getDefaultA()

    def getValue(self):
        return self._param.getValue()

    def getValueR(self):
        return self._param.getValueR()

    def getValueG(self):
        return self._param.getValueG()

    def getValueB(self):
        return self._param.getValueB()

    def getValueA(self):
        return self._param.getValueA()

    def getText(self):
        return self._param.getText()

    def getPositionColorSlider(self):
        print "colorSlider :", self._positionColorSlider
        return self._positionColorSlider

    def getPositionAlphaSlider(self):
        print "alphaSlider :", self._positionAlphaSlider
        return self._positionAlphaSlider

    def getPositionXcolorSelector(self):
        print "selectorX :", self._positionXcolorSelector
        return self._positionXcolorSelector

    def getPositionYcolorSelector(self):
        print "selectorY :", self._positionYcolorSelector
        return self._positionYcolorSelector

    #################### setters ####################

    def setValue(self, values):
        self._param.setValue(values)

    def setValueR(self, value):
        self._param.setValueR(value)

    def setValueG(self, value):
        self._param.setValueG(value)

    def setValueB(self, value):
        self._param.setValueB(value)

    def setValueA(self, value):
        self._param.setValueA(value)

    def setText(self, text):
        self._param.setText(text)

    def setPositionColorSlider(self, position):
        print "colorSlider: ", position
        self._positionColorSlider = position

    def setPositionAlphaSlider(self, position):
        print "alphaSlider: ", position
        self._positionAlphaSlider = position

    def setPositionXcolorSelector(self, position):
        print "colorSelectorX: ", position
        self._positionXcolorSelector = position

    def setPositionYcolorSelector(self, position):
        print "colorSelectorY: ", position
        self._positionYcolorSelector = position

    @QtCore.Signal
    def changed(self):
        pass

    def emitChanged(self):
        self.changed.emit()

    ################################################## DATA EXPOSED TO QML ##################################################

    paramType = QtCore.Property(unicode, getParamType, notify=changed)
    text = QtCore.Property(unicode, getText, setText, notify=changed)
    r = QtCore.Property(float, getValueR, setValueR, notify=changed)
    g = QtCore.Property(float, getValueG, setValueG, notify=changed)
    b = QtCore.Property(float, getValueB, setValueB, notify=changed)
    a = QtCore.Property(float, getValueA, setValueA, notify=changed)
    colorSlider = QtCore.Property(float, getPositionColorSlider, setPositionColorSlider, notify=changed)
    alphaSlider = QtCore.Property(float, getPositionAlphaSlider, setPositionAlphaSlider, notify=changed)
    colorSelectorX = QtCore.Property(float, getPositionXcolorSelector, setPositionXcolorSelector, notify=changed)
    colorSelectorY = QtCore.Property(float, getPositionYcolorSelector, setPositionYcolorSelector, notify=changed)
