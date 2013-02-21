import logging
from buttleofx.core.undo_redo.manageTools import UndoableCommand


class CmdSetParamChoice(UndoableCommand):
    """
        Command that update the value of a paramInt.
        Attributes :
        - _param : the target buttle param which will be changed by the update.
        - _oldValue : the old value of the target param, which will be used for reset the target in case of undo command.
        - _newValue : the value which will be mofidied.
    """

    def __init__(self, param, newValue):
        self._param = param
        self._oldValue = param.getOldValue()
        self._newValue = newValue

    def undoCmd(self):
        """
        Undoes the update of the param.
        """
        self._param.getTuttleParam().setValue(str(self._oldValue))
        self._param.setOldValue(str(self._oldValue))
        self._param.changed()

    def redoCmd(self):
        """
        Redoes the update of the param.
        """
        return self.doCmd()

    def doCmd(self):
        """
        Executes the update of the param.
        """
        self._param.getTuttleParam().setValue(str(self._newValue))
        self._param.setOldValue(str(self._newValue))
        self._param.changed()
