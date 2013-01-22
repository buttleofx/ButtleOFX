from PySide import QtCore


class DoubleWrapper(QtCore.QObject):
    """
        Gui class, which maps a ParamDouble.
    """

    def __init__(self, param):
        QtCore.QObject.__init__(self)
        self._param = param
        self._param.changed.connect(self.emitChanged)

    #################### getters ####################

    def getParamType(self):
        return self._param.setParamType()

    def getDefaultValue(self):
        return self._param.setDefaultValue()

    def getValue(self):
        return self._param.setValue()

    def getMaximum(self):
        return self._param.setMaximum()

    def getMinimum(self):
        return self._param.setMinimum()

    def getText(self):
        return self._param.setText()

    #################### setters ####################

    def setParamType(self, paramType):
        self._param.setParamType(paramType)

    def setDefaultValue(self, defaultValue):
        self._param.setDefaultValue(defaultValue)

    def setValue(self, value):
        self._param.setValue(value)

    def setMaximum(self, maximum):
        self._param.setMaximum(maximum)

    def setMinimum(self, minimum):
        self._param.setMinimum(minimum)

    def setText(self, text):
        self._param.setText(text)

    @QtCore.Signal
    def changed(self):
        pass

    def emitChanged(self):
        self.changed.emit()

    ################################################## DATA EXPOSED TO QML ##################################################

    paramType = QtCore.Property(unicode, getParamType, setParamType, notify=changed)
    text = QtCore.Property(unicode, getText, setText, notify=changed)
    value = QtCore.Property(float, getValue, setValue, notify=changed)
    maximum = QtCore.Property(float, getMaximum, setMaximum, notify=changed)
    minimum = QtCore.Property(float, getMinimum, setMinimum, notify=changed)
