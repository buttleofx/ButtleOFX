from PyQt5 import QtCore
from quickmamba.patterns import Signal
from buttleofx.data import globalButtleData


class NodeManager(QtCore.QObject):
    """
        This class manages actions about nodes.
    """

    def __init__(self):
        super(NodeManager, self).__init__()

        self.undoRedoChanged = Signal()

    # ############################################ Methods exposed to QML ############################################ #

    @QtCore.pyqtSlot(str, str, int, int)
    def creationNode(self, graph, nodeType, x=20, y=20):
        """
            Creates a node.
        """
        # globalButtleData.getGraph().createNode(nodeType, x, y)
        # graph.createNode(nodeType, x, y)

        if graph == "_buttleData.graph":
            globalButtleData.getGraph().createNode(nodeType, x, y)
        elif graph == "_buttleData.graphBrowser":
            globalButtleData.getGraphBrowser().createNode(nodeType, x, y)
        # By default creation is on the graph in grapheditor
        else:
            globalButtleData.getGraph().createNode(nodeType, x, y)

        # Update undo/redo display
        self.undoRedoChanged()

    @QtCore.pyqtSlot()
    def copyNode(self):
        """
            Copies the current node(s).
        """
        # Clear the info saved in currentCopiedNodesInfo
        globalButtleData.clearCurrentCopiedNodesInfo()
        # Save new data in currentCopiedNodesInfo for each selected node
        if globalButtleData.getCurrentSelectedNodeWrappers() != []:
            for node in globalButtleData.getCurrentSelectedNodeWrappers():
                copyNode = {}
                copyNode.update({"nodeType": node.getNode().getType()})
                copyNode.update({"nameUser": node.getNode().getNameUser()})
                copyNode.update({"color": node.getNode().getColor()})
                copyNode.update({"params": node.getNode().getTuttleNode().getParamSet()})
                copyNode.update({"mode": "_copy"})
                copyNode.update({"x": node.getNode().getCoord()[0]})
                copyNode.update({"y": node.getNode().getCoord()[1]})
                globalButtleData.getCurrentCopiedNodesInfo()[node.getName()] = copyNode
                # Emit the change for the toolbar
                globalButtleData.pastePossibilityChanged.emit()

    @QtCore.pyqtSlot()
    def cutNode(self):
        """
            Cuts the current node(s).
        """
        # Call the copyNode function to save the data of the selected nodes
        self.copyNode()

        # If we are sure that at least one node is selected
        if globalButtleData.getCurrentSelectedNodeWrappers() != []:
            for node in globalButtleData.getCurrentSelectedNodeWrappers():
                # We precise that we want to cut the node and not only copy it
                globalButtleData.getCurrentCopiedNodesInfo()[node.getName()].update({"mode": ""})
                # And we delete it
                self.destructionNodes()
                # And update the view if necessary
                if globalButtleData.getCurrentViewerNodeName() in globalButtleData.getCurrentSelectedNodeNames():
                    globalButtleData.setCurrentViewerNodeName(None)
                if globalButtleData.getCurrentParamNodeName() in globalButtleData.getCurrentSelectedNodeNames():
                    globalButtleData.setCurrentParamNodeName(None)
                # Emit the change for the toolbar
                globalButtleData.pastePossibilityChanged.emit()

    @QtCore.pyqtSlot()
    def destructionNodes(self):
        """
            Deletes the current node(s).
        """
        # If the params of the current node deleted are display
        if globalButtleData.getCurrentParamNodeName() in globalButtleData.getCurrentSelectedNodeNames():
            globalButtleData.setCurrentParamNodeName(None)

        # If the viewer of the current node deleted is display
        if globalButtleData.getCurrentViewerNodeName() in globalButtleData.getCurrentSelectedNodeNames():
            globalButtleData.setCurrentViewerNodeName(None)
        # If the viewer displays a node affected by the destruction
        # need something from Tuttle
        # if at least one node in the graph
        if len(globalButtleData.getGraphWrapper().getNodeWrappers()) > 0 and len(globalButtleData.getGraph().getNodes()) > 0:
            # If a node is selected
            if globalButtleData.getCurrentSelectedNodeNames() != []:
                globalButtleData.getGraph().deleteNodes([nodeWrapper.getNode() for nodeWrapper in
                                                   globalButtleData.getCurrentSelectedNodeWrappers()])
                globalButtleData.clearCurrentSelectedNodeNames()

        # Emit signals
        globalButtleData.currentParamNodeChanged.emit()
        globalButtleData.currentViewerNodeChanged.emit()
        globalButtleData.currentSelectedNodesChanged.emit()

        # Update undo/redo display
        self.undoRedoChanged()

    @QtCore.pyqtSlot(str, int, int)
    def dropFile(self, url, x, y):
        """
            Drops a file on the graph.
            - Image or video : creates a reader node.
            - Json : load a graph (if the format allows it)
        """
        if QtCore.QUrl(url).isLocalFile():
            url = QtCore.QUrl(url).toLocalFile()
        extension = url.split(".")[-1].lower()
        if extension == 'bofx':
            globalButtleData.loadData(url)  # Also need to verify the json format
        else:
            globalButtleData.getGraph().createReaderNode(url, x, y)

        # Update undo/redo display
        self.undoRedoChanged()

    @QtCore.pyqtSlot()
    def duplicationNode(self):
        """
            Duplicates the current node(s).
        """
        if globalButtleData.getCurrentSelectedNodeWrappers() != []:
            for node in globalButtleData.getCurrentSelectedNodeWrappers():
                # Create a node giving the current selected node's type, x and y
                nodeType = node.getNode().getType()
                coord = node.getNode().getCoord()
                globalButtleData.getGraph().createNode(nodeType, coord[0], coord[1])
                newNode = globalButtleData.getGraph().getNodes()[-1]

                # Get the current selected node's properties
                nameUser = node.getNameUser() + "_duplicate"
                oldCoord = node.getNode().getOldCoord()
                color = node.getNode().getColor()

                # Use the current selected node's properties to set the duplicated node's properties
                newNode.setNameUser(nameUser)
                newNode.setOldCoord(oldCoord[0], oldCoord[1])
                newNode.setColor(color)
                newNode.getTuttleNode().getParamSet().copyParamsValues(node.getNode().getTuttleNode().getParamSet())

        # Update undo/redo display
        self.undoRedoChanged()

    @QtCore.pyqtSlot(str, int, int)
    def nodeMoved(self, nodeName, x, y):
        """
            This function pushes a cmdMoved in the CommandManager.
        """
        globalButtleData.getGraph().nodeMoved(nodeName, x, y)
        globalButtleData.getGraph().nodesChanged()
        globalButtleData.getGraphWrapper().setResize(True)
        # Update undo/redo display
        self.undoRedoChanged()

    @QtCore.pyqtSlot(str, int, int)
    def moveNode(self, nodeName, newX, newY):
        """
            This function updates the position of the selected nodes and the connections,
            when one or several nodes are moving.
        """
        graphWrapper = globalButtleData.getGraphWrapper()

        oldX = graphWrapper.getTmpMoveNodeX()
        oldY = graphWrapper.getTmpMoveNodeY()

        # What is the value of the movement (compared to the old position) ?
        xMovement = newX - oldX
        yMovement = newY - oldY
        graphWrapper.setTmpMoveNodeX(newX)
        graphWrapper.setTmpMoveNodeY(newY)

        # For each selected node, we update the position considering the value of the movement
        for selectedNodeWrapper in globalButtleData.getCurrentSelectedNodeWrappers():
            selectedNode = selectedNodeWrapper.getNode()
            currentX, currentY = selectedNode.getCoord()
            if selectedNode._name != nodeName:
                selectedNode.setCoord(currentX + xMovement, currentY + yMovement)

    @QtCore.pyqtSlot()
    def pasteNode(self):
        """
            Pasts the current node(s).
        """
        globalButtleData.clearCurrentSelectedNodeNames()
        # If nodes have been copied previously
        if globalButtleData.getCurrentCopiedNodesInfo():
            # Create a copy for each node copied
            i = 0

            for node in globalButtleData.getCurrentCopiedNodesInfo():
                globalButtleData.getGraph().createNode(globalButtleData.getCurrentCopiedNodesInfo()[node]["nodeType"],
                                                 globalButtleData.getCurrentCopiedNodesInfo()[node]["x"] + 20,
                                                 globalButtleData.getCurrentCopiedNodesInfo()[node]["y"] + 20)
                newNode = globalButtleData.getGraph().getNodes()[-1]
                globalButtleData.appendToCurrentSelectedNodeNames(newNode._name)
                newNode.setColor(globalButtleData.getCurrentCopiedNodesInfo()[node]["color"])
                newNode.setNameUser(globalButtleData.getCurrentCopiedNodesInfo()[node]["nameUser"] +
                                    globalButtleData.getCurrentCopiedNodesInfo()[node]["mode"])
                newNode.getTuttleNode().getParamSet().copyParamsValues(globalButtleData.getCurrentCopiedNodesInfo()[node]
                                                                       ["params"])
                globalButtleData.getGraph().nodesChanged()
                globalButtleData.getCurrentCopiedNodesInfo()[node].update({node: newNode._name})
                i = i + 1

        # Update undo/redo display
        self.undoRedoChanged()
