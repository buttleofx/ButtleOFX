# common
from buttleofx.core.params import Param
# undo redo
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands.params import CmdSetParamBoolean


class ParamBoolean(Param):
    """
        Core class, which represents a boolean parameter.
        Contains :
            - _hasChanged : to know if the value of the param is changed by the user (at least once).
    """

    def __init__(self, tuttleParam):
        Param.__init__(self, tuttleParam)

        self._hasChanged = False

    #################### getters ####################

    def getParamType(self):
        return "ParamBoolean"

    def getDefaultValue(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropDefault")

    def getValue(self):
        return self._tuttleParam.getBoolValue()

    def getHasChanged(self):
        return self._hasChanged

    #################### setters ####################

    def setHasChanged(self, changed):
        self._hasChanged = changed
        self.paramChanged()

    def setValue(self, value):
        if(self.getDefaultValue() != value):
            self.setHasChanged(True)

        self._tuttleParam.setValue(bool(value))

    def pushValue(self, value):
        # Push the command
        cmdUpdate = CmdSetParamBoolean(self, value)
        cmdManager = CommandManager()
        cmdManager.push(cmdUpdate)
