from buttleofx.core.params import Param


class ParamPushButton(Param):
    """
        Core class, which represents a pushButton parameter.
    """

    def __init__(self, tuttleParam):
        Param.__init__(self, tuttleParam)

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getEnabled(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropEnabled")

    def getParamDoc(self):
        return self._tuttleParam.getProperties().getStringProperty("OfxParamPropHint")

    def getParamType(self):
        return "ParamPushButton"
