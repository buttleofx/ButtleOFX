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

    #################### getters ####################

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

    #################### setters ####################

    def setParamType(self, paramType):
        self._paramType = paramType

    def setText(self, text):
        self._text = text

    @QtCore.Slot(float)
    def setDefaultValue1(self, value1):
        self._defaultValue1

    @QtCore.Slot(float)
    def setDefaultValue2(self, value2):
        self._defaultValue2

    def setMaximum(self, maximum):
        self._maximum

    def setMinimum(self, minimum):
        self._minimum

    changed = QtCore.Signal()

    paramType = QtCore.Property(unicode, getParamType, setParamType, notify=changed)
    text = QtCore.Property(unicode, getText, setText, notify=changed)
    defaultValue1 = QtCore.Property(float, getDefaultValue1, setDefaultValue1, notify=changed)
    defaultValue2 = QtCore.Property(float, getDefaultValue2, setDefaultValue2, notify=changed)
    maximum = QtCore.Property(float, getMaximum, setMaximum, notify=changed)
    minimum = QtCore.Property(float, getMinimum, setMinimum, notify=changed)
