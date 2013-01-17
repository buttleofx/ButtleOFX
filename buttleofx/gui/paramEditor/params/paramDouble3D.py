class ParamDouble3D(object):

    def __init__(self, defaultValue, minimum, maximum, text="default"):
        self.paramType = "ParamDouble3D"
        self.defaultValue1 = defaultValue
        self.defaultValue2 = defaultValue
        self.defaultValue3 = defaultValue
        self.minimum = minimum
        self.maximum = maximum
        self.text = text
