from PySide import QtCore
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
from buttleofx.core.graph.connection import IdClip
# gui : graphWrapper
from buttleofx.gui.graph import GraphWrapper


class ButtleData(QtCore.QObject):
    """
        Class ButtleData defined by:
        - _graphWrapper : the graphWrapper
        - _graph : the graph (core)
        - _currentViewerNodeName : the name of the node currently in the viewer
        - _currentSelectedNodeNames : list of the names of the nodes currently selected
        - _currentParamNodeName : the name of the node currently displayed in the paramEditor
        - _currentConnectionId : the list of the id of the connections currently selected
        - _currentCopiedNodesInfo : the list of buttle info for the current node(s) copied
        - _mapNodeNameToComputedImage
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
        # boolean used in viewerManager
    _videoIsPlaying = False
        # processGraph used in viewerManager to compute images
    _processGraph = None
    _timeRange = None

    def init(self, view, filePath):
        self._graph = Graph()
        self._graphWrapper = GraphWrapper(self._graph, view)
        self._buttlePath = filePath
        for index in range(1, 10):
            self._mapViewerIndextoNodeName[str(index)] = None

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
        return self._graphWrapper.getNodeWrapper(self.getCurrentParamNodeName())

    def getCurrentSelectedNodeWrappers(self):
        """
            Returns the current selected nodeWrappers as a QObjectListModel.
        """
        currentSelectedNodeWrappers = QObjectListModel(self)
        currentSelectedNodeWrappers.setObjectList([self.getGraphWrapper().getNodeWrapper(nodeName) for nodeName in self.getCurrentSelectedNodeNames()])
        return currentSelectedNodeWrappers

    def getCurrentViewerIndex(self):
        """
            Returns the current viewer index.
        """
        return self._currentViewerIndex

    @QtCore.Slot(int, result=QtCore.QObject)
    def getNodeWrapperByViewerIndex(self, index):
        return self._graphWrapper.getNodeWrapper(self._mapViewerIndextoNodeName[str(index)])

    def getCurrentViewerNodeWrapper(self):
        """
            Returns the current viewer nodeWrapper.
        """
        return self._graphWrapper.getNodeWrapper(self.getCurrentViewerNodeName())

    def getCurrentConnectionWrapper(self):
        """
            Returns the current currentConnectionWrapper.
        """
        return self._graphWrapper.getConnectionWrapper(self._currentConnectionId)

    def getMapNodeNameToComputedImage(self):
        """
            Returns the map of images already computed.
        """
        return self._mapNodeNameToComputedImage


    #################### setters ####################

    ### current data ###

    def setCurrentParamNodeName(self, nodeName):
        self._currentParamNodeName = nodeName

    def setCurrentSelectedNodeNames(self, nodeNames):
        self._currentSelectedNodeNames = nodeNames

    def setCurrentViewerNodeName(self, nodeName):
        self._currentViewerNodeName = nodeName
        self.currentViewerNodeChanged.emit()

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
        """
            Set the value of the current viewer index.
        """
        # Update value of the current viewer index
        self._currentViewerIndex = index
        # Emit signal
        self.currentViewerIndexChanged.emit()

    def setCurrentViewerNodeWrapper(self, nodeWrapper):
        """
            Changes the current viewer node and emits the change.
        """
        if nodeWrapper == None:
            self._currentViewerNodeName = None
        elif self._currentViewerNodeName == nodeWrapper.getName():
            return
        else:
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

    ############################################### VIDEO FONCTIONS ##################################################
    def getVideoIsPlaying(self):
        return self._videoIsPlaying

    def getProcessGraph(self):
        return self._processGraph

    def setVideoIsPlaying(self, valueBool):
        self._videoIsPlaying = valueBool

    def setProcessGraph(self, processGraph):
        self._processGraph = processGraph

    def processGraphSetUp(self):
        self._processGraph.setup()

    def processGraphBeginSequence(self, timeRange):
        self._processGraph.beginSequence(timeRange)

    def setTimeRange(self, timeRange):
        self._timeRange = timeRange

    def getTimeRange(self):
        return self._timeRange

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
    def nodeIsSelected(self, nodeWrapper):
        """
            Returns True if the node is selected (=if nodeName is in the list _currentSelectedNodeNames), else False.
        """
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
            Returns True if we can paste (= if there is at least one node selected).
        """
        return self._currentCopiedNodesInfo != {}

    ################################################## PLUGIN LIST #####################################################

    @QtCore.Slot(str, result=QtCore.QObject)
    def getQObjectPluginsIdentifiersByParentPath(self, pathname):
        """
            Returns a QObjectListModel of all the PluginsIdentifiers (String) we expect to find after the submenu 'pathname'.
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

    @QtCore.Slot(str)
    @QtCore.Slot()
    def saveData(self, url='buttleofx/backup/data.json'):
        """
            Saves all data in a json file (default file : buttleofx/backup/data.json)
        """
        with io.open(url, 'w', encoding='utf-8') as f:
            dictJson = {
                "date": {},
                "window": {},
                "graph": {},
                "paramEditor": {},
                "viewer": {
                    "other_views": {},
                    "current_view": {}
                }
            }

            # date
            today = datetime.today().strftime("%A, %d. %B %Y %I:%M%p")
            dictJson["date"]["creation"] = today

            # graph
            dictJson["graph"] = self.getGraph().object_to_dict()

            # graph : currentSeletedNodes
            for node in self.getGraph().getNodes():
                if node.getName() in self.getCurrentSelectedNodeNames():
                    dictJson["graph"]["currentSelectedNodes"].append(node.getName())

            # paramEditor : currentParamNodeName
            dictJson["paramEditor"] = self.getCurrentParamNodeName()

            # viewer : currentViewerNodeName
            for num_view, view in self._mapViewerIndextoNodeName.iteritems():
                if self.getCurrentViewerNodeName() == view:
                    dictJson["viewer"]["current_view"][str(num_view)] = view
                if view is not None and self.getCurrentViewerNodeName() != view:
                    dictJson["viewer"]["other_views"].update({num_view: view})

            # write dictJson in a file
            f.write(unicode(json.dumps(dictJson, sort_keys=True, indent=2, ensure_ascii=False)))
        f.closed

    @QtCore.Slot(str)
    @QtCore.Slot()
    def loadData(self, url='buttleofx/backup/data.json'):
        """
            Loads all data from a Json file (the default Json file if no url is given)
        """
        with open(unicode(url), 'r') as f:
            read_data = f.read()

            decoded = json.loads(read_data, object_hook=_decode_dict)

            # create the graph
            self.getGraph().dict_to_object(decoded["graph"])

            # graph : currentSeletedNodes
            for currentSeletedNode in decoded["graph"]["currentSelectedNodes"]:
                self.appendToCurrentSelectedNodeNames(currentSeletedNode)
            self.currentSelectedNodesChanged.emit()
            # paramEditor : currentParamNodeName
            self.setCurrentParamNodeName(decoded["paramEditor"])
            self.currentParamNodeChanged.emit()
            # viewer : other views
            for index, view in decoded["viewer"]["other_views"].iteritems():
                self._mapViewerIndextoNodeName.update({index: view})
            # viewer : currentViewerNodeName
            for index, current_view in decoded["viewer"]["current_view"].iteritems():
                self._mapViewerIndextoNodeName.update({index: current_view})
                self.setCurrentViewerIndex(int(index))
                self.setCurrentViewerNodeName(current_view)
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
    currentViewerIndex = QtCore.Property(int, getCurrentViewerIndex, setCurrentViewerIndex, notify=currentViewerIndexChanged)

    # paste possibility
    pastePossibilityChanged = QtCore.Signal()
    canPaste = QtCore.Property(bool, canPaste, notify=pastePossibilityChanged)


# This class exists just because there are problems when a class extends 2 other classes (Singleton and QObject)
class ButtleDataSingleton(Singleton):

    _buttleData = ButtleData()

    def get(self):
        return self._buttleData


def _decode_dict(dict_):
    """
        This function will recursively pass in nested dicts, and will convert all unicode elements into string (essencial for some Tuttle functions). 
    """
    for key in dict_:
        if isinstance(dict_[key], unicode):
           dict_[key] = str(dict_[key])
    return dict_
