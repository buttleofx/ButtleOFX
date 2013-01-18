from PySide import QtCore


class IntWrapper(QtCore.QObject):
    def __init__(self, param):
        QtCore.QObject.__init__(self)
        self._param = param

    #################### getters ####################

    def getParamType(self):
        return self._param.paramType

    def getText(self):
        return self._param.text

    def getDefaultValue(self):
        return self._param.defaultValue

    def getValue(self):
        return self._param.value

    def getMaximum(self):
        return self._param.maximum

    def getMinimum(self):
        return self._param.minimum

    #################### setters ####################

    def setParamType(self, paramType):
        self._param.paramType = paramType

    def setText(self, text):
        self._param.text = text

    def setDefaultValue(self, defaultValue):
        self._param.defaultValue = defaultValue

    def setValue(self, value):
        self._param.value = value

    def setMaximum(self, maximum):
        self._param.maximum = maximum

    def setMinimum(self, minimum):
        self._param.minimum = minimum

    changed = QtCore.Signal()

    paramType = QtCore.Property(unicode, getParamType, setParamType, notify=changed)
    text = QtCore.Property(unicode, getText, setText, notify=changed)
    value = QtCore.Property(float, getValue, setValue, notify=changed)
    maximum = QtCore.Property(float, getMaximum, setMaximum, notify=changed)
    minimum = QtCore.Property(float, getMinimum, setMinimum, notify=changed)
