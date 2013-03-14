from PySide import QtCore, QtGui
# to parse data
import json
# to save and load data
import io
from datetime import datetime
# tools
from buttleofx.data import tuttleTools
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


class ButtleData(QtCore.QObject):
    """
        Class ButtleData defined by:
        - _graphWrapper
        - _graph
        - _currentNodeViewer
        - _currentNodeParam
        - _currentNodeGraph
        - _currentConnection
        - _currentCopiedNodeInfo
        - _computedImage
        - _buttlePath : the path of the root directory (usefull to import images)

        This class containts all data we need to manage the application.
    """

    _graph = None
    _graphWrapper = None

    # the current params
    _currentParamNodeName = None
    _currentSelectedNodeNames = []
    _currentViewerNodeName = None

    # for the connections
    _currentConnectionId = None

    # to eventually save current nodes data
    _currentCopiedNodesInfo = {}

    # for the viewer
    _currentViewerIndex = 1
    _mapViewerIndextoNodeName = {}
    _mapNodeNameToComputedImage = {}

    # signals
    paramChangedSignal = Signal()
    viewerChangedSignal = Signal()

    def init(self, view, filePath):
        self._graph = Graph()
        self._graphWrapper = GraphWrapper(self._graph, view)
        self._buttlePath = filePath

        return self

    ################################################## GETTERS ET SETTERS ##################################################

    #################### getters ####################

    def getGraph(self):
        return self._graph

    def getGraphWrapper(self):
        return self._graphWrapper

    def getButtlePath(self):
        return self._buttlePath

    ### current data ###

    def getCurrentParamNodeName(self):
        """
            Returns the name of the current param node.
        """
        return self._currentParamNodeName

    def getCurrentSelectedNodeNames(self):
        """
            Returns the names of the current selected nodes.
        """
        return self._currentSelectedNodeNames

    def getCurrentViewerNodeName(self):
        """
            Returns the name of the current viewer node.
        """
        return self._currentViewerNodeName

    def getCurrentCopiedNodesInfo(self):
        """
            Returns the list of buttle info for the current node(s) copied.
        """
        return self._currentCopiedNodesInfo

    ### current data wrapper ###

    def getCurrentParamNodeWrapper(self):
        """
            Returns the current param nodeWrapper.
        """
        return self.getGraphWrapper().getNodeWrapper(self.getCurrentParamNodeName())

    def getCurrentSelectedNodeWrappers(self):
        """
            Returns the current selected nodeWrappers.
        """
        currentSelectedNodeWrappers = QObjectListModel(self)
        currentSelectedNodeWrappers.setObjectList([self.getGraphWrapper().getNodeWrapper(nodeName) for nodeName in self.getCurrentSelectedNodeNames()])
        return currentSelectedNodeWrappers

    def getCurrentViewerIndex(self):
        """
            Returns the current viewer index.
        """
        return self._currentViewerIndex

    def getCurrentViewerNodeWrapper(self):
        """
            Returns the current viewer nodeWrapper.
        """
        return self.getGraphWrapper().getNodeWrapper(self.getCurrentViewerNodeName())

    def getCurrentConnectionWrapper(self):
        """
            Returns the current currentConnectionWrapper
        """
        return self.getGraphWrapper().getConnectionWrapper(self._currentConnectionId)

    #################### setters ####################

    ### current data ###

    def setCurrentParamNodeName(self, nodeName):
        self._currentParamNodeName = nodeName

    def setCurrentSelectedNodeNames(self, nodeNames):
        self._currentSelectedNodeNames = nodeNames

    def setCurrentViewerNodeName(self, nodeName):
        self._currentViewerNodeName = nodeName

    def setCurrentCopiedNodesInfo(self, nodesInfo):
        self._currentCopiedNodesInfo = nodesInfo

    ### current data wrapper ###

    def setCurrentParamNodeWrapper(self, nodeWrapper):
        """
            Changes the current param node and emits the change.
        """
        if self._currentParamNodeName == nodeWrapper.getName():
            return
        self._currentParamNodeName = nodeWrapper.getName()
        # Emit signal
        self.currentParamNodeChanged.emit()

    def setCurrentSelectedNodeWrappers(self, nodeWrappers):
        self.setCurrentSelectedNodeNames([nodeWrapper.getName() for nodeWrapper in nodeWrappers])
        self.currentSelectedNodesChanged.emit()

    def setCurrentViewerIndex(self, index):
        # Update value of the current viewer index
        self._currentViewerIndex = index
        # Emit signal
        self.currentViewerIndexChanged.emit()
        if str(index) in self._mapViewerIndextoNodeName.keys():
            print "Je suis dans la map !", self._mapViewerIndextoNodeName[str(index)]
            self.setCurrentViewerNodeName(self._mapViewerIndextoNodeName[str(index)])
        else:
            print "Je suis pas dans la map :("
            self.currentViewerNodeName = None
        self.currentViewerNodeChanged.emit()

    def setCurrentViewerNodeWrapper(self, nodeWrapper):
        """
        Changes the current viewer node and emits the change.
        """
        if self._currentViewerNodeName == nodeWrapper.getName():
            return
        self._currentViewerNodeName = nodeWrapper.getName()
        # emit signal
        self.currentViewerNodeChanged.emit()

    def setCurrentConnectionWrapper(self, connectionWrapper):
        """
        Changes the current conenctionWrapper and emits the change.
        """
        if self._currentConnectionId == connectionWrapper.getId():
            self._currentConnectionId = None
        else:
            self._currentConnectionId = connectionWrapper.getId()
        self.currentConnectionWrapperChanged.emit()

    ############################################### ADDITIONAL FUNCTIONS ##################################################

    @QtCore.Slot(QtCore.QObject)
    def appendToCurrentSelectedNodeWrappers(self, nodeWrapper):
        self.appendToCurrentSelectedNodeNames(nodeWrapper.getName())

    def appendToCurrentSelectedNodeNames(self, nodeName):
        if nodeName in self._currentSelectedNodeNames:
            self._currentSelectedNodeNames.remove(nodeName)
        else:
            self._currentSelectedNodeNames.append(nodeName)
        # emit signal
        self.currentSelectedNodesChanged.emit()

    @QtCore.Slot("QVariant", result=bool)
    def nodeInCurrentSelectedNodeNames(self, nodeWrapper):
        for nodeName in self._currentSelectedNodeNames:
            if nodeName == nodeWrapper.getName():
                return True
        return False

    @QtCore.Slot(int, int, int, int)
    def addNodeWrappersInRectangleSelection(self, x, y, width, height):
        for node in self.getGraph().getNodes():
            if node.getCoord()[0] >= x and node.getCoord()[0] <= x + width:
                if node.getCoord()[1] >= y and node.getCoord()[1] <= y + height:
                    self.appendToCurrentSelectedNodeNames(node.getName())

    @QtCore.Slot(QtCore.QObject)
    def assignNodeToViewerIndex(self, nodeWrapper):
        self._mapViewerIndextoNodeName.update({str(self._currentViewerIndex): nodeWrapper.getName()})
        print self._mapViewerIndextoNodeName

    @QtCore.Slot()
    def clearCurrentSelectedNodeNames(self):
        self._currentSelectedNodeNames[:] = []
        self.currentSelectedNodesChanged.emit()

    @QtCore.Slot()
    def clearCurrentConnectionId(self):
        self._currentConnectionId = None
        self.currentConnectionWrapperChanged.emit()

    def clearCurrentCopiedNodesInfo(self):
        self._currentCopiedNodesInfo.clear()

    def canPaste(self):
        """
            Returns true if we can paste (= if there was at least one node selected)
        """
        return self._currentCopiedNodesInfo != {}

    ################################################## PLUGIN LIST #####################################################

    @QtCore.Slot(str, result=QtCore.QObject)
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

    ################################################## SAVE / LOAD ##################################################

    @QtCore.Slot()
    def saveData(self):
        """
            Save all data in a json file : buttleofx/backup/data.json
        """
        with io.open('buttleofx/backup/data.json', 'w', encoding='utf-8') as f:
            dictJson = {
                "date": {},
                "window": {},
                "graph": {
                    "nodes": [],
                    "connections": [],
                    "currentSelectedNodes": []
                },
                "paramEditor": {},
                "viewer": {}
            }
            # date
            today = datetime.today().strftime("%A, %d. %B %Y %I:%M%p")
            dictJson["date"]["creation"] = today

            # nodes
            for node in self._graph.getNodes():
                dictJson["graph"]["nodes"].append(node.object_to_dict())
                if node.getName() in self.getCurrentSelectedNodeNames():
                    dictJson["graph"]["currentSelectedNodes"].append(node.getName())

            # connections
            for con in self._graph.getConnections():
                dictJson["graph"]["connections"].append(con.object_to_dict())

            # paramEditor
            dictJson["paramEditor"] = self.getCurrentParamNodeName()

            # viewer
            dictJson["viewer"] = self.getCurrentViewerNodeName()

            # write dictJson in a file
            f.write(unicode(json.dumps(dictJson, sort_keys=True, indent=2, ensure_ascii=False)))
        f.closed

    @QtCore.Slot()
    def loadData(self):
        """
            Load all data from a json file : buttleofx/backup/data.json
        """
        with open('buttleofx/backup/data.json', 'r') as f:
            read_data = f.read()
            decoded = json.loads(read_data)

            # create the nodes
            for nodeData in decoded["graph"]["nodes"]:
                tmpType = nodeData["pluginIdentifier"]
                tmpX = nodeData["uiParams"]["coord"][0]
                tmpY = nodeData["uiParams"]["coord"][1]
                node = self.getGraph().createNode(tmpType, tmpX, tmpY)
                node.dict_to_object(nodeData)

            # create the connections
            for connectionData in decoded["graph"]["connections"]:
                clipIn_nodeName = connectionData["clipIn"]["nodeName"]
                clipIn_clipName = connectionData["clipIn"]["clipName"]
                clipIn_nbClip = 0  # why ? => self.getGraph().getNode(clipIn_nodeName).getNbInput()
                clipIn_positionClip = self.getGraphWrapper().getPositionClip(clipIn_nodeName, clipIn_clipName, clipIn_nbClip)
                clipIn = IdClip(clipIn_nodeName, clipIn_clipName, clipIn_positionClip)

                clipOut_nodeName = connectionData["clipOut"]["nodeName"]
                clipOut_clipName = connectionData["clipOut"]["clipName"]
                clipOut_nbClip = 0  # strange too
                clipOut_positionClip = self.getGraphWrapper().getPositionClip(clipOut_nodeName, clipOut_clipName, clipOut_nbClip)
                clipOut = IdClip(clipOut_nodeName, clipOut_clipName, clipOut_positionClip)

                self.getGraph().createConnection(clipIn, clipOut)

            # selected nodes
            # in paramEditor
            self.setCurrentParamNodeName(decoded["paramEditor"])
            self.currentParamNodeChanged.emit()
            # in viewer
            self.setCurrentViewerNodeName(decoded["viewer"])
            self.currentViewerNodeChanged.emit()
            # in graph
            self.setCurrentSelectedNodeNames(decoded["graph"]["currentSelectedNodes"])
            self.currentSelectedNodesChanged.emit()

        f.closed

    ################################################## DATA EXPOSED TO QML ##################################################

    # graphWrapper
    graphWrapper = QtCore.Property(QtCore.QObject, getGraphWrapper, constant=True)

    # filePath
    buttlePath = QtCore.Property(str, getButtlePath, constant=True)

    # current param, view, and selected node
    currentParamNodeChanged = QtCore.Signal()
    currentParamNodeWrapper = QtCore.Property(QtCore.QObject, getCurrentParamNodeWrapper, setCurrentParamNodeWrapper, notify=currentParamNodeChanged)

    currentViewerNodeChanged = QtCore.Signal()
    currentViewerNodeWrapper = QtCore.Property(QtCore.QObject, getCurrentViewerNodeWrapper, setCurrentViewerNodeWrapper, notify=currentViewerNodeChanged)

    currentSelectedNodesChanged = QtCore.Signal()
    currentSelectedNodeWrappers = QtCore.Property("QVariant", getCurrentSelectedNodeWrappers, setCurrentSelectedNodeWrappers, notify=currentSelectedNodesChanged)

    currentConnectionWrapperChanged = QtCore.Signal()
    currentConnectionWrapper = QtCore.Property(QtCore.QObject, getCurrentConnectionWrapper, setCurrentConnectionWrapper, notify=currentConnectionWrapperChanged)

    currentViewerIndexChanged = QtCore.Signal()
    currentViewerIndex = QtCore.Property("int", getCurrentViewerIndex, setCurrentViewerIndex, notify = currentViewerIndexChanged)

    # paste possibility
    pastePossibilityChanged = QtCore.Signal()
    canPaste = QtCore.Property(bool, canPaste, notify=pastePossibilityChanged)

# This class exists just because thre are problems when a class extends 2 other class (Singleton and QObject)
class ButtleDataSingleton(Singleton):

    _buttleData = ButtleData()

    def get(self):
        return self._buttleData
