from PySide import QtCore


class PushButtonWrapper(QtCore.QObject):
    """
        Gui class, which maps a ParamPushButton.
    """

    def __init__(self, param):
        QtCore.QObject.__init__(self)
        self._param = param
        self._param.changed.connect(self.emitChanged)

    #################### getters ####################

    def getParamType(self):
        return self._param.getParamType()

    def getValue(self):
        self._param.getLabel()

    def getLabel(self):
        return self._param.getLabel()

    def getName(self):
        return self._param.getName()

    def getEnabled(self):
        return self._param.getEnabled()

    #################### setters ####################

    # def setParamType(self, paramType):
    #     self._param.setParamType(paramType)

    # def setLabel(self, label):
    #     self._param.setLabel(label)

    # def setValue(self, value):
    #     self._param.setValue(value)

    def setEnabled(self, enabled):
        self._param.setEnabled(enabled)

    @QtCore.Signal
    def changed(self):
        pass

    def emitChanged(self):
        self.changed.emit()

    ################################################## DATA EXPOSED TO QML ##################################################

    paramType = QtCore.Property(unicode, getParamType, constant=True)
    label = QtCore.Property(str, getLabel, constant=True)
    name = QtCore.Property(str, getName, constant=True)
    enabled = QtCore.Property(bool, getEnabled, setEnabled, notify=changed)
