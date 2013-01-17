from PySide import QtCore


class Double2DWrapper(QtCore.QObject):
    def __init__(self, paramElmt):
        QtCore.QObject.__init__(self)
        self._paramType = paramElmt.paramType
        self._text = paramElmt.text
        self._defaultValue1 = paramElmt.defaultValue1
        self._defaultValue2 = paramElmt.defaultValue2
        self._maximum = paramElmt.maximum
        self._minimum = paramElmt.minimum

    def getParamType(self):
        return self._paramType

    def getText(self):
        return self._text

    def getDefaultValue1(self):
        return self._defaultValue1

    def getDefaultValue2(self):
        return self._defaultValue2

    def getMaximum(self):
        return self._maximum

    def getMinimum(self):
        return self._minimum

    changed = QtCore.Signal()

    paramType = QtCore.Property(unicode, getParamType, notify=changed)
    text = QtCore.Property(unicode, getText, notify=changed)
    defaultValue1 = QtCore.Property(float, getDefaultValue1, notify=changed)
    defaultValue2 = QtCore.Property(float, getDefaultValue2, notify=changed)
    maximum = QtCore.Property(float, getMaximum, notify=changed)
    minimum = QtCore.Property(float, getMinimum, notify=changed)
