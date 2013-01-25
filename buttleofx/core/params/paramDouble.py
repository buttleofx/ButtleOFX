from quickmamba.patterns import Signal


class ParamDouble(object):
    """
        Core class, which represents a double parameter.
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
        return "ParamDouble"

    def getDefaultValue(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)

    def getValue(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)

    def getMinimum(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDisplayMin").getStringValue(0)

    def getMaximum(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDisplayMax").getStringValue(0)

    def getText(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxPropName").getStringValue(0)

    #################### setters ####################

    def setValue(self, value):
        self._tuttleParam.getProperties().setDoubleProperty("OfxParamPropDefault", float(value))
        self.changed()

        print "TuttleParam new Value : ", self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)
