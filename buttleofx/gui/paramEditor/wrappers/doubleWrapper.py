from PySide import QtCore


class DoubleWrapper(QtCore.QObject):
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

    changed = QtCore.Signal()

    paramType = QtCore.Property(unicode, getParamType, notify=changed)
    text = QtCore.Property(unicode, getText, notify=changed)
    defaultValue = QtCore.Property(float, getDefaultValue, notify=changed)
    maximum = QtCore.Property(float, getMaximum, notify=changed)
    minimum = QtCore.Property(float, getMinimum, notify=changed)
