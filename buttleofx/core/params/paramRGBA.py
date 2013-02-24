# common
from buttleofx.core.params import Param


class ParamRGBA(Param):
    """
        Core class, which represents a RGBA parameter.
        Contains :
            - _tuttleParam : link to the corresponding tuttleParam.
            - _positionColorSlider, _positionAlphaSlider, _positionXcolorSelector, _positionYcolorSelector : the old values of the param.
    """

    def __init__(self, tuttleParam):
        Param.__init__(self)
        
        self._tuttleParam = tuttleParam

        self._positionColorSlider = 0
        self._positionAlphaSlider = 0
        self._positionXcolorSelector = 0
        self._positionYcolorSelector = 0

    #################### getters ####################

    def getTuttleParam(self):
        return self._tuttleParam

    def getParamType(self):
        return "ParamRGBA"

    def getDefaultR(self):
        return self._tuttleParam.getDoubleValueAtIndex(0)

    def getDefaultG(self):
        return self._tuttleParam.getDoubleValueAtIndex(1)

    def getDefaultB(self):
        return self._tuttleParam.getDoubleValueAtIndex(2)

    def getDefaultA(self):
        print "fguhdgvgjhc", self._tuttleParam.getDoubleValueAtIndex(3)
        return self._tuttleParam.getDoubleValueAtIndex(3)

    def getValue(self):
        return (self.getValueR(), self.getValueG(), self.getValueB(), self.getValueA())

    def getValueR(self):
        print "red value: ", self._tuttleParam.getDoubleValueAtIndex(0)
        return self._tuttleParam.getDoubleValueAtIndex(0)

    def getValueG(self):
        print "green value: ", self._tuttleParam.getDoubleValueAtIndex(1)
        return self._tuttleParam.getDoubleValueAtIndex(1)

    def getValueB(self):
        print "blue value: ", self._tuttleParam.getDoubleValueAtIndex(2)
        return self._tuttleParam.getDoubleValueAtIndex(2)

    def getValueA(self):
        print "alpha value: ", self._tuttleParam.getDoubleValueAtIndex(3)
        return self._tuttleParam.getDoubleValueAtIndex(3)

    def getText(self):
        return self._tuttleParam.getName()[0].capitalize() + self._tuttleParam.getName()[1:]

    def getPositionColorSlider(self):
        print "colorSlider :", self._positionColorSlider
        return self._positionColorSlider

    def getPositionAlphaSlider(self):
        print "alphaSlider :", self._positionAlphaSlider
        return self._positionAlphaSlider

    def getPositionXcolorSelector(self):
        print "getColorselectorX :", self._positionXcolorSelector
        return self._positionXcolorSelector

    def getPositionYcolorSelector(self):
        print "getColorSelectorY :", self._positionYcolorSelector
        return self._positionYcolorSelector
        
    #################### setters ####################

    def setValueR(self, value1):
        self._tuttleParam.setValueAtIndex(0, float(value1 / 255))
        self.changed()

        print "Red : ", self.getValueR()

    def setValueG(self, value2):
        self._tuttleParam.setValueAtIndex(1, float(value2 / 255))
        self.changed()

        print "Green : ", self.getValueG()

    def setValueB(self, value3):
        self._tuttleParam.setValueAtIndex(2, float(value3 / 255))
        self.changed()

        print "Blue : ", self.getValueB()

    def setValueA(self, value4):
        self._tuttleParam.setValueAtIndex(3, float(value4 / 255))
        self.changed()

        print "Alpha : ", self.getValueA()

    def setPositionColorSlider(self, position):
        print "setcolorSlider: ", position
        self._positionColorSlider = position

    def setPositionAlphaSlider(self, position):
        print "setalphaSlider: ", position
        self._positionAlphaSlider = position

    def setPositionXcolorSelector(self, position):
        print "setcolorSelectorX: ", position
        self._positionXcolorSelector = position

    def setPositionYcolorSelector(self, position):
        print "setcolorSelectorY: ", position
        self._positionYcolorSelector = position

