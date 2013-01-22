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
        return self._param.setParamType()

    def getDefaultValue1(self):
        return self._param.setDefaultValue1()

    def getDefaultValue2(self):
        return self._param.setDefaultValue2()

    def getValue1(self):
        return self._param.setValue1()

    def getValue2(self):
        return self._param.setValue2()

    def getMaximum(self):
        return self._param.setMaximum()

    def getMinimum(self):
        return self._param.setMinimum()

    def getText(self):
        return self._param.setText()

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

    def setMaximum(self, maximum):
        self._param.setMaximum(maximum)

    def setMinimum(self, minimum):
        self._param.setMinimum(minimum)

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
    maximum = QtCore.Property(float, getMaximum, setMaximum, notify=changed)
    minimum = QtCore.Property(float, getMinimum, setMinimum, notify=changed)
