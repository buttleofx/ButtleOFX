from PyQt5 import QtCore
from .paramWrapper import ParamWrapper


class StringWrapper(ParamWrapper):
    """
        GUI class, which maps a ParamString.
    """

    def __init__(self, param):
        ParamWrapper.__init__(self, param)

    # ######################################## Methods exposed to QML ####################################### #

    @QtCore.pyqtSlot(result=str)
    def getDefaultValue(self):
        self.setHasChanged(False)
        return self._param.getDefaultValue()

    @QtCore.pyqtSlot(str)
    def pushValue(self, value):
        self._param.pushValue(value)

    @QtCore.pyqtSlot(str)
    def changeValue(self, value):
        self.setValue(value)
        self.pushValue(value)
        self.setHasChanged(True)

    @QtCore.pyqtSlot()
    def resetValue(self):
        # If we don't do it twice, the value is not refreshed in the QML file
        self.value = self.getDefaultValue()
        self.pushValue(self.value)
        self.value = self.getDefaultValue()
        self.pushValue(self.value)

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getHasChanged(self):
        return self._param.getHasChanged()

    def getStringType(self):
        return self._param.getStringType()

    def getStringFilePathExist(self):
        return self._param.getStringFilePathExist()

    def getValue(self):
        return self._param.getValue()

    # ## Setters ## #

    def setHasChanged(self, changed):
        self._param.setHasChanged(changed)

    def setValue(self, value):
        self._param.setValue(value)

    # ############################################# Data exposed to QML ############################################## #

    changed = QtCore.pyqtSignal()

    value = QtCore.pyqtProperty(str, getValue, setValue, notify=changed)
    stringType = QtCore.pyqtProperty(str, getStringType, constant=True)
    filePathExist = QtCore.pyqtProperty(bool, getStringFilePathExist, constant=True)

    hasChanged = QtCore.pyqtProperty(bool, getHasChanged, setHasChanged, notify=changed)
