from PySide import QtCore


class PushButtonWrapper(QtCore.QObject):
    def __init__(self, param):
        QtCore.QObject.__init__(self)
        self._param = param

    #################### getters ####################

    def getParamType(self):
        return self._param.paramType

    def getText(self):
        return self._param.text

    def getLabel(self):
        return self._param.label

    def getTrigger(self):
        return self._param.trigger

    def getEnabled(self):
        return self._param.enabled

    #################### setters ####################

    def setParamType(self, paramType):
        self._param.paramType = paramType

    def setText(self, text):
        self._param.text = text

    def setLabel(self, label):
        self._param.label = label

    def setTrigger(self, trigger):
        self._param.trigger = trigger

    def setEnabled(self, enabled):
        self._param.enabled = enabled

    # Just temporary : paramType must be constant
    changed = QtCore.Signal()

    paramType = QtCore.Property(unicode, getParamType, setParamType, notify=changed)
    text = QtCore.Property(unicode, getText, setText, notify=changed)
    label = QtCore.Property(bool, getLabel, setLabel, notify=changed)
    trigger = QtCore.Property(bool, getTrigger, setTrigger, notify=changed)
    enabled = QtCore.Property(bool, getEnabled, setEnabled, notify=changed)
