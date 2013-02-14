from PySide import QtCore
# Tuttle
from buttleofx.data import tuttleTools
from pyTuttle import tuttle
# quickmamba
from quickmamba.patterns import Singleton, Signal
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
from buttleofx.core.undo_redo.commands.node import CmdSetCoord


class ButtleData(QtCore.QObject):
    """
        Class ButtleData defined by:
        - _graphWrapper
        - _graph
        - _currentNodeViewer
        - _currentNodeParam
        - _currentNodeGraph
        - soon : _currentNodeCopy
        - _computedImage

        This class :
            - containts all data we need to manage the application.
            - receives the undo and redo from QML, and call the cmdManager to do this.
    """

    _graph = None
    _graphWrapper = None

    _currentParamNodeName = None
    _currentSelectedNodeName = None
    _currentViewerNodeName = None
    _currentCopiedNodeInfo = {}

    _computedImage = None
    _mapNodeNameToComputedImage = {}

    _nodeError = ""

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

    def getNodeError(self):
        """
            Returns the name of the node that can't be displayed.
        """
        return self._nodeError

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
        self.viewerChangedSignal()

    def setNodeError(self, nodeName):
        self._nodeError = nodeName
        self.nodeErrorChanged.emit()

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
                self._currentSelectedNodeName = None
                self.currentSelectedNodeChanged.emit()

        # set the current nodes
        # if the params of the current node just deleted are display
        if self._currentSelectedNodeName == self._currentParamNodeName:
            self._currentParamNodeName = None
            self.currentParamNodeChanged.emit()
        # if the viewer of the current node just deleted is display
        if self._currentSelectedNodeName == self._currentViewerNodeName:
            self._currentViewerNodeName = None
            self.currentViewerNodeChanged.emit()

    @QtCore.Slot()
    def cutNode(self):
        """
            Function called from the QML when we want to cut a node.
        """
        self.copyNode()
        if self.getCurrentSelectedNodeWrapper() != None:
            self._currentCopiedNodeInfo.update({"mode": ""})
            self.destructionNode()
            if self._currentSelectedNodeName == self._currentViewerNodeName:
                self._currentViewerNodeName = None
            if self._currentSelectedNodeName == self._currentParamNodeName:
                self._currentParamNodeName = None

    @QtCore.Slot()
    def copyNode(self):
        """
            Function called from the QML when we want to copy a node.
        """
        if self.getCurrentSelectedNodeWrapper() != None:
            self._currentCopiedNodeInfo.update({"nodeType": self.getCurrentSelectedNodeWrapper().getNode().getType()})
            self._currentCopiedNodeInfo.update({"nameUser": self.getCurrentSelectedNodeWrapper().getNode().getNameUser()})
            self._currentCopiedNodeInfo.update({"color": self.getCurrentSelectedNodeWrapper().getNode().getColor()})
            self._currentCopiedNodeInfo.update({"params": self.getCurrentSelectedNodeWrapper().getNode().getTuttleNode().getParamSet()})
            self._currentCopiedNodeInfo.update({"mode": "_copy"})
            self.pastePossibilityChanged.emit()

    @QtCore.Slot()
    def pasteNode(self):
        """
            Function called from the QML when we want to paste a node.
        """
        if self._currentCopiedNodeInfo:
            self.getGraph().createNode(self._currentCopiedNodeInfo["nodeType"], 20, 20)
            newNode = self.getGraph().getNodes()[-1]
            newNode.setColor(self._currentCopiedNodeInfo["color"][0], self._currentCopiedNodeInfo["color"][1], self._currentCopiedNodeInfo["color"][2])
            newNode.setNameUser(self._currentCopiedNodeInfo["nameUser"] + self._currentCopiedNodeInfo["mode"])
            newNode.getTuttleNode().getParamSet().copyParamsValues(self._currentCopiedNodeInfo["params"])

    def canPaste(self):
        """
            Returns true if we can paste (= if there was at least one node selected)
        """
        return self._currentCopiedNodeInfo != {}


    @QtCore.Slot()
    def duplicationNode(self):
        """
            Function called from the QML when we want to duplicate a node.
        """
        if self.getCurrentSelectedNodeWrapper() != None:
            # Create a node giving the current selected node's type, x and y
            nodeType = self.getCurrentSelectedNodeWrapper().getNode().getType()
            coord = self.getCurrentSelectedNodeWrapper().getNode().getCoord()
            self.getGraph().createNode(nodeType, coord[0], coord[1])
            newNode = self.getGraph().getNodes()[-1]

            # Get the current selected node's properties
            nameUser = self.getCurrentSelectedNodeWrapper().getNameUser() + "_duplicate"
            oldCoord = self.getCurrentSelectedNodeWrapper().getNode().getOldCoord()
            color = self.getCurrentSelectedNodeWrapper().getNode().getColor()

            # Use the current selected node's properties to set the duplicated node's properties
            newNode.setNameUser(nameUser)
            newNode.setOldCoord(oldCoord[0], oldCoord[1])
            newNode.setColor(color[0], color[1], color[2])
            newNode.getTuttleNode().getParamSet().copyParamsValues(self.getCurrentSelectedNodeWrapper().getNode().getTuttleNode().getParamSet())

    @QtCore.Slot(str, int, int)
    def dropReaderNode(self, url, x, y):
        """
            Function called when an image is dropped in the graph.
        """
        self.getGraph().createReaderNode(url, x, y)

    ##### Connection #####

    def connect(self, clipOut, clipIn):
        """
            Adds a connection between 2 clips.
        """
        self.getGraph().createConnection(clipOut, clipIn)
        self.getGraphWrapper().resetTmpClips()

    def disconnect(self, connection):
        """
            Removes a connection between 2 clips.
        """
        self.getGraph().deleteConnection(connection)
        self.getGraphWrapper().resetTmpClips()

    @QtCore.Slot(QtCore.QObject, int)
    def clipPressed(self, clip, clipNumber):
        """
            Function called when a clip is pressed (but not released yet).
            The function replace the tmpClipIn or tmpClipOut.
        """
        coord = self.getGraphWrapper().getPositionClip(clip.getNodeName(), clip.getName(), clipNumber)
        idClip = IdClip(clip.getNodeName(), clip.getName(), clipNumber, coord)
        if (clip.getName() == "Output"):
            self.getGraphWrapper().setTmpClipOut(idClip)
        else:
            self.getGraphWrapper().setTmpClipIn(idClip)

    @QtCore.Slot(QtCore.QObject, int)
    def clipReleased(self, clip, clipNumber):
        """
            Function called when a clip is released (after pressed).
        """

        if (clip.getName() == "Output"):
            #if there is a tmpNodeIn
            if (self.getGraphWrapper().getTmpClipIn() != None and self.getGraphWrapper().getTmpClipIn()._nodeName != clip.getNodeName()):
                position = self.getGraphWrapper().getPositionClip(clip.getNodeName(), clip.getName(), clipNumber)
                idClip = IdClip(clip.getNodeName(), clip.getName(), clipNumber, position)
                if self.getGraphWrapper().canConnect(idClip, self.getGraphWrapper().getTmpClipIn()):
                    self.connect(idClip, self.getGraphWrapper().getTmpClipIn())
                elif self.getGraph().contains(self.getGraphWrapper().getTmpClipIn()) and self.getGraph().contains(idClip):
                    self.disconnect(self.getGraphWrapper().getConnectionByClips(idClip, self.getGraphWrapper().getTmpClipIn()))
                else:
                    print "Unable to connect or delete the nodes."
        else:
            #if there is a tmpNodeOut
            if (self.getGraphWrapper().getTmpClipOut() != None and self.getGraphWrapper().getTmpClipOut()._nodeName != clip.getNodeName()):
                position = self.getGraphWrapper().getPositionClip(clip.getNodeName(), clip.getName(), clipNumber)
                idClip = IdClip(clip.getNodeName(), clip.getName(), clipNumber, position)
                if self.getGraphWrapper().canConnect(self.getGraphWrapper().getTmpClipOut(), idClip):
                    self.connect(self.getGraphWrapper().getTmpClipOut(), idClip)
                elif self.getGraph().contains(self.getGraphWrapper().getTmpClipOut()) and self.getGraph().contains(idClip):
                    self.disconnect(self.getGraphWrapper().getConnectionByClips(self.getGraphWrapper().getTmpClipOut(), idClip))
                else:
                    print "Unable to connect or delete the nodes."


    ################################################## INTERACTIONS ##################################################

    ##### Node #####

    @QtCore.Slot(str, int, int)
    def nodeMoved(self, nodeName, x, y):
        """
            Fonction called when a node has moved.
            This fonction push a cmdMoved in the CommandManager.
        """
        # only push a cmd if the node truly moved
        if self.getGraph().getNode(nodeName).getOldCoord() != (x, y):
            cmdMoved = CmdSetCoord(self.getGraph(), nodeName, (x, y))
            cmdManager = CommandManager()
            cmdManager.push(cmdMoved)

    @QtCore.Slot(str, int, int)
    def nodeIsMoving(self, nodeName, x, y):
        """
            Fonction called when a node is moving.
            This fonction update the position of the connections.
        """
        self.getGraph().getNode(nodeName).setCoord(x, y)
        self.getGraph().connectionsCoordChanged()

    ##### UNDO & REDO #####

    @QtCore.Slot()
    def undo(self):
        """
            Calls the cmdManager to undo the last command.
        """
        cmdManager = CommandManager()
        cmdManager.undo()
        self.undoRedoChanged.emit()

    @QtCore.Slot()
    def redo(self):
        """
            Calls the cmdManager to redo the last command.
        """
        cmdManager = CommandManager()
        cmdManager.redo()
        self.undoRedoChanged.emit()

    def canUndo(self):
        """
            Calls the cmdManager to return if we can undo or not.
        """
        cmdManager = CommandManager()
        return cmdManager.canUndo()

    def canRedo(self):
        """
            Calls the cmdManager to return if we can redo or not.
        """
        cmdManager = CommandManager()
        return cmdManager.canRedo()

    ##### Plugins' menu #####

    @QtCore.Slot(str, result="QVariant")
    def getQObjectPluginsIdentifiersByParentPath(self, pathname):
        """
            Returns a QObjectListModel
        """
        pluginsIds = QObjectListModel(self)
        pluginsIds.setObjectList(tuttleTools.getPluginsIdentifiersByParentPath(pathname))
        return pluginsIds

    @QtCore.Slot(str, result=bool)
    def isAPlugin(self, pluginId):
        """
            Returns if a string is a plugin identifier.
        """
        return pluginId in tuttleTools.getPluginsIdentifiers()

     ###################################################  TUTTLE  ############################################################
    def computeNode(self, frame):
        """
            Compute the node at the frame indicated
        """
        print "------- COMPUTE NODE -------"

        #Get the name of the currentNode of the viewer
        node = self.getCurrentViewerNodeName()

        #Get the output where we save the result
        self._tuttleImageCache = tuttle.MemoryCache()
        #should replace 25 by the fps of the video (a sort of getFPS(node))
        #should expose the duration of the video to the QML too
        self.getGraph().getGraphTuttle().compute(self._tuttleImageCache, node, tuttle.ComputeOptions(int(frame)))
        self._computedImage = self._tuttleImageCache.get(0)

        #Add the computedImage to the map
        self._mapNodeNameToComputedImage.update({node: self._computedImage})

        return self._computedImage

    def retrieveImage(self, frame, frameChanged):
        """
            Compute the node at the frame indicated if the frame has changed (if the time has changed)
        """
        #Get the name of the currentNode of the viewer
        node = self.getCurrentViewerNodeName()

        #Get the map
        mapNodeToImage = self._mapNodeNameToComputedImage

        try:
            self.setNodeError("")
            #If the image is already calculated
            for element in mapNodeToImage:
                if node == element and frameChanged is False:
                    print "**************************Image already calculated**********************"
                    return self._mapNodeNameToComputedImage[node]
                # If it is not
            print "************************Calcul of image***************************"
            return self.computeNode(frame)
        except Exception as e:
            print "Can't display node : " + node
            self.setNodeError(str(e))
            raise

    def updateMapAndViewer(self):
        # Clear the map
        self._mapNodeNameToComputedImage.clear()

        # Emit the signal to load the new image
        self.paramChangedSignal()

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

    # undo redo
    undoRedoChanged = QtCore.Signal()
    canUndo = QtCore.Property(bool, canUndo, notify=undoRedoChanged)
    canRedo = QtCore.Property(bool, canRedo, notify=undoRedoChanged)

    # paste possibility ?
    pastePossibilityChanged = QtCore.Signal()
    canPaste = QtCore.Property(bool, canPaste, notify=pastePossibilityChanged)

    # error display on the Viewer
    nodeErrorChanged = QtCore.Signal()
    nodeError = QtCore.Property(str, getNodeError, setNodeError, notify=nodeErrorChanged)

    # python signals
    paramChangedSignal = Signal()
    viewerChangedSignal = Signal()


# This class exists just because thre are problems when a class extends 2 other class (Singleton and QObject)
class ButtleDataSingleton(Singleton):

    _buttleData = ButtleData()

    def get(self):
        return self._buttleData
