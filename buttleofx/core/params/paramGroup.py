from buttleofx.core.params import Param


class ParamGroup(Param):
    """
        Core class, which represents a group parameter.
        Contains :
            - _tuttleParam : link to the corresponding tuttleParam
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
        return "ParamGroup"

    def getValue(self):
        "Fix for save graph because need to call getValue and getDefaultValue to save"
        return "ParamGroup"
    
    def getDefaultValue(self):
        "Fix for save graph because need to call getValue and getDefaultValue to save"
        return "ParamGroup"
