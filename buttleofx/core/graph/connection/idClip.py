class IdClip:
    """
        Class usefull to identify a clip with :
        - the graph
        - the node name
        - the clipName
        - the clip number
    """

    def __init__(self, nodeName, clipName, clipNumber, coord):
        
        #self._graph = graph
        self._nodeName = nodeName
        self._clipName = clipName
        self._clipNumber = clipNumber

        self._coord = coord

    def getNodeName(self):
        return self._nodeName

    def getPort(self):
        return self._clipName

    def getClipNumber(self):
        return self._clipNumber

    def getCoord(self):
        return self._coord

    def setNodeName(self, nodeName):
        self._nodeName = nodeName

    def setPort(self, clipName):
        self._clipName = clipName

    def setClipNumber(self, clipNumber):
        self._clipNumber = clipNumber

    def setCoord(self, coord):
        self._coord = coord

    def setXCoord(self, xCoord):
        self._coord[0] = xCoord

    def setYCoord(self, yCoord):
        self._coord[1] = yCoord

    def __eq__(self, otherClip):
        """
            Overloads the operator ==
        """
        return (self._nodeName == otherClip._nodeName and self._clipName == otherClip._clipName and self._clipNumber == otherClip._clipNumber)
