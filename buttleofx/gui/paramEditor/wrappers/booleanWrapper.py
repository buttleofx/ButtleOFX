from PySide import QtCore


class BooleanWrapper(QtCore.QObject):
    def __init__(self, paramElmt):
        QtCore.QObject.__init__(self)
        self._paramType = paramElmt.paramType
        self._text = paramElmt.text
        self._defaultValue = paramElmt.defaultValue

    def getParamType(self):
        return self._paramType

    def getText(self):
        return self._text

    def getDefaultValue(self):
        return self._defaultValue

    textChanged = QtCore.Signal()
    defaultValueChanged = QtCore.Signal()

    # Just temporary : paramType must be constant
    changed = QtCore.Signal()

    paramType = QtCore.Property(unicode, getParamType, notify=changed)
    text = QtCore.Property(unicode, getText, notify=textChanged)
    defaultValue = QtCore.Property(bool, getDefaultValue, notify=defaultValueChanged)
