from quickmamba.patterns import Signal


class ParamBoolean(object):

    def __init__(self, defaultValue, text):
        self.paramType = "ParamBoolean"
        self.defaultValue = defaultValue
        self.value = defaultValue
        self.text = text

        self.changed = Signal()

    #################### getters ####################

    def getParamType(self):
        return self.paramType

    def getDefaultValue(self):
        return self.defaultValue

    def getValue(self):
        return self.value

    def getText(self):
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

    def setText(self, text):
        self.text = text
        self.changed()
