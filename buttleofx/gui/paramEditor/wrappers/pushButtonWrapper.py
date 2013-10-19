from .paramWrapper import ParamWrapper

from PyQt5 import QtCore


class PushButtonWrapper(ParamWrapper):
    """
        Gui class, which maps a ParamPushButton.
    """

    def __init__(self, param):
        ParamWrapper.__init__(self, param)

    #################### getters ####################

    def getName(self):
        return self._param.getName()

    def getEnabled(self):
        return self._param.getEnabled()

    changed = QtCore.pyqtSignal()

    ################################################## DATA EXPOSED TO QML ##################################################

    name = QtCore.pyqtProperty(str, getName, constant=True)
    enabled = QtCore.pyqtProperty(bool, getEnabled, constant=True)
