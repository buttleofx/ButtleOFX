# common
from buttleofx.core.params import Param
# from quickmamba.gui import ColorExtended


class ParamRGBA(Param):
    """
        Core class, which represents a RGBA parameter.
    """

    def __init__(self, tuttleParam):
        Param.__init__(self, tuttleParam)

    #################### getters ####################

    def getParamType(self):
        return "ParamRGBA"

    def getDefaultR(self):
        return self._tuttleParam.getDoubleValueAtIndex(0)

    def getDefaultG(self):
        return self._tuttleParam.getDoubleValueAtIndex(1)

    def getDefaultB(self):
        return self._tuttleParam.getDoubleValueAtIndex(2)

    def getDefaultA(self):
        return self._tuttleParam.getDoubleValueAtIndex(3)

    def getValue(self):
        return (self.getValueR(), self.getValueG(), self.getValueB(), self.getValueA())

    def getValueR(self):
        #print "red value: ", self._tuttleParam.getDoubleValueAtIndex(0)
        return self._tuttleParam.getDoubleValueAtIndex(0)

    def getValueG(self):
        #print "green value: ", self._tuttleParam.getDoubleValueAtIndex(1)
        return self._tuttleParam.getDoubleValueAtIndex(1)

    def getValueB(self):
        #print "blue value: ", self._tuttleParam.getDoubleValueAtIndex(2)
        return self._tuttleParam.getDoubleValueAtIndex(2)

    def getValueA(self):
        #print "alpha value: ", self._tuttleParam.getDoubleValueAtIndex(3)
        return self._tuttleParam.getDoubleValueAtIndex(3)

    #################### setters ####################

    def setValue(self, values):
        self._tuttleParam.setValueAtIndex(0, values[0])
        self._tuttleParam.setValueAtIndex(1, values[1])
        self._tuttleParam.setValueAtIndex(2, values[2])
        self._tuttleParam.setValueAtIndex(3, values[3])

        self.paramChanged()

    def setValueR(self, value1):
        self._tuttleParam.setValueAtIndex(0, value1)
        self.paramChanged()
        #print "Red : ", self.getValueR()

    def setValueG(self, value2):
        self._tuttleParam.setValueAtIndex(1, value2)
        self.paramChanged()
        #print "Green : ", self.getValueG()

    def setValueB(self, value3):
        self._tuttleParam.setValueAtIndex(2, value3)
        self.paramChanged()
        #print "Blue : ", self.getValueB()

    def setValueA(self, value4):
        self._tuttleParam.setValueAtIndex(3, value4)
        self.paramChanged()
        #print "Alpha : ", self.getValueA()

    #setValue on rgba doesn't work ?
    #def setValue(self, r, g, b, a):
    #   self._tuttleParam.setValue(r, g, b, a)
