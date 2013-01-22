from PySide import QtCore


class StringWrapper(QtCore.QObject):
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

    def getStringType(self):
        return self._param.getStringType()

    #################### setters ####################

    def setParamType(self, paramType):
        self._param.setParamType(paramType)

    def setDefaultValue(self, defaultValue):
        self._param.setDefaultValue(defaultValue)

    def setValue(self, value):
        self._param.setValue(value)

    def setStringType(self, stringType):
        self._param.setStringType(stringType)

    @QtCore.Signal
    def changed(self):
        pass

    def emitChanged(self):
        self.changed.emit()

    paramType = QtCore.Property(unicode, getParamType, setParamType, notify=changed)
    value = QtCore.Property(str, getValue, setValue, notify=changed)
    stringType = QtCore.Property(str, getStringType, setStringType, notify=changed)
