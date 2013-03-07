# common
from buttleofx.core.params import Param
# undo redo
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands.params import CmdSetParamString


class ParamString(Param):
    """
        Core class, which represents a string parameter.
        Contains :
            - _oldValue : the old value of the param.
            - _hasChanged : to know if the value of the param is changed by the user (at least once).
    """

    def __init__(self, tuttleParam):
        Param.__init__(self, tuttleParam)
        
        self._oldValue = self.getValue()

        self._hasChanged = False

    #################### getters ####################

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

    def getHasChanged(self):
        return self._hasChanged

    #################### setters ####################

    def setHasChanged(self, changed):
        self._hasChanged = changed

    def setOldValue(self, value):
        self._oldValue = value

    def setValue(self, value):
        # if the value of the param changed, we put the boolean to True but the only way to put in to false is when the user reinitialises
        # the value with right click (in QML)
        if(self.getDefaultValue() != value):
            self._hasChanged = True
        
        # push command
        cmdUpdate = CmdSetParamString(self, str(value))
        cmdManager = CommandManager()
        cmdManager.push(cmdUpdate)
