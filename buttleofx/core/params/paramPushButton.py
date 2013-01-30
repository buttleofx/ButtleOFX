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

        print "PUSH BUTTON / ", tuttleParam

        self.changed = Signal()

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
        self.changed()
        from buttleofx.data import ButtleDataSingleton
        buttleData = ButtleDataSingleton().get()
        buttleData.updateMapAndViewer()
