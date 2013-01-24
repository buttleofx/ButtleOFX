from PySide import QtCore


class Double3DWrapper(QtCore.QObject):
    """
        Gui class, which maps a ParamDouble3D.
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

    def getDefaultValue3(self):
        return self._param.getDefaultValue3()

    def getValue1(self):
        return self._param.getValue1()

    def getValue2(self):
        return self._param.getValue2()

    def getValue3(self):
        return self._param.getValue3()

    def getMaximum1(self):
        return self._param.getMaximum1()

    def getMinimum1(self):
        return self._param.getMinimum1()

    def getMaximum2(self):
        return self._param.getMaximum2()

    def getMinimum2(self):
        return self._param.getMinimum2()

    def getMaximum3(self):
        return self._param.getMaximum3()

    def getMinimum3(self):
        return self._param.getMinimum3()

    def getText(self):
        return self._param.getText()

    #################### setters ####################

    def setParamType(self, paramType):
        self._param.setParamType(paramType)

    def setDefaultValue1(self, defaultValue1):
        self._param.setDefaultValue1(defaultValue1)

    def setDefaultValue2(self, defaultValue2):
        self._param.setDefaultValue2(defaultValue2)

    def setDefaultValue3(self, defaultValue3):
        self._param.setDefaultValue3(defaultValue3)

    def setValue1(self, value1):
        self._param.setValue1(value1)

    def setValue2(self, value2):
        self._param.setValue2(value2)

    def setValue3(self, value3):
        self._param.setValue3(value3)

    def setMaximum1(self, maximum):
        self._param.setMaximum1(maximum)

    def setMinimum1(self, minimum):
        self._param.setMinimum1(minimum)

    def setMaximum2(self, maximum):
        self._param.setMaximum2(maximum)

    def setMinimum2(self, minimum):
        self._param.setMinimum2(minimum)

    def setMaximum3(self, maximum):
        self._param.setMaximum3(maximum)

    def setMinimum3(self, minimum):
        self._param.setMinimum3(minimum)

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
    value1 = QtCore.Property(float, getValue1, setValue1, notify=changed)
    value2 = QtCore.Property(float, getValue2, setValue2, notify=changed)
    value3 = QtCore.Property(float, getValue3, setValue2, notify=changed)
    maximum1 = QtCore.Property(float, getMaximum1, setMaximum1, notify=changed)
    minimum1 = QtCore.Property(float, getMinimum1, setMinimum1, notify=changed)
    maximum2 = QtCore.Property(float, getMaximum2, setMaximum2, notify=changed)
    minimum2 = QtCore.Property(float, getMinimum2, setMinimum2, notify=changed)
    maximum3 = QtCore.Property(float, getMaximum3, setMaximum3, notify=changed)
    minimum3 = QtCore.Property(float, getMinimum3, setMinimum3, notify=changed)
