from buttleofx.core.params import Param
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands.params import CmdSetParamND


class ParamInt3D(Param):
    """
        Core class, which represents a int3D parameter.
        Contains :
            - _oldValue1, _oldValue2, _oldValue3 : the old values of the param.
            - _value1HasChanged, _value2HasChanged, _value3HasChanged : to know if a value of the param is changed
                                                                        by the user (at least once).
    """

    def __init__(self, tuttleParam):
        Param.__init__(self, tuttleParam)

        self._oldValue1 = self.getValue1()
        self._oldValue2 = self.getValue2()
        self._oldValue3 = self.getValue3()

        # Used to know if we display the param in font bold or not
        self._value1HasChanged = False
        self._value2HasChanged = False
        self._value3HasChanged = False

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getParamDoc(self):
        return self._tuttleParam.getProperties().getStringProperty("OfxParamPropHint")

    def getParamType(self):
        return "ParamInt3D"

    def getDefaultValue(self):
        return (self.getDefaultValue1(), self.getDefaultValue2(), self.getDefaultValue3())

    def getDefaultValue1(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropDefault", 0)

    def getDefaultValue2(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropDefault", 1)

    def getDefaultValue3(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropDefault", 2)

    def getMaximum1(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMax", 0)

    def getMaximum2(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMax", 1)

    def getMaximum3(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMax", 2)

    def getMinimum1(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMin", 0)

    def getMinimum2(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMin", 1)

    def getMinimum3(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMin", 2)

    def getOldValue1(self):
        return self._oldValue1

    def getOldValue2(self):
        return self._oldValue2

    def getOldValue3(self):
        return self._oldValue3

    def getValue(self):
        return (self.getValue1(), self.getValue2(), self.getValue3())

    def getValue1(self):
        return self._tuttleParam.getIntValueAtIndex(0)

    def getValue1HasChanged(self):
        return self._value1HasChanged

    def getValue2(self):
        return self._tuttleParam.getIntValueAtIndex(1)

    def getValue2HasChanged(self):
        return self._value2HasChanged

    def getValue3(self):
        return self._tuttleParam.getIntValueAtIndex(2)

    def getValue3HasChanged(self):
        return self._value3HasChanged

    # ## Setters ## #

    def setOldValues(self, values):
        self._oldValue1, self._oldValue2, self._oldValue3 = values

    def setValue(self, values):
        if self.getDefaultValue1() != values[0]:
            self.setValue1HasChanged(True)
        if self.getDefaultValue2() != values[1]:
            self.setValue2HasChanged(True)
        if self.getDefaultValue3() != values[2]:
            self.setValue3HasChanged(True)

        self.getTuttleParam().setValue(values)

    def setValue1(self, value):
        if self.getDefaultValue1() != value:
            self.setValue1HasChanged(True)

        if value != self.getValue1():
            # Push the command
            cmdUpdate = CmdSetParamND(self, (value, self.getValue2(), self.getValue3()))
            cmdManager = CommandManager()
            cmdManager.push(cmdUpdate)

    def setValue1HasChanged(self, changed):
        self._value1HasChanged = changed

    def setValue2(self, value):
        if self.getDefaultValue2() != value:
            self.setValue2HasChanged(True)
        if value != self.getValue2():
            # Push the command
            cmdUpdate = CmdSetParamND(self, (self.getValue1(), value, self.getValue3()))
            cmdManager = CommandManager()
            cmdManager.push(cmdUpdate)

    def setValue2HasChanged(self, changed):
        self._value2HasChanged = changed

    def setValue3(self, value):
        if self.getDefaultValue3() != value:
            self.setValue3HasChanged(True)

        if value != self.getValue3():
            # Push the command
            cmdUpdate = CmdSetParamND(self, (self.getValue1(), self.getValue2(), value))
            cmdManager = CommandManager()
            cmdManager.push(cmdUpdate)

    def setValue3HasChanged(self, changed):
        self._value3HasChanged = changed
