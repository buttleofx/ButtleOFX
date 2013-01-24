from quickmamba.patterns import Signal


class ParamInt2D(object):
    """
        Core class, which represents a int2D parameter.
        Contains : 
            - _tuttleParam : link to the corresponding tuttleParam
            - _paramType : the name of the type of this parameter
            - _defaultValue1 and _defaultValue2 : the default values for the 2 inputs
            - _value1 and _value2 : the values contained by the 2 inputs
            - _minimum : the min we can have for the value
            - _maximum : the max we can have for the value
            - _text : the label of the input
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
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)

    def getDefaultValue2(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(1)

    def getValue1(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)

    def getValue2(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(1)

    def getMinimum(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropMin").getStringValue(0)

    def getMaximum(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropMax").getStringValue(0)

    def getText(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxPropName").getStringValue(0)

    #################### setters ####################

    def setValue1(self, value):
        self._tuttleParam.getProperties().setIntProperty("OfxParamPropDefault", float(value), 0)
        self.changed()

        print "TuttleParam new Value : ", self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)

    def setValue2(self, value):
        self._tuttleParam.getProperties().setIntProperty("OfxParamPropDefault", float(value), 1)
        self.changed()

        print "TuttleParam new Value : ", self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(1)