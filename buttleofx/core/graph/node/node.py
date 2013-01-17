from quickmamba.patterns import Signal
from PySide import QtGui
# paramEditor
from buttleofx.gui.paramEditor.params import ParamInt
from buttleofx.gui.paramEditor.params import ParamString

nodeDescriptors = {
    "Blur": {
        "color": (58, 174, 206),
        "nbInput": 1,
        "url": "../img/brazil.jpg",
        "params": [
            ParamString(defaultValue="node.getName()", stringType="Name"),
            ParamString(defaultValue="node.getType()", stringType="Type"),
            ParamInt(defaultValue="node.getCoord()[0]", minimum=0, maximum=1000, text="Coord x"),
            ParamInt(defaultValue="node.getCoord()[1]", minimum=0, maximum=1000, text="Coord y"),
            ParamInt(defaultValue="node.getColor().red()", minimum=0, maximum=255, text="Color red"),
            ParamInt(defaultValue="node.getColor().green()", minimum=0, maximum=255, text="Color green"),
            ParamInt(defaultValue="node.getColor().blue()", minimum=0, maximum=255, text="Color blue"),
            ParamInt(defaultValue="node.getNbInput()", minimum=1, maximum=15, text="Nb input"),
            ParamString(defaultValue="node.getImage()", stringType="Image file"),
        ],
    },
    "Gamma": {
        "color": (221, 54, 138),
        "nbInput": 2,
        "url": "../img/brazil2.jpg",
        "params": [
            ParamString(defaultValue="node.getName()", stringType="Name"),
            ParamString(defaultValue="node.getType()", stringType="Type"),
            ParamInt(defaultValue="node.getCoord()[0]", minimum=0, maximum=1000, text="Coord x"),
            ParamInt(defaultValue="node.getCoord()[1]", minimum=0, maximum=1000, text="Coord y"),
            ParamInt(defaultValue="node.getNbInput()", minimum=1, maximum=15, text="Nb input"),
            ParamString(defaultValue="node.getImage()", stringType="Image file"),
        ],
    },
    "Invert": {
        "color": (90, 205, 45),
        "nbInput": 3,
        "url": "../img/brazil3.jpg",
        "params": [
            ParamString(defaultValue="node.getName()", stringType="Name"),
            ParamString(defaultValue="node.getType()", stringType="Type"),
            ParamInt(defaultValue="node.getColor().red()", minimum=0, maximum=255, text="Color red"),
            ParamInt(defaultValue="node.getColor().green()", minimum=0, maximum=255, text="Color green"),
            ParamInt(defaultValue="node.getColor().blue()", minimum=0, maximum=255, text="Color blue"),
            ParamInt(defaultValue="node.getNbInput()", minimum=1, maximum=15, text="Nb input"),
            ParamString(defaultValue="node.getImage()", stringType="Image file"),
        ],
    }
}

defaultNodeDesc = {
    "color": (187, 187, 187),
    "nbInput": 1,
    "url": "../img/uglycorn.jpg",
    "params": [
        ParamString(defaultValue="node.getName()", stringType="Name"),
        ParamString(defaultValue="node.getType()", stringType="Type"),
    ],
}

class Node(object):
    """
        Class Node defined by:
        - _name
        - _type
        - _coord
        - _color
        - _nbInput
        - _image

        Signals :
        - nameChanged : a signal emited to the wrapper layer
        - typeChanged : a signal emited to the wrapper layer
        - xChanged : a signal emited to the wrapper layer
        - yChanged : a signal emited to the wrapper layer
        - colorChanged : a signal emited to the wrapper layer
        - nbInputChanged : a signal emited to the wrapper layer
        - imageChanged : a signal emited to the wrapper layer

        Creates a python object Node.
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
        self._params = nodeDesc["params"]
        # ###

        self.NodeNameChanged = Signal()
        self.NodeTypeChanged = Signal()
        self.NodeCoordChanged = Signal()
        self.NodeColorChanged = Signal()
        self.NodeNbInputChanged = Signal()
        self.NodeImageChanged = Signal()

    def __str__(self):
        return 'Node "%s"' % (self._name)

    ######## getters ########

    def getName(self):
        return str(self._name)

    def getType(self):
        return str(self._type)

    def getCoord(self):
        return self._coord

    def getDesc(self):
        return self._desc

    def getColor(self):
        return QtGui.QColor(*self._color)

    def getNbInput(self):
        return self._nbInput

    def getImage(self):
        return self._image

    ######## setters ########

    def setName(self, name):
        self._name = name
        #self.NodeNameChanged()
        self.NodeNameChanged(name)

    def setType(self, nodeType):
        self._type = nodeType
        #self.NodeTypeChanged()
        self.NodeTypeChanged(nodeType)

    def setCoord(self, x, y):
        print "node.setCoord"
        self._coord = (x, y)
        print "Node Coords have changed : " + str(self._coord)
        self.NodeCoordChanged(x, y)

    def setColor(self, r, g, b):
        self._color = (r, g, b)
        #self.NodeColorChanged()
        self.NodeColorChanged(r, g, b)

    def setNbInput(self, nbInput):
        self._nbInput = nbInput
        #self.NodeNbInputChanged()
        self.NodeNbInputChanged(nbInput)

    def setImage(self, image):
        self._image = image
        #self.NodeImageChanged()
        self.NodeImageChanged(image)
