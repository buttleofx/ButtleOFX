from buttleofx.core.params import Param
from buttleofx.core.undo_redo.manageTools import globalCommandManager
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
            self._listValue.append(tuttleParam.getProperties().fetchProperty("OfxParamPropChoiceOption").
                                   getStringValueAt(choice))

        self._hasChanged = False

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getCurrentIndex(self):
        return self._tuttleParam.getIntValue()

    def getHasChanged(self):
        return self._hasChanged

    def getListValue(self):
        return self._listValue

    def getDefaultValue(self):
        defaultIndex = self._tuttleParam.getProperties().getIntProperty("OfxParamPropDefault")
        return self._tuttleParam.getProperties().getStringProperty("OfxParamPropChoiceOption", defaultIndex)

    def getOldValue(self):
        return self._oldValue

    def getParamDoc(self):
        return self._tuttleParam.getProperties().getStringProperty("OfxParamPropHint")

    def getParamType(self):
        return "ParamChoice"

    def getValue(self):
        return self._tuttleParam.getStringValue()

    # ## Setters ## #

    def setHasChanged(self, changed):
        self._hasChanged = changed

    def setOldValue(self, value):
        self._oldValue = value

    def setValue(self, value):
        if self.getDefaultValue() != value:
            self.setHasChanged(True)
        self._tuttleParam.setValue(str(value))

    # ## Others ## #

    def pushValue(self, value):
        if value != self.getOldValue():
            # Push the command
            cmdUpdate = CmdSetParamChoice(self, str(value))
            cmdManager = globalCommandManager
            cmdManager.push(cmdUpdate)
