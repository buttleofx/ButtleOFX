from PySide import QtCore
# common
from paramWrapper import ParamWrapper


class IntWrapper(ParamWrapper):
    """
        Gui class, which maps a ParamInt.
    """

    def __init__(self, param):
        ParamWrapper.__init__(self, param)

    #################### getters ####################

    @QtCore.Slot(result=int)
    def getDefaultValue(self):
        return self._param.getDefaultValue()

    def getValue(self):
        return self._param.getValue()

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

    @QtCore.Slot(int)
    def pushValue(self, value):
        self._param.pushValue(value)

    @QtCore.Signal
    def changed(self):
        pass

    ################################################## DATA EXPOSED TO QML ##################################################

    value = QtCore.Property(int, getValue, setValue, notify=changed)

    maximum = QtCore.Property(int, getMaximum, constant=True)
    minimum = QtCore.Property(int, getMinimum, constant=True)

    hasChanged = QtCore.Property(bool, getHasChanged, setHasChanged, notify=changed)
