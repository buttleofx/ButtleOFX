from PySide import QtCore
# common
from paramWrapper import ParamWrapper
#quickmamba
from quickmamba.models import QObjectListModel


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

    @QtCore.Slot(result=str)
    def getDefaultValue(self):
        self.setHasChanged(False)
        return self._param.getDefaultValue()

    def getListValue(self):
        return self._listValue

    def getValue(self):
        return self._param.getValue()

    def getHasChanged(self):
        return self._param.getHasChanged()

    #################### setters ####################

    def setValue(self, value):
        self._param.setValue(value)

    def setHasChanged(self, changed):
        self._param.setHasChanged(changed)

    @QtCore.Slot(str)
    def pushValue(self, value):
        self._param.pushValue(value)

    @QtCore.Signal
    def changed(self):
        pass

    ################################################## DATA EXPOSED TO QML ##################################################

    listValue = QtCore.Property(QtCore.QObject, getListValue, constant=True)
    value = QtCore.Property(str, getValue, setValue, notify=changed)

    hasChanged = QtCore.Property(bool, getHasChanged, setHasChanged, notify=changed)