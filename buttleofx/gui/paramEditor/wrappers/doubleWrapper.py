from .paramWrapper import ParamWrapper

from PyQt5 import QtCore


class DoubleWrapper(ParamWrapper):
    """
        Gui class, which maps a ParamDouble.
    """

    def __init__(self, param):
        ParamWrapper.__init__(self, param)

    #################### getters ####################

    @QtCore.pyqtSlot(result=float)
    def getDefaultValue(self):
        return self._param.getDefaultValue()

    def getValue(self):
        return self._param.getValue()

    @QtCore.pyqtSlot(result=float)
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

    @QtCore.pyqtSlot(float)
    def pushValue(self, value):
        self._param.pushValue(value)

    changed = QtCore.pyqtSignal()

    ################################################## DATA EXPOSED TO QML ##################################################

    value = QtCore.pyqtProperty(float, getValue, setValue, notify=changed)

    maximum = QtCore.pyqtProperty(float, getMaximum, constant=True)
    minimum = QtCore.pyqtProperty(float, getMinimum, constant=True)

    hasChanged = QtCore.pyqtProperty(bool, getHasChanged, setHasChanged, notify=changed)
