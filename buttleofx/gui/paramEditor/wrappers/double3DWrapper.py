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

    def getValues(self):
        return self._param.getValues()

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

    def setValues(self, values):
        self._param.setValues(values)

    def setValue1(self, value1):
        self._param.setValue1(value1)

    def setValue2(self, value2):
        self._param.setValue2(value2)

    def setValue3(self, value3):
        self._param.setValue3(value3)

    @QtCore.Slot(float, int)
    def pushValue(self, value, index):
        self._param.pushValue(value, index)

    @QtCore.Signal
    def changed(self):
        pass

    def emitChanged(self):
        self.changed.emit()

    ################################################## DATA EXPOSED TO QML ##################################################

    paramType = QtCore.Property(unicode, getParamType, notify=changed)
    text = QtCore.Property(unicode, getText, notify=changed)
    value1 = QtCore.Property(float, getValue1, setValue1, notify=changed)
    value2 = QtCore.Property(float, getValue2, setValue2, notify=changed)
    value3 = QtCore.Property(float, getValue3, setValue3, notify=changed)
    maximum1 = QtCore.Property(float, getMaximum1, notify=changed)
    minimum1 = QtCore.Property(float, getMinimum1, notify=changed)
    maximum2 = QtCore.Property(float, getMaximum2, notify=changed)
    minimum2 = QtCore.Property(float, getMinimum2, notify=changed)
    maximum3 = QtCore.Property(float, getMaximum3, notify=changed)
    minimum3 = QtCore.Property(float, getMinimum3, notify=changed)
