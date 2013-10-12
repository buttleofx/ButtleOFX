from .paramWrapper import ParamWrapper

from PySide import QtCore


class PageWrapper(ParamWrapper):
    """
        Gui class, which maps a ParamPage.
    """

    def __init__(self, param):
        ParamWrapper.__init__(self, param)

    # #################### getters ####################

    def getLabel(self):
        return self._param.getLabel()

    @QtCore.Signal
    def changed(self):
        pass

    # ################################################## DATA EXPOSED TO QML ##################################################

    label = QtCore.Property(str, getLabel, constant=True)
