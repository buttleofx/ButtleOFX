from quickmamba.patterns import Signal


class ParamDouble3D(object):
    """
        Core class, which represents a double3D parameter.
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
        return "ParamDouble3D"

    def getDefaultValue1(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDefault", 0)

    def getDefaultValue2(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDefault", 1)

    def getDefaultValue3(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDefault", 2)

    def getValue1(self):
        return self._tuttleParam.getDoubleValueAtIndex(0)

    def getValue2(self):
        return self._tuttleParam.getDoubleValueAtIndex(1)

    def getValue3(self):
        return self._tuttleParam.getDoubleValueAtIndex(2)

    def getMinimum1(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropMin", 0)

    def getMaximum1(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropMax", 0)

    def getMinimum2(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropMin", 1)

    def getMaximum2(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropMax", 1)

    def getMinimum3(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropMin", 2)

    def getMaximum3(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropMax", 2)

    def getText(self):
        return self._tuttleParam.getName()

    #################### setters ####################

    def setValue1(self, value1):
        self._tuttleParam.setValue([float(value), self.getValue2(), self.getValue3()])
        self.changed()

        print "TuttleParam new Value : ", self.getValue1()

    def setValue2(self, value2):
        self._tuttleParam.setValue([self.getValue1(), float(value), self.getValue3()])
        self.changed()

        print "TuttleParam new Value : ", self.getValue2()

    def setValue3(self, value3):
        self._tuttleParam.setValue([self.getValue1(), self.getValue2(), float(value)])
        self.changed()

        print "TuttleParam new Value : ", self.getValue3()
