from buttleofx.core.undo_redo.manageTools import UndoableCommand


class CmdSetParamString(UndoableCommand):
    """
        Command that update the value of a paramString.
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
        self._param.getTuttleParam().setValue(self._oldValue)
        self._param.setOldValue(self._oldValue)
        self._param.paramChanged()

    def redoCmd(self):
        """
        Redoes the update of the param.
        """
        self.doCmd()

    def doCmd(self):
        """
        Executes the update of the param.
        """
        self._param.getTuttleParam().setValue(self._newValue)
        self._param.setOldValue(self._newValue)
        self._param.paramChanged()
