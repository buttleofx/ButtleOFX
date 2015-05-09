from buttleofx.core.params import Param


class ParamRGBA(Param):
    """
        Core class, which represents a RGBA parameter.
    """

    def __init__(self, tuttleParam):
        Param.__init__(self, tuttleParam)

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getDefaultR(self):
        return self._tuttleParam.getDoubleValueAtIndex(0)

    def getDefaultG(self):
        return self._tuttleParam.getDoubleValueAtIndex(1)

    def getDefaultB(self):
        return self._tuttleParam.getDoubleValueAtIndex(2)

    def getDefaultA(self):
        return self._tuttleParam.getDoubleValueAtIndex(3)

    def getDefaultValue(self):
        return (self.getDefaultR(), self.getDefaultG(), self.getDefaultB(), self.getDefaultA())

    def getParamDoc(self):
        return self._tuttleParam.getProperties().getStringProperty("OfxParamPropHint")

    def getParamType(self):
        return "ParamRGBA"

    def getValue(self):
        return (self.getValueR(), self.getValueG(), self.getValueB(), self.getValueA())

    def getValueR(self):
        return self._tuttleParam.getDoubleValueAtIndex(0)

    def getValueG(self):
        return self._tuttleParam.getDoubleValueAtIndex(1)

    def getValueB(self):
        return self._tuttleParam.getDoubleValueAtIndex(2)

    def getValueA(self):
        return self._tuttleParam.getDoubleValueAtIndex(3)

    # ## Setters ## #

    def setValue(self, values):
        self._tuttleParam.setValueAtIndex(0, values[0])
        self._tuttleParam.setValueAtIndex(1, values[1])
        self._tuttleParam.setValueAtIndex(2, values[2])
        self._tuttleParam.setValueAtIndex(3, values[3])

        self.paramChanged()

    def setValueR(self, value1):
        self._tuttleParam.setValueAtIndex(0, value1)
        self.paramChanged()
        # logging.debug("Red : %s" % self.getValueR())

    def setValueG(self, value2):
        self._tuttleParam.setValueAtIndex(1, value2)
        self.paramChanged()
        # logging.debug("Green : %s" % self.getValueG())

    def setValueB(self, value3):
        self._tuttleParam.setValueAtIndex(2, value3)
        self.paramChanged()
        # logging.debug("Blue : %s" % self.getValueB())

    def setValueA(self, value4):
        self._tuttleParam.setValueAtIndex(3, value4)
        self.paramChanged()
        # logging.debug("Alpha : ", self.getValueA())

    # setValue on RGBA doesn't work?
    # def setValue(self, r, g, b, a):
    #    self._tuttleParam.setValue(r, g, b, a)
