from PyQt5 import QtCore
from .paramWrapper import ParamWrapper


class PageWrapper(ParamWrapper):
    """
        GUI class, which maps a ParamPage.
    """

    def __init__(self, param):
        ParamWrapper.__init__(self, param)

    # ######################################## Methods private to this class ####################################### #

    def getLabel(self):
        return self._param.getLabel()

    # ############################################# Data exposed to QML ############################################## #

    changed = QtCore.pyqtSignal()

    label = QtCore.pyqtProperty(str, getLabel, constant=True)
