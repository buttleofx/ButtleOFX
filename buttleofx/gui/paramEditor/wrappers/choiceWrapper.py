from PyQt5 import QtCore
from .paramWrapper import ParamWrapper
from quickmamba.models import QObjectListModel


class ChoiceWrapper(ParamWrapper):
    """
        GUI class, which maps a ParamChoice.
    """

    def __init__(self, param):
        ParamWrapper.__init__(self, param)

        self._listValue = QObjectListModel()
        for value in self._param.getListValue():
            self._listValue.append(value)

    # ############################################ Methods exposed to QML ############################################ #

    @QtCore.pyqtSlot(result=str)
    def getDefaultValue(self):
        return self._param.getDefaultValue()

    @QtCore.pyqtSlot(str)
    def pushValue(self, value):
        self._param.pushValue(value)

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getCurrentIndex(self):
        return self._param.getCurrentIndex()

    def getHasChanged(self):
        return self._param.getHasChanged()

    def getListValue(self):
        return self._listValue

    def getValue(self):
        return self._param.getValue()

    # ## Setters ## #

    def setHasChanged(self, changed):
        self._param.setHasChanged(changed)

    def setValue(self, value):
        self._param.setValue(value)

    # ############################################# Data exposed to QML ############################################## #

    changed = QtCore.pyqtSignal()

    listValue = QtCore.pyqtProperty(QtCore.QObject, getListValue, constant=True)
    value = QtCore.pyqtProperty(str, getValue, setValue, notify=changed)
    currentIndex = QtCore.pyqtProperty(int, getCurrentIndex, notify=changed)
    hasChanged = QtCore.pyqtProperty(bool, getHasChanged, setHasChanged, notify=changed)
