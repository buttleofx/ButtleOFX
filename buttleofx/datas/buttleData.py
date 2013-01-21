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
        - _graph
        - _currentNodeViewer
        - _currentNodeParam
        - _currentNodeGraph

        This class :
            - containts all data we need to manage the application.
            - receives the undo and redo from QML, and call the cmdManager to do this.
    """
    def init(self, view):
        self._graph = Graph()
        self._graphWrapper = GraphWrapper(self._graph, view)

        self._currentParamNodeName = None
        self._currentParamNodeWrapper = None

        self._currentSelectedNodeName = None
        self._currentSelectedNodeWrapper = None

        self._currentViewerNodeName = None
        self._currentViewerNodeWrapper = None

        return self

    ################################################## GETTERS ET SETTERS ##################################################

    #################### getters ####################

    def getGraph(self):
        return self._graph

    def getGraphWrapper(self):
        return self._graphWrapper

    def getCurrentParamNodeName(self):
        """
            Returns the name of the current param node.
        """
        return self._currentParamNodeName

    def getCurrentSelectedNodeName(self):
        """
            Returns the name of the current selected node.
        """
        return self._currentSelectedNodeName

    def getCurrentViewerNodeName(self):
        """
            Returns the name of the current viewer node.
        """
        return self._currentViewerNodeName

    def getCurrentParamNodeWrapper(self):
        """
            Returns the current param nodeWrapper.
        """
        return self.getGraphWrapper().getNodeWrapper(self.getCurrentParamNodeName())

    def getCurrentSelectedNodeWrapper(self):
        """
            Returns the current selected nodeWrapper.
        """
        return self.getGraphWrapper().getNodeWrapper(self.getCurrentSelectedNodeName())

    def getCurrentViewerNodeWrapper(self):
        """
            Returns the current viewer nodeWrapper.
        """
        return self.getGraphWrapper().getNodeWrapper(self.getCurrentViewerNodeName())

    #################### setters ####################

    def setCurrentParamNodeWrapper(self, nodeWrapper):
        """
            Changes the current param node and emits the change.
        """
        if self._currentParamNodeName == nodeWrapper.getName():
            return
        self._currentParamNodeName = nodeWrapper.getName()
        self.currentParamNodeChanged.emit()

    def setCurrentSelectedNodeWrapper(self, nodeWrapper):
        """
        Changes the current selected node and emits the change.
        """
        if self._currentSelectedNodeName == nodeWrapper.getName():
            return
        self._currentSelectedNodeName = nodeWrapper.getName()
        self.currentSelectedNodeChanged.emit()

    def setCurrentViewerNodeWrapper(self, nodeWrapper):
        """
        Changes the current viewer node and emits the change.
        """
        if self._currentViewerNodeName == nodeWrapper.getName():
            return
        self._currentViewerNodeName = nodeWrapper.getName()
        self.currentViewerNodeChanged.emit()

    ################################################## EVENT FROM QML #####################################################

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


    ################################################## DATA EXPOSED TO QML ##################################################

    # graphWrapper
    graphWrapper = QtCore.Property(QtCore.QObject, getGraphWrapper, constant=True)

    # current param, view, and selected node
    currentParamNodeChanged = QtCore.Signal()
    currentParamNodeWrapper = QtCore.Property(QtCore.QObject, getCurrentParamNodeWrapper, setCurrentParamNodeWrapper, notify=currentParamNodeChanged)
    currentViewerNodeChanged = QtCore.Signal()
    currentViewerNodeWrapper = QtCore.Property(QtCore.QObject, getCurrentViewerNodeWrapper, setCurrentViewerNodeWrapper, notify=currentViewerNodeChanged)
    currentSelectedNodeChanged = QtCore.Signal()
    currentSelectedNodeWrapper = QtCore.Property(QtCore.QObject, getCurrentSelectedNodeWrapper, setCurrentSelectedNodeWrapper, notify=currentSelectedNodeChanged)
