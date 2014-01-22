# common
from buttleofx.core.params import Param


class ParamPage(Param):
    """
        Core class, which represents a page parameter.
        Contains :
            - _tuttleParam : link to the corresponding tuttleParam.
    """

    def __init__(self, tuttleParam):
        Param.__init__(self, tuttleParam)

    # #################### getters ####################

    def getParamType(self):
        return "ParamPage"

    def getParamDoc(self):
        return self._tuttleParam.getProperties().getStringProperty("OfxParamPropHint")

    def getLabel(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxPropLabel").getStringValue(0)
