class ParamInt2D(object):

    def __init__(self, defaultValue1, defaultValue2, minimum, maximum, text="default"):
        self.paramType = "ParamInt2D"
        self.value1 = defaultValue1
        self.value2 = defaultValue2
        self.minimum = minimum
        self.maximum = maximum
        self.text = text
