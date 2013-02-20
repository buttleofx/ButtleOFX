from quickmamba.patterns import Signal
# undo redo
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands.params import CmdSetParamND


class ParamInt3D(object):
    """
        Core class, which represents a int3D parameter.
        Contains :
            - _tuttleParam : link to the corresponding tuttleParam.
            - _oldValue1, _oldValue2, _oldValue3 : the old values of the param.
            - changed : signal emitted when we set value(s) of the param.
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
        return "ParamInt3D"

    def getDefaultValue1(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropDefault", 0)

    def getDefaultValue2(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropDefault", 1)

    def getDefaultValue3(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropDefault", 2)

    def getValues(self):
        return (self.getValue1(), self.getValue2(), self.getValue3())

    def getOldValue1(self):
        return self._oldValue1

    def getOldValue2(self):
        return self._oldValue2

    def getOldValue3(self):
        return self._oldValue3

    def getValue1(self):
        return self._tuttleParam.getIntValueAtIndex(0)

    def getValue2(self):
        return self._tuttleParam.getIntValueAtIndex(1)

    def getValue3(self):
        return self._tuttleParam.getIntValueAtIndex(2)

    def getMinimum1(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMin", 0)

    def getMaximum1(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMax", 0)

    def getMinimum2(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMin", 1)

    def getMaximum2(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMax", 1)

    def getMinimum3(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMin", 2)

    def getMaximum3(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropMax", 2)

    def getText(self):
        return self._tuttleParam.getName()[0].capitalize() + self._tuttleParam.getName()[1:]
        
    def isSecret(self):
        return self._tuttleParam.getSecret()

    #################### setters ####################

    def setValues(self, values):
        self.setValue1(values[0])
        self.setValue2(values[1])
        self.setValue3(values[2])

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
        if value != self.getValue1():
            # Push the command
            cmdUpdate = CmdSetParamND(self, (value, self.getValue2(), self.getValue3()))
            cmdManager = CommandManager()
            cmdManager.push(cmdUpdate)

    def setValue2(self, value):
        if value != self.getValue2():
            # Push the command
            cmdUpdate = CmdSetParamND(self, (self.getValue1(), value, self.getValue3()))
            cmdManager = CommandManager()
            cmdManager.push(cmdUpdate)

    def setValue3(self, value):
        if value != self.getValue3():
            # Push the command
            cmdUpdate = CmdSetParamND(self, (self.getValue1(), self.getValue2(), value))
            cmdManager = CommandManager()
            cmdManager.push(cmdUpdate)
