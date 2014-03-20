from PyQt5 import QtCore, QtGui
import logging
#quickmamba
from quickmamba.models import QObjectListModel

class PluginWrapper(QtCore.QObject):
    """
        Define the common methods and fields for pluginWrapper.
    """

    def __init__(self, plugin):
        QtCore.QObject.__init__(self)

        self._plugin = plugin

    #################### getters ####################

    def getPlugin(self):
        return self._plugin

    def getType(self):
        return self._plugin.getIdentifier()

    def getLabel(self):
        return self._plugin.getDescriptor().getLabel()

    def getPluginDescription(self):
        return self._plugin.getDescriptor().getProperties().getStringProperty("OfxPropPluginDescription")

    def getPluginGroup(self):
        return self._plugin.getDescriptor().getProperties().getStringProperty("OfxImageEffectPluginPropGrouping")

    ################################################## DATA EXPOSED TO QML ##################################################
           
    pluginGroup = QtCore.pyqtProperty(str, getPluginGroup, constant=True)   
    pluginType = QtCore.pyqtProperty(str, getType, constant=True)
    pluginLabel = QtCore.pyqtProperty(str, getLabel, constant=True)
    pluginDescription = QtCore.pyqtProperty(str, getPluginDescription, constant=True)