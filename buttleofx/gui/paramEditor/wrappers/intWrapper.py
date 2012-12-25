from PySide import QtCore


class IntWrapper(QtCore.QObject):
    def __init__(self, paramElmt):
        QtCore.QObject.__init__(self)
        self._paramType = paramElmt.paramType
        self._text = paramElmt.text
        self._defaultValue = paramElmt.defaultValue
        self._maximum = paramElmt.maximum
        self._minimum = paramElmt.minimum

    def getParamType(self):
        return self._paramType

    def getText(self):
        return self._text

    def getDefaultValue(self):
        return self._defaultValue

    def getMaximum(self):
        return self._maximum

    def getMinimum(self):
        return self._minimum

    textChanged = QtCore.Signal()
    defaultValueChanged = QtCore.Signal()
    maximumChanged = QtCore.Signal()
    minimumChanged = QtCore.Signal()

    # Just temporary : paramType must be constant
    changed = QtCore.Signal()

    paramType = QtCore.Property(unicode, getParamType, notify=changed)
    text = QtCore.Property(unicode, getText, notify=textChanged)
    defaultValue = QtCore.Property(float, getDefaultValue, notify=defaultValueChanged)
    maximum = QtCore.Property(float, getMaximum, notify=maximumChanged)
    minimum = QtCore.Property(float, getMinimum, notify=minimumChanged)
