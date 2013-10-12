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
        self._param.paramChanged.connect(self.emitParamChanged)

    #################### getters ####################

    def getParam(self):
        return self._param

    def getParamType(self):
        return self._param.getParamType()

    def getName(self):
        return self._param.getName()
        
    def getText(self):
        return self._param.getText()

    def isSecret(self):
        return self._param.isSecret()


    # ################################################## DATA EXPOSED TO QML ##################################################

    def emitParamChanged(self):
        self.changed.emit()

    @QtCore.Signal
    def otherParamOfTheNodeChanged(self):
        pass

    def emitOtherParamOfTheNodeChanged(self):
        self.otherParamOfTheNodeChanged.emit()

    paramType = QtCore.Property(str, getParamType, constant=True)
    text = QtCore.Property(str, getText, constant=True)
    isSecret = QtCore.Property(bool, isSecret, notify=otherParamOfTheNodeChanged)
