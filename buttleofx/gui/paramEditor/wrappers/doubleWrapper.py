from PyQt5 import QtCore
from .paramWrapper import ParamWrapper


class DoubleWrapper(ParamWrapper):
    """
        GUI class, which maps a ParamDouble.
    """

    def __init__(self, param):
        ParamWrapper.__init__(self, param)

    ################################################## Methods exposed to QML ##################################################

    @QtCore.pyqtSlot(result=float)
    def getDefaultValue(self):
        return self._param.getDefaultValue()

    @QtCore.pyqtSlot(result=float)
    def getOldValue(self):
        return self._param.getOldValue()

    @QtCore.pyqtSlot(float)
    def pushValue(self, value):
        self._param.pushValue(value)

    ################################################## Methods private to this class ##################################################

    ### Getters ###

    def getHasChanged(self):
        return self._param.getHasChanged()

    def getMaximum(self):
        return self._param.getMaximum()

    def getMinimum(self):
        return self._param.getMinimum()

    def getValue(self):
        return self._param.getValue()

    ### Setters ###

    def setHasChanged(self, changed):
        self._param.setHasChanged(changed)

    def setValue(self, value):
        self._param.setValue(value)

    ################################################## Data exposed to QML ##################################################

    changed = QtCore.pyqtSignal()

    value = QtCore.pyqtProperty(float, getValue, setValue, notify=changed)

    maximum = QtCore.pyqtProperty(float, getMaximum, constant=True)
    minimum = QtCore.pyqtProperty(float, getMinimum, constant=True)

    hasChanged = QtCore.pyqtProperty(bool, getHasChanged, setHasChanged, notify=changed)
