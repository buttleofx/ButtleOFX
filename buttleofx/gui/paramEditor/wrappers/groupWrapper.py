from .paramWrapper import ParamWrapper

from PyQt5 import QtCore


class GroupWrapper(ParamWrapper):
    """
        Gui class, which maps a ParamGroup.
    """

    def __init__(self, param):
        ParamWrapper.__init__(self, param)

    # #################### getters ####################

    def getLabel(self):
        return self._param.getLabel()

    changed = QtCore.pyqtSignal()

    # ################################################## DATA EXPOSED TO QML ##################################################

    label = QtCore.pyqtProperty(str, getLabel, constant=True)
