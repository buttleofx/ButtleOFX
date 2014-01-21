# common
from buttleofx.core.params import Param


class ParamGroup(Param):
    """
        Core class, which represents a group parameter.
        Contains :
            - _tuttleParam : link to the corresponding tuttleParam
    """

    def __init__(self, tuttleParam):
        Param.__init__(self, tuttleParam)

    # #################### getters ####################

    def getParamType(self):
        return "ParamGroup"

    def getParamDoc(self):
        return self._tuttleParam.getProperties().getStringProperty("OfxParamPropHint")

    def getLabel(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxPropLabel").getStringValue(0)
    