from PyQt5 import QtCore
from buttleofx.core.undo_redo.manageTools import UndoableCommand


class CmdSetParamBoolean(UndoableCommand):
    """
        Command that update the value of a paramInt.
        Attributes :
        - _param : the target buttle param which will be changed by the update.
        - _newValue : the value which will be mofidied.
    """

    def __init__(self, param, newValue):
        self._param = param
        self._newValue = newValue

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getLabel(self):
        return "Modify param '{0}'".format(self._param.getName())

    def getParam(self):
        return self._param

    # ## Others ## #

    def doCmd(self):
        """
        Executes the update of the param.
        """
        self._param.getTuttleParam().setValue((bool)(self._newValue))
        self._param.paramChanged()

    def redoCmd(self):
        """
        Redoes the update of the param.
        """
        return self.doCmd()

    def undoCmd(self):
        """
        Undoes the update of the param.
        """
        if self._param.getTuttleParam().getBoolValue():
            self._param.getTuttleParam().setValue(False)
        else:
            self._param.getTuttleParam().setValue(True)
        self._param.paramChanged()

    # ############################################# Data exposed to QML ############################################# #

    param = QtCore.pyqtProperty(str, getParam, constant=True)
