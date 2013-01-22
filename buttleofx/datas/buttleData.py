# Tuttle
from pyTuttle import tuttle
from buttleofx.datas import tuttleTools

from quickmamba.models import QObjectListModel

from PySide import QtCore
# core : graph
from buttleofx.core.graph import Graph
# gui : graphWrapper
from buttleofx.gui.graph import GraphWrapper
# undo redo
from buttleofx.core.undo_redo.manageTools import CommandManager
#quickmamba
from quickmamba.patterns import Singleton


class ButtleData(QtCore.QObject, Singleton):
    """
        Class ButtleData defined by:
        - _graphWrapper
        - soon _currentNodeViewer
        - soon _currentNodeParam

        This class :
            - containts all data we need to manage the application.
            - receives the undo and redo from QML, and call the cmdManager to do this.
    """
    def init(self, view):
        self._graphWrapper = GraphWrapper(Graph(), view)
        return self

    def getGraphWrapper(self):
        return self._graphWrapper

    @QtCore.Slot()
    def undo(self):
        """
            Call the cmdManager to undo the last command.
        """
        cmdManager = CommandManager()
        cmdManager.undo()

    @QtCore.Slot()
    def redo(self):
        """
            Call the cmdManager to redo the last command.
        """
        cmdManager = CommandManager()
        cmdManager.redo()

    def getQObjectPluginsNames(self):
        """
            Returns a QObjectListModel of all names of Tuttle's plugins.
        """
        pluginsNames = QObjectListModel(self)
        pluginsNames.setObjectList(tuttleTools.getPluginsNames())
        return pluginsNames

    tuttlePluginsNames = QtCore.Property(QtCore.QObject, getQObjectPluginsNames, constant=True)
    graphWrapper = QtCore.Property(QtCore.QObject, getGraphWrapper, constant=True)
