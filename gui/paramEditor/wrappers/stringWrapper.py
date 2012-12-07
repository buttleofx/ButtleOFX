from PySide import QtCore


class StringWrapper(QtCore.QObject):
    def __init__(self, paramElmt):
        QtCore.QObject.__init__(self)
        self._paramType = paramElmt.paramType
        self._defaultValue = paramElmt.defaultValue
        self._stringType = paramElmt.stringType

    def getParamType(self):
        return self._paramType

    def getDefaultValue(self):
        return self._defaultValue

    def getStringType(self):
        return self._stringType

    defaultValueChanged = QtCore.Signal()
    stringTypeChanged = QtCore.Signal()

    # Just temporary : paramType must be constant
    changed = QtCore.Signal()

    paramType = QtCore.Property(unicode, getParamType, notify=changed)
    defaultValue = QtCore.Property(unicode, getDefaultValue, notify=defaultValueChanged)
    stringType = QtCore.Property(float, getStringType, notify=stringTypeChanged)
