from PySide import QtCore
# common
from paramWrapper import ParamWrapper


class RGBAWrapper(ParamWrapper):
    """
        Gui class, which maps a ParamRGBA.
    """

    def __init__(self, param):
        ParamWrapper.__init__(self, param)

    #################### getters ####################

    def getDefaultR(self):
        return self._param.getDefaultR()

    def getDefaultG(self):
        return self._param.getDefaultG()

    def getDefaultB(self):
        return self._param.getDefaultB()

    def getDefaultA(self):
        return self._param.getDefaultA()

    def getValueR(self):
        return self._param.getValueR()

    def getValueG(self):
        return self._param.getValueG()

    def getValueB(self):
        return self._param.getValueB()

    def getValueA(self):
        return self._param.getValueA()

    def getPositionColorSlider(self):
        return self._param.getPositionColorSlider()

    def getPositionAlphaSlider(self):
        return self._param.getPositionAlphaSlider()

    def getPositionXcolorSelector(self):
        return self._param.getPositionXcolorSelector()

    def getPositionYcolorSelector(self):
        return self._param.getPositionYcolorSelector()

    #################### setters ####################

    def setValueR(self, value):
        self._param.setValueR(value)

    def setValueG(self, value):
        self._param.setValueG(value)

    def setValueB(self, value):
        self._param.setValueB(value)

    def setValueA(self, value):
        self._param.setValueA(value)

    def setPositionColorSlider(self, position):
        print "setcolorSlider: ", position
        self._param.setPositionColorSlider(position)

    def setPositionAlphaSlider(self, position):
        print "setalphaSlider: ", position
        self._param.setPositionAlphaSlider(position)

    def setPositionXcolorSelector(self, position):
        print "setcolorSelectorX: ", position
        self._param.setPositionXcolorSelector(position)

    def setPositionYcolorSelector(self, position):
        print "setcolorSelectorY: ", position
        self._param.setPositionYcolorSelector(position)

    @QtCore.Signal
    def changed(self):
        pass

    ################################################## DATA EXPOSED TO QML ##################################################

    r = QtCore.Property(float, getValueR, setValueR, notify=changed)
    g = QtCore.Property(float, getValueG, setValueG, notify=changed)
    b = QtCore.Property(float, getValueB, setValueB, notify=changed)
    a = QtCore.Property(float, getValueA, setValueA, notify=changed)

    colorSlider = QtCore.Property(float, getPositionColorSlider, setPositionColorSlider, notify=changed)
    alphaSlider = QtCore.Property(float, getPositionAlphaSlider, setPositionAlphaSlider, notify=changed)
    colorSelectorX = QtCore.Property(float, getPositionXcolorSelector, setPositionXcolorSelector, notify=changed)
    colorSelectorY = QtCore.Property(float, getPositionYcolorSelector, setPositionYcolorSelector, notify=changed)
