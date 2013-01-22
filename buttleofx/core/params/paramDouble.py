from quickmamba.patterns import Signal


class ParamDouble(object):

    def __init__(self, defaultValue, minimum, maximum, text):
        self.paramType = "ParamDouble"
        self.defaultValue = defaultValue
        self.value = defaultValue
        self.minimum = minimum
        self.maximum = maximum
        self.text = text

        self.changed = Signal()

    #################### getters ####################

    def getParamType(self):
        return self.paramType

    def getDefaultValue(self):
        return self.defaultValue

    def getValue(self):
        return self.value

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

    def setDefaultValue(self, defaultValue):
        self.defaultValue = defaultValue
        self.changed()

    def setValue(self, value):
        self.value = value
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
