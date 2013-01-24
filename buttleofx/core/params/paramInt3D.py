from quickmamba.patterns import Signal


class ParamInt3D(object):
    """
        Core class, which represents a int3D parameter.
        Contains :
            - _paramType : the name of the type of this parameter
            - _defaultValue1, _defaultValue2 and _defaultValue3 : the default values for the 3 inputs
            - _value1, _value2 and _value3 : the values contained by the 3 inputs
            - _minimum1, _minimum2 and _minimum3 : the min we can have for the 3 values
            - _maximum1, _maximum2 and _minimum3 : the max we can have for the 3 values
            - _text : the label of the input
    """

    def __init__(self, defaultValue1, defaultValue2, defaultValue3, minimum1, maximum1, minimum2, maximum2, minimum3, maximum3, text="default"):
        self._paramType = "ParamInt2D"
        self._defaultValue1 = defaultValue1
        self._defaultValue2 = defaultValue2
        self._defaultValue3 = defaultValue3
        self._value1 = defaultValue1
        self._value2 = defaultValue2
        self._value3 = defaultValue3
        self._minimum1 = minimum1
        self._maximum1 = maximum1
        self._minimum2 = minimum2
        self._maximum2 = maximum2
        self._minimum3 = minimum3
        self._maximum3 = maximum3
        self._text = text

        self.changed = Signal()

    #################### getters ####################

    def getParamType(self):
        return self._paramType

    def getDefaultValue1(self):
        return self._defaultValue1

    def getDefaultValue2(self):
        return self._defaultValue2

    def getDefaultValue3(self):
        return self._defaultValue3

    def getValue1(self):
        return self._value1

    def getValue2(self):
        return self._value2

    def getValue3(self):
        return self._value3

    def getMinimum1(self):
        return self._minimum1

    def getMaximum1(self):
        return self._maximum1

    def getMinimum2(self):
        return self._minimum2

    def getMaximum2(self):
        return self._maximum2

    def getMinimum3(self):
        return self._minimum3

    def getMaximum3(self):
        return self._maximum3

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

    def setDefaultValue3(self, defaultValue):
        self._defaultValue3 = defaultValue
        self.changed()

    def setValue1(self, value):
        self._value1 = value
        self.changed()

    def setValue2(self, value):
        self._value2 = value
        self.changed()

    def setValue3(self, value):
        self._value3 = value
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

    def setMinimum3(self, minimum):
        self._minimum3 = minimum
        self.changed()

    def setMaximum3(self, maximum):
        self._maximum3 = maximum
        self.changed()

    def setText(self, text):
        self._text = text
        self.changed()
