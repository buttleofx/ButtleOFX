from PySide import QtCore


class Double2DWrapper(QtCore.QObject):
    def __init__(self, paramElmt):
        QtCore.QObject.__init__(self)
        self._paramType = paramElmt.paramType
        self._text1 = paramElmt.text
        self._text2 = paramElmt.text
        self._defaultValue = paramElmt.defaultValue
        self._maximum = paramElmt.maximum
        self._minimum = paramElmt.minimum

    def getParamType(self):
        return self._paramType

    def getText1(self):
        return self._text1

    def getText2(self):
        return self._text2

    def getDefaultValue(self):
        return self._defaultValue

    def getMaximum(self):
        return self._maximum

    def getMinimum(self):
        return self._minimum

    changed = QtCore.Signal()

    paramType = QtCore.Property(unicode, getParamType, notify=changed)
    text1 = QtCore.Property(unicode, getText1, notify=changed)
    text2 = QtCore.Property(unicode, getText2, notify=changed)
    defaultValue = QtCore.Property(float, getDefaultValue, notify=changed)
    maximum = QtCore.Property(float, getMaximum, notify=changed)
    minimum = QtCore.Property(float, getMinimum, notify=changed)
