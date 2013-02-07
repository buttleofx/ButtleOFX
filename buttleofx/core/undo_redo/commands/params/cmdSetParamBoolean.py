from buttleofx.core.undo_redo.manageTools import UndoableCommand


class CmdSetParamBoolean(UndoableCommand):
    """
        Command that update the value of a paramInt.
        Attributes :
        - param : the target param wich will be changed by the update
        - newValue : the value wich will be mofidy in the target
    """

    def __init__(self, param, newValue):
        self._param = param
        self._newValue = newValue

    def undoCmd(self):
        """
        Undoes the update of the param.
        """
        print "Undo Boolean"
        if self._param.getTuttleParam().getBoolValue() == True:
            print "True"
            self._param.getTuttleParam().setValue(False)
        else:
            print "False"
            self._param.getTuttleParam().setValue(True)
        self._param.changed()

        from buttleofx.data import ButtleDataSingleton
        buttleData = ButtleDataSingleton().get()
        buttleData.updateMapAndViewer()

    def redoCmd(self):
        """
        Redoes the update of the param.
        """
        print "Redo Boolean"
        print self._param.getTuttleParam().getBoolValue()
        return self.doCmd()

    def doCmd(self):
        """
        Executes the update of the param.
        """
        self._param.getTuttleParam().setValue((bool)(self._newValue))
        self._param.changed()

        from buttleofx.data import ButtleDataSingleton
        buttleData = ButtleDataSingleton().get()
        buttleData.updateMapAndViewer()
