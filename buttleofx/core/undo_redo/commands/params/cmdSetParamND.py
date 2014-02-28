import logging
from buttleofx.core.undo_redo.manageTools import UndoableCommand
from PyQt5 import QtCore

class CmdSetParamND(UndoableCommand):
    """
        Command that update the value of a paramDouble2D, paramDouble3D, paramInt2D or paramInt3D.
        Attributes :
        - _param : the target buttle param which will be changed by the update.
        - _oldValue : the old values of the target param, which will be used for reset the target in case of undo command.
        - _newValue : the values which will be mofidied.
    """

    def __init__(self, param, newValues):
        self._param = param

        if "2D" in param.getParamType():
            self._oldValues = (param.getOldValue1(), param.getOldValue2())
        elif "3D" in param.getParamType():
            self._oldValues = (param.getOldValue1(), param.getOldValue2(), param.getOldValue3())
        else:
            logging.error(param.getName() + " : do not recognize the type.")
            self._oldValue = None

        self._newValues = newValues

    def getParam(self):
        return self._param

    def undoCmd(self):
        """
        Undoes the update of the param.
        """
        self._param.getTuttleParam().setValue(self._oldValues)
        self._param.setOldValues(self._oldValues)
        self._param.paramChanged()

    def redoCmd(self):
        """
        Redoes the update of the param.
        """
        return self.doCmd()

    def doCmd(self):
        """
        Executes the update of the param.
        """
        self._param.getTuttleParam().setValue(self._newValues)
        self._param.setOldValues(self._newValues)
        self._param.paramChanged()

    param = QtCore.pyqtProperty(str, getParam, constant=True)