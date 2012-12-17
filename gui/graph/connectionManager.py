from PySide import QtCore
from QuickMamba.qobjectlistmodel import QObjectListModel
from connection import Connection
from connectionWrapper import ConnectionWrapper
from idClip import IdClip


class ConnectionManager(QtCore.QObject):

    """
        Class ConnectionManager
    """

    def __init__(self):
        super(ConnectionManager, self).__init__()

        self._coreConnections = []
        self._connectionWrappers = QObjectListModel(self)
        self._connectionsItem = None

        self._tmpClipIn = None
        self._tmpClipOut = None

    def getConnections(self):
        """
            Return the connectionWrapper ListModel
        """
        return self._connectionWrappers

    def getTmpClipIn(self):
        """
            Return the future first connected input clip when a connection is beeing created.
            It correspounds of the input clip which was beeing clicked and not connected for the moment.
        """
        return self._tmpClipIn

    def setTmpClipIn(self, tmpClip):
        """
            Set the temporary clipIn with an IdClip
        """
        self._tmpClipIn = tmpClip

    def getTmpClipOut(self):
        """
            Return the future first connected input clip when a connection is beeing created.
            It correspounds of the input clip which was beeing clicked and not connected for the moment.
        """
        return self._tmpClipOut

    def setTmpClipOut(self, tmpClip):
        """
            Set the temporary clipIn with an IdClip
        """
        self._tmpClipOut = tmpClip

    @QtCore.Slot(str, str)
    def addConnection(self, clipOut, clipIn):
        """
            Add a connection between the 2 nodes.
        """
        self._coreConnections.append(Connection(clipOut, clipIn))
        self._connectionWrappers.append(ConnectionWrapper(clipOut, clipIn))

        print "List of connections :"
        for con in self._coreConnections:
            con.__str__()

    @QtCore.Slot(str, str)
    def inputPressed(self, node, clip):
        idClip = IdClip(node, clip)
        self._tmpClipIn = idClip
        print "Add tmpNodeIn: " + node + " " + clip

    @QtCore.Slot(str, str)
    def inputReleased(self, node, clip):
        #if there is a tmpNodeOut we can connect the nodes
        if (self._tmpClipOut != None and self._tmpClipOut._node != node):
            idClip = IdClip(node, clip)
            self.addConnection(self._tmpClipOut, idClip)
            self._tmpClipIn = None
            self._tmpClipOut = None

    @QtCore.Slot(str, str)
    def outputPressed(self, node, clip):
        idClip = IdClip(node, clip)
        self._tmpClipOut = idClip
        print "Add tmpNodeOut: " + node + " " + clip

    @QtCore.Slot(str, str)
    def outputReleased(self, node, clip):
        #if there is a tmpClipOut we can connect the nodes
        if (self._tmpClipIn != None and self._tmpClipIn._node != node):
            idClip = IdClip(node, clip)
            self.addConnection(idClip, self._tmpClipIn)
            self._tmpClipIn = None
            self._tmpClipOut = None

    #connectionsChanged = QtCore.Signal()
    #tmpNodeChanged = QtCore.Signal()
    #connections = QtCore.Property("QVariant", getConnections, notify=connectionsChanged)
    #tmpNode = QtCore.Property(unicode, getTmpNode, setTmpNode, notify=tmpNodeChanged)
