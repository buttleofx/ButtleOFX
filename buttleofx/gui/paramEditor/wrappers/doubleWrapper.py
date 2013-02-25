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
        return self._param.getParamType()

    @QtCore.Slot(result=float)
    def getDefaultValue(self):
        return self._param.getDefaultValue()

    def getValue(self):
        return self._param.getValue()

    @QtCore.Slot(result=float)
    def getOldValue(self):
        return self._param.getOldValue()

    def getMaximum(self):
        return self._param.getMaximum()

    def getMinimum(self):
        return self._param.getMinimum()

    def getText(self):
        return self._param.getText()

    def isSecret(self):
        return self._param.isSecret()

    def getHasChanged(self):
        return self._param.getHasChanged()

    #################### setters ####################

    def setValue(self, value):
        self._param.setValue(value)

    def setHasChanged(self, changed):
        self._param.setHasChanged(changed)

    @QtCore.Slot(float)
    def pushValue(self, value):
        self._param.pushValue(value)

    @QtCore.Signal
    def changed(self):
        pass

    def emitChanged(self):
        self.changed.emit()

    ################################################## DATA EXPOSED TO QML ##################################################

    paramType = QtCore.Property(unicode, getParamType, constant=True)
    text = QtCore.Property(unicode, getText, constant=True)
    value = QtCore.Property(float, getValue, setValue, notify=changed)
    maximum = QtCore.Property(float, getMaximum, constant=True)
    minimum = QtCore.Property(float, getMinimum, constant=True)
    hasChanged = QtCore.Property(bool, getHasChanged, setHasChanged, notify=changed)
