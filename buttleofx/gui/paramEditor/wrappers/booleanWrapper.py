from PySide import QtCore
# common
from paramWrapper import ParamWrapper


class BooleanWrapper(ParamWrapper):
    """
        Gui class, which maps a ParamBoolean.
    """

    def __init__(self, param):
        ParamWrapper.__init__(self, param)

    #################### getters ####################

    @QtCore.Slot(result=bool)
    def getDefaultValue(self):
        return self._param.getDefaultValue()

    def getValue(self):
        return self._param.getValue()

    def getHasChanged(self):
        return self._param.getHasChanged()

    #################### setters ####################

    def setValue(self, value):
        self._param.setValue(value)

    def setHasChanged(self, changed):
        self._param.setHasChanged(changed)

    @QtCore.Slot(bool)
    def pushValue(self, value):
        self._param.pushValue(value)

    @QtCore.Signal
    def changed(self):
        pass

    ################################################## DATA EXPOSED TO QML ##################################################

    value = QtCore.Property(bool, getValue, setValue, notify=changed)
    hasChanged = QtCore.Property(bool, getHasChanged, setHasChanged, notify=changed)
