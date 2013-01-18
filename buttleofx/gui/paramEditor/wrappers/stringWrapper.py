from PySide import QtCore


class StringWrapper(QtCore.QObject):
    def __init__(self, param):
        QtCore.QObject.__init__(self)
        self._param = param

    #################### getters ####################

    def getParamType(self):
        return self._param.paramType

    def getDefaultValue(self):
        return self._param.defaultValue

    def getValue(self):
        return self._param.value

    def getStringType(self):
        return self._param.stringType

    #################### setters ####################

    def setParamType(self, paramType):
        self._param.paramType = paramType

    def setDefaultValue(self, defaultValue):
        self._param.defaultValue = defaultValue

    def setValue(self, value):
        self._param.value = value

    def setStringType(self, stringType):
        self._param.stringType = stringType

    changed = QtCore.Signal()

    paramType = QtCore.Property(unicode, getParamType, setParamType, notify=changed)
    value = QtCore.Property(str, getValue, setValue, notify=changed)
    stringType = QtCore.Property(str, getStringType, setStringType, notify=changed)
