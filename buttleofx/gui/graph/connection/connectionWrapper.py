from PySide import QtCore


class ConnectionWrapper(QtCore.QObject):

    """
        Class ConnectionWrapper
    """

    def __init__(self, clipOut, clipIn):
        super(ConnectionWrapper, self).__init__()
        self._clipOut = clipOut
        self._clipIn = clipIn

    @QtCore.Signal
    def changed(self):
        pass

    # invokable
    # @QtCore.Slot()

    def getClipOut(self):
        return self._clipOut

    def setClipOut(self, clipOut):
        self._clipOut = clipOut

    def getClipIn(self):
        return self._clipOut

    def setClipIn(self, clipIn):
        self._clipIn = clipIn

    #nodeOut = QtCore.Property(QtCore.QObject, getNodeOut, setNodeOut, notify=changed)
    #nodeIn = QtCore.Property(QtCore.QObject, getNodeIn, setNodeIn, notify=changed)
    clipOut = QtCore.Property(QtCore.QObject, getClipOut, setClipOut, notify=changed)
    clipIn = QtCore.Property(QtCore.QObject, getClipIn, setClipIn, notify=changed)

    def __str__(self):
        print 'Connection between the clip "%s (%s %d)" and the clip "%s (%s %d)' % (self._clipOut._node, self._clipOut._port, self._clipOut._clipNumber, self._clipIn._node, self._clipIn._port, self._clipIn._clipNumber)