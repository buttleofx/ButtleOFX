from PySide import QtCore


class Double2DWrapper(QtCore.QObject):
    """
        Gui class, which maps a ParamDouble2D.
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

    def getParent(self):
        return self._param.getParent()

    #################### setters ####################

    def setParamType(self, paramType):
        self._param.setParamType(paramType)

    def setDefaultValue1(self, value1):
        self._param.setDefaultValue1(value1)

    def setDefaultValue2(self, value2):
        self._param.setDefaultValue2(value2)

    def setValue1(self, value1):
        self._param.setValue1(value1)

    def setValue2(self, value2):
        self._param.setVlue2(value2)

    def setMaximum1(self, maximum):
        self._param.setMaximum1(maximum)

    def setMinimum1(self, minimum):
        self._param.setMinimum1(minimum)

    def setMaximum2(self, maximum):
        self._param.setMaximum2(maximum)

    def setMinimum2(self, minimum):
        self._param.setMinimum2(minimum)

    def setText(self, text):
        self._param.setTxt(text)

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
    maximum1 = QtCore.Property(float, getMaximum1, setMaximum1, notify=changed)
    minimum1 = QtCore.Property(float, getMinimum1, setMinimum1, notify=changed)
    maximum2 = QtCore.Property(float, getMaximum2, setMaximum2, notify=changed)
    minimum2 = QtCore.Property(float, getMinimum2, setMinimum2, notify=changed)
    parent = QtCore.Property(unicode, getParent, constant=True)
