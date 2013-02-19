# quickmamba
from quickmamba.patterns import Singleton
# data
from buttleofx.data import ButtleDataSingleton


class NodeManager(Singleton):
    """
        This class manages actions about nodes.
    """

    def creationNode(self, nodeType, x, y):
        """
            Create a node.
        """
        buttleData = ButtleDataSingleton().get()
        buttleData.getGraph().createNode(nodeType, x, y)

    def destructionNode(self):
        """
            Delete the current node(s).
        """
        buttleData = ButtleDataSingleton().get()
        
        # if the params of the current node deleted are display
        if buttleData.getCurrentParamNodeName() == buttleData.getCurrentSelectedNodeName():
            buttleData.setCurrentParamNodeName(None)

        # if the viewer of the current node deleted is display
        if buttleData.getCurrentViewerNodeName() == buttleData.getCurrentSelectedNodeName():
            buttleData.setCurrentViewerNodeName(None)
        # if the viewer display a node affected by the destruction
        if buttleData.getCurrentViewerNodeName() in buttleData._mapNodeNameToComputedImage:
            buttleData.setCurrentViewerNodeName(None)

        # if at least one node in the graph
        if len(buttleData.getGraphWrapper().getNodeWrappers()) > 0 and len(buttleData.getGraph().getNodes()) > 0:
            # if a node is selected
            if buttleData.getCurrentSelectedNodeName() != None:
                buttleData.getGraph().deleteNode(buttleData.getCurrentSelectedNodeWrapper().getNode())
                buttleData.setCurrentSelectedNodeName(None)

        # emit signals
        buttleData.currentParamNodeChanged.emit()
        buttleData.currentViewerNodeChanged.emit()
        buttleData.currentSelectedNodeChanged.emit()

    def cutNode(self):
        """
            Cut the current node(s).
        """
        self.copyNode()
        buttleData = ButtleDataSingleton().get()
        if buttleData.getCurrentSelectedNodeWrapper() != None:
            buttleData.getCurrentCopiedNodeInfo().update({"mode": ""})
            self.destructionNode()
            if buttleData.getCurrentSelectedNodeName() == buttleData.getCurrentViewerNodeName():
                buttleData.setCurrentViewerNodeName(None)
            if buttleData.getCurrentSelectedNodeName() == buttleData.getCurrentParamNodeName():
                buttleData.setCurrentParamNodeName(None)

    def copyNode(self):
        """
            Copy the current node(s).
        """
        buttleData = ButtleDataSingleton().get()
        if buttleData.getCurrentSelectedNodeWrapper() != None:
            buttleData.getCurrentCopiedNodeInfo().update({"nodeType": buttleData.getCurrentSelectedNodeWrapper().getNode().getType()})
            buttleData.getCurrentCopiedNodeInfo().update({"nameUser": buttleData.getCurrentSelectedNodeWrapper().getNode().getNameUser()})
            buttleData.getCurrentCopiedNodeInfo().update({"color": buttleData.getCurrentSelectedNodeWrapper().getNode().getColor()})
            buttleData.getCurrentCopiedNodeInfo().update({"params": buttleData.getCurrentSelectedNodeWrapper().getNode().getTuttleNode().getParamSet()})
            buttleData.getCurrentCopiedNodeInfo().update({"mode": "_copy"})
            buttleData.pastePossibilityChanged.emit()

    def pasteNode(self):
        """
            Past the current node(s).
        """
        buttleData = ButtleDataSingleton().get()
        if buttleData.getCurrentCopiedNodeInfo():
            buttleData.getGraph().createNode(buttleData.getCurrentCopiedNodeInfo()["nodeType"], 20, 20)
            newNode = buttleData.getGraph().getNodes()[-1]
            newNode.setColor(buttleData.getCurrentCopiedNodeInfo()["color"][0], buttleData.getCurrentCopiedNodeInfo()["color"][1], buttleData.getCurrentCopiedNodeInfo()["color"][2])
            newNode.setNameUser(buttleData.getCurrentCopiedNodeInfo()["nameUser"] + buttleData.getCurrentCopiedNodeInfo()["mode"])
            newNode.getTuttleNode().getParamSet().copyParamsValues(buttleData.getCurrentCopiedNodeInfo()["params"])

    def duplicationNode(self):
        """
            Duplicate the current node(s).
        """
        buttleData = ButtleDataSingleton().get()
        if buttleData.getCurrentSelectedNodeWrapper() != None:
            # Create a node giving the current selected node's type, x and y
            nodeType = buttleData.getCurrentSelectedNodeWrapper().getNode().getType()
            coord = buttleData.getCurrentSelectedNodeWrapper().getNode().getCoord()
            buttleData.getGraph().createNode(nodeType, coord[0], coord[1])
            newNode = buttleData.getGraph().getNodes()[-1]

            # Get the current selected node's properties
            nameUser = buttleData.getCurrentSelectedNodeWrapper().getNameUser() + "_duplicate"
            oldCoord = buttleData.getCurrentSelectedNodeWrapper().getNode().getOldCoord()
            color = buttleData.getCurrentSelectedNodeWrapper().getNode().getColor()

            # Use the current selected node's properties to set the duplicated node's properties
            newNode.setNameUser(nameUser)
            newNode.setOldCoord(oldCoord[0], oldCoord[1])
            newNode.setColor(color[0], color[1], color[2])
            newNode.getTuttleNode().getParamSet().copyParamsValues(buttleData.getCurrentSelectedNodeWrapper().getNode().getTuttleNode().getParamSet())

    def dropReaderNode(self, url, x, y):
        """
            Drop an image or a video on the graph : create a reader node.
        """
        buttleData = ButtleDataSingleton().get()
        buttleData.getGraph().createReaderNode(url, x, y)

    def nodeMoved(self, nodeName, x, y):
        """
            This fonction push a cmdMoved in the CommandManager.
        """
        buttleData = ButtleDataSingleton().get()
        buttleData.getGraph().nodeMoved(nodeName, x, y)

    def nodeIsMoving(self, nodeName, x, y):
        """
            This fonction update the position of the connections.
        """
        buttleData = ButtleDataSingleton().get()
        buttleData.getGraph().getNode(nodeName).setCoord(x, y)
        buttleData.getGraph().connectionsCoordChanged()


        