from quickmamba.patterns import Signal


class ParamInt2D(object):
    """
        Core class, which represents an int parameter.
        Contains : 
            - _paramType : the name of the type of this parameter
            - _defaultValue1 and _defaultValue2 : the default values for the 2 inputs
            - _value1 and _value2 : the values contained by the 2 inputs
            - _minimum : the min we can have for the value
            - _maximum : the max we can have for the value
            - _text : the label of the input
    """

    def __init__(self, defaultValue1, defaultValue2, minimum, maximum, text="default"):
        self._paramType = "ParamInt2D"
        self._defaultValue1 = defaultValue1
        self._defaultValue2 = defaultValue2
        self._value1 = defaultValue1
        self._value2 = defaultValue2
        self._minimum = minimum
        self._maximum = maximum
        self._text = text

        self.changed = Signal()

    #################### getters ####################

    def getParamType(self):
        return self._paramType

    def getDefaultValue1(self):
        return self._defaultValue1

    def getDefaultValue2(self):
        return self._defaultValue2

    def getValue1(self):
        return self._value1

    def getValue2(self):
        return self._value2

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

    def setDefaultValue1(self, defaultValue):
        self._defaultValue1 = defaultValue
        self.changed()

    def setDefaultValue2(self, defaultValue):
        self._defaultValue2 = defaultValue
        self.changed()

    def setValue1(self, value):
        self._value1 = value
        self.changed()

    def setValue2(self, value):
        self._value2 = value
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
