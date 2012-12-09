
nodeDescriptors = {
    "Blur": {
        "color": (58, 174, 206),
        "nbInput": 1,
        "url": "img/brazil.jpg"
    },
    "Gamma": {
        "color": (221, 54, 138),
        "nbInput": 2,
        "url": "img/brazil2.jpg"
    },
    "Invert": {
        "color": (90, 205, 45),
        "nbInput": 3,
        "url": "img/brazil3.jpg"
    }
}

defaultNodeDesc = {
    "color": (187, 187, 187),
    "nbInput": 1,
    "url": "img/licorne.jpg"
}


class Node(object):

    """
        Class Node defined by:
        - name
        - coord : Node position
        - color : node color
        - nbInput : Number of inputs fot the node

        Creates a python object Node.
    """

    def __init__(self, nodeType, index, coord):
        super(Node, self).__init__()
        self._name = ("%s_%d") % (nodeType, index)

        nodeDesc = nodeDescriptors[nodeType] if nodeType in nodeDescriptors else defaultNodeDesc

        self._coord = coord

        self._color = nodeDesc["color"]
        self._nbInput = nodeDesc["nbInput"]
        self._url = nodeDesc["url"]

    def __str__(self):
        return 'Node "%s"' % (self._name)
