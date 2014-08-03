from buttleofx.core.undo_redo.manageTools import UndoableCommand


class CmdDeleteNodes(UndoableCommand):
    """
        Command that deletes a node.
        Attributes :
        - graphTarget : the graph in which the node will be deleted.
        - nodes : we save the node's data because we will need it for the redo
        - connections : list of the connections of the node, based on all the connections.
                        We just keep the connections concerning our node.
    """

    def __init__(self, graphTarget, nodes):
        self._graphTarget = graphTarget
        # Keep tuttle nodes
        self._nodes = nodes
        # Keep tuttle connection (no duplicate connection)
        self._connections = [connection for connection in self._graphTarget.getConnections() if
                             (self._graphTarget.getNode(connection.getClipOut().getNodeName()) in nodes or
                              self._graphTarget.getNode(connection.getClipIn().getNodeName()) in nodes)]

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getLabel(self):
        tmp = "Delete nodes"

        for n in self._nodes:
            tmp += " '" + n.getName() + "' "
        return tmp

    # ## Others ## #

    def doCmd(self):
        """
            Deletes a node.
        """
        for node in self._nodes:
            # Delete the tuttle connections
            self._graphTarget.getGraphTuttle().unconnect(node.getTuttleNode())
            # Delete the buttle connections
            self._graphTarget.deleteNodeConnections(node.getName())
            # Disconnect each param of the node
            for param in node.getParams():
                if param.paramChanged is not None:
                    # Warn the node that one of his param just changed
                    param.paramChanged.disconnect(node.emitNodeContentChanged)
            # Delete the node
            self._graphTarget.getNodes().remove(node)

        # Emit signal
        self._graphTarget.nodesChanged()
        self._graphTarget.connectionsChanged()

    def redoCmd(self):
        """
            Redoes the suppression of the node.
            Just calls doCmd() function.
        """
        self.doCmd()

    def undoCmd(self):
        """
            Undoes the suppression of the node <=> recreate the node.
        """
        for node in self._nodes:
            # We recreate the node
            self._graphTarget.getNodes().append(node)
            # Connect each param to the node
            for param in node.getParams():
                if param.paramChanged is not None:
                    # Warn the node that one of his param just changed
                    param.paramChanged.connect(node.emitNodeContentChanged)

        # Emit signal
        self._graphTarget.nodesChanged()

        # We recreate all the connections
        for connection in self._connections:
            tuttleNodeSource = self._graphTarget.getNode(connection.getClipOut().getNodeName()).getTuttleNode()
            tuttleNodeOutput = self._graphTarget.getNode(connection.getClipIn().getNodeName()).getTuttleNode()
            tuttleConnection = self._graphTarget.getGraphTuttle().connect(tuttleNodeSource, tuttleNodeOutput)
            connection.setTuttleConnection(tuttleConnection)
            self._graphTarget.getConnections().append(connection)

        # Emit signal
        self._graphTarget.connectionsChanged()
