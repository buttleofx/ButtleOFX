import logging
from PySide import QtCore


class ConnectionWrapper(QtCore.QObject):
    """
        Class ConnectionWrapper defined by :
            - _connection : the buttle connection
    """

    def __init__(self, connection, view):
        super(ConnectionWrapper, self).__init__(view)

        self._connection = connection

        # the link between the connection and the connectionWarpper
        self._connection.connectionClipOutChanged.connect(self.emitConnectionClipOutChanged)
        self._connection.connectionClipInChanged.connect(self.emitConnectionClipInChanged)

        logging.info("Gui : ConnectionWrapper created")

    def __str__(self):
        return 'Connection between the clip "%s (%s %d)" and the clip "%s (%s %d)' % (self._connection._clipOut._nodeName, self._connection._clipOut._port, self._connection._clipOut._clipNumber, self._connection._clipIn._nodeName, self._connection._clipIn._port, self._connection._clipIn._clipNumber)

    def __del__(self):
        logging.info("Gui : ConnectionWrapper deleted")

    ######## getters ########

    def getConnection(self):
        return self._connection

    def getId(self):
        return self._connection.getId()

    def getClipOutPosX(self):
        """
            Returns the x position of the first clip of the connection (= the output clip). => x1
        """
        return self._connection.getClipOut().getCoord()[0]

    def getClipOutPosY(self):
        """
            Returns the y position of the first clip of the connection (= the output clip). => y1
        """
        return self._connection.getClipOut().getCoord()[1]

    def getClipInPosX(self):
        """
            Returns the x position of the second clip of the connection (= the input clip). => x2
        """
        return self._connection.getClipIn().getCoord()[0]

    def getClipInPosY(self):
        """
            Returns the y position of the second clip of the connection (= the input clip). => y2
        """
        return self._connection.getClipIn().getCoord()[1]

    ######## setters ########

    def setClipOutPosX(self, posX):
        """
            Sets the x position of the first clip of the connection (= the output clip). => x1
        """
        self._connection.getClipOut().setXCoord(posX)

    def setClipOutPosY(self, posY):
        """
            Sets the y position of the first clip of the connection (= the output clip). => y1
        """
        self._connection.getClipOut().setYCoord(posY)

    def setClipInPosX(self, posX):
        """
            Sets the x position of the second clip of the connection (= the input clip). => x2
        """
        self._connection.getClipIn().setXCoord(posX)

    def setClipInPosY(self, posY):
        """
            Sets the y position of the second clip of the connection (= the input clip). => y2
        """
        self._connection.getClipIn().setYCoord(posY)

    ################################################## LINK WRAPPER LAYER TO QML ##################################################

    connectionClipOutChanged = connectionClipInChanged = QtCore.Signal()

    def emitConnectionClipOutChanged(self):
        """
            Emits the signal connectionClipOutChanged.
        """
        self.connectionClipOutChanged.emit()

    def emitConnectionClipInChanged(self):
        """
            Emits the signal connectionClipInChanged.
        """
        self.connectionClipInChanged.emit()

    ################################################## DATA EXPOSED TO QML ##################################################

    clipOutPosX = QtCore.Property(int, getClipOutPosX, setClipOutPosX, notify=connectionClipOutChanged)  # x1
    clipOutPosY = QtCore.Property(int, getClipOutPosY, setClipOutPosX, notify=connectionClipOutChanged)  # y1

    clipInPosX = QtCore.Property(int, getClipInPosX, setClipInPosX, notify=connectionClipInChanged)  # x2
    clipInPosY = QtCore.Property(int, getClipInPosY, setClipInPosX, notify=connectionClipInChanged)  # y2
