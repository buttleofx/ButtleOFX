from PySide import QtCore


class ConnectionWrapper(QtCore.QObject):

    """
        Class ConnectionWrapper
    """

    def __init__(self, nodeOut, nodeIn):
        super(ConnectionWrapper, self).__init__()
        self._nodeOut = nodeOut
        self._nodeIn = nodeIn

    @QtCore.Signal
    def changed(self):
        pass

    # invokable
    # @QtCore.Slot()

    def getNodeOut(self):
        return self._nodeOut

    def setNodeOut(self, nodeOut):
        self._nodeOut = nodeOut

    def getNodeIn(self):
        return self._nodeOut

    def setNodeIn(self, nodeIn):
        self._nodeIn = nodeIn

    #nodeOut = QtCore.Property(QtCore.QObject, getNodeOut, setNodeOut, notify=changed)
    #nodeIn = QtCore.Property(QtCore.QObject, getNodeIn, setNodeIn, notify=changed)
    nodeOut = QtCore.Property(unicode, getNodeOut, setNodeOut, notify=changed)
    nodeIn = QtCore.Property(unicode, getNodeIn, setNodeIn, notify=changed)
