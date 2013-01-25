from PySide import QtCore
# copy
from copy import copy
# Tuttle
from buttleofx.data import tuttleTools
# quickmamba
from quickmamba.patterns import Singleton
from quickmamba.models import QObjectListModel
# core : graph
from buttleofx.core.graph import Graph
from buttleofx.core.graph.node import Node
from buttleofx.core.graph.connection import IdClip
# gui : graphWrapper
from buttleofx.gui.graph import GraphWrapper
from buttleofx.gui.graph.node import NodeWrapper
# undo redo
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands import CmdSetCoord


class ButtleData(QtCore.QObject):
    """
        Class ButtleData defined by:
        - _graphWrapper
        - _graph
        - _currentNodeViewer
        - _currentNodeParam
        - _currentNodeGraph
        - _currentNodeCopy

        This class :
            - containts all data we need to manage the application.
            - receives the undo and redo from QML, and call the cmdManager to do this.
    """

    _graph = None
    _graphWrapper = None

    _currentParamNodeName = None
    _currentSelectedNodeName = None
    _currentViewerNodeName = None
    
    _computedImage = None

    def init(self, view):
        self._graph = Graph()
        self._graphWrapper = GraphWrapper(self._graph, view)

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
        #self._currentSelectedNodeWrapper = nodeWrapper
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

    ########################## CREATION & DESTRUCTION ############################

    ##### Node #####

    @QtCore.Slot(str, int, int)
    def creationNode(self, nodeType, x, y):
        """
            Function called when we want to create a node from the QML.
        """
        self.getGraph().createNode(nodeType, x, y)

    @QtCore.Slot()
    def destructionNode(self):
        """
            Function called when we want to delete a node from the QML.
        """
        # if at least one node in the graph
        if len(self.getGraphWrapper().getNodeWrappers()) > 0 and len(self.getGraph().getNodes()) > 0:
            # if a node is selected
            if self._currentSelectedNodeName != None:
                self.getGraph().deleteNode(self.getCurrentSelectedNodeWrapper().getNode())

        # set the current nodes
        # if the params of the current node just deleted are display
        if self._currentSelectedNodeName == self._currentParamNodeName:
            self._currentParamNodeName = None
            self.currentParamNodeChanged.emit()
        # if the viewer of the current node just deleted is display
        if self._currentSelectedNodeName == self.currentViewerNodeWrapper:
            self._currentViewerNodeName = None
            self.currentViewerNodeChanged.emit()

    @QtCore.Slot()
    def duplicationNode(self):
        """
            Function called from the QML when we want to duplicate a node.
        """
        # Create node
        self.getGraph().__str__()
        nodeType = self.getCurrentSelectedNodeWrapper().getType()
        coord = self.getCurrentSelectedNodeWrapper().getNode().getCoord()
        self.getGraph().createNode(nodeType, coord[0], coord[1])
        self.getGraph().__str__()

        # Get the current selected node's properties
        nameUser = self.getCurrentSelectedNodeWrapper().getNameUser() + "_duplicate"
        oldCoord = self.getCurrentSelectedNodeWrapper().getNode().getOldCoord()
        tuttleNode = copy(self.getCurrentSelectedNodeWrapper().getNode().getTuttleNode())
        color = self.getCurrentSelectedNodeWrapper().getColor()
        nbInput = self.getCurrentSelectedNodeWrapper().getNbInput()
        image = self.getCurrentSelectedNodeWrapper().getImage()
        # doesn't work : the params are pointer, but we want real copy...
        params = []
        for param in self.getCurrentSelectedNodeWrapper().getNode().getParams():
            params.append(copy(param))

        # Use the current selected node's properties to set the duplicated node's properties
        self.getGraph().getNodes()[-1].setNameUser(nameUser)
        self.getGraph().getNodes()[-1].setOldCoord(oldCoord[0], oldCoord[1])
        self.getGraph().getNodes()[-1].setTuttleNode(tuttleNode)
        self.getGraph().getNodes()[-1].setColor(color.red(), color.green(), color.blue())
        self.getGraph().getNodes()[-1].setNbInput(nbInput)
        self.getGraph().getNodes()[-1].setImage(image)
        self.getGraph().getNodes()[-1].setParams(params)

    ##### Connection #####

    def connect(self, clipOut, clipIn):
        """
            Add a connection between 2 clips.
        """
        self.getGraph().createConnection(clipOut, clipIn)
        self.getGraphWrapper().resetTmpClips()

    def disconnect(self, connection):
        """
            Remove a connection between 2 clips.
        """
        self.getGraph().deleteConnection(connection)
        self.getGraphWrapper().resetTmpClips()

    @QtCore.Slot(str, str, int)
    def clipPressed(self, nodeName, port, clipNumber):
        """
            Function called when a clip is pressed (but not released yet).
            The function replace the tmpClipIn or tmpClipOut.
        """
        position = self.getGraphWrapper().getPositionClip(nodeName, port, clipNumber)
        idClip = IdClip(nodeName, port, clipNumber, position)
        if (port == "input"):
            self.getGraphWrapper().setTmpClipIn(idClip)
        elif (port == "output"):
            self.getGraphWrapper().setTmpClipOut(idClip)

    @QtCore.Slot(str, str, int)
    def clipReleased(self, nodeName, port, clipNumber):
        """
            Function called when a clip is released (after pressed).
        """
        if (port == "input"):
            #if there is a tmpNodeOut
            if (self.getGraphWrapper().getTmpClipOut() != None and self.getGraphWrapper().getTmpClipOut()._nodeName != nodeName):
                position = self.getGraphWrapper().getPositionClip(nodeName, port, clipNumber)
                idClip = IdClip(nodeName, port, clipNumber, position)
                if self.getGraphWrapper().canConnect(self.getGraphWrapper().getTmpClipOut(), idClip):
                    self.connect(self.getGraphWrapper().getTmpClipOut(), idClip)
                elif self.getGraph().contains(self.getGraphWrapper().getTmpClipOut()) and self.getGraph().contains(idClip):
                    self.disconnect(self.getGraphWrapper().getConnectionByClips(self.getGraphWrapper().getTmpClipOut(), idClip))
                else:
                    print "Unable to connect or delete the nodes."

        elif (port == "output"):
            #if there is a tmpNodeIn
            if (self.getGraphWrapper().getTmpClipIn() != None and self.getGraphWrapper().getTmpClipIn()._nodeName != nodeName):
                position = self.getGraphWrapper().getPositionClip(nodeName, port, clipNumber)
                idClip = IdClip(nodeName, port, clipNumber, position)
                if self.getGraphWrapper().canConnect(idClip, self.getGraphWrapper().getTmpClipIn()):
                    self.connect(idClip, self.getGraphWrapper().getTmpClipIn())
                elif self.getGraph().contains(self.getGraphWrapper().getTmpClipIn()) and self.getGraph().contains(idClip):
                    self.disconnect(self.getGraphWrapper().getConnectionByClips(idClip, self.getGraphWrapper().getTmpClipIn()))
                else:
                    print "Unable to connect or delete the nodes."

    ################################################## INTERACTIONS ##################################################

    @QtCore.Slot(str, int, int)
    def nodeMoved(self, nodeName, x, y):
        """
            Manage when a node is moved.
        """
        # only push a cmd if the node truly moved
        if self.getGraph().getNode(nodeName).getOldCoord() != (x, y):
            cmdMoved = CmdSetCoord(self.getGraph(), nodeName, (x, y))
            cmdManager = CommandManager()
            cmdManager.push(cmdMoved)

    @QtCore.Slot(str, int, int)
    def nodeIsMoving(self, nodeName, x, y):
        """
            Manage when a node is moved.
        """
        self.getGraph().getNode(nodeName).setCoord(x, y)
        self.getGraph().connectionsCoordChanged()

    ######################### UNDO & REDO ############################

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

    def getQObjectPluginsIdentifiers(self):
        """
            Returns a QObjectListModel of all names of Tuttle's plugins.
        """
        pluginsNames = QObjectListModel(self)
        pluginsNames.setObjectList(tuttleTools.getPluginsNames())
        return pluginsNames

    @QtCore.Slot(str, result="QVariant")
    def getQObjectPluginsIdentifiersByParentPath(self, pathname):
        pluginsIds = QObjectListModel(self)
        pluginsIds.setObjectList(tuttleTools.getPluginsIdentifiersByParentPath(pathname))
        return pluginsIds

    @QtCore.Slot(str, result=bool)
    def nextSonIsAPlugin(self, pathname):
        print "pathname :", pathname
        return pathname not in tuttleTools.getPluginsIdentifiersAsDictionary()

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

    # tuttle data
    tuttlePlugins = QtCore.Property(QtCore.QObject, getQObjectPluginsIdentifiers, constant=True)


class ButtleDataSingleton(Singleton):

    _buttleData = ButtleData()

    def get(self):
        return self._buttleData
