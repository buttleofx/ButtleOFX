from .paramWrapper import ParamWrapper

from quickmamba.models import QObjectListModel

from PyQt5 import QtCore


class ChoiceWrapper(ParamWrapper):
    """
        Gui class, which maps a ParamChoice.
    """

    def __init__(self, param):
        ParamWrapper.__init__(self, param)

        self._listValue = QObjectListModel()
        for value in self._param.getListValue():
            self._listValue.append(value)

    #################### getters ####################

    @QtCore.pyqtSlot(result=str)
    def getDefaultValue(self):
        return self._param.getDefaultValue()

    def getListValue(self):
        return self._listValue

    def getValue(self):
        return self._param.getValue()

    def getCurrentIndex(self):
        return self._param.getCurrentIndex()

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

    ################################################## DATA EXPOSED TO QML ##################################################

    listValue = QtCore.pyqtProperty(QtCore.QObject, getListValue, constant=True)
    value = QtCore.pyqtProperty(str, getValue, setValue, notify=changed)
    currentIndex = QtCore.pyqtProperty(int, getCurrentIndex, notify=changed)

    hasChanged = QtCore.pyqtProperty(bool, getHasChanged, setHasChanged, notify=changed)
