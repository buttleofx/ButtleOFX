from PySide import QtCore


class StringWrapper(QtCore.QObject):
    def __init__(self, paramElmt):
        QtCore.QObject.__init__(self)
        self._paramType = paramElmt.paramType
        self._defaultValue = paramElmt.defaultValue
        self._stringType = paramElmt.stringType

    #################### getters ####################

    def getParamType(self):
        return self._paramType

    def getDefaultValue(self):
        return self._defaultValue

    def getStringType(self):
        return self._stringType

    #################### setters ####################

    def setParamType(self, paramType):
        self._paramType = paramType

    @QtCore.Slot(str)
    def setDefaultValue(self, defaultValue):
        self._defaultValue = defaultValue
        self.changed.emit()

    def setStringType(self, stringType):
        self._stringType = stringType

    changed = QtCore.Signal()

    paramType = QtCore.Property(str, getParamType, setParamType, notify=changed)
    defaultValue = QtCore.Property(str, getDefaultValue, setDefaultValue, notify=changed)
    stringType = QtCore.Property(str, getStringType, setStringType, notify=changed)
