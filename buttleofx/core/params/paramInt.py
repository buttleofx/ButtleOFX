from quickmamba.patterns import Signal


class ParamInt(object):
    """
        Core class, which represents an int parameter.
        Contains : 
            - _paramType : the name of the type of this parameter
            - _defaultValue : the default value for the input
            - _value : the value contained by the input
            - _minimum : the min we can have for the value
            - _maximum : the max we can have for the value
            - _text : the label of the input
    """

    def __init__(self, defaultValue, minimum, maximum, text):
        self._paramType = "ParamInt"
        self._defaultValue = defaultValue
        self._value = defaultValue
        self._minimum = minimum
        self._maximum = maximum
        self._text = text

        self.changed = Signal()

    #################### getters ####################

    def getParamType(self):
        return self._paramType

    def getDefaultValue(self):
        return self._defaultValue

    def getValue(self):
        return self._value

    def getMinimum(self):
        return self._minimum

    def getMaximum(self):
        return self._maximum

    def getText(self, text):
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

    def setMinimum(self, minimum):
        self._minimum = minimum
        self.changed()

    def setMaximum(self, maximum):
        self._maximum = maximum
        self.changed()

    def setText(self, text):
        self._text = text
        self.changed()