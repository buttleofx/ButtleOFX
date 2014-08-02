from buttleofx.core.params import Param
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands.params import CmdSetParamDouble


class ParamDouble(Param):
    """
        Core class, which represents a double parameter.
        Contains :
            - _oldValue : the old value of the param.
            - _hasChanged : to know if the value of the param is changed by the user (at least once).
    """

    def __init__(self, tuttleParam):
        Param.__init__(self, tuttleParam)

        self._oldValue = self.getValue()

        self._hasChanged = False

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getDefaultValue(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDefault")

    def getHasChanged(self):
        return self._hasChanged

    def getMaximum(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDisplayMax")

    def getMinimum(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDisplayMin")

    def getOldValue(self):
        return self._oldValue

    def getParamDoc(self):
        return self._tuttleParam.getProperties().getStringProperty("OfxParamPropHint")

    def getParamType(self):
        return "ParamDouble"

    def getValue(self):
        return self._tuttleParam.getDoubleValue()

    # ## Setters ## #

    def setHasChanged(self, changed):
        self._hasChanged = changed

    def setOldValue(self, value):
        self._oldValue = value

    # Distinction between setValue and pushValue, because it's a slider we do not push a
    # command until the user don't release the cursor (but we update the model)

    def setValue(self, value):
        # Used to know if bold font or not
        if self.getDefaultValue() != value:
            self.setHasChanged(True)
        self._tuttleParam.setValue(float(value))

    def pushValue(self, newValue):
        if newValue != self.getOldValue():
            # Push the command
            cmdUpdate = CmdSetParamDouble(self, float(newValue))
            cmdManager = CommandManager()
            cmdManager.push(cmdUpdate)
