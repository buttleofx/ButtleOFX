from PyQt5 import QtCore


class ParamWrapper(QtCore.QObject):
    """
        Define the common methods and fields for paramWrappers.
    """

    def __init__(self, param):
        QtCore.QObject.__init__(self)

        # The buttle param
        self._param = param

        # Link buttle param to the paramWrapper
        self._param.paramChanged.connect(self.emitParamChanged)

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getParam(self):
        return self._param

    def getParamType(self):
        return self._param.getParamType()

    def getParamDoc(self):
        return self._param.getParamDoc()

    def getParamName(self):
        return self._param.getName()

    def getParamText(self):
        return self._param.getText()

    # ## Others ## #

    def isSecret(self):
        return self._param.isSecret()

    def emitParamChanged(self):
        self.changed.emit()

    def emitOtherParamOfTheNodeChanged(self):
        self.otherParamOfTheNodeChanged.emit()

    # ############################################# Data exposed to QML ############################################## #

    otherParamOfTheNodeChanged = QtCore.pyqtSignal()

    paramType = QtCore.pyqtProperty(str, getParamType, constant=True)
    paramText = QtCore.pyqtProperty(str, getParamText, constant=True)
    doc = QtCore.pyqtProperty(str, getParamDoc, constant=True)
    isSecret = QtCore.pyqtProperty(bool, isSecret, notify=otherParamOfTheNodeChanged)
