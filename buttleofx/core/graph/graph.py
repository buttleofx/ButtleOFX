import os
import logging
from pyTuttle import tuttle
from quickmamba.patterns import Signal
from buttleofx.core.undo_redo.manageTools import globalCommandManager, GroupUndoableCommands
from buttleofx.core.undo_redo.commands.connection import CmdCreateConnection, CmdDeleteConnection
from buttleofx.core.undo_redo.commands.node import CmdCreateNode, CmdDeleteNodes, CmdCreateReaderNode, CmdSetCoord


class Graph(object):
    """
        Class Graph contains :
            - _graphTuttle : the tuttle graph

            - _nodes : list of buttle nodes (python objects, the core nodes)
            - _connections : list of buttle connections (python objects, the core connections)

            Signals :
                - nodesChanged : the signal emited when a node changed
                - connectionsChanged : the signal emited when a connection changed
                - connectionsCoordChanged : the signal emited when the coords of a connection changed (it's a QML trick)
    """

    def __init__(self):
        self._graphTuttle = tuttle.Graph()

        self._nodes = []
        self._connections = []

        # Signals
        self.nodesChanged = Signal()
        self.connectionsChanged = Signal()
        self.connectionsCoordChanged = Signal()

        logging.info("Core : Graph created")

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getConnections(self):
        """
            Returns the connection list.
        """
        return self._connections

    def getConnectionByClips(self, clipOut, clipIn):
        """
            Returns a connection, given the output clip and the input clip. (None if no connection found).
            The order of the clips is important.
        """
        for connection in self._connections:
            if connection.getClipOut() == clipOut and connection.getClipIn() == clipIn:
                return connection
        return None

    def getConnectionById(self, connectionId):
        """
            Returns the right connection object given its id (None if no connection found).
        """
        for connection in self._connections:
            if connection.getId() == connectionId:
                return connection
        return None

    def getGraphTuttle(self):
        """
            Returns the Tuttle's graph.
        """
        return self._graphTuttle

    def getNode(self, nodeName):
        """
            Returns the right node object given its name (None if no node found).
        """
        for node in self._nodes:
            if node.getName() == nodeName:
                return node
        return None

    def getNodes(self):
        """
            Returns the node List.
        """
        return self._nodes

    # ## Creators & Deleters ## #

    def createConnection(self, clipOut, clipIn):
        """
            Adds a connection in the connection list when a connection is created.
            Pushes a command in the CommandManager.
        """
        cmdCreateConnection = CmdCreateConnection(self, clipOut, clipIn)
        cmdManager = globalCommandManager
        return cmdManager.push(cmdCreateConnection)

    def createNode(self, nodeType, x=20, y=20):
        """
            Adds a node from the node list when a node is created.
        """
        cmdCreateNode = CmdCreateNode(self, nodeType, x, y)
        cmdManager = globalCommandManager
        return cmdManager.push(cmdCreateNode)

    def createReaderNode(self, url, x, y):
        """
            Creates a reader node when an image has been dropped in the graph.
        """
        (shortname, extension) = os.path.splitext(url)
        try:
            nodeType = tuttle.getBestReader(extension)
        except Exception:
            logging.debug("Unknown format. Can't create the reader node for extension '%s'." % extension)
            return

        # We create the node.
        # We can't use a group of commands because we need the tuttle node to set the value, and this tuttle node is
        # created in the function doCmd() of the cmdCreateNode. So we use a special command CmdCreateReaderNode which
        # creates a new node and set its value with the correct url.
        # See the definition of the class CmdCreateReaderNode.
        cmdCreateReaderNode = CmdCreateReaderNode(self, nodeType, x, y, url)
        cmdManager = globalCommandManager
        return cmdManager.push(cmdCreateReaderNode)

    def deleteConnection(self, connection):
        """
            Removes a connection.
            Pushes a command in the CommandManager.
        """
        cmdDeleteConnection = CmdDeleteConnection(self, connection)
        cmdManager = globalCommandManager
        cmdManager.push(cmdDeleteConnection)

    def deleteNodeConnections(self, nodeName):
        """
            Removes all the connections of the node.
        """
        # We have to rebuild the list of connections, based on the current values.
        self._connections = [connection for connection in self._connections if not
                             (connection.getClipOut().getNodeName() == nodeName or
                              connection.getClipIn().getNodeName() == nodeName)]

    def deleteNodes(self, nodes):
        """
            Removes a node in the node list when a node is deleted.
            Pushes a command in the CommandManager.
        """
        cmdDeleteNodes = CmdDeleteNodes(self, nodes)
        cmdManager = globalCommandManager
        cmdManager.push(cmdDeleteNodes)

    # ## Others ## #

    def contains(self, clip):
        """
            Returns True if the clip is already connected, else False.
        """
        for connection in self._connections:
            if (clip.getNodeName() == connection.getClipOut().getNodeName() and
                clip.getClipName() == connection.getClipOut().getClipName()) or (
                    clip.getNodeName() == connection.getClipIn().getNodeName() and
                    clip.getClipName() == connection.getClipIn().getClipName()):
                return True
        return False

    def nodesConnected(self, clipOut, clipIn):
        """
            Returns True if the nodes containing the clips are already connected (in the other direction).
        """
        for connection in self._connections:
            if (clipOut.getNodeName() == connection.getClipIn().getNodeName() and
                    clipIn.getNodeName() == connection.getClipOut().getNodeName()):
                return True
        return False

    def nodeMoved(self, nodeName, newX, newY):
        """
            This function pushes a cmdMoved in the globalCommandManager.
        """
        from buttleofx.data import globalButtleData
        node = globalButtleData.getCurrentGraph().getNode(nodeName)
        if not node:
            logging.debug("nodeMoved -- graph : %s" % globalButtleData.getCurrentGraph())

        # What is the value of the movement (compared to the old position)?
        oldX, oldY = node.getOldCoord()
        xMovement = newX - oldX
        yMovement = newY - oldY

        # If the node didn't really move, nothing is done
        if (xMovement, xMovement) == (0, 0):
            return

        commands = []

        # We create a GroupUndoableCommands of CmdSetCoord for each selected node
        for selectedNodeWrapper in globalButtleData.getCurrentSelectedNodeWrappers():
            # We get the needed informations for this node
            selectedNode = selectedNodeWrapper.getNode()
            selectedNodeName = selectedNode.getName()
            oldX, oldY = selectedNode.getOldCoord()

            # We set the new coordinates of the node (each selected node is doing the same movement)
            cmdMoved = CmdSetCoord(self, selectedNodeName, (oldX + xMovement, oldY + yMovement))

            commands.append(cmdMoved)

        # Then we push the group of commands
        globalCommandManager.push(GroupUndoableCommands(commands, "Move nodes"))

    def object_to_dict(self):
        """
            Convert the graph to a dictionary of his representation.
        """
        graph = {
            "nodes": [],
            "connections": [],
            "currentSelectedNodes": []
        }

        # Nodes
        for node in self.getNodes():
            graph["nodes"].append(node.object_to_dict())

        # Connections
        for con in self.getConnections():
            graph["connections"].append(con.object_to_dict())

        return graph

    def dict_to_object(self, graphData):
        """
            Set all elements of the graph (nodes, connections...), from a dictionary.
        """
        # Create the nodes
        for nodeData in graphData["nodes"]:
            node = self.createNode(nodeData["pluginIdentifier"])
            self.getGraphTuttle().renameNode(node.getTuttleNode(), nodeData["name"])
            node.dict_to_object(nodeData)

        # Create the connections
        from buttleofx.core.graph.connection import IdClip
        for connectionData in graphData["connections"]:
            clipIn_nodeName = connectionData["clipIn"]["nodeName"]
            clipIn_clipName = connectionData["clipIn"]["clipName"]
            clipIn = IdClip(clipIn_nodeName, clipIn_clipName)

            clipOut_nodeName = connectionData["clipOut"]["nodeName"]
            clipOut_clipName = connectionData["clipOut"]["clipName"]
            clipOut = IdClip(clipOut_nodeName, clipOut_clipName)

            self.createConnection(clipOut, clipIn)

    def __str__(self):
        """
            Displays on terminal some data.
            Usefull to debug the class.
        """
        str_list = []

        str_list.append("=== Graph Buttle === \n")
        str_list.append("---- all nodes ---- \n")

        for node in self._nodes:
            str_list.append(node.__str__())
            str_list.append("\n")

        str_list.append("---- all connections ----")
        for con in self._connections:
            str_list.append(con.__str__())
            str_list.append("\n")

        return "".join(str_list)
