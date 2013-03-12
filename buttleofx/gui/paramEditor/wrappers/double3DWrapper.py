from PySide import QtCore
# common
from paramWrapper import ParamWrapper


class Double3DWrapper(ParamWrapper):
    """
        Gui class, which maps a ParamDouble3D.
    """

    def __init__(self, param):
        ParamWrapper.__init__(self, param)

    #################### getters ####################

    @QtCore.Slot(result=float)
    def getDefaultValue1(self):
        self.setValue1HasChanged(False)
        return self._param.getDefaultValue1()

    @QtCore.Slot(result=float)
    def getDefaultValue2(self):
        self.setValue2HasChanged(False)
        return self._param.getDefaultValue2()

    @QtCore.Slot(result=float)
    def getDefaultValue3(self):
        self.setValue3HasChanged(False)
        return self._param.getDefaultValue3()

    def getValue1(self):
        return self._param.getValue1()

    def getValue2(self):
        return self._param.getValue2()

    def getValue3(self):
        return self._param.getValue3()

    def getMaximum1(self):
        return self._param.getMaximum1()

    def getMinimum1(self):
        return self._param.getMinimum1()

    def getMaximum2(self):
        return self._param.getMaximum2()

    def getMinimum2(self):
        return self._param.getMinimum2()

    def getMaximum3(self):
        return self._param.getMaximum3()

    def getMinimum3(self):
        return self._param.getMinimum3()

    def getValue1HasChanged(self):
        return self._param.getValue1HasChanged()

    def getValue2HasChanged(self):
        return self._param.getValue2HasChanged()

    def getValue3HasChanged(self):
        return self._param.getValue3HasChanged()

    #################### setters ####################

    def setValue1(self, value1):
        self._param.setValue1(value1)

    def setValue2(self, value2):
        self._param.setValue2(value2)

    def setValue3(self, value3):
        self._param.setValue3(value3)

    def setValue1HasChanged(self, changed):
        self._param.setValue1HasChanged(changed)

    def setValue2HasChanged(self, changed):
        self._param.setValue2HasChanged(changed)

    def setValue3HasChanged(self, changed):
        self._param.setValue3HasChanged(changed)

    @QtCore.Signal
    def changed(self):
        pass

    ################################################## DATA EXPOSED TO QML ##################################################

    value1 = QtCore.Property(float, getValue1, setValue1, notify=changed)
    value2 = QtCore.Property(float, getValue2, setValue2, notify=changed)
    value3 = QtCore.Property(float, getValue3, setValue3, notify=changed)

    maximum1 = QtCore.Property(float, getMaximum1, constant=True)
    minimum1 = QtCore.Property(float, getMinimum1, constant=True)
    maximum2 = QtCore.Property(float, getMaximum2, constant=True)
    minimum2 = QtCore.Property(float, getMinimum2, constant=True)
    maximum3 = QtCore.Property(float, getMaximum3, constant=True)
    minimum3 = QtCore.Property(float, getMinimum3, constant=True)

    value1HasChanged = QtCore.Property(bool, getValue1HasChanged, setValue1HasChanged, notify=changed)
    value2HasChanged = QtCore.Property(bool, getValue2HasChanged, setValue2HasChanged, notify=changed)
    value3HasChanged = QtCore.Property(bool, getValue3HasChanged, setValue3HasChanged, notify=changed)
