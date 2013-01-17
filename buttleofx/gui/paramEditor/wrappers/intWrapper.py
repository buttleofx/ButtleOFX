from PySide import QtCore


class IntWrapper(QtCore.QObject):
    def __init__(self, paramElmt):
        QtCore.QObject.__init__(self)
        self._paramType = paramElmt.paramType
        self._text = paramElmt.text
        self._defaultValue = paramElmt.defaultValue
        self._maximum = paramElmt.maximum
        self._minimum = paramElmt.minimum

    #################### getters ####################

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

    #################### setters ####################

    def setParamType(self, paramType):
        self._paramType = paramType

    def setText(self, text):
        self._text = text

    @QtCore.Slot(float)
    def setDefaultValue(self, defaultValue):
        self._defaultValue = defaultValue

    def setMaximum(self, maximum):
        self._maximum = maximum

    def setMinimum(self, minimum):
        self._minimum = minimum

    changed = QtCore.Signal()

    paramType = QtCore.Property(unicode, getParamType, setParamType, notify=changed)
    text = QtCore.Property(unicode, getText, setText, notify=changed)
    defaultValue = QtCore.Property(float, getDefaultValue, setDefaultValue, notify=changed)
    maximum = QtCore.Property(float, getMaximum, setMaximum, notify=changed)
    minimum = QtCore.Property(float, getMinimum, setMinimum, notify=changed)
