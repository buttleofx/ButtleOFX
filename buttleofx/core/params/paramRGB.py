# common
from buttleofx.core.params import Param


class ParamRGB(Param):
    """
        Core class, which represents a RGB parameter.
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

    def setValue(self, values):
        self._tuttleParam.setValueAtIndex(0, values[0])
        self._tuttleParam.setValueAtIndex(1, values[1])
        self._tuttleParam.setValueAtIndex(2, values[2])

    def setValueR(self, value1):
        self._tuttleParam.setValueAtIndex(0, float(value1 / 255))

    def setValueG(self, value2):
        self._tuttleParam.setValueAtIndex(1, float(value2 / 255))

    def setValueB(self, value3):
        self._tuttleParam.setValueAtIndex(2, float(value3 / 255))
