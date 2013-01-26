from quickmamba.patterns import Signal


class ParamPushButton(object):
    """
        Core class, which represents a pushButton parameter.
        Contains : 
            - _paramType : the name of the type of this parameter
            - _label : the label display on the push button
            - _trigger : the function launch when the push button is clicked
            - _enabled : flag to see if the push button is clickable or not 
    """

    def __init__(self, tuttleParam):
        self._tuttleParam = tuttleParam

        self.changed = Signal()

    #################### getters ####################

    def getTuttleParam(self):
        return self._tuttleParam

    def getParamType(self):
        return "ParamPushButton"

    def getLabel(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxPropName").getStringValue(0)

    def getEnabled(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)

    #################### setters ####################

    def setEnabled(self, enabled):
        self._tuttleParam.getProperties().seValue(enabled)
        self.changed()

        print "TuttleParam new Value : ", self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)