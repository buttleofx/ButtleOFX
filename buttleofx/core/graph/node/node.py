from quickmamba.patterns import Signal
from PySide import QtGui
# paramEditor
from buttleofx.core.params import ParamInt
from buttleofx.core.params import ParamString
from buttleofx.core.params import ParamDouble2D
from buttleofx.core.params import ParamDouble3D

nodeDescriptors = {
    "Blur": {
        "color": (58, 174, 206),
        "nbInput": 1,
        "url": "../img/brazil.jpg",
        "params": [
            ParamString(defaultValue="Blur", stringType="Name"),
            ParamString(defaultValue="node.getType()", stringType="Type"),
            ParamDouble2D(defaultValue1="node.getCoord()[0]", defaultValue2="node.getCoord()[1]", minimum=0, maximum=1000, text="Coord"),
            ParamDouble3D(defaultValue1=58, defaultValue2=174, defaultValue3=206, minimum=0, maximum=255, text="Color"),
            ParamInt(defaultValue="node.getNbInput()", minimum=1, maximum=15, text="Nb input"),
            ParamString(defaultValue="node.getImage()", stringType="Image file"),
        ],
    },
    "Gamma": {
        "color": (221, 54, 138),
        "nbInput": 2,
        "url": "../img/brazil2.jpg",
        "params": [
            ParamString(defaultValue="Gamma", stringType="Name"),
            ParamString(defaultValue="node.getType()", stringType="Type"),
            ParamDouble3D(defaultValue1=221, defaultValue2=54, defaultValue3=138, minimum=0, maximum=255, text="Color"),
            ParamDouble2D(defaultValue1="node.getCoord()[0]", defaultValue2="node.getCoord()[1]", minimum=0, maximum=1000, text="Coord"),
            ParamInt(defaultValue="node.getNbInput()", minimum=1, maximum=15, text="Nb input"),
            ParamString(defaultValue="node.getImage()", stringType="Image file"),
        ],
    },
    "Invert": {
        "color": (90, 205, 45),
        "nbInput": 3,
        "url": "../img/brazil3.jpg",
        "params": [
            ParamString(defaultValue="Invert", stringType="Name"),
            ParamString(defaultValue="node.getType()", stringType="Type"),
            ParamDouble3D(defaultValue1=90, defaultValue2=205, defaultValue3=45, minimum=0, maximum=255, text="Color"),
            ParamDouble2D(defaultValue1="node.getCoord()[0]", defaultValue2="node.getCoord()[1]", minimum=0, maximum=1000, text="Coord"),
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
        Creates a python object Node.

        Class Node defined by:
        - _name
        - _type
        - _coord
        - _color
        - _nbInput
        - _image
        - _params

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
        # ###
        self._params = [
            ParamString(defaultValue=self.getName(), stringType="Name"),
            ParamString(defaultValue=self.getType(), stringType="Type"),
        ]

        if nodeType == "Blur":
            self._params.extend(
                [
                ParamDouble2D(defaultValue1=self.getCoord()[0], defaultValue2=self.getCoord()[1], minimum=0, maximum=1000, text="Coord"),
                ParamDouble3D(defaultValue1=58, defaultValue2=174, defaultValue3=206, minimum=0, maximum=255, text="Color"),
                ParamInt(defaultValue=self.getNbInput(), minimum=1, maximum=15, text="Nb input"),
                ParamString(defaultValue=self.getImage(), stringType="Image file")
                ]
            )
        elif nodeType == "Gamma":
            self._params.extend(
                [
                ParamDouble3D(defaultValue1=221, defaultValue2=54, defaultValue3=138, minimum=0, maximum=255, text="Color"),
                ParamDouble2D(defaultValue1=self.getCoord()[0], defaultValue2=self.getCoord()[1], minimum=0, maximum=1000, text="Coord"),
                ParamInt(defaultValue=self.getNbInput(), minimum=1, maximum=15, text="Nb input"),
                ParamString(defaultValue=self.getImage(), stringType="Image file")
                ]
            )
        elif nodeType == "Invert":
            self._params.extend(
                [
                ParamDouble3D(defaultValue1=90, defaultValue2=205, defaultValue3=45, minimum=0, maximum=255, text="Color"),
                ParamDouble2D(defaultValue1=self.getCoord()[0], defaultValue2=self.getCoord()[1], minimum=0, maximum=1000, text="Coord"),
                ParamInt(defaultValue=self.getNbInput(), minimum=1, maximum=15, text="Nb input"),
                ParamString(defaultValue=self.getImage(), stringType="Image file")
                ]
            )

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

    def getDesc(self):
        return self._desc

    def getColor(self):
        return QtGui.QColor(*self._color)

    def getNbInput(self):
        return self._nbInput

    def getImage(self):
        return self._image

    def getParams(self):
        return self._params

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
