import logging
from PyQt5 import QtCore, QtGui
from quickmamba.models import QObjectListModel


class PluginWrapper(QtCore.QObject):
    """
        Define the common methods and fields for pluginWrapper.
    """

    def __init__(self, plugin):
        QtCore.QObject.__init__(self)

        self._plugin = plugin

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getLabel(self):
        return self._plugin.getDescriptor().getLabel()

    def getPlugin(self):
        return self._plugin

    def getPluginDescription(self):
        return self._plugin.getDescriptor().getProperties().getStringProperty("OfxPropPluginDescription")

    def getPluginGroup(self):
        return self._plugin.getDescriptor().getProperties().getStringProperty("OfxImageEffectPluginPropGrouping")

    def getType(self):
        return self._plugin.getIdentifier()

    # ############################################# Data exposed to QML ############################################## #

    pluginGroup = QtCore.pyqtProperty(str, getPluginGroup, constant=True)
    pluginType = QtCore.pyqtProperty(str, getType, constant=True)
    pluginLabel = QtCore.pyqtProperty(str, getLabel, constant=True)
    pluginDescription = QtCore.pyqtProperty(str, getPluginDescription, constant=True)
