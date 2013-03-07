# common
from buttleofx.core.params import Param
# undo redo
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands.params import CmdSetParamChoice


class ParamChoice(Param):
    """
        Core class, which represents a choice parameter.
        Contains :
            - _tuttleParam : link to the corresponding tuttleParam.
            - _oldValue : the old value of the param.
            - _listValue : the list of possible choices.
    """

    def __init__(self, tuttleParam):
        Param.__init__(self)
        
        self._tuttleParam = tuttleParam

        self._oldValue = self.getValue()
        
        self._listValue = []
        for choice in range(tuttleParam.getProperties().fetchProperty("OfxParamPropChoiceOption").getDimension()):
            self._listValue.append(tuttleParam.getProperties().fetchProperty("OfxParamPropChoiceOption").getStringValue(choice))

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

    #################### setters ####################

    def setOldValue(self, value):
        self._oldValue = value

    def setValue(self, value):
        # if the value of the param changed, we put the boolean to True but the only way to put in to false is when the user reinitialises
        # the value with right click (in QML)
        if(self.getDefaultValue() != value):
            self._hasChanged = True
        # for the moment we consider that if the user chooses the default value, it's like he didn't modified it, so it's not in bold font
        else:
            self._hasChanged = False
        
        if value != self.getOldValue():
            #Push the command
            cmdUpdate = CmdSetParamChoice(self, value)
            cmdManager = CommandManager()
            cmdManager.push(cmdUpdate)
