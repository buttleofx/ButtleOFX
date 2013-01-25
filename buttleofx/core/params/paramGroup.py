from quickmamba.patterns import Signal


class ParamGroup(object):
    """
        Core class, which represents a group parameter.
        Contains :
            - _tuttleParam : link to the corresponding tuttleParam
    """

    def __init__(self, tuttleParam):
        self._tuttleParam = tuttleParam

        self.changed = Signal()

    # #################### getters ####################

    # def getTuttleParam(self):
    #     return self._tuttleParam

    def getParamType(self):
        return "ParamGroup"

    def getLabel(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxPropLabel").getStringValue(0)

    def getName(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxPropName").getStringValue(0)
