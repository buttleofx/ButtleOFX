from PySide import QtCore
#quickmamba
from quickmamba.models import QObjectListModel


class ChoiceWrapper(QtCore.QObject):
    def __init__(self, param):
        QtCore.QObject.__init__(self)
        self._param = param

    #################### getters ####################

    def getParamType(self):
        return self._param.paramType

    def getText(self):
        return self._param.text

    def getListValue(self):
        tmp = self._param.listValue
        self._param.listValue = QObjectListModel()
        for value in tmp:
            #["coucou", "ohoh", "ahahah"]:
            self._param.listValue.append(value)
        return self._param.listValue

    def getValue(self):
            return self._param.value

    #################### setters ####################

    def setParamType(self, paramType):
        self._param.paramType = paramType

    def setText(self, text):
        self._param.text = text

    def setListValue(self, listValue):
        self._param.listValue = listValue

    def setValue(self, value):
        self._param.value = value

    # Just temporary : paramType must be constant
    changed = QtCore.Signal()

    paramType = QtCore.Property(unicode, getParamType, setParamType, notify=changed)
    text = QtCore.Property(unicode, getText, setText, notify=changed)
    listValue = QtCore.Property("QVariant", getListValue, setListValue, notify=changed)
    value = QtCore.Property(unicode, getValue, setValue, notify=changed)
