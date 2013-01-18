class ParamDouble(object):

    def __init__(self, defaultValue, minimum, maximum, text="default"):
        self.paramType = "ParamDouble"
        self.defaultValue = defaultValue
        self.value = defaultValue
        self.minimum = minimum
        self.maximum = maximum
        self.text = text
