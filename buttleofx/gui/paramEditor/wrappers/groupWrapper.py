from PyQt5 import QtCore
from .paramWrapper import ParamWrapper


class GroupWrapper(ParamWrapper):
    """
        GUI class, which maps a ParamGroup.
    """

    def __init__(self, param):
        ParamWrapper.__init__(self, param)

    # ## Getters ## #

    def getLabel(self):
        return self._param.getLabel()

    # ############################################# Data exposed to QML ############################################## #

    changed = QtCore.pyqtSignal()

    label = QtCore.pyqtProperty(str, getLabel, constant=True)
