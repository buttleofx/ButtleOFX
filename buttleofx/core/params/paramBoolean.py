# common
from buttleofx.core.params import Param
# undo redo
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands.params import CmdSetParamBoolean


class ParamBoolean(Param):
    """
        Core class, which represents a boolean parameter.
        Contains :
            - _tuttleParam : link to the corresponding tuttleParam.
    """

    def __init__(self, tuttleParam):
        Param.__init__(self)

        self._tuttleParam = tuttleParam


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

    #################### setters ####################

    def setValue(self, value):
        # if the value of the param changed, we put the boolean to True but the only way to put in to false is when the user reinitialises
        # the value with right click (in QML)
        if(self.getDefaultValue() != value):
            self._hasChanged = True
        # Push the command
        cmdUpdate = CmdSetParamBoolean(self, value)
        cmdManager = CommandManager()
        cmdManager.push(cmdUpdate)
