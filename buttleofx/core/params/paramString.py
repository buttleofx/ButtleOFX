from quickmamba.patterns import Signal


class ParamString(object):

    def __init__(self, defaultValue, stringType):
        self.paramType = "ParamString"
        self.defaultValue = defaultValue
        self.value = defaultValue
        self.stringType = stringType

        self.changed = Signal()

    #################### getters ####################

    def getParamType(self):
        return self.paramType

    def getDefaultValue(self):
        return self.defaultValue

    def getValue(self):
        return self.value

    def getStringType(self):
        return self.stringType

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

    def setStringType(self, stringType):
        self.stringType = stringType
        self.changed()
