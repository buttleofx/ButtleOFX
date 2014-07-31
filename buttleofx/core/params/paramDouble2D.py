from buttleofx.core.params import Param
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands.params import CmdSetParamND


class ParamDouble2D(Param):
    """
        Core class, which represents a double2D parameter.
        Contains :
            - _oldValue1, _oldValue2 : the old values of the param.
            - _value1HasChanged, _value2HasChanged : to know if a value of the param is changed
                                                     by the user (at least once).
    """

    def __init__(self, tuttleParam):
        Param.__init__(self, tuttleParam)

        self._oldValue1 = self.getValue1()
        self._oldValue2 = self.getValue2()

        # Used to know if we display the param in bold font or not
        self._value1HasChanged = False
        self._value2HasChanged = False

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getDefaultValue(self):
        return (self.getDefaultValue1(), self.getDefaultValue2())

    def getDefaultValue1(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDefault", 0)

    def getDefaultValue2(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDefault", 1)

    def getMinimum1(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDisplayMin", 0)

    def getMinimum2(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDisplayMin", 1)

    def getMaximum1(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDisplayMax", 0)

    def getMaximum2(self):
        return self._tuttleParam.getProperties().getDoubleProperty("OfxParamPropDisplayMax", 1)

    def getOldValue1(self):
        return self._oldValue1

    def getOldValue2(self):
        return self._oldValue2

    def getParamDoc(self):
        return self._tuttleParam.getProperties().getStringProperty("OfxParamPropHint")

    def getParamType(self):
        return "ParamDouble2D"

    def getParent(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropParent").getStringValue(0)

    def getValue(self):
        return (self.getValue1(), self.getValue2())

    def getValue1(self):
        return self._tuttleParam.getDoubleValueAtIndex(0)

    def getValue1HasChanged(self):
        return self._value1HasChanged

    def getValue2(self):
        return self._tuttleParam.getDoubleValueAtIndex(1)

    def getValue2HasChanged(self):
        return self._value2HasChanged

    # ## Setters ## #

    def setOldValues(self, values):
        self._oldValue1, self._oldValue2 = values

    def setValue(self, values):
        if self.getDefaultValue1() != values[0]:
            self.setValue1HasChanged(True)
        if self.getDefaultValue2() != values[1]:
            self.setValue2HasChanged(True)

        self.getTuttleParam().setValue(values)

    def setValue1(self, value):
        # If the value which is setting is different of the default value,
        # so the value has changed and title of param is displayed in bold in QML
        if self.getDefaultValue1() != value:
            self.setValue1HasChanged(True)

        if value != self.getValue1():
            # Push the command
            cmdUpdate = CmdSetParamND(self, (value, self.getValue2()))
            cmdManager = CommandManager()
            cmdManager.push(cmdUpdate)

    def setValue1HasChanged(self, changed):
        self._value1HasChanged = changed

    def setValue2(self, value):
        if self.getDefaultValue2() != value:
            self.setValue2HasChanged(True)

        if value != self.getValue2():
            # Set the command
            cmdUpdate = CmdSetParamND(self, (self.getValue1(), value))
            cmdManager = CommandManager()
            cmdManager.push(cmdUpdate)

    def setValue2HasChanged(self, changed):
        self._value2HasChanged = changed
