# common
from buttleofx.core.params import Param


class ParamRGB(Param):
    """
        Core class, which represents a RGB parameter.
        Contains :
            - _tuttleParam : link to the corresponding tuttleParam.
    """

    def __init__(self, tuttleParam):
        Param.__init__(self)
        
        self._tuttleParam = tuttleParam

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

    def getValue(self):
        return (self.getValueR(), self.getValueG(), self.getValueB())

    def getValueR(self):
        return self._tuttleParam.getDoubleValueAtIndex(0)

    def getValueG(self):
        return self._tuttleParam.getDoubleValueAtIndex(1)

    def getValueB(self):
        return self._tuttleParam.getDoubleValueAtIndex(2)

    def getText(self):
        return self._tuttleParam.getName()[0].capitalize() + self._tuttleParam.getName()[1:]

    #################### setters ####################

    def setValueR(self, value1):
        self._tuttleParam.setValueAtIndex(0, float(value1 / 255))
        self.paramChanged()

        print "Rouge : ", self.getValueR()

    def setValueG(self, value2):
        self._tuttleParam.setValueAtIndex(1, float(value2 / 255))
        self.paramChanged()

        print "Vert : ", self.getValueG()

    def setValueB(self, value3):
        self._tuttleParam.setValueAtIndex(2, float(value3 / 255))
        self.paramChanged()

        print "Blue : ", self.getValueB()
