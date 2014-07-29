from PyQt5 import QtCore
from .paramWrapper import ParamWrapper


class Double2DWrapper(ParamWrapper):
    """
        GUI class, which maps a ParamDouble2D.
    """

    def __init__(self, param):
        ParamWrapper.__init__(self, param)

    # ############################################ Methods exposed to QML ############################################ #

    @QtCore.pyqtSlot(result=float)
    def getDefaultValue1(self):
        return self._param.getDefaultValue1()

    @QtCore.pyqtSlot(result=float)
    def getDefaultValue2(self):
        return self._param.getDefaultValue2()

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getMaximum1(self):
        return self._param.getMaximum1()

    def getMinimum1(self):
        return self._param.getMinimum1()

    def getMaximum2(self):
        return self._param.getMaximum2()

    def getMinimum2(self):
        return self._param.getMinimum2()

    def getValue1(self):
        return self._param.getValue1()

    def getValue2(self):
        return self._param.getValue2()

    def getValue1HasChanged(self):
        return self._param.getValue1HasChanged()

    def getValue2HasChanged(self):
        return self._param.getValue2HasChanged()

    # ## Setters ## #

    def setValue1(self, value1):
        self._param.setValue1(value1)

    def setValue2(self, value2):
        self._param.setValue2(value2)

    def setValue1HasChanged(self, changed):
        self._param.setValue1HasChanged(changed)

    def setValue2HasChanged(self, changed):
        self._param.setValue2HasChanged(changed)

    # ############################################# Data exposed to QML ############################################## #

    changed = QtCore.pyqtSignal()

    value1 = QtCore.pyqtProperty(float, getValue1, setValue1, notify=changed)
    value2 = QtCore.pyqtProperty(float, getValue2, setValue2, notify=changed)

    maximum1 = QtCore.pyqtProperty(float, getMaximum1, constant=True)
    minimum1 = QtCore.pyqtProperty(float, getMinimum1, constant=True)
    maximum2 = QtCore.pyqtProperty(float, getMaximum2, constant=True)
    minimum2 = QtCore.pyqtProperty(float, getMinimum2, constant=True)

    value1HasChanged = QtCore.pyqtProperty(bool, getValue1HasChanged, setValue1HasChanged, notify=changed)
    value2HasChanged = QtCore.pyqtProperty(bool, getValue2HasChanged, setValue2HasChanged, notify=changed)
