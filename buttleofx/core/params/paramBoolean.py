from quickmamba.patterns import Signal


class ParamBoolean(object):
    """
        Core class, which represents a boolean parameter.
        Contains :
            - _tuttleParam : link to the corresponding tuttleParam
            - _paramType : the name of the type of this parameter
            - _defaultValue : the default value for the input
            - _value : the value contained by the input
            - _text : the label of the input
    """

    def __init__(self, tuttleParam):
        self._tuttleParam = tuttleParam

        self.changed = Signal()

    #################### getters ####################

    def getTuttleParam(self):
        return self._tuttleParam

    def getParamType(self):
        return "ParamBoolean"

    def getDefaultValue(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)

    def getValue(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)

    def getText(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxPropName").getStringValue(0)

    #################### setters ####################

    def setValue(self, value):
        self._tuttleParam.getProperties().seValue(value)
        self.changed()

        print "TuttleParam new Value : ", self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)