# common
from buttleofx.core.params import Param
# undo redo
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands.params import CmdSetParamND


class ParamDouble2D(Param):
    """
        Core class, which represents a double2D parameter.
        Contains :
            - _tuttleParam : link to the corresponding tuttleParam.
            - _oldValue1, _oldValue2 : the old values of the param.
    """

    def __init__(self, tuttleParam):
        Param.__init__(self)
        
        self._tuttleParam = tuttleParam

        self._oldValue1 = self.getValue1()
        self._oldValue2 = self.getValue2()

        # used to know if we display the param in font bold or not
        self._value1HasChanged = False
        self._value2HasChanged = False

    #################### getters ####################

    def getTuttleParam(self):
        return self._tuttleParam

    def getParamType(self):
        return "ParamDouble2D"

    def getDefaultValue1(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDefault", 0)

    def getDefaultValue2(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDefault", 1)

    def getValues(self):
        return (self.getValue1(), self.getValue2())

    def getOldValue1(self):
        return self._oldValue1

    def getOldValue2(self):
        return self._oldValue2

    def getValue1(self):
        return self._tuttleParam.getDoubleValueAtIndex(0)

    def getValue2(self):
        return self._tuttleParam.getDoubleValueAtIndex(1)

    def getMinimum1(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDisplayMin", 0)

    def getMaximum1(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDisplayMax", 0)

    def getMinimum2(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDisplayMin", 1)

    def getMaximum2(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDisplayMax", 1)

    def getText(self):
        return self._tuttleParam.getName()[0].capitalize() + self._tuttleParam.getName()[1:]

    def getParent(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropParent").getStringValue(0)

    def getValue1HasChanged(self):
        return self._value1HasChanged

    def getValue2HasChanged(self):
        return self._value2HasChanged

    #################### setters ####################

    def setOldValues(self, values):
        index = 0
        for value in values:
            if index == 0:
                self._oldValue1 = value
            elif index == 1:
                self._oldValue2 = value
            index += 1

    def setValue1(self, value):
        if(self.getDefaultValue1() != value):
            self._value1HasChanged = True
        if value != self.getValue1():
            # Push the command
            cmdUpdate = CmdSetParamND(self, (value, self.getValue2()))
            cmdManager = CommandManager()
            cmdManager.push(cmdUpdate)

    def setValue2(self, value):
        if(self.getDefaultValue2() != value):
            self._value2HasChanged = True
        if value != self.getValue2():
            # Set the command
            cmdUpdate = CmdSetParamND(self, (self.getValue1(), value))
            cmdManager = CommandManager()
            cmdManager.push(cmdUpdate)

    def setValue1HasChanged(self, changed):
        self._value1HasChanged = changed

    def setValue2HasChanged(self, changed):
        self._value2HasChanged = changed
