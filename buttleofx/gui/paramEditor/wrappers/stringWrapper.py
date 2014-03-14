# common
from .paramWrapper import ParamWrapper

from PyQt5 import QtCore


class StringWrapper(ParamWrapper):
    """
        Gui class, which maps a ParamString.
    """

    def __init__(self, param):
        ParamWrapper.__init__(self, param)

    #################### getters ####################

    @QtCore.pyqtSlot(result=str)
    def getDefaultValue(self):
        self.setHasChanged(False)
        return self._param.getDefaultValue()

    def getStringFilePathExist(self):
        return self._param.getStringFilePathExist()

    def getValue(self):
        return self._param.getValue()

    def getStringType(self):
        return self._param.getStringType()

    def getHasChanged(self):
        return self._param.getHasChanged()

    #################### setters ####################

    def setValue(self, value):
        self._param.setValue(value)

    def setHasChanged(self, changed):
        self._param.setHasChanged(changed)

    @QtCore.pyqtSlot(str)
    def pushValue(self, value):
        self._param.pushValue(value)

    changed = QtCore.pyqtSignal()

    @QtCore.pyqtSlot(str)
    def changeValue(self, value):
        self.setValue(value)
        self.pushValue(value)
        self.setHasChanged(True)

    @QtCore.pyqtSlot()
    def resetValue(self):
        # if we don't do it twice, the value is not refreshed in the qml file
        self.value = self.getDefaultValue()
        self.pushValue(self.value)
        self.value = self.getDefaultValue()
        self.pushValue(self.value)
    
    ################################################## DATA EXPOSED TO QML ##################################################

    value = QtCore.pyqtProperty(str, getValue, setValue, notify=changed)
    stringType = QtCore.pyqtProperty(str, getStringType, constant=True)
    filePathExist = QtCore.pyqtProperty(bool, getStringFilePathExist, constant=True)
    
    hasChanged = QtCore.pyqtProperty(bool, getHasChanged, setHasChanged, notify=changed)
