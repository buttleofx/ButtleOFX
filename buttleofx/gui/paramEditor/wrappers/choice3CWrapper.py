from PySide import QtCore


class Choice3CWrapper(QtCore.QObject):
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

    def getValue1(self):
        return self._param.value1

    def getValue2(self):
        return self._param.value2

    def getValue3(self):
        return self._param.value3

    #################### setters ####################

    def setParamType(self, paramType):
        self._param.paramType = paramType

    def setText(self, text):
        self._param.text = text

    def setDefaultValue(self, defaultValue):
        self._param.defaultValue = defaultValue

    def setValue1(self, value):
        self._param.value1 = value

    def setValue2(self, value):
        self._param.value2 = value

    def setValue3(self, value):
        self._param.value3 = value

    # Just temporary : paramType must be constant
    changed = QtCore.Signal()

    paramType = QtCore.Property(unicode, getParamType, setParamType, notify=changed)
    text = QtCore.Property(unicode, getText, setText, notify=changed)
    value1 = QtCore.Property(str, getValue1, setValue1, notify=changed)
    value2 = QtCore.Property(str, getValue2, setValue2, notify=changed)
    value3 = QtCore.Property(str, getValue3, setValue3, notify=changed)
