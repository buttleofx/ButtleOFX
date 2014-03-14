# common
from buttleofx.core.params import Param
# undo redo
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands.params import CmdSetParamString

from PyQt5 import QtCore

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

    def getParamDoc(self):
        return self._tuttleParam.getProperties().getStringProperty("OfxParamPropHint")

    def getDefaultValue(self):
        return self._tuttleParam.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)

    def getStringFilePathExist(self):
        return self._tuttleParam.getProperties().getIntProperty("OfxParamPropStringFilePathExists")

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
        self.paramChanged()

    def setOldValue(self, value):
        self._oldValue = value

    def setValue(self, value):
        if(self.getDefaultValue() != value):
            self.setHasChanged(True)
        
        self._tuttleParam.setValue(str(value))

    def pushValue(self, newValue):
        # if it's an url, conversion to local url
        if self.getStringType() == "OfxParamStringIsFilePath":
            print (newValue)
            newValue = QtCore.QUrl(newValue).toLocalFile()
            print (newValue)
        if newValue != self.getOldValue():
            # push the command
            cmdUpdate = CmdSetParamString(self, str(newValue))
            cmdManager = CommandManager()
            cmdManager.push(cmdUpdate)
