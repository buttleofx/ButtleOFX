from PyQt5 import QtCore
from .paramWrapper import ParamWrapper


class BooleanWrapper(ParamWrapper):
    """
        GUI class, which maps a ParamBoolean.
    """

    def __init__(self, param):
        ParamWrapper.__init__(self, param)

    # ############################################ Methods exposed to QML ############################################ #

    @QtCore.pyqtSlot(result=bool)
    def getDefaultValue(self):
        return self._param.getDefaultValue()

    @QtCore.pyqtSlot(bool)
    def pushValue(self, value):
        self._param.pushValue(value)

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getHasChanged(self):
        return self._param.getHasChanged()

    def getValue(self):
        return self._param.getValue()

    # ## Setters ## #

    def setHasChanged(self, changed):
        self._param.setHasChanged(changed)

    def setValue(self, value):
        self._param.setValue(value)

    # ############################################# Data exposed to QML ############################################## #

    changed = QtCore.pyqtSignal()

    value = QtCore.pyqtProperty(bool, getValue, setValue, notify=changed)
    hasChanged = QtCore.pyqtProperty(bool, getHasChanged, setHasChanged, notify=changed)
