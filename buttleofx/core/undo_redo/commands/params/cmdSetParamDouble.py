from buttleofx.core.undo_redo.manageTools import UndoableCommand


class CmdSetParamDouble(UndoableCommand):
    """
        Command that update the value of a paramDouble.
        Attributes :
        - param : the target param wich will be changed by the update
        - newValue : the value wich will be mofidy in the target
        - oldValue : the old value of the target param, wich will be used for reset the target in case of undo command
    """

    def __init__(self, param, newValue):
        self._param = param
        self._oldValue = param.getOldValue()
        self._newValue = newValue

    def undoCmd(self):
        """
        Undoes the update of the param.
        """
        self._param.getTuttleParam().setValue(float(self._oldValue))
        self._param.setOldValue(float(self._oldValue))
        self._param.changed()
        from buttleofx.data import ButtleDataSingleton
        buttleData = ButtleDataSingleton().get()
        buttleData.updateMapAndViewer()

        print "TuttleParam new Value : ", self._param.getValue()

    def redoCmd(self):
        """
        Redoes the update of the param.
        """
        return self.doCmd()

    def doCmd(self):
        """
        Executes the update of the param.
        """
        self._param.getTuttleParam().setValue(float(self._newValue))
        self._param.setOldValue(float(self._newValue))
        self._param.changed()
        from buttleofx.data import ButtleDataSingleton
        buttleData = ButtleDataSingleton().get()
        buttleData.updateMapAndViewer()

        print "TuttleParam new Value : ", self._param.getValue()
