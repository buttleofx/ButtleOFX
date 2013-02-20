from quickmamba.patterns import Signal
# undo redo
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands.params import CmdSetParamString


class ParamString(object):
    """
        Core class, which represents a string parameter.
        Contains :
            - _tuttleParam : link to the corresponding tuttleParam.
            - _oldValue : the old value of the param.
            - changed : signal emitted when we set value(s) of the param.
    """

    def __init__(self, tuttleParam):
        self._tuttleParam = tuttleParam
        self._oldValue = self.getValue()

        self.changed = Signal()

    #################### getters ####################

    def getTuttleParam(self):
        return self._tuttleParam

    def getParamType(self):
        return "ParamString"

    def getDefaultValue(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)

    def getValue(self):
        return self._tuttleParam.getStringValue()

    def getOldValue(self):
        return self._oldValue

    def getStringType(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropStringMode").getStringValue(0)

    def getText(self):
        return self._tuttleParam.getName()[0].capitalize() + self._tuttleParam.getName()[1:]
        
    def isSecret(self):
        return self._tuttleParam.getSecret()

    #################### setters ####################

    def setOldValue(self, value):
        self._oldValue = value

    def setValue(self, value):
        # push command
        cmdUpdate = CmdSetParamString(self, str(value))
        cmdManager = CommandManager()
        cmdManager.push(cmdUpdate)
