import logging
from PyQt5 import QtCore


class ConnectionWrapper(QtCore.QObject):
    """
        Class ConnectionWrapper defined by :
            - _connection : the buttle connection
    """

    def __init__(self, connection, view):
        # print("ConnectionWrapper constructor")
        super(ConnectionWrapper, self).__init__(view)

        self._connection = connection

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

    def getOut_clipNodeName(self):
        return self._connection.getClipOut().getNodeName()
    
    def getOut_clipName(self):
        return self._connection.getClipOut().getClipName()
    
    def getIn_clipNodeName(self):
        return self._connection.getClipIn().getNodeName()
    
    def getIn_clipName(self):
        return self._connection.getClipIn().getClipName()

    ################################################## DATA EXPOSED TO QML ##################################################

    in_clipNodeName = QtCore.pyqtProperty(str, getIn_clipNodeName, constant=True)
    in_clipName = QtCore.pyqtProperty(str, getIn_clipName, constant=True)
    out_clipNodeName = QtCore.pyqtProperty(str, getOut_clipNodeName, constant=True)
    out_clipName = QtCore.pyqtProperty(str, getOut_clipName, constant=True)
