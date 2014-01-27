from PyQt5 import QtCore
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
# gui : pluginWrapper
from buttleofx.gui.plugin import PluginWrapper
# commands
from buttleofx.core.undo_redo.manageTools import CommandManager
# events
from buttleofx.event import ButtleEvent

# node
from buttleofx.core.graph.node import Node
from buttleofx.gui.graph.node import NodeWrapper

from pyTuttle import tuttle


import math

class ButtleData(QtCore.QObject):
    """
        Class ButtleData defined by:
        - _mapGraph : map of graph
        - _graphWrapper : the graphWrapper
        - _currentGraph : the currentGraph
        - _currentGraphWrapper : the current graph wrapper between graph and graphBrowser
        - _graph : the graph (core)
        - _graphBrowser : the graph of the browser
        - _graphBrowserWrapper : the graphWrapper of the browser
       	- _currentViewerNodeName : the name of the node currently in the viewer
        - _currentSelectedNodeNames : list of the names of the nodes currently selected
        - _currentParamNodeName : the name of the node currently displayed in the paramEditor
        - _currentConnectionId : the list of the id of the connections currently selected
        - _currentCopiedConnectionsInfo : the list of buttle info for the connections of the current nodes copied
        - _currentCopiedNodesInfo : the list of buttle info for the current node(s) copied
        - _mapNodeNameToComputedImage : this map makes the correspondance between a gloablHash and a computed image (max 20 images stored)
        - _buttlePath : the path of the root directory (useful to import images)
        - _graphCanBeSaved : a boolean indicating if the graph had changed since the last saving (useful for the display of the icon "save graph")
        This class contains all data we need to manage the application.
    """

    _graph = None
    _graphWrapper = None

    _graphBrowser = None
    _graphBrowserWrapper = None

    _currentGraph = None
    _currentGraphWrapper = None

    _mapGraph = {}

    _graphCanBeSaved = False

    # the current params
    _currentParamNodeName = None
    _currentSelectedNodeNames = []

    # for the connections
    _currentConnectionId = None

    # to eventually save current nodes data
    _currentCopiedNodesInfo = {}
    
    # to eventually save current connections data
    _currentCopiedConnectionsInfo = {}

    # for the viewer
    _currentViewerIndex = 1
    _currentViewerFrame = 0
    _currentViewerNodeName = None
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

        self._graphBrowser = Graph()
        self._graphBrowserWrapper = GraphWrapper(self._graphBrowser, view)


        self._mapGraph = {
            "graph": self._graph,
            "graphBrowser": self._graphBrowser,
        }

        self._currentGraph = self._graph #by default, the current graph is the graph of the graphEditor
        self._currentGraphWrapper = self._graphWrapper #by default, the current graph is the graph of the graphEditor

        self._buttlePath = filePath

        # 9 views for the viewer, the 10th for the browser, the 11th temporary
        for index in range(1, 12):
            self._mapViewerIndextoNodeName[str(index)] = None

        return self

    ################################################## GETTERS ET SETTERS ##################################################

    #################### getters ####################

    def getGraph(self):
        return self._graph

    def getCurrentGraphWrapper(self):
        return self._currentGraphWrapper

    def getCurrentGraph(self):
        return self._currentGraph

    def getGraphBrowser(self):
        return self._graphBrowser

    def getGraphWrapper(self):
        return self._graphWrapper

    def getGraphBrowserWrapper(self):
        return self._graphBrowserWrapper

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

    @QtCore.pyqtSlot()
    def getCurrentViewerNodeName(self):
        """
            Returns the name of the current viewer node.
        """
        return self._currentViewerNodeName
        
    def getCurrentCopiedConnectionsInfo(self):
        """
            Returns the list of buttle info for the connection(s) of the current nodes copied.
        """
        return self._currentCopiedConnectionsInfo


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
        return self._currentGraphWrapper.getNodeWrapper(self.getCurrentParamNodeName())

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

    def getEditedNodesWrapper(self):
        """
            Returns the total of param nodeWrapper for the parametersEditor.
        """
        return self.getCurrentGraphWrapper().getNodeWrappers()

    @QtCore.pyqtSlot(int, result=QtCore.QObject)
    def getNodeWrapperByViewerIndex(self, index):
        """
            Returns the nodeWrapper of the node contained in the viewer at the corresponding index.
        """
        # We get the infos of this node. It's a tuple (fodeName, frame), so we have to return the first element nodeViewerInfos[0].
        nodeViewerInfos = self._mapViewerIndextoNodeName[str(index)]
        if nodeViewerInfos is None:
            return None
        else:
            return self._currentGraphWrapper.getNodeWrapper(nodeViewerInfos[0])

    @QtCore.pyqtSlot(int, result=int)
    def getFrameByViewerIndex(self, index):
        """
            Returns the frame of the node contained in the viewer at the corresponding index.
        """
        # We get the infos of this node. It's a tuple (fodeName, frame), so we have to return the second element nodeViewerInfos[1].
        nodeViewerInfos = self._mapViewerIndextoNodeName[str(index)]
        if nodeViewerInfos is None:
            return 0
        else:
            return nodeViewerInfos[1]


    #def getCurrentViewerNodeWrapper(self):
    #    """
    #        Returns the current viewer nodeWrapper.
    #    """
    #    return self._graphWrapper.getNodeWrapper(self.getCurrentViewerNodeName())

    def getCurrentViewerNodeWrapper(self):
        """
            Returns the current viewer nodeWrapper.
        """
        return self._currentGraphWrapper.getNodeWrapper(self.getCurrentViewerNodeName())

    def getCurrentViewerFrame(self):
        """
            Returns the frame of the current viewer nodeWrapper.
        """
        return self._currentViewerFrame

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

    def graphCanBeSaved(self):
        """
            Returns the value of the boolean self._graphCanBeSaved
        """
        return self._graphCanBeSaved


    #################### setters ####################

    ### current data ###

    def setCurrentParamNodeName(self, nodeName):
        self._currentParamNodeName = nodeName

    def setCurrentSelectedNodeNames(self, nodeNames):
        self._currentSelectedNodeNames = nodeNames

    def setCurrentViewerNodeName(self, nodeName):
        self._currentViewerNodeName = nodeName
        self.currentViewerNodeChanged.emit()

    def setCurrentViewerFrame(self, frame):
        self._currentViewerFrame = frame
        self.currentViewerFrameChanged.emit()
        
    def setCurrentCopiedConnectionsInfo(self, connectionsInfo):
        self._currentCopiedConnectionsInfo = connectionsInfo

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

    #def setCurrentViewerNodeWrapper(self, nodeWrapper):
    #    """
    #        Changes the current viewer node and emits the change.
    #    """
    #    if nodeWrapper is None:
    #        self._currentViewerNodeName = None
    #    elif self._currentViewerNodeName == nodeWrapper.getName():
    #        return
    #    else:
    #        self._currentViewerNodeName = nodeWrapper.getName()
    #    # emit signal
    #    self.currentViewerNodeChanged.emit()

    def setCurrentViewerNodeWrapper(self, nodeWrapper):
        """
            Changes the current viewer node and emits the change.
        """
        if nodeWrapper is None:
            self._currentViewerNodeName = None
        elif self._currentViewerNodeName == nodeWrapper.getName():
            return
        else:
            self._currentViewerNodeName = nodeWrapper.getName()
        # emit signal
        #print ("setCurrentViewerId buttleData.getCurrentGraphWrapper()", self.getCurrentGraphWrapper())
        #print ("setCurrentViewerId nodeWrapper.getName()", nodeWrapper.getName())

        #print ("setCurrentViewerId self._graphBrowser._graphTuttle", self._graphBrowser._graphTuttle)

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

    def setGraphCanBeSaved(self, canBeSaved):
        """
            Set the value of the boolean self._graphCanBeSaved.
        """
        self._graphCanBeSaved = canBeSaved
        self.graphCanBeSavedChanged.emit()

    def setCurrentGraphWrapper(self, currentGraphWrapper):
        """
            Set the _currentGraphWrapper
        """
        self._currentGraphWrapper = currentGraphWrapper
        self.currentGraphWrapperChanged.emit()

    def setCurrentGraph(self, currentGraph):
        """
            Set the _currentGraph // doesn't work in QML
        """
        self._currentGraph = currentGraph
        self.currentGraphChanged.emit()

    @QtCore.pyqtSlot()
    def currentGraphIsGraphBrowser(self):
        """
            Set the _currentGraph to graphBrowser // work in QML
        """
        self._currentGraph = self._graphBrowser

    @QtCore.pyqtSlot()
    def currentGraphIsGraph(self):
        """
            Set the _currentGraph to graph // work in QML
        """
        self._currentGraph = self._graph



    ############################################### VIDEO FONCTIONS ##################################################
    def getVideoIsPlaying(self):
        return self._videoIsPlaying

    def setVideoIsPlaying(self, valueBool):
        self._videoIsPlaying = valueBool

    def getProcessGraph(self):
        return self._processGraph

    def setProcessGraph(self, processGraph):
        self._processGraph = processGraph

    ############################################### ADDITIONAL FUNCTIONS ##################################################

    @QtCore.pyqtSlot(QtCore.QObject)
    def appendToCurrentSelectedNodeWrappers(self, nodeWrapper):
        self.appendToCurrentSelectedNodeNames(nodeWrapper.getName())

    def appendToCurrentSelectedNodeNames(self, nodeName):
        if nodeName in self._currentSelectedNodeNames:
            self._currentSelectedNodeNames.remove(nodeName)
        else:
            self._currentSelectedNodeNames.append(nodeName)
        # emit signal
        self.currentSelectedNodesChanged.emit()

    @QtCore.pyqtSlot("QVariant", result=bool)
    def nodeIsSelected(self, nodeWrapper):
        """
            Returns True if the node is selected (=if nodeName is in the list _currentSelectedNodeNames), else False.
        """
        for nodeName in self._currentSelectedNodeNames:
            if nodeName == nodeWrapper.getName():
                return True
        return False

    @QtCore.pyqtSlot(int, int, int, int)
    def addNodeWrappersInRectangleSelection(self, xRect, yRect, widthRect, heightRect):
        """
            Selects the nodes which are is the rectangle selection area.
        """
        for nodeW in self.getGraphWrapper().getNodeWrappers():
            xNode = nodeW.getNode().getCoord()[0]
            yNode = nodeW.getNode().getCoord()[1]
            # TODO: should be done in QML
            widthNode = 40
            heightNode = 10

            # we project the bounding-boxes on the axes and we check if the segments overlap
            horizontalOverlap = (xNode < xRect + widthRect) and (xRect < xNode + widthNode)
            verticalOverlap = (yNode < yRect + heightRect) and (yRect < yNode + heightNode)
            overlap = horizontalOverlap and verticalOverlap

            # if the bounding-boxes overlap then the node is in the selection area
            if overlap:
                self.appendToCurrentSelectedNodeNames(nodeW.getName())


    @QtCore.pyqtSlot(QtCore.QObject, int)
    def assignNodeToViewerIndex(self, nodeWrapper, frame):
        """
            Assigns a node to the _mapViewerIndextoNodeName at the current viewerIndex.
            It adds a tuple (nodeName, frame).
        """
        if nodeWrapper:
            self._mapViewerIndextoNodeName.update({str(self._currentViewerIndex): (nodeWrapper.getName(), frame)})

    @QtCore.pyqtSlot()
    def clearCurrentSelectedNodeNames(self):
        self._currentSelectedNodeNames[:] = []
        self.currentSelectedNodesChanged.emit()

    @QtCore.pyqtSlot()
    def clearCurrentConnectionId(self):
        self._currentConnectionId = None
        self.currentConnectionWrapperChanged.emit()
        
    def clearCurrentCopiedConnectionsInfo(self):
        self._currentCopiedConnectionsInfo.clear()

    def clearCurrentCopiedNodesInfo(self):
        self._currentCopiedNodesInfo.clear()

    def canPaste(self):
        """
            Returns True if we can paste (= if there is at least one node selected).
        """
        return self._currentCopiedNodesInfo != {}
        
    @QtCore.pyqtSlot(int, int, int, float, float, float, float, float, int, int)
    def zoom(self, width, height, nodeWidth, zoomCoeff, graphPreviousWidth, graphPreviousHeight, mouseX, mouseY, offsetX, offsetY):
    
          mouseXRatio = (mouseX - offsetX) / width
          mouseYRatio = (mouseY - offsetY) / height
          newWidth = zoomCoeff * width
          newHeight = zoomCoeff * height
          reinitOriginX = (width * mouseXRatio) - (graphPreviousWidth * mouseXRatio)
          reinitOriginY = (height * mouseYRatio) - (graphPreviousHeight * mouseYRatio)
          newOriginX = (width * mouseXRatio) - (newWidth * mouseXRatio)
          newOriginY = (height * mouseYRatio) - (newHeight * mouseYRatio)  

          nodes = self._graphWrapper.getNodeWrappers()
          for i in nodes:
              if graphPreviousWidth != width :
                  i.xCoord = ((i.xCoord - reinitOriginX) * width) / graphPreviousWidth
                  i.yCoord = ((i.yCoord - reinitOriginY) * height) / graphPreviousHeight
                  
              i.xCoord = ((i.xCoord * newWidth) / width) + newOriginX #- (nodeWidth * 0.5)
              i.yCoord = ((i.yCoord * newHeight) / height) + newOriginY #- (nodeWidth * 0.5)
     
          self._graphWrapper.updateNodeWrappers()
          self._graphWrapper.updateConnectionWrappers()
        
    ################################################## PLUGIN LIST #####################################################

    def getPluginsIdentifiers(self):
        from pyTuttle import tuttle
        pluginCache = tuttle.core().getImageEffectPluginCache()
        plugins = pluginCache.getPlugins()
        print("getPluginsIdentifiers => nb plugins:", len(plugins))

        pluginsIds = [plugin.getIdentifier() for plugin in plugins]
        pluginsIdsModel = QObjectListModel(self)
        for p in pluginsIds:
            pluginsIdsModel.append(p)
        return pluginsIdsModel

    def getPluginsWrappers(self):
        from pyTuttle import tuttle
        pluginCache = tuttle.core().getImageEffectPluginCache()
        plugins = pluginCache.getPlugins()         

        pluginsW = [PluginWrapper(plugin) for plugin in plugins]
        pluginsWModel = QObjectListModel(self)
        for p in pluginsW:
            pluginsWModel.append(p)
        return pluginsWModel

    @QtCore.pyqtSlot(str, result=QtCore.QObject)
    def getPluginsWrappersSuggestions(self, pluginSearched):
        from pyTuttle import tuttle
        pluginCache = tuttle.core().getImageEffectPluginCache()
        plugins = pluginCache.getPlugins()         

        pluginsW = [PluginWrapper(plugin) for plugin in plugins]
        pluginsWModel = QObjectListModel(self)
        for p in pluginsW:
            if (pluginSearched in p.pluginType) :
                pluginsWModel.append(p)
        return pluginsWModel

    @QtCore.pyqtSlot(str, result=QtCore.QObject)
    def getPluginsByPath(self, menuPath):
        from pyTuttle import tuttle
        pluginCache = tuttle.core().getImageEffectPluginCache()
        plugins = pluginCache.getPlugins()         

        pluginsW = [PluginWrapper(plugin) for plugin in plugins]
        pluginsWModel = QObjectListModel(self)
        for p in pluginsW:
            path = p.pluginGroup
            while "/" in path :
                listOfPath = path.split("/")
                path = path.replace(listOfPath[0] + "/","")
            if menuPath in path :
                pluginsWModel.append(p)
        return pluginsWModel

    @QtCore.pyqtSlot(int, str, result=QtCore.QObject)
    def getMenu(self, nb, parentMenuPath):
        from pyTuttle import tuttle
        pluginCache = tuttle.core().getImageEffectPluginCache()
        plugins = pluginCache.getPlugins()         

        pluginsW = [PluginWrapper(plugin) for plugin in plugins]
        pluginsListMenu = QObjectListModel(self)
        for p in pluginsW:
            path = p.pluginGroup + "/"
            parentPath = path
            if path.count("/") >= nb :
                for i in range(nb) :
                    listOfPath = path.split("/")
                    path = path.replace(listOfPath[0] + "/","")
                    print (path)
                if not pluginsListMenu.contains(listOfPath[0]) and listOfPath[0] :
                    if parentMenuPath in parentPath :
                        pluginsListMenu.append(listOfPath[0])
        return pluginsListMenu
        
    @QtCore.pyqtSlot(str, result=QtCore.QObject)
    def getQObjectPluginsIdentifiersByParentPath(self, pathname):
        """
            Returns a QObjectListModel of all the PluginsIdentifiers (String) we expect to find after the submenu 'pathname'.
        """
        pluginsIds = QObjectListModel(self)
        pluginsIds.setObjectList(tuttleTools.getPluginsIdentifiersByParentPath(pathname))
        return pluginsIds

    @QtCore.pyqtSlot(str, result=bool)
    def isAPlugin(self, pluginId):
        """
            Returns if a string is a plugin identifier.
        """
        return pluginId in tuttleTools.getPluginsIdentifiers()


    ################################################## GRAPH BROWSER & GRAPH PARAMETERS EDITOR ##################################################

    @QtCore.pyqtSlot(str, result=QtCore.QObject)
    def nodeReaderWrapperForBrowser(self, url):
        self._graphBrowser._nodes = []  # clear the graph
        self._graphBrowser._graphTuttle = tuttle.Graph()  # clear the graphTuttle
        self._currentGraph = self._graphBrowser
        self._currentGraphWrapper = self._graphBrowserWrapper

        readerNode = self._graphBrowser.createReaderNode(url, 0, 0) # create a reader node (like for the drag & drop of file)

        readerNodeWrapper = NodeWrapper(readerNode, self._graphBrowserWrapper._view) # wrapper of the reader file

        return readerNodeWrapper


    @QtCore.pyqtSlot(result=QtCore.QObject)
    def lastNode(self):
        # return the last node to connect to the new node

        sizeOfGraph = self._currentGraphWrapper._nodeWrappers.size()

        if (sizeOfGraph >= 1):
            #nodes to connect
            lastNode = self._currentGraphWrapper._nodeWrappers[sizeOfGraph-1]

        else : lastNode = None

        # update undo/redo display
        #self.undoRedoChanged()

        return lastNode



    ################################################## SAVE / LOAD ##################################################

    @QtCore.pyqtSlot(str)
    @QtCore.pyqtSlot()
    def saveData(self, url='buttleofx/backup/data.bofx'):
        """
            Saves all data in a json file (default file : buttleofx/backup/data.bofx)
        """

        filepath = QtCore.QUrl(url).toLocalFile()
        if not (filepath.endswith(".bofx")):
            filepath = filepath + ".bofx"

        with io.open(filepath, 'w', encoding='utf-8') as f:
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
            for num_view, view in self._mapViewerIndextoNodeName.items():
                if view is not None:
                    (nodeName, frame) = view
                    if self.getCurrentViewerNodeName() == nodeName:
                        dictJson["viewer"]["current_view"][str(num_view)] = {}
                        dictJson["viewer"]["current_view"][str(num_view)]["nodeName"] = nodeName
                        dictJson["viewer"]["current_view"][str(num_view)]["frame"] = frame
                    else:
                        dictJson["viewer"]["other_views"][str(num_view)] = {}
                        dictJson["viewer"]["other_views"][str(num_view)]["nodeName"] = nodeName
                        dictJson["viewer"]["other_views"][str(num_view)]["frame"] = frame

            # write dictJson in a file
            f.write(str(json.dumps(dictJson, sort_keys=True, indent=2, ensure_ascii=False)))
        f.closed

        # Finally we update the savedGraphIndex of the CommandManager : it must be equal to the current index
        CommandManager().setSavedGraphIndex(CommandManager().getIndex())

    @QtCore.pyqtSlot(str)
    @QtCore.pyqtSlot()
    def loadData(self, url='buttleofx/backup/data.bofx'):
        """
            Loads all data from a Json file (the default Json file if no url is given)
        """

        filepath = QtCore.QUrl(url).toLocalFile()

        with open(filepath, 'r') as f:
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
                nodeName, frame = view["nodeName"], view["frame"]
                self._mapViewerIndextoNodeName.update({index: (nodeName, frame)})
            # viewer : currentViewerNodeName
            for index, current_view in decoded["viewer"]["current_view"].iteritems():
                nodeName, frame = current_view["nodeName"], current_view["frame"]
                self._mapViewerIndextoNodeName.update({index: (nodeName, frame)})
            # #The next commands doesn't work : we need to click on the viewer's number to see the image in the viewer. Need to be fixed.
            #     self.setCurrentViewerIndex(int(index))
            #     self.setCurrentViewerNodeName(current_view)
            #     self.setCurrentViewerNodeWrapper = self.getNodeWrapperByViewerIndex(int(index))
            #     self.setCurrentViewerFrame(frame)
            # ButtleEvent().emitViewerChangedSignal()
        f.closed

    ################################################## DATA EXPOSED TO QML ##################################################

    pluginsIdentifiers = QtCore.pyqtProperty(QtCore.QObject, getPluginsIdentifiers, constant=True)
    pluginsDocs = QtCore.pyqtProperty(QtCore.QObject, getPluginsWrappers, constant=True)

    graph = QtCore.pyqtProperty(QtCore.QObject, getGraph, constant=True)
    graphBrowser = QtCore.pyqtProperty(QtCore.QObject, getGraphBrowser, constant=True)

    # graphWrapper
    graphWrapper = QtCore.pyqtProperty(QtCore.QObject, getGraphWrapper, constant=True)
    graphBrowserWrapper = QtCore.pyqtProperty(QtCore.QObject, getGraphBrowserWrapper, constant=True)

    # filePath
    buttlePath = QtCore.pyqtProperty(str, getButtlePath, constant=True)

    # current param, view, and selected node
    currentParamNodeChanged = QtCore.pyqtSignal()
    currentParamNodeWrapper = QtCore.pyqtProperty(QtCore.QObject, getCurrentParamNodeWrapper, setCurrentParamNodeWrapper, notify=currentParamNodeChanged)

    currentViewerNodeChanged = QtCore.pyqtSignal()
    currentViewerNodeWrapper = QtCore.pyqtProperty(QtCore.QObject, getCurrentViewerNodeWrapper, setCurrentViewerNodeWrapper, notify=currentViewerNodeChanged)
    currentViewerFrameChanged = QtCore.pyqtSignal()
    currentViewerFrame = QtCore.pyqtProperty(int, getCurrentViewerFrame, setCurrentViewerFrame, notify=currentViewerFrameChanged)

    currentViewerNodeName = QtCore.pyqtProperty(QtCore.QObject, getCurrentViewerNodeName, constant=True)

    currentSelectedNodesChanged = QtCore.pyqtSignal()
    currentSelectedNodeWrappers = QtCore.pyqtProperty("QVariant", getCurrentSelectedNodeWrappers, setCurrentSelectedNodeWrappers, notify=currentSelectedNodesChanged)

    currentConnectionWrapperChanged = QtCore.pyqtSignal()
    currentConnectionWrapper = QtCore.pyqtProperty(QtCore.QObject, getCurrentConnectionWrapper, setCurrentConnectionWrapper, notify=currentConnectionWrapperChanged)

    currentViewerIndexChanged = QtCore.pyqtSignal()
    currentViewerIndex = QtCore.pyqtProperty(int, getCurrentViewerIndex, setCurrentViewerIndex, notify=currentViewerIndexChanged)

    # total of the nodes
    editedNodesWrapper = QtCore.pyqtProperty(QtCore.QObject, getEditedNodesWrapper, constant=True)

    currentGraphWrapperChanged = QtCore.pyqtSignal()
    currentGraphWrapper = QtCore.pyqtProperty(QtCore.QObject, getCurrentGraphWrapper, setCurrentGraphWrapper, notify=currentGraphWrapperChanged)

    currentGraphChanged = QtCore.pyqtSignal()
    currentGraph = QtCore.pyqtProperty(QtCore.QObject, getCurrentGraph, setCurrentGraph, notify=currentGraphChanged)

    # paste possibility
    pastePossibilityChanged = QtCore.pyqtSignal()
    canPaste = QtCore.pyqtProperty(bool, canPaste, notify=pastePossibilityChanged)

    # possibility to save graph
    graphCanBeSavedChanged = QtCore.pyqtSignal()
    graphCanBeSaved = QtCore.pyqtProperty(bool, graphCanBeSaved, notify=graphCanBeSavedChanged)



# This class exists just because there are problems when a class extends 2 other classes (Singleton and QObject)
class ButtleDataSingleton(Singleton):

    _buttleData = ButtleData()

    def get(self):
        return self._buttleData


def _decode_dict(dict_):
    """
        This function will recursively pass in nested dicts, and will convert all str elements into string (essential for some Tuttle functions). 
    """
    for key in dict_:
        if isinstance(dict_[key], str):
            dict_[key] = str(dict_[key])
    return dict_
