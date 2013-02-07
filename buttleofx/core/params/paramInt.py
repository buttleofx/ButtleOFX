from quickmamba.patterns import Signal
# undo redo
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands.params import CmdSetParamInt


class ParamInt(object):
    """
        Core class, which represents an int parameter.
        Contains :
            - _tuttleParam : link to the corresponding tuttleParam
    """

    def __init__(self, tuttleParam):
        self._tuttleParam = tuttleParam
        self._oldValue = self.getValue()

        self.changed = Signal()

    #################### getters ####################

    def getTuttleParam(self):
        return self._tuttleParam

    def getParamType(self):
        return "ParamInt"

    def getDefaultValue(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropDefault")

    def getOldValue(self):
        return self._oldValue

    def getValue(self):
        return self._tuttleParam.getIntValue()

    def getMinimum(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropDisplayMin")

    def getMaximum(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropDisplayMax")

    def getText(self):
        return self._tuttleParam.getName()[0].capitalize() + self._tuttleParam.getName()[1:]

    #################### setters ####################

    def setOldValue(self, value):
        self._oldValue = value

    def setValue(self, value):
        self._tuttleParam.setValue(int(value))
        self.changed()

    def pushValue(self, newValue):
        cmdUpdate = CmdSetParamInt(self, newValue)
        cmdManager = CommandManager()
        cmdManager.push(cmdUpdate)
