

class ParamGroup(object):
    """
        Core class, which represents a group parameter.
        Contains :
            - _tuttleParam : link to the corresponding tuttleParam
    """

    def __init__(self, tuttleParam):
        self._tuttleParam = tuttleParam

        self.changed = None # important for the nodeManager -> creationNode() function.

    # #################### getters ####################

    def getTuttleParam(self):
        return self._tuttleParam

    def getParamType(self):
        return "ParamGroup"

    def getLabel(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxPropLabel").getStringValue(0)

    def getName(self):
        return self._tuttleParam.getName()[0].capitalize() + self._tuttleParam.getName()[1:]
        
    def isSecret(self):
        return self._tuttleParam.getSecret()
