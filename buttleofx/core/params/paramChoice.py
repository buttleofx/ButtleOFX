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

    def __init__(self, defaultValue, listValue, text):
        self._paramType = "ParamChoice"
        self._defaultValue = defaultValue
        self._value = defaultValue
        self._listValue = listValue
        self._text = text

        self.changed = Signal()

    #################### getters ####################

    def getParamType(self):
        return self._paramType

    def getDefaultValue(self):
        return self._defaultValue

    def getValue(self):
        return self._value

    def getListValue(self):
        return self._listValue

    def getText(self):
        return self._text

    #################### setters ####################

    def setParamType(self, paramType):
        self._paramType = paramType
        self.changed()

    def setDefaultValue(self, defaultValue):
        self._defaultValue = defaultValue
        self.changed()

    def setValue(self, value):
        self._value = value
        self.changed()

    def setListValue(self, listValue):
        self._listValue = listValue
        self.changed()

    def setText(self, text):
        self._text = text
        self.changed()
