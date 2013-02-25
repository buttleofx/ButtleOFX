from PySide import QtCore

# common
from buttleofx.gui.paramEditor.wrappers.paramWrapper import ParamWrapper


class BooleanWrapper(ParamWrapper, QtCore.QObject):
    """
        Gui class, which maps a ParamBoolean.
    """

    def __init__(self, param):
        QtCore.QObject.__init__(self)
        ParamWrapper.__init__(self, param)

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

    def getHasChanged(self):
        return self._param.getHasChanged()

    def setHasChanged(self, changed):
        self._param.setHasChanged(changed)

    #################### setters ####################

    def setValue(self, value):
        self._param.setValue(value)

    @QtCore.Slot(bool)
    def pushValue(self, value):
        self._param.pushValue(value)

    @QtCore.Signal
    def changed(self):
        pass

    def emitChanged(self):
        self.changed.emit()

    ################################################## DATA EXPOSED TO QML ##################################################

    paramType = QtCore.Property(unicode, getParamType, constant=True)
    value = QtCore.Property(bool, getValue, setValue, notify=changed)
    text = QtCore.Property(unicode, getText, constant=True)
    hasChanged = QtCore.Property(bool, getHasChanged, setHasChanged, notify=changed)
