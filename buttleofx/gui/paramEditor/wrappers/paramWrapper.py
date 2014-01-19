from PyQt5 import QtCore


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

    def getParamDoc(self):
        return self._param.getParamDoc()

    def getName(self):
        return self._param.getName()
        
    def getText(self):
        return self._param.getText()

    def isSecret(self):
        return self._param.isSecret()


    # ################################################## DATA EXPOSED TO QML ##################################################

    def emitParamChanged(self):
        self.changed.emit()

    otherParamOfTheNodeChanged = QtCore.pyqtSignal()

    def emitOtherParamOfTheNodeChanged(self):
        self.otherParamOfTheNodeChanged.emit()

    paramType = QtCore.pyqtProperty(str, getParamType, constant=True)
    text = QtCore.pyqtProperty(str, getText, constant=True)
    doc = QtCore.pyqtProperty(str, getParamDoc, constant=True)
    isSecret = QtCore.pyqtProperty(bool, isSecret, notify=otherParamOfTheNodeChanged)
