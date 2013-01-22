class ParamChoice(object):

    def __init__(self, defaultValue, listValue, text="default"):
        self.paramType = "ParamChoice"
        self.defaultValue = defaultValue
        self.value = defaultValue
        self.listValue = listValue
        self.text = text

