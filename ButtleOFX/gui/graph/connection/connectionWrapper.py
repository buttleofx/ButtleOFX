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
    clipOut = QtCore.Property(unicode, getClipOut, setClipOut, notify=changed)
    clipIn = QtCore.Property(unicode, getClipIn, setClipIn, notify=changed)
