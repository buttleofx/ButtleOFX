import logging
from quickmamba.patterns import Signal


class Connection(object):
    """
        Creates a python object Connection. This class is useful to identify a connection between 2 clips.

        Class Connection defined by:
        - data from tuttle :
            - _tuttleConnection : the corresponding tuttle connection
        - data from Buttle :
            - _id : a string which follow the pattern : "idClipOut_idClipIn"
            - _clipOut : the IdClip of the first clip
            - _clipIn : the IdClip of the second clip

        Signals :
            - connectionClipOutChanged : a signal emited when the clipOut od the connection changed
            - connectionClipInChanged : a signal emited when the clipIn od the connection changed
    """

    def __init__(self, clipOut, clipIn, tuttleConnection):
        object.__init__(self)

        # Tuttle connection
        self._tuttleConnection = tuttleConnection

        # Buttle data
        self._id = clipOut.getId() + " => " + clipIn.getId()
        self._clipOut = clipOut
        self._clipIn = clipIn

        # Signal
        self.connectionClipOutChanged = Signal()
        self.connectionClipInChanged = Signal()

        logging.info("Core : Connection created")

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getClipIn(self):
        return self._clipIn

    def getClipOut(self):
        return self._clipOut

    def getConcernedNodes(self):
        """
            Returns a list, which is the name of the the concerned nodes about this Connection.
        """
        nameOfConcernedNodes = []
        nameOfConcernedNodes.append(self._clipOut.getNodeName())
        nameOfConcernedNodes.append(self._clipIn.getNodeName())
        return nameOfConcernedNodes

    def getId(self):
        return self._id

    def getTuttleConnection(self):
        return self._tuttleConnection

    # ## Setters ## #

    def setClipOut(self, clipOut):
        self._clipOut = clipOut
        self.connectionClipOutChanged()

    def setClipIn(self, clipIn):
        self._clipIn = clipIn
        self.connectionClipInChanged()

    def setTuttleConnection(self, tuttleConnection):
        self._tuttleConnection = tuttleConnection

    # ## Others ## #

    def object_to_dict(self):
        """
            Convert the connection to a dictionary of his representation.
        """
        connection = {
            "id": self._id,
            "clipOut": self._clipOut.object_to_dict(),
            "clipIn": self._clipIn.object_to_dict()
        }
        return connection

    def __del__(self):
        logging.info("Core : Connection deleted")

    def __str__(self):
        str_list = []

        str_list.append("Connection : ")
        str_list.append(self._clipOut.__str__())
        str_list.append(" => ")
        str_list.append(self._clipIn.__str__())

        return "".join(str_list)
