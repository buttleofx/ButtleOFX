from PySide import QtCore
from QuickMamba.qobjectlistmodel import QObjectListModel
from connexion import Connexion
from connexionWrapper import ConnexionWrapper


class ConnexionManager(QtCore.QObject):

    """
        Class ConnexionManager
    """

    def __init__(self):
        super(ConnexionManager, self).__init__()

        self._coreConnexions = []
        self._connexionWrappers = QObjectListModel(self)
        self._connexionsItem = None

        self._tmpNodeIn = None
        self._tmpNodeOut = None

    def getConnexions(self):
        """
            Return the connexionWrapper ListModel
        """
        return self._connexionWrappers

    def getTmpNode(self):
        """
            Return the future first connected node when a connexion is beeing created.
            It correspounds of the node which was beeing clicked and not connected for the moment.
        """
        return self._tmpNode

    def setTmpNode(self, tmpNode):
        """
            Set the temporary node.
        """
        self._tmpNode = tmpNode

    @QtCore.Slot(str, str)
    def addConnexion(self, nodeOut, nodeIn):
        """
            Add a connexion between the 2 nodes.
        """
        self._coreConnexions.append(Connexion(nodeOut, nodeIn))
        self._connexionWrappers.append(ConnexionWrapper(nodeOut, nodeIn))

        print "List of connexions :"
        for con in self._coreConnexions:
            con.__str__()

    @QtCore.Slot(str)
    def inputClicked(self, node):
        # if there isn't any temporary output node to be connected, we update the temporary input node
        if (self._tmpNodeOut == None):
            self._tmpNodeIn = node
            print "Add tmpNodeIn: " + node
        # else we can connect the nodes
        else:
            self.addConnexion(self._tmpNodeOut, node)
            self._tmpNodeIn = None
            self._tmpNodeOut = None

    @QtCore.Slot(str)
    def outputClicked(self, node):
        # if there isn't any temporary input node to be connected, we update the temporary output node
        if (self._tmpNodeIn == None):
            self._tmpNodeOut = node
            print "Add tmpNodeOut: " + node
        # else we can connect the nodes
        else:
            self.addConnexion(node, self._tmpNodeIn)
            self._tmpNodeIn = None
            self._tmpNodeOut = None

    #connexionsChanged = QtCore.Signal()
    #tmpNodeChanged = QtCore.Signal()
    #connexions = QtCore.Property("QVariant", getConnexions, notify=connexionsChanged)
    #tmpNode = QtCore.Property(unicode, getTmpNode, setTmpNode, notify=tmpNodeChanged)
