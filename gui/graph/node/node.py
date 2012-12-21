
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
    "url": "img/uglycorn.jpg"
}

from gui.graph.node.idNode import IdNode
from QuickMamba.quickmamba.patterns.signalEvent import Signal

class Node(object):

    """
        Class Node defined by:
        - _id
        - _name
        - _type
        - _coord
        - _color
        - _nbInput
        - _url
        - changed : the signal emited to the wrapper layer

        Creates a python object Node.
    """

    def __init__(self, nodeId, nodeName, nodeType, nodeCoord):
        # super(Node, self).__init__()
        self._id = nodeId
        self._name = ("%s_%d") % (nodeType, nodeId)
        self._type = nodeType
        self._coord = nodeCoord

        nodeDesc = nodeDescriptors[nodeType] if nodeType in nodeDescriptors else defaultNodeDesc

        self._color = nodeDesc["color"]
        self._nbInput = nodeDesc["nbInput"]
        self._image = nodeDesc["url"]
        
        self.idChanged = Signal()
        self.nameChanged = Signal()
        self.typeChanged = Signal()
        self.xChanged = Signal()
        self.yChanged = Signal()
        self.colorChanged = Signal()
        self.nbInputChanged = Signal()
        self.imageChanged = Signal()

    def __str__(self):
        return 'Node "%s"' % (self._name)

    def getId(self):
        return self._id

    def setId(self, idNode):
        self._id = idNode
        self.idChanged(idNode)

    def getName(self):
        return str(self._name)

    def setName(self, name):
        self._name = name
        self.nameChanged(name)

    def getType(self):
        return str(self._type)

    def setType(self, nodeType):
        self._type = nodeType
        self.tyepChanged(nodeType)

    def getCoord(self):
        return self._coord

    def setCoord(self, coord):
        self._coord = coord
        self.xChanged(coord)
        self.yChanged(coord)

    def getColor(self):
        return QtGui.QColor(*self._color)

    def setColor(self, r, g, b):
        self._color = (r, g, b)
        self.colorChanged(self._color)

    def getNbInput(self):
        return self._nbInput

    def setNbInput(self, nbInput):
        self._nbInput = nbInput
        self.nbInputChanged(nbInput)

    def getImage(self):
        return self._image

    def setImage(self, image):
        self._image = image
        self.imageChanged(image)