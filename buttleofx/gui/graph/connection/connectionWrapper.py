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

    def getClipOut(self):
        return self._connection._clipOut

    def getClipIn(self):
        return self._connection._clipOut

    def setClipOut(self, clipOut):
        self._connection._clipOut = clipOut
        self.changed()

    def setClipIn(self, clipIn):
        self._connection._clipIn = clipIn
        self.changed()

    clipOut = QtCore.Property(QtCore.QObject, getClipOut, setClipOut, notify=changed)
    clipIn = QtCore.Property(QtCore.QObject, getClipIn, setClipIn, notify=changed)

    def __str__(self):
        print 'Connection between the clip "%s (%s %d)" and the clip "%s (%s %d)' % (self._connection._clipOut._nodeName, self._connection._clipOut._port, self._connection._clipOut._clipNumber, self._connection._clipIn._nodeName, self._connection._clipIn._port, self._connection._clipIn._clipNumber)
