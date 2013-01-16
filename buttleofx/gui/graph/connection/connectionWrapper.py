from PySide import QtCore


class ConnectionWrapper(QtCore.QObject):

    """
        Class ConnectionWrapper
    """

    def __init__(self, connection):
        super(ConnectionWrapper, self).__init__()
        self._connection = connection
        self._connection.changed.connect(self.emitChanged)

    @QtCore.Signal
    def changed(self):
        pass

    # invokable
    # @QtCore.Slot()

    def emitChanged(self):
        print "ConnectionWrapper : emitChanged"
        self.changed.emit()

    def getClipOutPosX(self):
        return self._connection._clipOut._coord[0]

    def getClipOutPosY(self):
        return self._connection._clipOut._coord[1]

    def getClipInPosX(self):
        return self._connection._clipIn._coord[0]

    def getClipInPosY(self):
        return self._connection._clipIn._coord[1]

    def setClipOutPosX(self, posX):
        self._connection._clipOut._coord[0] = posX

    def setClipOutPosY(self, posY):
        self._connection._clipOut._coord[1] = posY

    def setClipInPosX(self, posX):
        self._connection._clipIn._coord[0] = posX

    def setClipInPosY(self, posY):
        self._connection._clipIn._coord[1] = posY

    clipOutPosX = QtCore.Property(int, getClipOutPosX, getClipOutPosX, notify=changed)
    clipOutPosY = QtCore.Property(int, getClipOutPosY, setClipOutPosX, notify=changed)
    clipInPosX = QtCore.Property(int, getClipInPosX, getClipInPosX, notify=changed)
    clipInPosY = QtCore.Property(int, getClipInPosY, setClipInPosX, notify=changed)

    def __str__(self):
        print 'Connection between the clip "%s (%s %d)" and the clip "%s (%s %d)' % (self._connection._clipOut._nodeName, self._connection._clipOut._port, self._connection._clipOut._clipNumber, self._connection._clipIn._nodeName, self._connection._clipIn._port, self._connection._clipIn._clipNumber)
