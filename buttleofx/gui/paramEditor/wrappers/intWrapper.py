from .paramWrapper import ParamWrapper

from PyQt5 import QtCore


class IntWrapper(ParamWrapper):
    """
        Gui class, which maps a ParamInt.
    """

    def __init__(self, param):
        ParamWrapper.__init__(self, param)

    #################### getters ####################

    @QtCore.pyqtSlot(result=int)
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

    @QtCore.pyqtSlot(int)
    def pushValue(self, value):
        self._param.pushValue(value)

    changed = QtCore.pyqtSignal()

    ################################################## DATA EXPOSED TO QML ##################################################

    value = QtCore.pyqtProperty(int, getValue, setValue, notify=changed)

    maximum = QtCore.pyqtProperty(int, getMaximum, constant=True)
    minimum = QtCore.pyqtProperty(int, getMinimum, constant=True)

    hasChanged = QtCore.pyqtProperty(bool, getHasChanged, setHasChanged, notify=changed)
