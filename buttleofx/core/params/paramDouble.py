# common
from buttleofx.core.params import Param
# undo redo
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands.params import CmdSetParamDouble


class ParamDouble(Param):
    """
        Core class, which represents a double parameter.
        Contains :
            - _tuttleParam : link to the corresponding tuttleParam.
            - _oldValue : the old value of the param.
    """

    def __init__(self, tuttleParam):
        Param.__init__(self)

        self._tuttleParam = tuttleParam

        self._oldValue = self.getValue()

    #################### getters ####################

    def getTuttleParam(self):
        return self._tuttleParam

    def getParamType(self):
        return "ParamDouble"

    def getDefaultValue(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDefault")

    def getOldValue(self):
        return self._oldValue

    def getValue(self):
        return self._tuttleParam.getDoubleValue()

    def getMinimum(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDisplayMin")

    def getMaximum(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDisplayMax")

    def getText(self):
        return self._tuttleParam.getName()[0].capitalize() + self._tuttleParam.getName()[1:]

    #################### setters ####################

    def setOldValue(self, value):
        self._oldValue = value

    # distinction between setValue and pushValue, because it's a slider : we do not push a command until the user don't release the cursor (but we update the model).

    def setValue(self, value):
        # used to know if bold font or not
        if(self.getDefaultValue() != value):
            self._hasChanged = True
        self._tuttleParam.setValue(float(value))
        self.changed()

    def pushValue(self, newValue):
        if newValue != self.getOldValue():
            # Push the command
            cmdUpdate = CmdSetParamDouble(self, float(newValue))
            cmdManager = CommandManager()
            cmdManager.push(cmdUpdate)
