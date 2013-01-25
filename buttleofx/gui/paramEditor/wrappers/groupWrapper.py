from PySide import QtCore


class GroupWrapper(QtCore.QObject):
    """
        Gui class, which maps a ParamGroup.
    """

    def __init__(self, param):
        QtCore.QObject.__init__(self)
        self._param = param
        self._param.changed.connect(self.emitChanged)

    # #################### getters ####################

    def getParamType(self):
        return self._param.getParamType()

    # def getParamSet(self):
    #     return self._param.getName()

    def getLabel(self):
        return self._param.getLabel()

    def getName(self):
        return self._param.getName()

    # def getDefaultValue(self):
    #     return self._param.getDefaultValue()

    # def getValue(self):
    #     return self._param.getValue()

    # def getMaximum(self):
    #     return self._param.getMaximum()

    # def getMinimum(self):
    #     return self._param.getMinimum()

    # def getText(self):
    #     return self._param.getText()

    # #################### setters ####################

    # def setValue(self, value):
    #     self._param.setValue(value)

    @QtCore.Signal
    def changed(self):
        pass

    def emitChanged(self):
        self.changed.emit()

    # ################################################## DATA EXPOSED TO QML ##################################################

    paramType = QtCore.Property(unicode, getParamType, constant=True)
    label = QtCore.Property(unicode, getLabel, constant=True)
    name = QtCore.Property(unicode, getName, constant=True)

    # text = QtCore.Property(unicode, getText, notify=changed)
    # value = QtCore.Property(unicode, getValue, setValue, notify=changed)
    # maximum = QtCore.Property(unicode, getMaximum, notify=changed)
    # minimum = QtCore.Property(unicode, getMinimum, notify=changed)