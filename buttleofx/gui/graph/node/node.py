from buttleofx.gui.paramEditor.params import ParamInt


nodeDescriptors = {
    "Blur": {
        "color": (58, 174, 206),
        "nbInput": 1,
        "url": "../img/brazil.jpg",
        "params": [
            ParamInt(defaultValue=20, minimum=0, maximum=100, text="opacity"),
            ParamInt(defaultValue=10, minimum=0, maximum=500, text="intensity")
        ],
    },
    "Gamma": {
        "color": (221, 54, 138),
        "nbInput": 2,
        "url": "../img/brazil2.jpg",
        "params": [
            ParamInt(defaultValue=50, minimum=0, maximum=100, text="opacity"),
            ParamInt(defaultValue=20, minimum=0, maximum=500, text="intensity")
        ],
    },
    "Invert": {
        "color": (90, 205, 45),
        "nbInput": 3,
        "url": "../img/brazil3.jpg",
        "params": [
            ParamInt(defaultValue=80, minimum=0, maximum=100, text="opacity"),
            ParamInt(defaultValue=30, minimum=0, maximum=500, text="intensity")
        ]
    }
}


defaultNodeDesc = {
    "color": (187, 187, 187),
    "nbInput": 1,
    "url": "../img/uglycorn.jpg",
    "params": [
        ParamInt(defaultValue=100, minimum=0, maximum=100, text="opacity"),
        ParamInt(defaultValue=100, minimum=0, maximum=500, text="intensity")
    ]
}


from quickmamba.patterns import Signal
from PySide import QtGui


class Node(object):
    """
        Creates a python object Node.

        Class Node defined by:
        - _name
        - _type
        - _coord
        - _color
        - _nbInput
        - _image
        - _paramList

        Signal :
        - changed : a signal emited to the wrapper layer
    """

    def __init__(self, nodeName, nodeType, nodeCoord):
        self._name = nodeName
        self._type = nodeType
        self._coord = nodeCoord

        # soon from Tuttle
        nodeDesc = nodeDescriptors[nodeType] if nodeType in nodeDescriptors else defaultNodeDesc
        self._color = nodeDesc["color"]
        self._nbInput = nodeDesc["nbInput"]
        self._image = nodeDesc["url"]
        self._paramList = nodeDesc["params"]
        # ###

        self.changed = Signal()

    def __str__(self):
        return 'Node "%s"' % (self._name)

    ######## getters ########

    def getName(self):
        return str(self._name)

    def getType(self):
        return str(self._type)

    def getCoord(self):
        return self._coord

    def getColor(self):
        return QtGui.QColor(*self._color)

    def getNbInput(self):
        return self._nbInput

    def getImage(self):
        return self._image

    def getParamList(self):
        return self._paramList

    ######## setters ########

    def setName(self, name):
        self._name = name
        #self.NodeNameChanged()
        self.changed()

    def setType(self, nodeType):
        self._type = nodeType
        #self.NodeTypeChanged()
        self.changed()

    def setCoord(self, x, y):
        print "node.setCoord"
        self._coord = (x, y)
        print "Node Coords have changed : " + str(self._coord)
        self.changed()

    def setColor(self, r, g, b):
        self._color = (r, g, b)
        #self.NodeColorChanged()
        self.changed()

    def setNbInput(self, nbInput):
        self._nbInput = nbInput
        #self.NodeNbInputChanged()
        self.changed()

    def setImage(self, image):
        self._image = image
        #self.NodeImageChanged()
        self.changed()
