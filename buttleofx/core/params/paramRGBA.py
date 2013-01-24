from quickmamba.patterns import Signal


class ParamRGBA(object):
    """
        Core class, which represents a RGBA parameter.
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
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)

    def getDefaultG(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(1)

    def getDefaultB(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(2)

    def getDefaultA(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(2)

    def getValueR(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)

    def getValueG(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(1)

    def getValueB(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(2)

    def getValueA(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(2)

    def getText(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxPropName").getStringValue(0)

    #################### setters ####################

    def setValueR(self, value1):
        self._tuttleParam.getProperties().setIntProperty("OfxParamPropDefault", float(value), 0)
        self.changed()

        print "TuttleParam new Value : ", self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)

    def setValueG(self, value2):
        self._tuttleParam.getProperties().setIntProperty("OfxParamPropDefault", float(value), 1)
        self.changed()

        print "TuttleParam new Value : ", self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(1)

    def setValueB(self, value3):
        self._tuttleParam.getProperties().setIntProperty("OfxParamPropDefault", float(value), 2)

        print "TuttleParam new Value : ", self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(3)

    def setValueA(self, value3):
        self._tuttleParam.getProperties().setIntProperty("OfxParamPropDefault", float(value), 3)

        print "TuttleParam new Value : ", self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(4)
