from quickmamba.patterns import Signal


class ParamRGB(object):
    """
        Core class, which represents a RGB parameter.
        Contains :
            - _tuttleParam : link to the corresponding tuttleParam.
            - changed : signal emitted when we set value(s) of the param.
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
        self.setValueR(values[0])
        self.setValueG(values[1])
        self.setValueB(values[2])

    def setValueR(self, value1):
        self._tuttleParam.setValueAtIndex(0, float(value1 / 255))
        self.changed()

        print "Rouge : ", self.getValueR()

    def setValueG(self, value2):
        self._tuttleParam.setValueAtIndex(1, float(value2 / 255))
        self.changed()

        print "Vert : ", self.getValueG()

    def setValueB(self, value3):
        self._tuttleParam.setValueAtIndex(2, float(value3 / 255))
        self.changed()

        print "Blue : ", self.getValueB()
