from quickmamba.patterns import Signal
# undo redo
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands.params import CmdSetParamDouble


class ParamDouble(object):
    """
        Core class, which represents a double parameter.
        Contains :
            - _tuttleParam : link to the corresponding tuttleParam
    """

    def __init__(self, tuttleParam):
        self._tuttleParam = tuttleParam

        self.changed = Signal()

    #################### getters ####################

    def getTuttleParam(self):
        return self._tuttleParam

    def getParamType(self):
        return "ParamDouble"

    def getDefaultValue(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDefault", 0)

    def getValue(self):
        return self._tuttleParam.getDoubleValue()

    def getMinimum(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDisplayMin", 0)

    def getMaximum(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDisplayMax", 0)

    def getText(self):
        return self._tuttleParam.getName()

    #################### setters ####################

    def setValue(self, newValue):
        from buttleofx.data import ButtleDataSingleton
        buttleData = ButtleDataSingleton().get()
        cmdUpdate = CmdSetParamDouble(self, newValue)
        cmdManager = CommandManager()
        cmdManager.push(cmdUpdate)
        buttleData.paramChanged()
