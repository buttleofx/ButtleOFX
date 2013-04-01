# common
from buttleofx.core.params import Param


class ParamPushButton(Param):
    """
        Core class, which represents a pushButton parameter.
    """

    def __init__(self, tuttleParam):
        Param.__init__(self, tuttleParam)
        
    #################### getters ####################
    
    def getParamType(self):
        return "ParamPushButton"

    def getEnabled(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropEnabled").getStringValue(0)
