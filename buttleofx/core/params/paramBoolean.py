from buttleofx.core.params import Param
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

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getDefaultValue(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropDefault")

    def getHasChanged(self):
        return self._hasChanged

    def getParamDoc(self):
        return self._tuttleParam.getProperties().getStringProperty("OfxParamPropHint")

    def getParamType(self):
        return "ParamBoolean"

    def getValue(self):
        return self._tuttleParam.getBoolValue()

    # ## Setters ## #

    def setHasChanged(self, changed):
        self._hasChanged = changed

    def setValue(self, value):
        if self.getDefaultValue() != value:
            self.setHasChanged(True)

        self._tuttleParam.setValue(bool(value))

    # ## Others ## #

    def pushValue(self, value):
        # Push the command
        cmdUpdate = CmdSetParamBoolean(self, value)
        cmdManager = CommandManager()
        cmdManager.push(cmdUpdate)
