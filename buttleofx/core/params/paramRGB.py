from quickmamba.patterns import Signal


class ParamRGB(object):
    """
        Core class, which represents a RGB parameter.
        Contains :
            - _paramType : the name of the type of this parameter
    """

    def __init__(self, tuttleParam):
        self._tuttleParam = tuttleParam

        self.changed = Signal()

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

    def getValueR(self):
        return self._tuttleParam.getDoubleValueAtIndex(0)

    def getValueG(self):
        return self._tuttleParam.getDoubleValueAtIndex(1)

    def getValueB(self):
        return self._tuttleParam.getDoubleValueAtIndex(2)

    def getText(self):
        return self._tuttleParam.getName()

    #################### setters ####################

    def setValueR(self, value1):
        self._tuttleParam.setValueAtIndex(0, float(value1))
        self.changed()

        print "TuttleParam new Value : ", self.getValueR()

    def setValueG(self, value2):
        self._tuttleParam.setValueAtIndex(1, float(value2))
        self.changed()

        print "TuttleParam new Value : ", self.getValueG()

    def setValueB(self, value3):
        self._tuttleParam.setValueAtIndex(2, float(value3))

        print "TuttleParam new Value : ", self.getValueB()
