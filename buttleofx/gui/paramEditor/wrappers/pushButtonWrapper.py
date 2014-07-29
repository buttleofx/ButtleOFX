from PyQt5 import QtCore
from .paramWrapper import ParamWrapper


class PushButtonWrapper(ParamWrapper):
    """
        GUI class, which maps a ParamPushButton.
    """

    def __init__(self, param):
        ParamWrapper.__init__(self, param)

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getName(self):
        return self._param.getName()

    def getEnabled(self):
        return self._param.getEnabled()

    # ############################################# Data exposed to QML ############################################## #

    changed = QtCore.pyqtSignal()

    name = QtCore.pyqtProperty(str, getName, constant=True)
    enabled = QtCore.pyqtProperty(bool, getEnabled, constant=True)
