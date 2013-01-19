class ParamString(object):

    def __init__(self, defaultValue, stringType):
        self.paramType = "ParamString"
        self.defaultValue = defaultValue
        self.value = defaultValue
        self.stringType = stringType
