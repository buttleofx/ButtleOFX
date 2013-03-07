from PySide import QtCore


class ParamWrapper(QtCore.QObject):
    """
        Define the common methods and fields for paramWrappers.
    """
    def __init__(self, param):
        QtCore.QObject.__init__(self)

        # the buttle param
        self._param = param

        # link buttle param to the paramWrapper
        self._param.paramChanged.connect(self.emitChanged)


    def getParamType(self):
        return self._param.getParamType()

    def isSecret(self):
        return self._param.isSecret()

    def getText(self):
        return self._param.getText()

    # ################################################## DATA EXPOSED TO QML ##################################################

    def emitChanged(self):
        self.changed.emit()

    paramType = QtCore.Property(unicode, getParamType, constant=True)
    text = QtCore.Property(unicode, getText, constant=True)
    isSecret = QtCore.Property(bool, isSecret, constant=True)