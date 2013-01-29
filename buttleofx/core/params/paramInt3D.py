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

    def getValue(self):
        return (self.getValue1(), self.getValue2(), self.getValue3())

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

    def setValue(self, values):
        self.setValue1(values[0])
        self.setValue2(values[1])
        self.setValue3(values[2])

    def setValue1(self, value1):
        self._tuttleParam.setValue([int(value1), self.getValue2(), self.getValue2()])
        self.changed()

    def setValue2(self, value2):
        self._tuttleParam.setValue([self.getValue1(), int(value2), self.getValue3()])
        self.changed()

    def setValue3(self, value3):
        self._tuttleParam.setValue([self.getValue1(), self.getValue2(), int(value3)])
        self.changed()
