from PySide import QtCore
# common
from paramWrapper import ParamWrapper


class DoubleWrapper(ParamWrapper):
    """
        Gui class, which maps a ParamDouble.
    """

    def __init__(self, param):
        ParamWrapper.__init__(self, param)

    #################### getters ####################

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

    ################################################## DATA EXPOSED TO QML ##################################################

    value = QtCore.Property(float, getValue, setValue, notify=changed)

    maximum = QtCore.Property(float, getMaximum, constant=True)
    minimum = QtCore.Property(float, getMinimum, constant=True)

    hasChanged = QtCore.Property(bool, getHasChanged, setHasChanged, notify=changed)
