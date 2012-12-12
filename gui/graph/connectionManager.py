from PySide import QtCore
from QuickMamba.qobjectlistmodel import QObjectListModel
from connection import Connection
from connectionWrapper import ConnectionWrapper


class ConnectionManager(QtCore.QObject):

    """
        Class ConnectionManager
    """

    def __init__(self):
        super(ConnectionManager, self).__init__()

        self._coreConnections = []
        self._connectionWrappers = QObjectListModel(self)
        self._connectionsItem = None

        self._tmpNodeIn = None
        self._tmpNodeOut = None

    def getConnections(self):
        """
            Return the connectionWrapper ListModel
        """
        return self._connectionWrappers

    def getTmpNode(self):
        """
            Return the future first connected node when a connection is beeing created.
            It correspounds of the node which was beeing clicked and not connected for the moment.
        """
        return self._tmpNode

    def setTmpNode(self, tmpNode):
        """
            Set the temporary node.
        """
        self._tmpNode = tmpNode

    @QtCore.Slot(str, str)
    def addConnection(self, nodeOut, nodeIn):
        """
            Add a connection between the 2 nodes.
        """
        self._coreConnections.append(Connection(nodeOut, nodeIn))
        self._connectionWrappers.append(ConnectionWrapper(nodeOut, nodeIn))

        print "List of connections :"
        for con in self._coreConnections:
            con.__str__()

    @QtCore.Slot(str)
    def inputClicked(self, node):
        #if there isn't any tmpNodeOut to be connected, we update the tmpNodeIn
        if (self._tmpNodeOut == None or self._tmpNodeOut == node):
            self._tmpNodeIn = node
            print "Add tmpNodeIn: " + node
        # else we can connect the nodes
        else:
            self.addConnection(self._tmpNodeOut, node)
            self._tmpNodeIn = None
            self._tmpNodeOut = None

    @QtCore.Slot(str)
    def outputClicked(self, node):
        #if there isn't any tmpNodeIn to be connected, we update the tmpNodeOut
        if (self._tmpNodeIn == None or self._tmpNodeIn == node):
            self._tmpNodeOut = node
            print "Add tmpNodeOut: " + node
        # else we can connect the nodes
        else:
            self.addConnection(node, self._tmpNodeIn)
            self._tmpNodeIn = None
            self._tmpNodeOut = None

    #connectionsChanged = QtCore.Signal()
    #tmpNodeChanged = QtCore.Signal()
    #connections = QtCore.Property("QVariant", getConnections, notify=connectionsChanged)
    #tmpNode = QtCore.Property(unicode, getTmpNode, setTmpNode, notify=tmpNodeChanged)
