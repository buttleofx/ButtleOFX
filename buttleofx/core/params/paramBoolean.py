from quickmamba.patterns import Signal


class ParamBoolean(object):
    """
        Core class, which represents a boolean parameter.
        Contains :
            - _tuttleParam : link to the corresponding tuttleParam
    """

    def __init__(self, tuttleParam):
        self._tuttleParam = tuttleParam
        #buttleData = ButtleDataSingleton().get()
        self.changed = Signal()
        #self.changed.connect(buttleData.paramChanged)

    #################### getters ####################

    def getTuttleParam(self):
        return self._tuttleParam

    def getParamType(self):
        return "ParamBoolean"

    def getDefaultValue(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropDefault")

    def getValue(self):
        return self._tuttleParam.getBoolValue()

    def getText(self):
        return self._tuttleParam.getName()

    #################### setters ####################

    def setValue(self, value):
        self._tuttleParam.setValue(value)
        self.changed()
        # data
        from buttleofx.data import ButtleDataSingleton
        buttleData = ButtleDataSingleton().get()
        buttleData.updateMapAndViewer()
