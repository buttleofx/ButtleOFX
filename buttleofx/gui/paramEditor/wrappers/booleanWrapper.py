from .paramWrapper import ParamWrapper

from PyQt5 import QtCore


class BooleanWrapper(ParamWrapper):
    """
        Gui class, which maps a ParamBoolean.
    """

    def __init__(self, param):
        ParamWrapper.__init__(self, param)

    #################### getters ####################

    @QtCore.pyqtSlot(result=bool)
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

    @QtCore.pyqtSlot(bool)
    def pushValue(self, value):
        self._param.pushValue(value)

    changed = QtCore.pyqtSignal()

    ################################################## DATA EXPOSED TO QML ##################################################

    value = QtCore.pyqtProperty(bool, getValue, setValue, notify=changed)
    hasChanged = QtCore.pyqtProperty(bool, getHasChanged, setHasChanged, notify=changed)
