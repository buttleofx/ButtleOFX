# Tuttle
from buttleofx.data import tuttleTools
# Quickmamba
from quickmamba.patterns import Signal
from PySide import QtGui
# paramEditor
from buttleofx.core.params import ParamInt, ParamInt2D, ParamString, ParamDouble, ParamDouble2D, ParamBoolean, ParamDouble3D, ParamChoice3C, ParamPushButton

nodeDescriptors = {
    "Blur": {
        "color": (58, 174, 206),
        "nbInput": 1,
        "url": "../img/brazil.jpg",
    },
    "Gamma": {
        "color": (221, 54, 138),
        "nbInput": 2,
        "url": "../img/brazil2.jpg",
    },
    "Invert": {
        "color": (90, 205, 45),
        "nbInput": 3,
        "url": "../img/brazil3.jpg",
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
        - _oldCoord : when a node is being dragged, we need to remember its old coordinates for the undo/redo
        - _color
        - _nbInput
        - _image
        - _params

        Signal :
        - changed : a signal emited to the wrapper layer
    """

    #def __init__(self, nodeName, nodeType, nodeCoord, tuttleNode):
    def __init__(self, nodeName, nodeType, nodeCoord):
        self._name = nodeName
        self._type = nodeType
        self._coord = nodeCoord
        self._oldCoord = nodeCoord
        #self._tuttleNode = tuttleNode

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



        if nodeType == "tuttle.blur":
            self._params.extend(
                [
                ParamDouble2D(defaultValue1=0, defaultValue2=0, minimum=0, maximum=10, text="Size"),
                ParamDouble3D(defaultValue1=58, defaultValue2=174, defaultValue3=206, minimum=0, maximum=255, text="Color"),
                ParamChoice3C(defaultValue="Coco", text="Border"),
                ParamBoolean(defaultValue="false", text="Normalized kernel"),
                ParamDouble(defaultValue=0, minimum=0, maximum=0.01, text="Kernel Espilon"),
                ParamPushButton(label="Compute", trigger="testFunction", enabled=True),
                ]
            )

        elif nodeType == "tuttle.gamma":
            self._params.extend(
                [
                #Miss Choice - Global - RGBA
                ParamDouble(defaultValue=0, minimum=0.001, maximum=20, text="Master"),
                ParamDouble(defaultValue=0, minimum=0.001, maximum=20, text="Red"),
                ParamDouble(defaultValue=0, minimum=0.001, maximum=20, text="Green"),
                ParamDouble(defaultValue=0, minimum=0.001, maximum=20, text="Blue"),
                ParamDouble(defaultValue=0, minimum=0.001, maximum=20, text="Alpha"),
                ParamBoolean(defaultValue="false", text="Invert"),
                ParamInt(defaultValue=0, minimum=0, maximum=100, text="ParamInt"),
                ]
            )

        elif nodeType == "Invert":
            self._params.extend(
                [
                 ParamBoolean(defaultValue="false", text="Gray"),
                 ParamBoolean(defaultValue="false", text="Red"),
                 ParamBoolean(defaultValue="false", text="Green"),
                 ParamBoolean(defaultValue="false", text="Blue"),
                 ParamBoolean(defaultValue="false", text="Alpha"),
                 ParamInt2D(defaultValue1=0, defaultValue2=0, minimum=0, maximum=100, text="Int2D"),
                ]
            )

        self.changed = Signal()

        print "Core : node created"

    def __str__(self):
        return 'Node "%s"' % (self._name)

    def __del__(self):
        print "Core : Node deleted"

    ######## getters ########

    def getName(self):
        return str(self._name)

    def getType(self):
        return str(self._type)

    def getCoord(self):
        return self._coord

    def getOldCoord(self):
        return self._oldCoord

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
        self.changed()

    def setType(self, nodeType):
        self._type = nodeType
        self.changed()

    def setCoord(self, x, y):
        self._coord = (x, y)
        self.changed()

    def setOldCoord(self, x, y):
        self._oldCoord = (x, y)
        self.changed()

    def setColor(self, r, g, b):
        self._color = (r, g, b)
        self.changed()

    def setNbInput(self, nbInput):
        self._nbInput = nbInput
        self.changed()

    def setImage(self, image):
        self._image = image
        self.changed()
