from quickmamba.patterns import Signal


class ParamDouble3D(object):
    """
        Core class, which represents a double3D parameter.
        Contains : 
            - _paramType : the name of the type of this parameter
            - _defaultValue1, _defaultValue2, and _defaultValue3 : the default values for the 3 inputs
            - _value1, _value2 and _value3 : the values contained by the 3 inputs
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
        return "ParamDouble3D"

    def getDefaultValue1(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)

    def getDefaultValue2(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(1)

    def getDefaultValue3(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(2)

    def getValue1(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)

    def getValue2(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(1)

    def getValue3(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(2)

    def getMinimum(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropMin").getStringValue(0)

    def getMaximum(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropMax").getStringValue(0)

    def getText(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxPropName").getStringValue(0)

    #################### setters ####################

    def setValue1(self, value1):
        self._tuttleParam.getProperties().setDoubleProperty("OfxParamPropDefault", float(value), 0)
        self.changed()

        print "TuttleParam new Value : ", self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)

    def setValue2(self, value2):
        self._tuttleParam.getProperties().setDoubleProperty("OfxParamPropDefault", float(value), 1)
        self.changed()

        print "TuttleParam new Value : ", self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(1)

    def setValue3(self, value3):
        self._tuttleParam.getProperties().setDoubleProperty("OfxParamPropDefault", float(value), 2)
        self.changed()

        print "TuttleParam new Value : ", self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(3)
