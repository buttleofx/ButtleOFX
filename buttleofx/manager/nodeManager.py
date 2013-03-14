from PySide import QtCore
# quickmamba
from quickmamba.patterns import Signal
# data
from buttleofx.data import ButtleDataSingleton


class NodeManager(QtCore.QObject):
    """
        This class manages actions about nodes.
    """

    def __init__(self):
        super(NodeManager, self).__init__()

        self.undoRedoChanged = Signal()

    ############### EVENTS FROM QML ###############

    @QtCore.Slot(str, int, int)
    def creationNode(self, nodeType, x, y):
        """
            Create a node.
        """
        buttleData = ButtleDataSingleton().get()
        buttleData.getGraph().createNode(nodeType, x, y)

        # update undo/redo display
        self.undoRedoChanged()

    @QtCore.Slot()
    def destructionNodes(self):
        """
            Delete the current node(s).
        """
        buttleData = ButtleDataSingleton().get()

        # if the params of the current node deleted are display
        if buttleData.getCurrentParamNodeName() in buttleData.getCurrentSelectedNodeNames():
            buttleData.setCurrentParamNodeName(None)

        # if the viewer of the current node deleted is display
        if buttleData.getCurrentViewerNodeName() in buttleData.getCurrentSelectedNodeNames():
            buttleData.setCurrentViewerNodeName(None)
        # if the viewer display a node affected by the destruction
        if buttleData.getCurrentViewerNodeName() in buttleData._mapNodeNameToComputedImage:
            buttleData.setCurrentViewerNodeName(None)

        # if at least one node in the graph
        if len(buttleData.getGraphWrapper().getNodeWrappers()) > 0 and len(buttleData.getGraph().getNodes()) > 0:
            # if a node is selected
            if buttleData.getCurrentSelectedNodeNames() != []:
                buttleData.getGraph().deleteNodes([nodeWrapper.getNode() for nodeWrapper in buttleData.getCurrentSelectedNodeWrappers()])
                buttleData.clearCurrentSelectedNodeNames()

        # emit signals
        buttleData.currentParamNodeChanged.emit()
        buttleData.currentViewerNodeChanged.emit()
        buttleData.currentSelectedNodesChanged.emit()

        # update undo/redo display
        self.undoRedoChanged()

    @QtCore.Slot()
    def cutNode(self):
        """
            Cut the current node(s).
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

    @QtCore.Slot()
    def copyNode(self):
        """
            Copy the current node(s).
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
                buttleData.getCurrentCopiedNodesInfo()[node.getName()] = copyNode
                # Emit the change for the toolbar
                buttleData.pastePossibilityChanged.emit()

    @QtCore.Slot()
    def pasteNode(self):
        """
            Past the current node(s).
        """
        buttleData = ButtleDataSingleton().get()
        # If nodes have been copied previously
        if buttleData.getCurrentCopiedNodesInfo():
            # Create a copy for each node copied
            for node in buttleData.getCurrentCopiedNodesInfo():
                buttleData.getGraph().createNode(buttleData.getCurrentCopiedNodesInfo()[node]["nodeType"], 20, 20)
                newNode = buttleData.getGraph().getNodes()[-1]
                newNode.setColor(buttleData.getCurrentCopiedNodesInfo()[node]["color"])
                newNode.setNameUser(buttleData.getCurrentCopiedNodesInfo()[node]["nameUser"] + buttleData.getCurrentCopiedNodesInfo()[node]["mode"])
                newNode.getTuttleNode().getParamSet().copyParamsValues(buttleData.getCurrentCopiedNodesInfo()[node]["params"])

        # update undo/redo display
        self.undoRedoChanged()

    @QtCore.Slot()
    def duplicationNode(self):
        """
            Duplicate the current node(s).
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

        # update undo/redo display
        self.undoRedoChanged()

    @QtCore.Slot(str, int, int)
    def dropReaderNode(self, url, x, y):
        """
            Drop an image or a video on the graph : create a reader node.
        """
        buttleData = ButtleDataSingleton().get()
        buttleData.getGraph().createReaderNode(url, x, y)

        # update undo/redo display
        self.undoRedoChanged()

    @QtCore.Slot(str, int, int)
    def nodeMoved(self, nodeName, x, y):
        """
            This fonction push a cmdMoved in the CommandManager.
        """
        buttleData = ButtleDataSingleton().get()
        buttleData.getGraph().nodeMoved(nodeName, x, y)

        # update undo/redo display
        self.undoRedoChanged()

    @QtCore.Slot(str, int, int)
    def nodeIsMoving(self, nodeName, x, y):
        """
            This fonction update the position of the connections.
        """
        buttleData = ButtleDataSingleton().get()
        node = buttleData.getGraph().getNode(nodeName)
        node.setCoord(x, y)
        buttleData.getGraph().connectionsCoordChanged(node)
