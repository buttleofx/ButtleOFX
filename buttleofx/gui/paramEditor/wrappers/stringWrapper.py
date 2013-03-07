from PySide import QtCore

#from buttleofx.data import ButtleDataSingleton

class StringWrapper(QtCore.QObject):
    """
        Gui class, which maps a ParamString.
    """

    def __init__(self, param):
        QtCore.QObject.__init__(self)
        self._param = param
        self._param.paramChanged.connect(self.emitChanged)

    #################### getters ####################

    def getParamType(self):
        return self._param.getParamType()

    @QtCore.Slot(result=unicode)
    def getDefaultValue(self):
        return self._param.getDefaultValue()

    def getValue(self):
        return self._param.getValue()

    def getStringType(self):
        return self._param.getStringType()

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

    @QtCore.Signal
    def changed(self):
        pass

    def emitChanged(self):
        self.changed.emit()

    ################################################## DATA EXPOSED TO QML ##################################################

    paramType = QtCore.Property(unicode, getParamType, constant=True)
    value = QtCore.Property(str, getValue, setValue, notify=changed)
    stringType = QtCore.Property(str, getStringType, constant=True)
    text = QtCore.Property(unicode, getText, constant=True)
    hasChanged = QtCore.Property(bool, getHasChanged, setHasChanged, notify=changed)
