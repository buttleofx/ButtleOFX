from .paramWrapper import ParamWrapper

from PySide import QtCore


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

    @QtCore.Signal
    def changed(self):
        pass

    ################################################## DATA EXPOSED TO QML ##################################################

    name = QtCore.Property(str, getName, constant=True)
    enabled = QtCore.Property(bool, getEnabled, constant=True)
