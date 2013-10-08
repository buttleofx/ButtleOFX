from PySide import QtCore
# common
from paramWrapper import ParamWrapper


class GroupWrapper(ParamWrapper):
    """
        Gui class, which maps a ParamGroup.
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

    label = QtCore.Property(unicode, getLabel, constant=True)
