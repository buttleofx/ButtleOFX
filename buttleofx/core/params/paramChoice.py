from quickmamba.patterns import Signal


class ParamChoice(object):
    """
        Core class, which represents a choice parameter.
        Contains :
            - _paramType : the name of the type of this parameter
            - _defaultValue : the default value for the input
            - _value : the value selected in the list the input
            - _listValue : the list of possible values
            - _text : the label of the input
    """

    def __init__(self, tuttleParam):
        self._tuttleParam = tuttleParam

        self._listValue = []
        for choice in range(tuttleParam.getProperties().fetchProperty("OfxParamPropChoiceOption").getDimension()):
            self._listValue.append(tuttleParam.getProperties().fetchProperty("OfxParamPropChoiceOption").getStringValue(choice))

        self.changed = Signal()

    #################### getters ####################

    def getTuttleParam(self):
        return self._tuttleParam

    def getParamType(self):
        return "ParamChoice"

    def getDefaultValue(self):
        return self._tuttleParam.getProperties().getStringProperty("OfxParamPropChoiceOption", 0)

    def getValue(self):
        return self._tuttleParam.getStringValue()

    def getListValue(self):
        return self._listValue

    def getText(self):
        return self._tuttleParam.getName()

    #################### setters ####################

    def setValue(self, value):
        self._tuttleParam.setValue(str(value))
        self.changed()

        print "TuttleParam new Value : ", self._tuttleParam.getStringValue()
