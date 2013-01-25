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

    #################### setters ####################

    def setValue1(self, value1):
        self._param.setValue1(value1)

    def setValue2(self, value2):
        self._param.setValue2(value2)

    @QtCore.Signal
    def changed(self):
        pass

    def emitChanged(self):
        self.changed.emit()

    ################################################## DATA EXPOSED TO QML ##################################################

    paramType = QtCore.Property(unicode, getParamType, notify=changed)
    text = QtCore.Property(unicode, getText, notify=changed)
    value1 = QtCore.Property(unicode, getValue1, setValue1, notify=changed)
    value2 = QtCore.Property(unicode, getValue2, setValue2, notify=changed)
    maximum1 = QtCore.Property(unicode, getMaximum1, notify=changed)
    minimum1 = QtCore.Property(unicode, getMinimum1, notify=changed)
    maximum2 = QtCore.Property(unicode, getMaximum2, notify=changed)
    minimum2 = QtCore.Property(unicode, getMinimum2, notify=changed)
