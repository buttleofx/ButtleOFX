from PySide import QtCore


class BooleanWrapper(QtCore.QObject):
    """
        Gui class, which maps a ParamBoolean.
    """

    def __init__(self, param):
        QtCore.QObject.__init__(self)
        self._param = param
        self._param.changed.connect(self.emitChanged)

    #################### getters ####################

    def getParamType(self):
        return self._param.getParamType()

    @QtCore.Slot(result=bool)
    def getDefaultValue(self):
        return self._param.getDefaultValue()

    def getValue(self):
        return self._param.getValue()

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
        print "wrapperHasChanged :", changed
        self._param.setHasChanged(changed)

    @QtCore.Slot(bool)
    def pushValue(self, value):
        self._param.pushValue(value)

    @QtCore.Signal
    def changed(self):
        pass

    def emitChanged(self):
        self.changed.emit()

    ################################################## DATA EXPOSED TO QML ##################################################

    paramType = QtCore.Property(unicode, getParamType, notify=changed)
    value = QtCore.Property(bool, getValue, setValue, notify=changed)
    text = QtCore.Property(unicode, getText, notify=changed)
    hasChanged = QtCore.Property(bool, getHasChanged, setHasChanged, notify=changed)
