import os
import io
import json
import logging
from datetime import datetime

from PyQt5 import QtCore

from pyTuttle import tuttle

from quickmamba.models import QObjectListModel

from buttleofx.data import tuttleTools
from buttleofx.core.graph import Graph
from buttleofx.gui.shortcut import Shortcut
from buttleofx.gui.graph import GraphWrapper
from buttleofx.gui.plugin import PluginWrapper
from buttleofx.core.undo_redo.manageTools import globalCommandManager
from buttleofx.gui.graph.node import NodeWrapper


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
        - _listOfShortcut : list of all shortcuts used
        - _currentViewerNodeName : the name of the node currently in the viewer
        - _currentSelectedNodeNames : list of the names of the nodes currently selected
        - _currentParamNodeName : the name of the node currently displayed in the paramEditor
        - _currentConnectionId : the list of the id of the connections currently selected
        - _currentCopiedConnectionsInfo : the list of buttle info for the connections of the current nodes copied
        - _currentCopiedNodesInfo : the list of buttle info for the current node(s) copied
        - _mapNodeNameToComputedImage : this map makes the correspondance between a gloablHash and a computed image
          (max 20 images stored)
        - _buttlePath : the path of the root directory (useful to import images)
        - _graphCanBeSaved : a boolean indicating if the graph had changed since the last saving
          (useful for the display of the icon "save graph")
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

    # The current params
    _currentParamNodeName = None
    _currentSelectedNodeNames = []

    # For the connections
    _currentConnectionId = None

    # To eventually save current nodes data
    _currentCopiedNodesInfo = {}

    # To eventually save current connections data
    _currentCopiedConnectionsInfo = {}

    # For the viewer
    _currentViewerIndex = 1
    _currentViewerFrame = 0
    _currentViewerNodeName = None
    _mapViewerIndextoNodeName = {}
    _mapNodeNameToComputedImage = {}

    # Boolean used in viewerManager
    _videoIsPlaying = False

    # Processgraph used in viewerManager to compute images
    _processGraph = None
    _timeRange = None

    _urlOfFileToSave = ""

    def init(self, view, filePath=''):
        self._graph = Graph()
        self._graphWrapper = GraphWrapper(self._graph, view)

        self._graphBrowser = Graph()
        self._graphBrowserWrapper = GraphWrapper(self._graphBrowser, view)

        self._listOfShortcut = QObjectListModel(self)

        self._mapGraph = {
            "graph": self._graph,
            "graphBrowser": self._graphBrowser,
        }

        self._currentGraph = self._graph  # By default, the current graph is the graph of the graphEditor
        self._currentGraphWrapper = self._graphWrapper  # By default, the current graph is the graph of the graphEditor
        self._buttlePath = filePath

        # 9 views for the viewer, the 10th for the browser, the 11th temporary
        for index in range(1, 12):
            self._mapViewerIndextoNodeName[str(index)] = None

        return self

    # ############################################ Methods exposed to QML ############################################ #

    # ## Getters ## #

    @QtCore.pyqtSlot()
    def getCurrentViewerNodeName(self):
        """
            Returns the name of the current viewer node.
        """
        return self._currentViewerNodeName

    @QtCore.pyqtSlot(str, result=str)
    def getFileName(self, path):
        return os.path.basename(path)

    @QtCore.pyqtSlot(int, result=int)
    def getFrameByViewerIndex(self, index):
        """
            Returns the frame of the node contained in the viewer at the corresponding index.
        """
        # We get info about this node. It's a tuple (fodeName, frame), so we have to return
        # the second element nodeViewerInfos[1].
        nodeViewerInfos = self._mapViewerIndextoNodeName[str(index)]
        if nodeViewerInfos is None:
            return 0
        else:
            return nodeViewerInfos[1]

    @QtCore.pyqtSlot(result=QtCore.QObject)
    def getlistOfContext(self):
        listOfShortcutContext = QObjectListModel(self)
        self.getlistOfShortcut()
        for s in self._listOfShortcut:
            if not listOfShortcutContext.contains(s._shortcutContext):
                listOfShortcutContext.append(s._shortcutContext)
        return listOfShortcutContext

    @QtCore.pyqtSlot(result=QtCore.QObject)
    def getlistOfShortcut(self):
        self._listOfShortcut = QObjectListModel(self)

        self.addShortcut("Ctrl", "C", "Copy", "Permit to copy nodes or portions of graph", "Graph")
        self.addShortcut("Ctrl", "X", "Cut", "Permit to cut nodes or portions of graph", "Graph")
        self.addShortcut(
            "Ctrl", "V", "Paste",
            "Permit to paste nodes or portions of graph previously cut or copied", "Graph")
        self.addShortcut("Ctrl", "S", "Save", "Permit to save the current graph", "Graph")
        self.addShortcut("Ctrl", "Z", "Undo", "Abort the last modification in the graph", "Graph")
        self.addShortcut("Ctrl", "Y", "Redo", "Restore the last action undid", "Graph")
        self.addShortcut("Ctrl", "A", "Select all", "Select all nodes of the graph", "Graph")
        self.addShortcut("Ctrl", "D", "Duplicate", "Duplicate selected nodes", "Graph")
        self.addShortcut("Ctrl", "N", "New graph", "Close the current graph and create an other one", "Graph")
        self.addShortcut(
            "Ctrl", "O", "Open graph",
            "Close the current graph and open a browser which permit to open another one", "Graph")
        self.addShortcut("Del", "", "Delete", "Delete selected nodes or oprtion of graph", "Graph")
        self.addShortcut("P", "", "Parameters", "Show parameters of the node in the parameter editor", "Graph")
        self.addShortcut(
            "Return", "", "Display",
            "Assign the mosquito to the selected node, and diplay it in the viewer", "Graph")
        self.addShortcut(
            "Enter", "", "Display",
            "Assign the mosquito to the selected node, and diplay it in the viewer", "Graph")
        self.addShortcut(
            "Tab", "", "Plugin browser",
            "Permit to paste a node or a portion of graph previously cut or copied", "Graph")

        self.addShortcut("Up", "", "Previous", "Go to the next plugin in the list", "Plugin Documentation")
        self.addShortcut("Down", "", "Next", "Go to the previous plugin in the list", "Plugin Documentation")
        self.addShortcut(
            "Return", "", "Plugin help",
            "Show the documentation for the selected plugin", "Plugin Documentation")
        self.addShortcut(
            "Enter", "", "Plugin help",
            "Show the documentation for the selected plugin", "Plugin Documentation")

        self.addShortcut("Up", "", "Previous", "Go to the next plugin in the list", "Plugin Browser")
        self.addShortcut("Down", "", "Next", "Go to the previous plugin in the list", "Plugin Browser")
        self.addShortcut("Return", "", "Add", "Create the selected plugin", "Plugin Browser")
        self.addShortcut("Enter", "", "Add", "Create the selected plugin", "Plugin Browser")

        self.addShortcut("1", "", "Viewer 1", "Show the view 1 of the viewer previously assigned to a node", "Viewer")
        self.addShortcut("2", "", "Viewer 2", "Show the view 2 of the viewer previously assigned to a node", "Viewer")
        self.addShortcut("3", "", "Viewer 3", "Show the view 3 of the viewer previously assigned to a node", "Viewer")
        self.addShortcut("4", "", "Viewer 4", "Show the view 4 of the viewer previously assigned to a node", "Viewer")
        self.addShortcut("5", "", "Viewer 5", "Show the view 5 of the viewer previously assigned to a node", "Viewer")
        self.addShortcut("6", "", "Viewer 6", "Show the view 6 of the viewer previously assigned to a node", "Viewer")
        self.addShortcut("7", "", "Viewer 7", "Show the view 7 of the viewer previously assigned to a node", "Viewer")
        self.addShortcut("8", "", "Viewer 8", "Show the view 8 of the viewer previously assigned to a node", "Viewer")
        self.addShortcut("9", "", "Viewer 9", "Show the view 9 of the viewer previously assigned to a node", "Viewer")
        self.addShortcut(
            "Space", "", "Pause/Play",
            "If you are visionning an image sequence, then you can press this key to pause or play/resume", "Viewer")

        self.addShortcut("Ctrl", "L", "", "", "Browser")
        self.addShortcut(
            "Ctrl", "N",
            "New folder", "Create a new folder which default name is ''New directory''", "Browser")
        self.addShortcut("F2", "", "Rename", "Rename the selected file or folder", "Browser")
        self.addShortcut(
            "Tab", "", "Auto-completion",
            "Propose subfolders of the current directory that match what you already wrote in the search bar",
            "Browser")
        self.addShortcut("Del", "", "Delete", "Delete selected folders. Warning: it still irreversible!", "Browser")

        return self._listOfShortcut

    @QtCore.pyqtSlot(str, result=QtCore.QObject)
    def getlistOfShortcutByContext(self, context):
        listOfShortcutByContext = QObjectListModel(self)
        self.getlistOfShortcut()
        for s in self._listOfShortcut:
            if s._shortcutContext == context:
                if not listOfShortcutByContext.contains(s):
                    listOfShortcutByContext.append(s)
        return listOfShortcutByContext

    @QtCore.pyqtSlot(int, result=QtCore.QObject)
    def getNodeWrapperByViewerIndex(self, index):
        """
            Returns the nodeWrapper of the node contained in the viewer at the corresponding index.
        """
        # We get info about this node. It's a tuple (fodeName, frame), so we have to return
        # the first element nodeViewerInfos[0].
        nodeViewerInfos = self._mapViewerIndextoNodeName[str(index)]
        if nodeViewerInfos is None:
            return None
        else:
            return self._currentGraphWrapper.getNodeWrapper(nodeViewerInfos[0])

    @QtCore.pyqtSlot(result=QtCore.QObject)
    def getParentNodes(self):
        """
            Return the list of parents of selected nodes as a QObjectListModel
        """
        currentSelectedNodeWrappers = self.getCurrentSelectedNodeWrappers()
        toVisit = set()
        visited = set()

        for selectedNodeWrapper in currentSelectedNodeWrappers:
            toVisit.add(selectedNodeWrapper)

        while len(toVisit) != 0:
            currentNodeWrapper = toVisit.pop()

            # If the node has not already been visited
            if currentNodeWrapper in visited:
                continue

            # If the node has inputs
            if currentNodeWrapper.getNbInput() > 0:
                currentNodeSrcClips = currentNodeWrapper.getSrcClips()

                # For all inputs
                for currentNodeSrcClip in currentNodeSrcClips:
                    # If the input is connected to a parent
                    if self.getGraphWrapper().getConnectedClipWrapper(currentNodeSrcClip, False) is not None:
                        parentNodeWrapper = self.getGraphWrapper().getNodeWrapper(
                            self.getGraphWrapper().getConnectedClipWrapper(currentNodeSrcClip, False).getNodeName())
                        toVisit.add(parentNodeWrapper)
            # currentNodeWrapper.getNode().setColorRGB(255, 255, 255)
            # currentNodeWrapper.setIsHighlighted(True)
            visited.add(currentNodeWrapper)

        parentNodesWrappers = QObjectListModel(self)

        while len(visited) != 0:
            parentNodesWrappers.append(visited.pop())
        return parentNodesWrappers

    @QtCore.pyqtSlot(str, result=QtCore.QObject)
    def getPluginsWrappersSuggestions(self, pluginSearched):
        from pyTuttle import tuttle
        pluginCache = tuttle.core().getImageEffectPluginCache()
        plugins = pluginCache.getPlugins()
        plugins = sorted(plugins, key=lambda plugin: plugin.getDescriptor().getLabel())
        pluginsW = [PluginWrapper(plugin) for plugin in plugins]
        pluginsWModel = QObjectListModel(self)

        for p in pluginsW:
            if pluginSearched in p.pluginLabel.lower() or pluginSearched in p.pluginLabel:
                pluginsWModel.append(p)
        return pluginsWModel

    @QtCore.pyqtSlot(str, result=QtCore.QObject)
    def getPluginsByPath(self, menuPath):
        from pyTuttle import tuttle
        pluginCache = tuttle.core().getImageEffectPluginCache()
        plugins = pluginCache.getPlugins()
        plugins = sorted(plugins, key=lambda plugin: plugin.getDescriptor().getLabel())
        pluginsW = [PluginWrapper(plugin) for plugin in plugins]
        pluginsWModel = QObjectListModel(self)

        # For each plugin
        for p in pluginsW:
            path = p.pluginGroup

            # While path is not the final submenu, path is cropped
            while "/" in path:
                listOfPath = path.split("/")
                path = path.replace(listOfPath[0] + "/", "")

            # If the parentMenu name is in the parentPath of the plugin, we add the plugin to the list
            if menuPath == path:
                pluginsWModel.append(p)
        return pluginsWModel

    @QtCore.pyqtSlot(int, str, result=QtCore.QObject)
    def getMenu(self, nb, parentMenuPath):
        from pyTuttle import tuttle
        pluginCache = tuttle.core().getImageEffectPluginCache()
        plugins = pluginCache.getPlugins()
        pluginsW = [PluginWrapper(plugin) for plugin in plugins]
        pluginsListMenu = QObjectListModel(self)

        # For each plugin
        for p in pluginsW:
            path = p.pluginGroup + "/"
            parentPath = path

            # If the number of submenus of the plugin is higher than nb
            if path.count("/") >= nb:

                # Withdraw one submenu per loop from the path
                for _ in range(nb):
                    listOfPath = path.split("/")
                    path = path.replace(listOfPath[0] + "/", "")

                # If the submenu is not already in the list of submenu
                if not pluginsListMenu.contains(listOfPath[0]) and listOfPath[0]:

                    # If the submenu is not the first
                    if nb > 2:
                        # If the parentMenu name is in the parentPath of the plugin, the plugin is add to the list
                        if "/" + parentMenuPath + "/" in parentPath:
                            pluginsListMenu.append(listOfPath[0])
                    else:
                        if parentMenuPath + "/" in parentPath:
                            pluginsListMenu.append(listOfPath[0])
        return pluginsListMenu

    @QtCore.pyqtSlot(str, result=QtCore.QObject)
    def getQObjectPluginsIdentifiersByParentPath(self, pathname):
        """
            Returns a QObjectListModel of all the PluginsIdentifiers (String) we expect to
            find after the submenu 'pathname'.
        """
        pluginsIds = QObjectListModel(self)
        pluginsIds.setObjectList(tuttleTools.getPluginsIdentifiersByParentPath(pathname))
        return pluginsIds

    @QtCore.pyqtSlot(str, result=QtCore.QObject)
    def getSinglePluginSuggestion(self, pluginSearched):
        from pyTuttle import tuttle
        pluginCache = tuttle.core().getImageEffectPluginCache()
        plugins = pluginCache.getPlugins()
        pluginsW = [PluginWrapper(plugin) for plugin in plugins]
        pluginList = QObjectListModel(self)

        for p in pluginsW:
            if pluginSearched in p.pluginLabel.lower() or pluginSearched in p.pluginLabel:
                pluginList.append(p)
        if len(pluginList) == 1:
            return pluginList[0]

    @QtCore.pyqtSlot(result=QtCore.QObject)
    def getSortedNodesWrapper(self):
        """
            Returns the total of sorted param nodeWrapper for the parametersEditor.
        """
        listOfNodes = QObjectListModel(self)
        if len(self._graphWrapper.getNodeWrappers()) != 0:
            for nodes in self._graphWrapper.getNodeWrappers():
                if nodes.pluginContext == "OfxImageEffectContextReader":
                    listOfNodes.append(nodes)
                    firstNode = nodes
                else:
                    firstNode = self._graphWrapper.getNodeWrappers()[0]

            toVisit = set()
            visited = set()
            toVisit.add(firstNode)
            while len(toVisit) != 0:
                currentNodeWrapper = toVisit.pop()

                # If the node has not already been visited
                if currentNodeWrapper not in visited:
                    # If the node has inputs
                    currentNodeOutputClip = currentNodeWrapper.getOutputClip()

                    # If the input is connected to a parent
                    if self.getGraphWrapper().getConnectedClipWrapper_Output(currentNodeOutputClip) is not None:
                        parentNodeWrapper = self.getGraphWrapper().getNodeWrapper(
                            self.getGraphWrapper().getConnectedClipWrapper_Output(currentNodeOutputClip).getNodeName())
                        toVisit.add(parentNodeWrapper)

                    visited.add(currentNodeWrapper)

            listOfParents = QObjectListModel(self)
            listOfParents.append(firstNode)
            visited.remove(firstNode)
            while len(visited) != 0:
                listOfParents.append(visited.pop())

            for _ in range(len(listOfParents)):
                if len(listOfNodes) > 0:
                    currentNode = listOfNodes[len(listOfNodes) - 1]
                    currentNodeOutputClip = currentNode.getOutputClip()

                    # If the input is connected to a parent
                    if self.getGraphWrapper().getConnectedClipWrapper_Output(currentNodeOutputClip) is not None:
                        parentNode = self.getGraphWrapper().getNodeWrapper(
                            self.getGraphWrapper().getConnectedClipWrapper_Output(currentNodeOutputClip).getNodeName())
                        listOfNodes.append(parentNode)
            return listOfNodes
        else:
            return None

    # ## Others ## #

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

            # We project the bounding-boxes on the axes and we check if the segments overlap
            horizontalOverlap = (xNode < xRect + widthRect) and (xRect < xNode + widthNode)
            verticalOverlap = (yNode < yRect + heightRect) and (yRect < yNode + heightNode)
            overlap = horizontalOverlap and verticalOverlap

            # If the bounding-boxes overlap then the node is in the selection area
            if overlap:
                self.appendToCurrentSelectedNodeNames(nodeW.getName())

    @QtCore.pyqtSlot(str, str, str, str, str, result=QtCore.QObject)
    def addShortcut(self, key1, key2, name, doc, context):
        shortcut = Shortcut(key1, key2, name, doc, context)
        if not self._listOfShortcut.contains(shortcut):
            self._listOfShortcut.append(shortcut)

    @QtCore.pyqtSlot(QtCore.QObject)
    def appendToCurrentSelectedNodeWrappers(self, nodeWrapper):
        self.appendToCurrentSelectedNodeNames(nodeWrapper.getName())

    @QtCore.pyqtSlot(QtCore.QObject, int)
    def assignNodeToViewerIndex(self, nodeWrapper, frame):
        """
            Assigns a node to the _mapViewerIndextoNodeName at the current viewerIndex.
            It adds a tuple (nodeName, frame).
        """
        if nodeWrapper:
            self._mapViewerIndextoNodeName.update({str(self._currentViewerIndex): (nodeWrapper.getName(), frame)})

    @QtCore.pyqtSlot()
    def clearCurrentConnectionId(self):
        self._currentConnectionId = None
        self.currentConnectionWrapperChanged.emit()

    @QtCore.pyqtSlot()
    def clearCurrentSelectedNodeNames(self):
        self._currentSelectedNodeNames[:] = []
        self.currentSelectedNodesChanged.emit()

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

    @QtCore.pyqtSlot(str, result=bool)
    def isAPlugin(self, pluginId):
        """
            Returns if a string is a plugin identifier.
        """
        return pluginId in tuttleTools.getPluginsIdentifiers()

    @QtCore.pyqtSlot(result=QtCore.QObject)
    def lastNode(self):
        # Return the last node to connect to the new node

        sizeOfGraph = self._currentGraphWrapper._nodeWrappers.size()

        if (sizeOfGraph >= 1):
            # Nodes to connect
            lastNode = self._currentGraphWrapper._nodeWrappers[sizeOfGraph-1]
        else:
            lastNode = None

        # Update undo/redo display
        # self.undoRedoChanged()

        return lastNode

    @QtCore.pyqtSlot(str)
    @QtCore.pyqtSlot()
    def loadData(self, url='buttleofx/backup/data.bofx'):
        """
            Loads all data from a Json file (the default Json file if no url is given)
        """
        Qurl = QtCore.QUrl(url)
        filepath = (Qurl.isLocalFile() and Qurl.toLocalFile()) or url
        self.newData()

        with open(filepath, 'r') as f:
            read_data = f.read()
            decoded = json.loads(read_data, object_hook=_decode_dict)

            # Create the graph
            self.getGraph().dict_to_object(decoded["graph"])

            # Graph : currentSeletedNodes
            for currentSeletedNode in decoded["graph"]["currentSelectedNodes"]:
                self.appendToCurrentSelectedNodeNames(currentSeletedNode)
            self.currentSelectedNodesChanged.emit()

            # paramEditor : currentParamNodeName
            self.setCurrentParamNodeName(decoded["paramEditor"])
            self.currentParamNodeChanged.emit()

            # Viewer : other views
            for index, view in decoded["viewer"]["other_views"].items():
                nodeName, frame = view["nodeName"], view["frame"]
                self._mapViewerIndextoNodeName.update({index: (nodeName, frame)})

            # Viewer : currentViewerNodeName
            for index, current_view in decoded["viewer"]["current_view"].items():
                nodeName, frame = current_view["nodeName"], current_view["frame"]
                self._mapViewerIndextoNodeName.update({index: (nodeName, frame)})
            # The next commands need to be fixed: We need to click on the viewers number to see the image in the viewer
            #     self.setCurrentViewerIndex(int(index))
            #     self.setCurrentViewerNodeName(current_view)
            #     self.setCurrentViewerNodeWrapper = self.getNodeWrapperByViewerIndex(int(index))
            #     self.setCurrentViewerFrame(frame)
            # ButtleEvent().emitViewerChangedSignal()

        self.urlOfFileToSave = filepath

    @QtCore.pyqtSlot()
    def newData(self):
        """
            Create a new graph
        """
        self.graphWrapper.deleteGraphWrapper()
        globalCommandManager.clean()
        self.setUrlOfFileToSave("")
        self.setGraphCanBeSaved(False)

    @QtCore.pyqtSlot(int, result=QtCore.QObject)
    def nodeGoesDown(self, index):
        """
            The node which position in list is index goes to the position index+1
        """
        if index < self._graphWrapper.getNodeWrappers().size() - 1:

            if self._graphWrapper.getNodeWrapperByIndex(index).pluginContext != "OfxImageEffectContextReader":

                firstNodeX = self._graphWrapper.getNodeWrapperByIndex(index).getXCoord()
                firstNodeY = self._graphWrapper.getNodeWrapperByIndex(index).getYCoord()
                secondNodeX = self._graphWrapper.getNodeWrapperByIndex(index + 1).getXCoord()
                secondNodeY = self._graphWrapper.getNodeWrapperByIndex(index + 1).getYCoord()

                self._graphWrapper.getNodeWrapperByIndex(index).setXCoord(secondNodeX)
                self._graphWrapper.getNodeWrapperByIndex(index).setYCoord(secondNodeY)

                self._graphWrapper.getNodeWrapperByIndex(index + 1).setXCoord(firstNodeX)
                self._graphWrapper.getNodeWrapperByIndex(index + 1).setYCoord(firstNodeY)

                self._graphWrapper.getNodeWrappers().move(index, index + 1)

        return self._graphWrapper.getNodeWrappers()

    @QtCore.pyqtSlot(int, result=QtCore.QObject)
    def nodeGoesUp(self, index):
        """
            The node which position in list is index goes to the position index - 1
        """
        if index > 0:
            if self._graphWrapper.getNodeWrapperByIndex(index - 1).pluginContext != "OfxImageEffectContextReader":
                firstNodeX = self._graphWrapper.getNodeWrapperByIndex(index - 1).getXCoord()
                firstNodeY = self._graphWrapper.getNodeWrapperByIndex(index - 1).getYCoord()
                secondNodeX = self._graphWrapper.getNodeWrapperByIndex(index).getXCoord()
                secondNodeY = self._graphWrapper.getNodeWrapperByIndex(index).getYCoord()

                self._graphWrapper.getNodeWrapperByIndex(index - 1).setXCoord(secondNodeX)
                self._graphWrapper.getNodeWrapperByIndex(index - 1).setYCoord(secondNodeY)

                self._graphWrapper.getNodeWrapperByIndex(index).setXCoord(firstNodeX)
                self._graphWrapper.getNodeWrapperByIndex(index).setYCoord(firstNodeY)

                self._graphWrapper.getNodeWrappers().move(index, index - 1)

        return self._graphWrapper.getNodeWrappers()

    @QtCore.pyqtSlot("QVariant", result=bool)
    def nodeIsSelected(self, nodeWrapper):
        """
            Returns True if the node is selected (=if nodeName is in the list _currentSelectedNodeNames), else False.
        """
        for nodeName in self._currentSelectedNodeNames:
            if nodeName == nodeWrapper.getName():
                return True
        return False

    @QtCore.pyqtSlot(str, result=QtCore.QObject)
    def nodeReaderWrapperForBrowser(self, url):
        self._graphBrowser._nodes = []  # Clear the graph
        self._graphBrowser._graphTuttle = tuttle.Graph()  # Clear the graphTuttle
        self._currentGraph = self._graphBrowser
        self._currentGraphWrapper = self._graphBrowserWrapper

        readerNode = self._graphBrowser.createReaderNode(url, 0, 0)  # Create a reader node (like for file drag & drop)

        readerNodeWrapper = NodeWrapper(readerNode, self._graphBrowserWrapper._view)  # Wrapper of the reader file

        return readerNodeWrapper

    @QtCore.pyqtSlot(QtCore.QUrl)
    def saveData(self, url):
        """
            Saves all data in a json file
        """
        # If called from Python, it could be a str or a QUrl
        if isinstance(url, str):
            filepath = url
        else:
            filepath = url.toLocalFile() if url.isLocalFile() else url.toString()

        if filepath.endswith('buttleSave_now.bofx'):
            filepath = os.path.dirname(filepath)

        # if destination path is a folder, we create a file name containing date and time of now
        if os.path.isdir(filepath):
            filepath = os.path.join(filepath, 'buttleSave%s' % datetime.today().strftime('%m_%d_%y_%I_%M'))

        if not filepath.lower().endswith('.bofx'):
            filepath += '.bofx'

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

            # Date
            today = datetime.today().strftime("%A, %d. %B %Y %I:%M%p")
            dictJson["date"]["creation"] = today

            # Graph
            dictJson["graph"] = self.getGraph().object_to_dict()

            # Graph : currentSelectedNodes
            for node in self._graph.getNodes():
                if node.getName() in self.getCurrentSelectedNodeNames():
                    dictJson["graph"]["currentSelectedNodes"].append(node.getName())

            # paramEditor : currentParamNodeName
            dictJson["paramEditor"] = self.getCurrentParamNodeName()

            # Viewer : currentViewerNodeName
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

            # Write dictJson in a file
            f.write(str(json.dumps(dictJson, sort_keys=True, indent=2, ensure_ascii=False)))

        # Finally we update the savedGraphIndex of the CommandManager : it must be equal to the current index
        globalCommandManager.setSavedGraphIndex(globalCommandManager.getIndex())

        self.urlOfFileToSave = filepath

    @QtCore.pyqtSlot(int, int, int, float, float, float, float, float, int, int)
    def zoom(self, width, height, nodeWidth, zoomCoeff, graphPreviousWidth, graphPreviousHeight,
             mouseX, mouseY, offsetX, offsetY):

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
            if graphPreviousWidth != width:
                i.xCoord = ((i.xCoord - reinitOriginX) * width) / graphPreviousWidth
                i.yCoord = ((i.yCoord - reinitOriginY) * height) / graphPreviousHeight

            i.xCoord = ((i.xCoord * newWidth) / width) + newOriginX  # (nodeWidth * 0.5)
            i.yCoord = ((i.yCoord * newHeight) / height) + newOriginY  # (nodeWidth * 0.5)

        self._graphWrapper.updateNodeWrappers()
        self._graphWrapper.updateConnectionWrappers()

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getButtlePath(self):
        return self._buttlePath

    def getHomeDir(self):
        return os.path.expanduser("~")

    def getCurrentConnectionWrapper(self):
        """
            Returns the current currentConnectionWrapper.
        """
        return self._graphWrapper.getConnectionWrapper(self._currentConnectionId)

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

    def getCurrentGraph(self):
        return self._currentGraph

    def getCurrentGraphWrapper(self):
        return self._currentGraphWrapper

    def getCurrentParamNodeName(self):
        """
            Returns the name of the current param node.
        """
        return self._currentParamNodeName

    def getCurrentParamNodeWrapper(self):
        """
            Returns the current param nodeWrapper.
        """
        return self._currentGraphWrapper.getNodeWrapper(self.getCurrentParamNodeName())

    def getCurrentSelectedNodeNames(self):
        """
            Returns the names of the current selected nodes.
        """
        return self._currentSelectedNodeNames

    def getCurrentSelectedNodeWrappers(self):
        """
            Returns the current selected nodeWrappers as a QObjectListModel.
        """
        currentSelectedNodeWrappers = QObjectListModel(self)
        currentSelectedNodeWrappers.setObjectList([self.getGraphWrapper().getNodeWrapper(nodeName)
                                                   for nodeName in self.getCurrentSelectedNodeNames()])
        return currentSelectedNodeWrappers

    def getCurrentViewerFrame(self):
        """
            Returns the frame of the current viewer nodeWrapper.
        """
        return self._currentViewerFrame

    def getCurrentViewerIndex(self):
        """
            Returns the current viewer index.
        """
        return self._currentViewerIndex

    # def getCurrentViewerNodeWrapper(self):
    #     """
    #         Returns the current viewer nodeWrapper.
    #     """
    #     return self._graphWrapper.getNodeWrapper(self.getCurrentViewerNodeName())

    def getCurrentViewerNodeWrapper(self):
        """
            Returns the current viewer nodeWrapper.
        """
        return self._currentGraphWrapper.getNodeWrapper(self.getCurrentViewerNodeName())

    def getEditedNodesWrapper(self):
        """
            Returns the total of param nodeWrapper for the parametersEditor.
        """
        return self.getCurrentGraphWrapper().getNodeWrappers()

    def getGraph(self):
        return self._graph

    def getGraphBrowser(self):
        return self._graphBrowser

    def getGraphBrowserWrapper(self):
        return self._graphBrowserWrapper

    def getGraphWrapper(self):
        return self._graphWrapper

    def getMapNodeNameToComputedImage(self):
        """
            Returns the map of images already computed.
        """
        return self._mapNodeNameToComputedImage

    def getProcessGraph(self):
        return self._processGraph

    def getPluginsIdentifiers(self):
        from pyTuttle import tuttle
        pluginCache = tuttle.core().getImageEffectPluginCache()
        plugins = pluginCache.getPlugins()
        plugins = sorted(plugins, key=lambda plugin: plugin.getIdentifier().upper())
        logging.debug("getPluginsIdentifiers => nb plugins: %d", len(plugins))

        pluginsIds = [plugin.getIdentifier() for plugin in plugins]
        pluginsIdsModel = QObjectListModel(self)

        for p in pluginsIds:
            pluginsIdsModel.append(p)
        return pluginsIdsModel

    def getPluginsWrappers(self):
        from pyTuttle import tuttle
        pluginCache = tuttle.core().getImageEffectPluginCache()
        plugins = pluginCache.getPlugins()
        plugins = sorted(plugins, key=lambda plugin: plugin.getDescriptor().getLabel())
        pluginsW = [PluginWrapper(plugin) for plugin in plugins]
        pluginsWModel = QObjectListModel(self)

        for p in pluginsW:
            pluginsWModel.append(p)
        return pluginsWModel

    def getUrlOfFileToSave(self):
        return self._urlOfFileToSave

    def getVideoIsPlaying(self):
        return self._videoIsPlaying

    # ## Setters ## #

    def setCurrentConnectionWrapper(self, connectionWrapper):
        """
            Changes the current conenctionWrapper and emits the change.
        """
        if self._currentConnectionId == connectionWrapper.getId():
            self._currentConnectionId = None
        else:
            self._currentConnectionId = connectionWrapper.getId()
        self.currentConnectionWrapperChanged.emit()

    def setCurrentCopiedConnectionsInfo(self, connectionsInfo):
        self._currentCopiedConnectionsInfo = connectionsInfo

    def setCurrentCopiedNodesInfo(self, nodesInfo):
        self._currentCopiedNodesInfo = nodesInfo

    def setCurrentGraph(self, currentGraph):
        """
            Set the _currentGraph // doesn't work in QML
        """
        self._currentGraph = currentGraph
        self.currentGraphChanged.emit()

    def setCurrentGraphWrapper(self, currentGraphWrapper):
        """
            Set the _currentGraphWrapper
        """
        self._currentGraphWrapper = currentGraphWrapper
        self.currentGraphWrapperChanged.emit()

    def setCurrentParamNodeName(self, nodeName):
        self._currentParamNodeName = nodeName
        self.currentSelectedNodesChanged.emit()

    def setCurrentParamNodeWrapper(self, nodeWrapper):
        """
            Changes the current param node and emits the change.
        """
        if self._currentParamNodeName == nodeWrapper.getName():
            return
        self._currentParamNodeName = nodeWrapper.getName()
        # Emit signal
        self.currentParamNodeChanged.emit()

    def setCurrentSelectedNodeNames(self, nodeNames):
        self._currentSelectedNodeNames = nodeNames

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

    def setCurrentViewerFrame(self, frame):
        self._currentViewerFrame = frame
        self.currentViewerFrameChanged.emit()

    def setCurrentViewerNodeName(self, nodeName):
        self._currentViewerNodeName = nodeName
        self.currentViewerNodeChanged.emit()

    # def setCurrentViewerNodeWrapper(self, nodeWrapper):
    #     """
    #         Changes the current viewer node and emits the change.
    #     """
    #     if nodeWrapper is None:
    #         self._currentViewerNodeName = None
    #     elif self._currentViewerNodeName == nodeWrapper.getName():
    #         return
    #     else:
    #         self._currentViewerNodeName = nodeWrapper.getName()
    #     # emit signal
    #     self.currentViewerNodeChanged.emit()

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
        # Emit signal
        # logging.debug("setCurrentViewerId globalButtleData.getCurrentGraphWrapper(): %s",self.getCurrentGraphWrapper())
        # logging.debug("setCurrentViewerId nodeWrapper.getName(): %s", nodeWrapper.getName())

        # logging.debug("setCurrentViewerId self._graphBrowser._graphTuttle: ", self._graphBrowser._graphTuttle)

        self.currentViewerNodeChanged.emit()

    def setGraphCanBeSaved(self, canBeSaved):
        """
            Set the value of the boolean self._graphCanBeSaved.
        """
        self._graphCanBeSaved = canBeSaved
        self.graphCanBeSavedChanged.emit()

    def setProcessGraph(self, processGraph):
        self._processGraph = processGraph

    def setUrlOfFileToSave(self, url):
        self._urlOfFileToSave = url
        self.urlOfFileToSaveChanged.emit()

    def setVideoIsPlaying(self, valueBool):
        self._videoIsPlaying = valueBool

    # ## Others ## #

    def appendNodeWrapper(self, nodeWrapper):
        if nodeWrapper.getName() in self._currentSelectedNodeNames:
                self._currentSelectedNodeNames.remove(nodeWrapper.getName())
        self._currentSelectedNodeNames.append(nodeWrapper.getName())
        self.currentSelectedNodesChanged.emit()

    def appendToCurrentSelectedNodeNames(self, nodeName):
        if nodeName in self._currentSelectedNodeNames:
            self._currentSelectedNodeNames.remove(nodeName)
        else:
            self._currentSelectedNodeNames.append(nodeName)
        # Emit signal
        self.currentSelectedNodesChanged.emit()

    def canPaste(self):
        """
            Returns True if we can paste (= if there is at least one node selected).
        """
        return self._currentCopiedNodesInfo != {}

    def clearCurrentCopiedConnectionsInfo(self):
        self._currentCopiedConnectionsInfo.clear()

    def clearCurrentCopiedNodesInfo(self):
        self._currentCopiedNodesInfo.clear()

    def graphCanBeSaved(self):
        """
            Returns the value of the boolean self._graphCanBeSaved
        """
        return self._graphCanBeSaved

    # ############################################# Data exposed to QML ############################################## #

    pluginsIdentifiers = QtCore.pyqtProperty(QtCore.QObject, getPluginsIdentifiers, constant=True)
    pluginsDocs = QtCore.pyqtProperty(QtCore.QObject, getPluginsWrappers, constant=True)

    graph = QtCore.pyqtProperty(QtCore.QObject, getGraph, constant=True)
    graphBrowser = QtCore.pyqtProperty(QtCore.QObject, getGraphBrowser, constant=True)

    # graphWrapper
    graphWrapper = QtCore.pyqtProperty(QtCore.QObject, getGraphWrapper, constant=True)
    graphBrowserWrapper = QtCore.pyqtProperty(QtCore.QObject, getGraphBrowserWrapper, constant=True)

    # filePath
    buttlePath = QtCore.pyqtProperty(str, getButtlePath, constant=True)
    homeDir = QtCore.pyqtProperty(str, getHomeDir, constant=True)

    # Current param, view, and selected node
    currentParamNodeChanged = QtCore.pyqtSignal()
    currentParamNodeWrapper = QtCore.pyqtProperty(QtCore.QObject, getCurrentParamNodeWrapper,
                                                  setCurrentParamNodeWrapper, notify=currentParamNodeChanged)

    currentViewerNodeChanged = QtCore.pyqtSignal()
    currentViewerNodeWrapper = QtCore.pyqtProperty(QtCore.QObject, getCurrentViewerNodeWrapper,
                                                   setCurrentViewerNodeWrapper, notify=currentViewerNodeChanged)
    currentViewerFrameChanged = QtCore.pyqtSignal()
    currentViewerFrame = QtCore.pyqtProperty(int, getCurrentViewerFrame, setCurrentViewerFrame,
                                             notify=currentViewerFrameChanged)

    currentViewerNodeName = QtCore.pyqtProperty(QtCore.QObject, getCurrentViewerNodeName, constant=True)

    currentSelectedNodesChanged = QtCore.pyqtSignal()
    currentSelectedNodeWrappers = QtCore.pyqtProperty("QVariant", getCurrentSelectedNodeWrappers,
                                                      setCurrentSelectedNodeWrappers,
                                                      notify=currentSelectedNodesChanged)

    currentConnectionWrapperChanged = QtCore.pyqtSignal()
    currentConnectionWrapper = QtCore.pyqtProperty(QtCore.QObject, getCurrentConnectionWrapper,
                                                   setCurrentConnectionWrapper,
                                                   notify=currentConnectionWrapperChanged)

    currentViewerIndexChanged = QtCore.pyqtSignal()
    currentViewerIndex = QtCore.pyqtProperty(int, getCurrentViewerIndex, setCurrentViewerIndex,
                                             notify=currentViewerIndexChanged)

    # Total of the nodes
    editedNodesWrapper = QtCore.pyqtProperty(QtCore.QObject, getEditedNodesWrapper, constant=True)

    currentGraphWrapperChanged = QtCore.pyqtSignal()
    currentGraphWrapper = QtCore.pyqtProperty(QtCore.QObject, getCurrentGraphWrapper,
                                              setCurrentGraphWrapper, notify=currentGraphWrapperChanged)

    currentGraphChanged = QtCore.pyqtSignal()
    currentGraph = QtCore.pyqtProperty(QtCore.QObject, getCurrentGraph, setCurrentGraph,
                                       notify=currentGraphChanged)

    # Paste possibility
    pastePossibilityChanged = QtCore.pyqtSignal()
    canPaste = QtCore.pyqtProperty(bool, canPaste, notify=pastePossibilityChanged)

    # Possibility to save graph
    graphCanBeSavedChanged = QtCore.pyqtSignal()
    graphCanBeSaved = QtCore.pyqtProperty(bool, graphCanBeSaved, notify=graphCanBeSavedChanged)

    # Url of the file to save
    urlOfFileToSaveChanged = QtCore.pyqtSignal()
    urlOfFileToSave = QtCore.pyqtProperty(str, getUrlOfFileToSave, setUrlOfFileToSave, notify=urlOfFileToSaveChanged)


globalButtleData = ButtleData()


def _decode_dict(_dict):
    """
        This function will recursively pass in nested dicts, and will convert
        all str elements into string (essential for some Tuttle functions).
    """
    for key in _dict:
        if isinstance(_dict[key], str):
            _dict[key] = str(_dict[key])
    return _dict
