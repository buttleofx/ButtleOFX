class ParamDouble3D(object):

    def __init__(self, defaultValue1, defaultValue2, defaultValue3, minimum, maximum, text="default"):
        self.paramType = "ParamDouble3D"
        self.defaultValue1 = defaultValue1
        self.defaultValue2 = defaultValue2
        self.defaultValue3 = defaultValue3
        self.minimum = minimum
        self.maximum = maximum
        self.text = text
