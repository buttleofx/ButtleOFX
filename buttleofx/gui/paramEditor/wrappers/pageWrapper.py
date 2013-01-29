from PySide import QtCore


class PageWrapper(QtCore.QObject):
    """
        Gui class, which maps a ParamPage.
    """

    def __init__(self, param):
        QtCore.QObject.__init__(self)
        self._param = param
        self._param.changed.connect(self.emitChanged)

    # #################### getters ####################

    def getParamType(self):
        return self._param.getParamType()

    def getLabel(self):
        return self._param.getLabel()

    def getName(self):
        return self._param.getName()

    @QtCore.Signal
    def changed(self):
        pass

    def emitChanged(self):
        self.changed.emit()

    # ################################################## DATA EXPOSED TO QML ##################################################

    paramType = QtCore.Property(unicode, getParamType, constant=True)
    label = QtCore.Property(unicode, getLabel, constant=True)
    name = QtCore.Property(unicode, getName, constant=True)
