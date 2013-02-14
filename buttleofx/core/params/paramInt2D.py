from quickmamba.patterns import Signal
# undo redo
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands.params import CmdSetParamInt2D


class ParamInt2D(object):
    """
        Core class, which represents a int2D parameter.
        Contains :
            - _tuttleParam : link to the corresponding tuttleParam
    """

    def __init__(self, tuttleParam):
        self._tuttleParam = tuttleParam
        self._oldValue1 = self.getValue1()
        self._oldValue2 = self.getValue2()

        self.changed = Signal()

    #################### getters ####################

    def getTuttleParam(self):
        return self._tuttleParam

    def getParamType(self):
        return "ParamInt2D"

    def getDefaultValue1(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropDefault", 0)

    def getDefaultValue2(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropDefault", 1)

    def getValues(self):
        return (self.getValue1(), self.getValue2())

    def getOldValue1(self):
        return self._oldValue1

    def getOldValue2(self):
        return self._oldValue2

    def getValue1(self):
        return self._tuttleParam.getIntValueAtIndex(0)

    def getValue2(self):
        return self._tuttleParam.getIntValueAtIndex(1)

    def getMinimum1(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMin", 0)

    def getMaximum1(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMax", 0)

    def getMinimum2(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMin", 1)

    def getMaximum2(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMax", 1)

    def getText(self):
        return self._tuttleParam.getName()[0].capitalize() + self._tuttleParam.getName()[1:]

    #################### setters ####################

    def setValues(self, values):
        self.setValue1(values[0])
        self.setValue2(values[1])

    def setOldValueAt(self, value, index):
        if index == 0:
            self._oldValue1 = value
        else:
            self._oldValue2 = value

    def setValue1(self, value):
        self._tuttleParam.setValueAtIndex(0, int(value))
        self.changed()

        # Update Viewer
        from buttleofx.data import ButtleDataSingleton
        buttleData = ButtleDataSingleton().get()
        buttleData.updateMapAndViewer()

    def setValue2(self, value):
        self._tuttleParam.setValueAtIndex(1, int(value))
        self.changed()

        # Update Viewer
        from buttleofx.data import ButtleDataSingleton
        buttleData = ButtleDataSingleton().get()
        buttleData.updateMapAndViewer()

    def pushValue(self, newValue, index):
        if index == 0:
            cmdUpdate = CmdSetParamInt2D(self, (newValue, self.getValue2()), 0)
            cmdManager = CommandManager()
            cmdManager.push(cmdUpdate)
        else:
            cmdUpdate = CmdSetParamInt2D(self, (self.getValue1(), newValue), 1)
            cmdManager = CommandManager()
            cmdManager.push(cmdUpdate)
