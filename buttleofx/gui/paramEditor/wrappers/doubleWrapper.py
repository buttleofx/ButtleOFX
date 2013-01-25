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

    def getDefaultValue(self):
        return self._param.getDefaultValue()

    def getValue(self):
        return self._param.getValue()

    def getMaximum(self):
        return self._param.getMaximum()

    def getMinimum(self):
        return self._param.getMinimum()

    def getText(self):
        return self._param.getText()

    #################### setters ####################

    def setValue(self, value):
        self._param.setValue(value)

    @QtCore.Signal
    def changed(self):
        pass

    def emitChanged(self):
        self.changed.emit()

    ################################################## DATA EXPOSED TO QML ##################################################

    paramType = QtCore.Property(unicode, getParamType, notify=changed)
    text = QtCore.Property(unicode, getText, notify=changed)
    value = QtCore.Property(float, getValue, setValue, notify=changed)
    maximum = QtCore.Property(float, getMaximum, notify=changed)
    minimum = QtCore.Property(float, getMinimum, notify=changed)
