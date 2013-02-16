from quickmamba.patterns import Signal
# undo redo
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands.params import CmdSetParamDouble3D


class ParamDouble3D(object):
    """
        Core class, which represents a double3D parameter.
        Contains :
            - _paramType : the name of the type of this parameter
    """

    def __init__(self, tuttleParam):
        self._tuttleParam = tuttleParam
        self._oldValue1 = self.getValue1()
        self._oldValue2 = self.getValue2()
        self._oldValue3 = self.getValue3()

        self.changed = Signal()

    #################### getters ####################

    def getTuttleParam(self):
        return self._tuttleParam

    def getParamType(self):
        return "ParamDouble3D"

    def getDefaultValue1(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDefault", 0)

    def getDefaultValue2(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDefault", 1)

    def getDefaultValue3(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDefault", 2)

    def getValues(self):
        return (self.getValue1(), self.getValue2(), self.getValue3())

    def getOldValue1(self):
        return self._oldValue1

    def getOldValue2(self):
        return self._oldValue2

    def getOldValue3(self):
        return self._oldValue3

    def getValue1(self):
        return self._tuttleParam.getDoubleValueAtIndex(0)

    def getValue2(self):
        return self._tuttleParam.getDoubleValueAtIndex(1)

    def getValue3(self):
        return self._tuttleParam.getDoubleValueAtIndex(2)

    def getMinimum1(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropMin", 0)

    def getMaximum1(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropMax", 0)

    def getMinimum2(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropMin", 1)

    def getMaximum2(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropMax", 1)

    def getMinimum3(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropMin", 2)

    def getMaximum3(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropMax", 2)

    def getText(self):
        return self._tuttleParam.getName()[0].capitalize() + self._tuttleParam.getName()[1:]

    #################### setters ####################

    def setValues(self, values):
        self.setValue1(values[0])
        self.setValue2(values[1])
        self.setValue3(values[2])

    def setOldValueAt(self, value, index):
        if index == 0:
            self._oldValue1 = value
        if index == 1:
            self._oldValue2 = value
        if index == 2:
            self._oldValue3 = value

    def setValue1(self, value):
        if value != self.getValue1():
            # Set the value
            self._tuttleParam.setValueAtIndex(0, float(value))
            self.changed()

            # Push the command
            cmdUpdate = CmdSetParamDouble3D(self, (value, self.getValue2(), self.getValue3()), 0)
            cmdManager = CommandManager()
            cmdManager.push(cmdUpdate)

            # Update the viewer
            from buttleofx.data import ButtleDataSingleton
            buttleData = ButtleDataSingleton().get()
            buttleData.updateMapAndViewer()

    def setValue2(self, value):
        if value != self.getValue2():
            # Set the value
            self._tuttleParam.setValueAtIndex(1, float(value))
            self.changed()

            # Push the command
            cmdUpdate = CmdSetParamDouble3D(self, (self.getValue1(), value, self.getValue3()), 1)
            cmdManager = CommandManager()
            cmdManager.push(cmdUpdate)

            # Update the viewer
            from buttleofx.data import ButtleDataSingleton
            buttleData = ButtleDataSingleton().get()
            buttleData.updateMapAndViewer()

    def setValue3(self, value):
        if value != self.getValue3():
            # Set the value
            self._tuttleParam.setValueAtIndex(2, float(value))
            self.changed()

            # Push the command
            cmdUpdate = CmdSetParamDouble3D(self, (self.getValue1(), self.getValue2(), value), 2)
            cmdManager = CommandManager()
            cmdManager.push(cmdUpdate)

            # Update the viewer
            from buttleofx.data import ButtleDataSingleton
            buttleData = ButtleDataSingleton().get()
            buttleData.updateMapAndViewer()
