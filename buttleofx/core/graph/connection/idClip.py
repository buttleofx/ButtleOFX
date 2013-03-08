class IdClip:
    """
        Class usefull to identify a clip with :
        - _id : the clipId
        - _nodeName : the node name
        - _clipName : the clipName
        - _clipNumber : the clip number
        - _coord : the clip's coords
    """

    def __init__(self, nodeName, clipName, clipNumber, coord):
        self._id = nodeName + clipName
        self._nodeName = nodeName
        self._clipName = clipName
        self._clipNumber = clipNumber
        self._coord = coord

    def __eq__(self, otherClip):
        """
            Overloads the operator ==
        """
        return (self._nodeName == otherClip._nodeName and self._clipName == otherClip._clipName and self._clipNumber == otherClip._clipNumber)

    ######## getters ########

    def getId(self):
        return self._id

    def getNodeName(self):
        return self._nodeName

    def getClipName(self):
        return self._clipName

    def getClipNumber(self):
        return self._clipNumber

    def getCoord(self):
        return self._coord

    ######## setters ########

    def setCoord(self, coord):
        self._coord = coord

    def setXCoord(self, xCoord):
        self._coord[0] = xCoord

    def setYCoord(self, yCoord):
        self._coord[1] = yCoord
