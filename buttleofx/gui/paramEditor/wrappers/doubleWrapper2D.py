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

    #################### getters ####################

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

    #################### setters ####################

    def setParamType(self, paramType):
        self._paramType = paramType

    def setText1(self, text1):
        self._text1 = text1

    def setText2(self, text2):
        self._text2 = text2

    @QtCore.Slot(float)
    def setDefaultValue(self, defaultValue):
        self._defaultValue = defaultValue

    def setMaximum(self, maximum):
        self._maximum = maximum

    def setMinimum(self, minimum):
        self._minimum = minimum

    changed = QtCore.Signal()

    paramType = QtCore.Property(unicode, getParamType, setParamType, notify=changed)
    text1 = QtCore.Property(unicode, getText1, setText1, notify=changed)
    text2 = QtCore.Property(unicode, getText2, setText2, notify=changed)
    defaultValue = QtCore.Property(float, getDefaultValue, setDefaultValue, notify=changed)
    maximum = QtCore.Property(float, getMaximum, setMaximum, notify=changed)
    minimum = QtCore.Property(float, getMinimum, setMinimum, notify=changed)
