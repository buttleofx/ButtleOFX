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

    #################### getters ####################

    def getParamType(self):
        return self._param.getParamType()

    def getListValue(self):
        tmp = self._param.getListValue()
        self._param._listValue = QObjectListModel()
        for value in tmp:
            self._param._listValue.append(value)
        return self._param._listValue

    def getValue(self):
            return self._param.getValue()

    def getText(self):
        return self._param.getText()

    #################### setters ####################

    def setParamType(self, paramType):
        self._param.setParamType(paramType)

    def setListValue(self, listValue):
        self._param.setListValue(listValue)

    def setValue(self, value):
        self._param.setValue(value)

    def setText(self, text):
        self._param.setText(text)

    @QtCore.Signal
    def changed(self):
        pass

    def emitChanged(self):
        self.changed.emit()

    ################################################## DATA EXPOSED TO QML ##################################################

    paramType = QtCore.Property(unicode, getParamType, setParamType, notify=changed)
    text = QtCore.Property(unicode, getText, setText, notify=changed)
    listValue = QtCore.Property("QVariant", getListValue, constant=True)
    value = QtCore.Property(unicode, getValue, setValue, notify=changed)
