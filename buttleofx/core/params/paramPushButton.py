# common
from buttleofx.core.params import Param


class ParamPushButton(Param):
    """
        Core class, which represents a pushButton parameter.
        Contains : 
            - _tuttleParam : link to the corresponding tuttleParam.
    """

    def __init__(self, tuttleParam):
        Param.__init__(self)
        
        self._tuttleParam = tuttleParam

    #################### getters ####################

    def getTuttleParam(self):
        return self._tuttleParam

    def getParamType(self):
        return "ParamPushButton"

    def getValue(self):
        self.getLabel()

    def getName(self):
        return self._tuttleParam.getName()[0].capitalize() + self._tuttleParam.getName()[1:]

    def getLabel(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxPropLabel").getStringValue(0)

    def getEnabled(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropEnabled").getStringValue(0)

    #################### setters ####################

    # def setValue(self, value):
    #     self.setEnabled()

    def setEnabled(self, enabled):
        self._tuttleParam.setValue(enabled)
