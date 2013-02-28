from PySide import QtCore
#quickmamba
from quickmamba.models import QObjectListModel


class ChoiceWrapper(QtCore.QObject):
    """
        Gui class, which maps a ParamChoice.
    """

    def __init__(self, param):
        QtCore.QObject.__init__(self)
        self._param = param
        self._param.changed.connect(self.emitChanged)

        self._listValue = QObjectListModel()
        for value in self._param.getListValue():
            self._listValue.append(value)

    #################### getters ####################

    def getParamType(self):
        return self._param.getParamType()

    def getListValue(self):
        return self._listValue

    def getValue(self):
        return self._param.getValue()

    @QtCore.Slot(result=str)
    def getDefaultValue(self):
        return self._param.getDefaultValue()

    def getText(self):
        return self._param.getText()

    def isSecret(self):
        return self._param.isSecret()

    def getHasChanged(self):
        return self._param.getHasChanged()

    #################### setters ####################

    def setValue(self, value):
        self._param.setValue(value)

    def setHasChanged(self, changed):
        self._param.setHasChanged(changed)

    @QtCore.Signal
    def changed(self):
        pass

    def emitChanged(self):
        self.changed.emit()

    ################################################## DATA EXPOSED TO QML ##################################################

    paramType = QtCore.Property(unicode, getParamType, constant=True)
    text = QtCore.Property(str, getText, constant=True)
    listValue = QtCore.Property(QtCore.QObject, getListValue, constant=True)
    value = QtCore.Property(str, getValue, setValue, notify=changed)
    hasChanged = QtCore.Property(bool, getHasChanged, setHasChanged, notify=changed)