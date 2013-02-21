from quickmamba.patterns import Signal
# undo redo
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands.params import CmdSetParamBoolean


class ParamBoolean(object):
    """
        Core class, which represents a boolean parameter.
        Contains :
            - _tuttleParam : link to the corresponding tuttleParam.
            - changed : signal emitted when we set value(s) of the param.
    """

    def __init__(self, tuttleParam):
        self._tuttleParam = tuttleParam

        self.changed = Signal()

    #################### getters ####################

    def getTuttleParam(self):
        return self._tuttleParam

    def getParamType(self):
        return "ParamBoolean"

    def getDefaultValue(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropDefault")

    def getValue(self):
        return self._tuttleParam.getBoolValue()

    def getText(self):
        return self._tuttleParam.getName()[0].capitalize() + self._tuttleParam.getName()[1:]

    def isSecret(self):
        return self._tuttleParam.getSecret()

    #################### setters ####################

    def setValue(self, value):
        # Push the command
        cmdUpdate = CmdSetParamBoolean(self, value)
        cmdManager = CommandManager()
        cmdManager.push(cmdUpdate)
