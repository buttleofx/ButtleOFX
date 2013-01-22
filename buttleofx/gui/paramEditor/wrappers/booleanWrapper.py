from PySide import QtCore


class BooleanWrapper(QtCore.QObject):
    def __init__(self, param):
        QtCore.QObject.__init__(self)
        self._param = param
        self._param.changed.connect(self.emitChanged)

    #################### getters ####################

    def getParamType(self):
        return self._param.paramType

    def getText(self):
        return self._param.text

    def getDefaultValue(self):
        return self._param.defaultValue

    def getValue(self):
        return self._param.value

    #################### setters ####################

    def setParamType(self, paramType):
        self._param.paramType = paramType

    def setText(self, text):
        self._param.text = text

    def setDefaultValue(self, defaultValue):
        self._param.defaultValue = defaultValue

    def setValue(self, value):
        self._param.value = value

    @QtCore.Signal
    def changed(self):
        pass

    def emitChanged(self):
        self.changed.emit()

    paramType = QtCore.Property(unicode, getParamType, setParamType, notify=changed)
    text = QtCore.Property(unicode, getText, setText, notify=changed)
    value = QtCore.Property(bool, getValue, setValue, notify=changed)
