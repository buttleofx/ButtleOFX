from quickmamba.patterns import Signal


class ParamInt3D(object):
    """
        Core class, which represents a int3D parameter.
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
        return "ParamInt3D"

    def getDefaultValue1(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropDefault", 0)

    def getDefaultValue2(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropDefault", 1)

    def getDefaultValue3(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropDefault", 2)

    def getValue1(self):
        return self._tuttleParam.getIntValueAtIndex(0)

    def getValue2(self):
        return self._tuttleParam.getIntValueAtIndex(1)

    def getValue3(self):
        return self._tuttleParam.getIntValueAtIndex(2)

    def getMinimum1(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMin", 0)

    def getMaximum1(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMax", 0)

    def getMinimum2(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMin", 1)

    def getMaximum2(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMax", 1)

    def getMinimum3(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMin", 2)

    def getMaximum3(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMax", 2)

    def getText(self):
        return self._tuttleParam.getName()

    #################### setters ####################

    def setValue1(self, value1):
        self._tuttleParam.setValue(int(value))
        self.changed()

        print "TuttleParam new Value : ", self.getValue1()

    def setValue2(self, value2):
        self._tuttleParam.setValue(int(value), 1)
        self.changed()

        print "TuttleParam new Value : ", self.getValue2()

    def setValue3(self, value3):
        self._tuttleParam.setValue(int(value), 2)
        self.changed()

        print "TuttleParam new Value : ", self.getValue3()
