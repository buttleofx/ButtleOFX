from buttleofx.core.params import Param


class ParamPage(Param):
    """
        Core class, which represents a page parameter.
        Contains :
            - _tuttleParam : link to the corresponding tuttleParam.
    """

    def __init__(self, tuttleParam):
        Param.__init__(self, tuttleParam)

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getLabel(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxPropLabel").getStringValueAt(0)

    def getParamDoc(self):
        return self._tuttleParam.getProperties().getStringProperty("OfxParamPropHint")

    def getParamType(self):
        return "ParamPage"

    def getValue(self):
        "Fix for saving graph because need to call getValue and getDefaultValue to save"
        return "ParamPage"

    def getDefaultValue(self):
        "Fix for saving graph because need to call getValue and getDefaultValue to save"
        return "ParamPage"
