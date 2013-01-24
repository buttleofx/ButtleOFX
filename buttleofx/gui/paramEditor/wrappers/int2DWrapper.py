from PySide import QtCore


class Int2DWrapper(QtCore.QObject):
    """
        Gui class, which maps a ParamInt2D.
    """

    def __init__(self, param):
        QtCore.QObject.__init__(self)
        self._param = param
        self._param.changed.connect(self.emitChanged)

    #################### getters ####################

    def getParamType(self):
        return self._param.getParamType()

    def getDefaultValue1(self):
        return self._param.getDefaultValue1()

    def getDefaultValue2(self):
        return self._param.getDefaultValue2()

    def getValue1(self):
        return self._param.getValue1()

    def getValue2(self):
        return self._param.getValue2()

    def getMaximum1(self):
        return self._param.getMaximum1()

    def getMinimum1(self):
        return self._param.getMinimum1()

    def getMaximum2(self):
        return self._param.getMaximum2()

    def getMinimum2(self):
        return self._param.getMinimum2()

    def getText(self):
        return self._param.getText()

    #################### setters ####################

    def setParamType(self, paramType):
        self._param.setParamType(paramType)

    def setDefaultValue1(self, defaultValue):
        self._param.setDefaultValue1(defaultValue)

    def setDefaultValue2(self, defaultValue):
        self._param.setDefaultValue2(defaultValue)

    def setValue1(self, value):
        self._param.setValue1(value)

    def setValue2(self, value):
        self._param.setValue2(value)

    def setMaximum1(self, maximum):
        self._param.setMaximum1(maximum)

    def setMinimum1(self, minimum):
        self._param.setMinimum1(minimum)

    def setMaximum2(self, maximum):
        self._param.setMaximum2(maximum)

    def setMinimum2(self, minimum):
        self._param.setMinimum2(minimum)

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
    value1 = QtCore.Property(int, getValue1, setValue1, notify=changed)
    value2 = QtCore.Property(int, getValue2, setValue2, notify=changed)
    maximum1 = QtCore.Property(int, getMaximum1, setMaximum1, notify=changed)
    minimum1 = QtCore.Property(int, getMinimum1, setMinimum1, notify=changed)
    maximum2 = QtCore.Property(int, getMaximum2, setMaximum2, notify=changed)
    minimum2 = QtCore.Property(int, getMinimum2, setMinimum2, notify=changed)
