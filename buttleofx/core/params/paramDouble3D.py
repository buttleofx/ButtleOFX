# common
from buttleofx.core.params import Param
# undo redo
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands.params import CmdSetParamND


class ParamDouble3D(Param):
    """
        Core class, which represents a double3D parameter.
        Contains :
            - _tuttleParam : link to the corresponding tuttleParam.
            - _oldValue1, _oldValue2, _oldValue3 : the old values of the param.
            - changed : signal emitted when we set value(s) of the param.
    """

    def __init__(self, tuttleParam):
        Param.__init__(self)

        self._tuttleParam = tuttleParam

        self._oldValue1 = self.getValue1()
        self._oldValue2 = self.getValue2()
        self._oldValue3 = self.getValue3()

        # used to know if we display the param in font bold or not
        self._value1HasChanged = False
        self._value2HasChanged = False
        self._value3HasChanged = False

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

    def getValue1HasChanged(self):
        return self._value1HasChanged

    def getValue2HasChanged(self):
        return self._value2HasChanged

    def getValue3HasChanged(self):
        return self._value3HasChanged

    #################### setters ####################

    def setOldValues(self, values):
        index = 0
        for value in values:
            if index == 0:
                self._oldValue1 = value
            elif index == 1:
                self._oldValue2 = value
            elif index == 2:
                self._oldValue3 = value
            index += 1

    def setValue1(self, value):
        # used to know if bold font or not
        if(self.getDefaultValue1() != value):
            self._value1HasChanged = True

        if value != self.getValue1():
            # Push the command
            cmdUpdate = CmdSetParamND(self, (value, self.getValue2(), self.getValue3()))
            cmdManager = CommandManager()
            cmdManager.push(cmdUpdate)

    def setValue2(self, value):
        # used to know if bold font or not
        if(self.getDefaultValue2() != value):
            self._value2HasChanged = True

        if value != self.getValue2():
            # Push the command
            cmdUpdate = CmdSetParamND(self, (self.getValue1(), value, self.getValue3()))
            cmdManager = CommandManager()
            cmdManager.push(cmdUpdate)

    def setValue3(self, value):
        # used to know if bold font or not
        if(self.getDefaultValue3() != value):
            self._value3HasChanged = True
        
        if value != self.getValue3():
            # Push the command
            cmdUpdate = CmdSetParamND(self, (self.getValue1(), self.getValue2(), value))
            cmdManager = CommandManager()
            cmdManager.push(cmdUpdate)

    def setValue1HasChanged(self, changed):
        self._value1HasChanged = changed

    def setValue2HasChanged(self, changed):
        self._value2HasChanged = changed

    def setValue3HasChanged(self, changed):
        self._value3HasChanged = changed
