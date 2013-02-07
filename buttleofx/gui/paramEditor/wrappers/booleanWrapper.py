from PySide import QtCore


class BooleanWrapper(QtCore.QObject):
    """
        Gui class, which maps a ParamBoolean.
    """

    def __init__(self, param):
        QtCore.QObject.__init__(self)
        self._param = param
        self._param.changed.connect(self.emitChanged)

    #################### getters ####################

    def getParamType(self):
        return self._param.getParamType()

    def getDefaultValue(self):
        return self._param.getDefaultValue()

    def getValue(self):
        return self._param.getValue()

    def getText(self):
        return self._param.getText()

    #################### setters ####################

    def setValue(self, value):
        self._param.setValue(value)

    @QtCore.Slot(bool)
    def pushValue(self, value):
        self._param.pushValue(value)

    @QtCore.Signal
    def changed(self):
        pass

    def emitChanged(self):
        self.changed.emit()

    ################################################## DATA EXPOSED TO QML ##################################################

    paramType = QtCore.Property(unicode, getParamType, notify=changed)
    value = QtCore.Property(bool, getValue, setValue, notify=changed)
    text = QtCore.Property(unicode, getText, notify=changed)
