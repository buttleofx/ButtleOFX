from quickmamba.patterns import Signal


class ParamInt2D(object):
    """
        Core class, which represents a int2D parameter.
        Contains :
            - _paramType : the name of the type of this parameter
            - _defaultValue1 and _defaultValue2 : the default values for the 2 inputs
            - _value1 and _value2 : the values contained by the 2 inputs
            - _minimum1 and minimum2 : the min we can have for the 2 values
            - _maximum1 and maximum2 : the max we can have for the 2 values
            - _text : the label of the input
    """

    def __init__(self, defaultValue1, defaultValue2, minimum1, maximum1, minimum2, maximum2, text="default"):
        self._paramType = "ParamInt2D"
        self._defaultValue1 = defaultValue1
        self._defaultValue2 = defaultValue2
        self._value1 = defaultValue1
        self._value2 = defaultValue2
        self._minimum1 = minimum1
        self._maximum1 = maximum1
        self._minimum2 = minimum2
        self._maximum2 = maximum2
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

    def getMinimum1(self):
        return self._minimum1

    def getMaximum1(self):
        return self._maximum1

    def getMinimum2(self):
        return self._minimum2

    def getMaximum2(self):
        return self._maximum2

    def getText(self):
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

    def setMinimum1(self, minimum):
        self._minimum1 = minimum
        self.changed()

    def setMaximum1(self, maximum):
        self._maximum1 = maximum
        self.changed()

    def setMinimum2(self, minimum):
        self._minimum2 = minimum
        self.changed()

    def setMaximum2(self, maximum):
        self._maximum2 = maximum
        self.changed()

    def setText(self, text):
        self._text = text
        self.changed()
