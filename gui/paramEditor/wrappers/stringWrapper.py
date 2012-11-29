from PySide import QtCore


class StringWrapper(QtCore.QObject):
    def __init__(self, paramElmt):
        QtCore.QObject.__init__(self)
        self._defaultValue = paramElmt.defaultValue
        self._stringType = paramElmt.stringType

    def getDefaultValue(self):
        return self._defaultValue

    def getStringType(self):
        return self._stringType

    defaultValueChanged = QtCore.Signal()
    stringTypeChanged = QtCore.Signal()

    defaultValue = QtCore.Property(unicode, getDefaultValue, notify=defaultValueChanged)
    stringType = QtCore.Property(float, getStringType, notify=stringTypeChanged)
