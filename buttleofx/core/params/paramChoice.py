# common
from buttleofx.core.params import Param
# undo redo
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands.params import CmdSetParamChoice


class ParamChoice(Param):
    """
        Core class, which represents a choice parameter.
        Contains :
            - _oldValue : the old value of the param.
            - _listValue : the list of possible choices.
            - _hasChanged : to know if the value of the param is changed by the user (at least once).
    """

    def __init__(self, tuttleParam):
        Param.__init__(self, tuttleParam)

        self._oldValue = self.getValue()

        self._listValue = []
        for choice in range(tuttleParam.getProperties().fetchProperty("OfxParamPropChoiceOption").getDimension()):
            self._listValue.append(tuttleParam.getProperties().fetchProperty("OfxParamPropChoiceOption").getStringValue(choice))

        self._hasChanged = False

    #################### getters ####################

    def getParamType(self):
        return "ParamChoice"

    def getDefaultValue(self):
        defaultIndex = self._tuttleParam.getProperties().getIntProperty("OfxParamPropDefault")
        return self._tuttleParam.getProperties().getStringProperty("OfxParamPropChoiceOption",defaultIndex)

    def getOldValue(self):
        return self._oldValue

    def getValue(self):
        return self._tuttleParam.getStringValue()

    def getCurrentIndex(self):
        return self._tuttleParam.getIntValue()

    def getListValue(self):
        return self._listValue

    def getHasChanged(self):
        return self._hasChanged

    #################### setters ####################

    def setOldValue(self, value):
        self._oldValue = value

    def setHasChanged(self, changed):
        self._hasChanged = changed

    def setValue(self, value):
        if(self.getDefaultValue() != value):
            self.setHasChanged(True)
        self._tuttleParam.setValue(str(value))

    def pushValue(self, value):
        if value != self.getOldValue():
            # push the command
            cmdUpdate = CmdSetParamChoice(self, str(value))
            cmdManager = CommandManager()
            cmdManager.push(cmdUpdate)
