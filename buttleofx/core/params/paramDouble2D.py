from quickmamba.patterns import Signal


class ParamDouble2D(object):

    def __init__(self, defaultValue1, defaultValue2, minimum, maximum, text):
        self.paramType = "ParamDouble2D"
        self.defaultValue1 = defaultValue1
        self.defaultValue2 = defaultValue2
        self.value1 = defaultValue1
        self.value2 = defaultValue2
        self.minimum = minimum
        self.maximum = maximum
        self.text = text

        self.changed = Signal()

    #################### getters ####################

    def getParamType(self):
        return self.paramType

    def getDefaultValue1(self):
        return self.defaultValue1

    def getDefaultValue2(self):
        return self.defaultValue2

    def getValue1(self):
        return self.value1

    def getValue2(self):
        return self.value2

    def getMinimum(self):
        return self.minimum

    def getMaximum(self):
        return self.maximum

    def getText(self, text):
        return self.text

    #################### setters ####################

    def setParamType(self, paramType):
        self.paramType = paramType
        self.changed()

    def setDefaultValue1(self, defaultValue1):
        self.defaultValue1 = defaultValue1
        self.changed()

    def setDefaultValue2(self, defaultValue2):
        self.defaultValue2 = defaultValue2
        self.changed()

    def setValue1(self, value1):
        self.value1 = value1
        self.changed()

    def setValue2(self, value2):
        self.value2 = value2
        self.changed()

    def setMinimum(self, minimum):
        self.minimum = minimum
        self.changed()

    def setMaximum(self, maximum):
        self.maximum = maximum
        self.changed()

    def setText(self, text):
        self.text = text
        self.changed()
