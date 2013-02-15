import logging
from PySide import QtCore


class ConnectionWrapper(QtCore.QObject):

    """
        Class ConnectionWrapper
    """

    def __init__(self, connection, view):
        super(ConnectionWrapper, self).__init__(view)
        self._connection = connection
        self._connection.changed.connect(self.emitChanged)

        logging.info("Gui : ConnectionWrapper created")

    def __str__(self):
        logging.info('Connection between the clip "%s (%s %d)" and the clip "%s (%s %d)' % (self._connection._clipOut._nodeName, self._connection._clipOut._port, self._connection._clipOut._clipNumber, self._connection._clipIn._nodeName, self._connection._clipIn._port, self._connection._clipIn._clipNumber))

    def __del__(self):
        logging.info("Gui : ConnectionWrapper deleted")

    @QtCore.Signal
    def changed(self):
        pass

    # invokable
    # @QtCore.Slot()

    def emitChanged(self):
        self.changed.emit()

    def getConnection(self):
        return self._connection

    def getId(self):
        return self._connection.getId()

    def getClipOutPosX(self):
        return self._connection.getClipOut().getCoord()[0]

    def getClipOutPosY(self):
        return self._connection.getClipOut().getCoord()[1]

    def getClipInPosX(self):
        return self._connection.getClipIn().getCoord()[0]

    def getClipInPosY(self):
        return self._connection.getClipIn().getCoord()[1]

    def setClipOutPosX(self, posX):
        self._connection.getClipOut().setXCoord(posX)

    def setClipOutPosY(self, posY):
        self._connection.getClipOut().setYCoord(posY)

    def setClipInPosX(self, posX):
        self._connection.getClipIn().setXCoord(posX)

    def setClipInPosY(self, posY):
        self._connection.getClipIn().setYCoord(posY)

    clipOutPosX = QtCore.Property(int, getClipOutPosX, getClipOutPosX, notify=changed)
    clipOutPosY = QtCore.Property(int, getClipOutPosY, setClipOutPosX, notify=changed)
    clipInPosX = QtCore.Property(int, getClipInPosX, getClipInPosX, notify=changed)
    clipInPosY = QtCore.Property(int, getClipInPosY, setClipInPosX, notify=changed)
