from quickmamba.patterns import Signal


class ParamString(object):
    """
        Core class, which represents a string parameter.
        Contains : 
            - _paramType : the name of the type of this parameter
            - _defaultValue : the default value for the input
            - _value : the value contained by the input
            - _stringType : the type of the string (url, path...)
            - _text : the label of the input
    """

    def __init__(self, defaultValue, stringType, text):
        self._paramType = "ParamString"
        self._defaultValue = defaultValue
        self._value = defaultValue
        self._stringType = stringType
        self._text = text

        self.changed = Signal()

    #################### getters ####################

    def getParamType(self):
        return self._paramType

    def getDefaultValue(self):
        return self._defaultValue

    def getValue(self):
        return self._value

    def getStringType(self):
        return self._stringType

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

    def setStringType(self, stringType):
        self._stringType = stringType
        self.changed()

    def setText(self, text):
        self._text = text
        self.changed()
