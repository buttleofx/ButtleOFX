class IdNode:
    """
        Class usefull to identify a node with the nodeName, the nodeType, and the nodeCoord (x, y).
    """

    def __init__(self, nodeName, nodeType, x, y):
        self._nodeName = nodeName
        self._nodeType = nodeType
        self._nodeXCoord = x
        self._nodeYCoord = y

    def __str__(self):
    	return "Id du noeud : " + str(self._nodeName) + " - " + str(self._nodeType) + " - " + str(self._nodeXCoord) + "," + str(self._nodeYCoord)