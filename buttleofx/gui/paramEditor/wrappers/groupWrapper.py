from PySide import QtCore


class GroupWrapper(QtCore.QObject):
    """
        Gui class, which maps a ParamGroup.
    """

    def __init__(self, param):
        QtCore.QObject.__init__(self)
        self._param = param

    # #################### getters ####################

    def getParamType(self):
        return self._param.getParamType()

    def getLabel(self):
        return self._param.getLabel()

    def getName(self):
        return self._param.getName()
        
    def isSecret(self):
        return self._param.isSecret()

    @QtCore.Signal
    def changed(self):
        pass

    # ################################################## DATA EXPOSED TO QML ##################################################

    paramType = QtCore.Property(unicode, getParamType, constant=True)
    label = QtCore.Property(unicode, getLabel, constant=True)
    name = QtCore.Property(unicode, getName, constant=True)
