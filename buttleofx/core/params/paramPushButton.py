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

    def __init__(self, label, trigger, enabled=True):
        self._paramType = "ParamPushButton"
        self._label = label
        self._trigger = trigger
        self._enabled = enabled

        self.changed = Signal()

    #################### getters ####################

    def getParamType(self):
        return self._paramType

    def getLabel(self):
        return self._label

    def getTrigger(self):
        return self._trigger

    def getEnabled(self):
        return self._enabled

    #################### setters ####################

    def setParamType(self, paramType):
        self._paramType = paramType
        self.changed()

    def setLabel(self, label):
        self._label = label
        self.changed()

    def setTrigger(self, trigger):
        self._trigger = trigger
        self.changed()

    def setEnabled(self, enabled):
        self._enabled = enabled
        self.changed()
