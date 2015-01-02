from PyQt5 import QtCore
from quickmamba.patterns import Signal
from buttleofx.data import ButtleDataSingleton


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
        buttleData = ButtleDataSingleton().get()
        # buttleData.getGraph().createNode(nodeType, x, y)
        # graph.createNode(nodeType, x, y)

        if graph == "_buttleData.graph":
            buttleData.getGraph().createNode(nodeType, x, y)
        elif graph == "_buttleData.graphBrowser":
            buttleData.getGraphBrowser().createNode(nodeType, x, y)
        # By default creation is on the graph in grapheditor
        else:
            buttleData.getGraph().createNode(nodeType, x, y)

        # Update undo/redo display
        self.undoRedoChanged()

    @QtCore.pyqtSlot()
    def copyNode(self):
        """
            Copies the current node(s).
        """
        buttleData = ButtleDataSingleton().get()
        # Clear the info saved in currentCopiedNodesInfo
        buttleData.clearCurrentCopiedNodesInfo()
        # Save new data in currentCopiedNodesInfo for each selected node
        if buttleData.getCurrentSelectedNodeWrappers() != []:
            for node in buttleData.getCurrentSelectedNodeWrappers():
                copyNode = {}
                copyNode.update({"nodeType": node.getNode().getType()})
                copyNode.update({"nameUser": node.getNode().getNameUser()})
                copyNode.update({"color": node.getNode().getColor()})
                copyNode.update({"params": node.getNode().getTuttleNode().getParamSet()})
                copyNode.update({"mode": "_copy"})
                copyNode.update({"x": node.getNode().getCoord()[0]})
                copyNode.update({"y": node.getNode().getCoord()[1]})
                buttleData.getCurrentCopiedNodesInfo()[node.getName()] = copyNode
                # Emit the change for the toolbar
                buttleData.pastePossibilityChanged.emit()

    @QtCore.pyqtSlot()
    def cutNode(self):
        """
            Cuts the current node(s).
        """
        # Call the copyNode function to save the data of the selected nodes
        self.copyNode()
        buttleData = ButtleDataSingleton().get()

        # If we are sure that at least one node is selected
        if buttleData.getCurrentSelectedNodeWrappers() != []:
            for node in buttleData.getCurrentSelectedNodeWrappers():
                # We precise that we want to cut the node and not only copy it
                buttleData.getCurrentCopiedNodesInfo()[node.getName()].update({"mode": ""})
                # And we delete it
                self.destructionNodes()
                # And update the view if necessary
                if buttleData.getCurrentViewerNodeName() in buttleData.getCurrentSelectedNodeNames():
                    buttleData.setCurrentViewerNodeName(None)
                if buttleData.getCurrentParamNodeName() in buttleData.getCurrentSelectedNodeNames():
                    buttleData.setCurrentParamNodeName(None)
                # Emit the change for the toolbar
                buttleData.pastePossibilityChanged.emit()

    @QtCore.pyqtSlot()
    def destructionNodes(self):
        """
            Deletes the current node(s).
        """
        buttleData = ButtleDataSingleton().get()

        # If the params of the current node deleted are display
        if buttleData.getCurrentParamNodeName() in buttleData.getCurrentSelectedNodeNames():
            buttleData.setCurrentParamNodeName(None)

        # If the viewer of the current node deleted is display
        if buttleData.getCurrentViewerNodeName() in buttleData.getCurrentSelectedNodeNames():
            buttleData.setCurrentViewerNodeName(None)
        # If the viewer displays a node affected by the destruction
        # need something from Tuttle
        # if at least one node in the graph
        if len(buttleData.getGraphWrapper().getNodeWrappers()) > 0 and len(buttleData.getGraph().getNodes()) > 0:
            # If a node is selected
            if buttleData.getCurrentSelectedNodeNames() != []:
                buttleData.getGraph().deleteNodes([nodeWrapper.getNode() for nodeWrapper in
                                                   buttleData.getCurrentSelectedNodeWrappers()])
                buttleData.clearCurrentSelectedNodeNames()

        # Emit signals
        buttleData.currentParamNodeChanged.emit()
        buttleData.currentViewerNodeChanged.emit()
        buttleData.currentSelectedNodesChanged.emit()

        # Update undo/redo display
        self.undoRedoChanged()

    @QtCore.pyqtSlot(str, int, int)
    def dropFile(self, url, x, y):
        """
            Drops a file on the graph.
            - Image or video : creates a reader node.
            - Json : load a graph (if the format allows it)
        """
        buttleData = ButtleDataSingleton().get()

        if QtCore.QUrl(url).isLocalFile():
            url = QtCore.QUrl(url).toLocalFile()
        extension = url.split(".")[-1].lower()
        if extension == 'bofx':
            buttleData.loadData(url)  # Also need to verify the json format
        else:
            buttleData.getGraph().createReaderNode(url, x, y)

        # Update undo/redo display
        self.undoRedoChanged()

    @QtCore.pyqtSlot()
    def duplicationNode(self):
        """
            Duplicates the current node(s).
        """
        buttleData = ButtleDataSingleton().get()
        if buttleData.getCurrentSelectedNodeWrappers() != []:
            for node in buttleData.getCurrentSelectedNodeWrappers():
                # Create a node giving the current selected node's type, x and y
                nodeType = node.getNode().getType()
                coord = node.getNode().getCoord()
                buttleData.getGraph().createNode(nodeType, coord[0], coord[1])
                newNode = buttleData.getGraph().getNodes()[-1]

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
        buttleData = ButtleDataSingleton().get()
        buttleData.getGraph().nodeMoved(nodeName, x, y)
        buttleData.getGraph().nodesChanged()
        buttleData.getGraphWrapper().setResize(True)
        # Update undo/redo display
        self.undoRedoChanged()

    @QtCore.pyqtSlot(str, int, int)
    def moveNode(self, nodeName, newX, newY):
        """
            This function updates the position of the selected nodes and the connections,
            when one or several nodes are moving.
        """
        buttleData = ButtleDataSingleton().get()
        graphWrapper = buttleData.getGraphWrapper()

        oldX = graphWrapper.getTmpMoveNodeX()
        oldY = graphWrapper.getTmpMoveNodeY()

        # What is the value of the movement (compared to the old position) ?
        xMovement = newX - oldX
        yMovement = newY - oldY
        graphWrapper.setTmpMoveNodeX(newX)
        graphWrapper.setTmpMoveNodeY(newY)

        # For each selected node, we update the position considering the value of the movement
        for selectedNodeWrapper in buttleData.getCurrentSelectedNodeWrappers():
            selectedNode = selectedNodeWrapper.getNode()
            currentX, currentY = selectedNode.getCoord()
            if selectedNode._name != nodeName:
                selectedNode.setCoord(currentX + xMovement, currentY + yMovement)

    @QtCore.pyqtSlot()
    def pasteNode(self):
        """
            Pasts the current node(s).
        """
        buttleData = ButtleDataSingleton().get()
        buttleData.clearCurrentSelectedNodeNames()
        # If nodes have been copied previously
        if buttleData.getCurrentCopiedNodesInfo():
            # Create a copy for each node copied
            i = 0

            for node in buttleData.getCurrentCopiedNodesInfo():
                buttleData.getGraph().createNode(buttleData.getCurrentCopiedNodesInfo()[node]["nodeType"],
                                                 buttleData.getCurrentCopiedNodesInfo()[node]["x"] + 20,
                                                 buttleData.getCurrentCopiedNodesInfo()[node]["y"] + 20)
                newNode = buttleData.getGraph().getNodes()[-1]
                buttleData.appendToCurrentSelectedNodeNames(newNode._name)
                newNode.setColor(buttleData.getCurrentCopiedNodesInfo()[node]["color"])
                newNode.setNameUser(buttleData.getCurrentCopiedNodesInfo()[node]["nameUser"] +
                                    buttleData.getCurrentCopiedNodesInfo()[node]["mode"])
                newNode.getTuttleNode().getParamSet().copyParamsValues(buttleData.getCurrentCopiedNodesInfo()[node]
                                                                       ["params"])
                buttleData.getGraph().nodesChanged()
                buttleData.getCurrentCopiedNodesInfo()[node].update({node: newNode._name})
                i = i + 1

        # Update undo/redo display
        self.undoRedoChanged()
