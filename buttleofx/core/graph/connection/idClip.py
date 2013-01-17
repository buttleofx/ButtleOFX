class IdClip:
    """
        Class usefull to identify a clip with :
        - the graph
        - the node name
        - the port (input or output)
        - the clip number
    """

    def __init__(self, nodeName, port, clipNumber, coord):
        #self._graph = graph
        self._nodeName = nodeName
        self._port = port
        self._clipNumber = clipNumber

        self._coord = coord

    def getNodeName(self):
        return self._nodeName

    def getPort(self):
        return self._port

    def getClipNumber(self):
        return self._clipNumber

    def getCoord(self):
        return self._coord

    def setNodeName(self, nodeName):
        self._nodeName = nodeName

    def setPort(self, port):
        self._port = port

    def setClipNumber(self, clipNumber):
        self._clipNumber = clipNumber

    def setCoord(self, coord):
        self._coord = coord

    def __eq__(self, otherClip):
        """
            Overloads the operator ==
        """
        return (self._nodeName == otherClip._nodeName and self._port == otherClip._port and self._clipNumber == otherClip._clipNumber)
