from PyQt5 import QtCore
from .paramWrapper import ParamWrapper


class IntWrapper(ParamWrapper):
    """
        GUI class, which maps a ParamInt.
    """

    def __init__(self, param):
        ParamWrapper.__init__(self, param)

    #################################################### Methods exposed to QML ##################################################

    @QtCore.pyqtSlot(result=int)
    def getDefaultValue(self):
        return self._param.getDefaultValue()

    @QtCore.pyqtSlot(int)
    def pushValue(self, value):
        self._param.pushValue(value)

    #################################################### Methods private to this class ##################################################

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

    value = QtCore.pyqtProperty(int, getValue, setValue, notify=changed)

    maximum = QtCore.pyqtProperty(int, getMaximum, constant=True)
    minimum = QtCore.pyqtProperty(int, getMinimum, constant=True)

    hasChanged = QtCore.pyqtProperty(bool, getHasChanged, setHasChanged, notify=changed)
