from quickmamba.patterns import Signal


class ParamInt2D(object):
    """
        Core class, which represents a int2D parameter.
        Contains : 
            - _tuttleParam : link to the corresponding tuttleParam
    """

    def __init__(self, tuttleParam):
        self._tuttleParam = tuttleParam

        self.changed = Signal()

    #################### getters ####################

    def getTuttleParam(self):
        return self._tuttleParam

    def getParamType(self):
        return "ParamInt2D"

    def getDefaultValue1(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropDefault", 0)

    def getDefaultValue2(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropDefault", 1)

    def getValue(self):
        return (self.getValue1(), self.getValue2())

    def getValue1(self):
        return self._tuttleParam.getIntValueAtIndex(0)

    def getValue2(self):
        return self._tuttleParam.getIntValueAtIndex(1)

    def getMinimum1(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMin", 0)

    def getMaximum1(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMax", 0)

    def getMinimum2(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMin", 1)

    def getMaximum2(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMax", 1)

    def getText(self):
        return self._tuttleParam.getName()

    #################### setters ####################

    def setValue(self, values):
        self.setValue1(values[0])
        self.setValue2(values[1])

    def setValue1(self, value):
        self._tuttleParam.setValue([int(value), self.getValue2()])
        self.changed()

    def setValue2(self, value):
        self._tuttleParam.setValue([self.getValue1(), int(value)])
        self.changed()
