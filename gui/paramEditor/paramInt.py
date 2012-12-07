class ParamInt(object):

    def __init__(self, defaultValue, minimum, maximum, text="default"):
        self.paramType = "ParamInt.qml"
        self.defaultValue = defaultValue
        self.minimum = minimum
        self.maximum = maximum
        self.text = text
