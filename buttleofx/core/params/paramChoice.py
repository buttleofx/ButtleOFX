# quickmamba
from quickmamba.patterns import Signal
# undo redo
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands.params import CmdSetParamChoice


class ParamChoice(object):
    """
        Core class, which represents a choice parameter.
        Contains :
            - _tuttleParam : link to the corresponding tuttleParam.
            - _oldValue : the old value of the param.
            - _listValue : the list of possible choices.
            - changed : signal emitted when we set value(s) of the param.
    """

    def __init__(self, tuttleParam):
        self._tuttleParam = tuttleParam

        self._oldValue = self.getValue()
        
        self._listValue = []
        for choice in range(tuttleParam.getProperties().fetchProperty("OfxParamPropChoiceOption").getDimension()):
            self._listValue.append(tuttleParam.getProperties().fetchProperty("OfxParamPropChoiceOption").getStringValue(choice))

        self.changed = Signal()

    #################### getters ####################

    def getTuttleParam(self):
        return self._tuttleParam

    def getParamType(self):
        return "ParamChoice"

    def getDefaultValue(self):
        return self._tuttleParam.getProperties().getStringProperty("OfxParamPropChoiceOption")

    def getOldValue(self):
        return self._oldValue

    def getValue(self):
        return self._tuttleParam.getStringValue()

    def getListValue(self):
        return self._listValue

    def getText(self):
        return self._tuttleParam.getName()[0].capitalize() + self._tuttleParam.getName()[1:]

    def isSecret(self):
        return self._tuttleParam.getSecret()

    #################### setters ####################

    def setOldValue(self, value):
        self._oldValue = value

    def setValue(self, value):
        if value != self.getOldValue():
            #Push the command
            cmdUpdate = CmdSetParamChoice(self, value)
            cmdManager = CommandManager()
            cmdManager.push(cmdUpdate)
