# Tuttle
from buttleofx.data import tuttleTools
# Quickmamba
from quickmamba.patterns import Signal
from PySide import QtGui
# paramEditor
from buttleofx.core.params import ParamInt, ParamInt2D, ParamInt3D, ParamString, ParamDouble, ParamDouble2D, ParamBoolean, ParamDouble3D, ParamChoice, ParamPushButton, ParamRGBA, ParamRGB

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
    "color": (0, 178, 161),
    "nbInput": 1,
    #"url": "../img/uglycorn.jpg",
    "url": "../img/brazil.jpg"
}

mapTuttleParamToButtleParam = {
    "OfxParamTypeInteger": ParamInt,
    "OfxParamTypeDouble": ParamDouble,
    "OfxParamTypeBoolean": ParamBoolean,
    "OfxParamTypeChoice": ParamChoice,
    "OfxParamTypeRGBA": ParamRGBA,
    "OfxParamTypeRGB": ParamRGB,
    "OfxParamTypeDouble2D": ParamDouble2D,
    "OfxParamTypeInteger2D": ParamInt2D,
    "OfxParamTypeDouble3D": ParamDouble3D,
    "OfxParamTypeInteger3D": ParamInt3D,
    "OfxParamTypeString": ParamString,
    #"OfxParamTypeCustom": ParamCustom,
    #"OfxParamTypeGroup": ParamGroup,
    #"OfxParamTypePage": ParamPage,
    "OfxParamTypePushButton": ParamPushButton
}


class Node(object):
    """
        Creates a python object Node.

        Class Node defined by:
        - params from Buttle :
            - _name
            - _nameUser
            - _type
            - _coord
            - _oldCoord : when a node is being dragged, we need to remember its old coordinates for the undo/redo
            - _color
            - _nbInput
            - _image
            - _params : params from Tuttle (depend on the node type)

        Signal :
        - changed : a signal emited to the wrapper layer
    """

    def __init__(self, nodeName, nodeType, nodeCoord, tuttleNode):
        self._tuttleNode = tuttleNode
        nodeDesc = nodeDescriptors[nodeType] if nodeType in nodeDescriptors else defaultNodeDesc

        self._name = nodeName # useful for us inside buttle (same id as tuttle)
        self._nameUser = nodeName.strip('tuttle.') # the name visible for the user
        self._type = nodeType
        self._coord = nodeCoord
        self._oldCoord = nodeCoord
        self._color = nodeDesc["color"]
        self._nbInput = nodeDesc["nbInput"]
        self._image = nodeDesc["url"]
        self._params = []

        # Filling the node's param list
        for param in range(self._tuttleNode.asImageEffectNode().getNbParams()):

            tuttleParam = self._tuttleNode.asImageEffectNode().getParam(param)
            self._params.append(mapTuttleParamToButtleParam[tuttleParam.getProperties().fetchProperty("OfxParamPropType").getStringValue(0)](tuttleParam))

        self.changed = Signal()

        print "Core : node created"

    def __str__(self):
        return 'Node "%s"' % (self._name)

    def __del__(self):
        print "Core : Node deleted"

    ######## getters ########

    def getName(self):
        return str(self._name)

    def getNameUser(self):
        return str(self._nameUser)

    def getType(self):
        return str(self._type)

    def getCoord(self):
        return self._coord

    def getOldCoord(self):
        return self._oldCoord

    def getDesc(self):
        return self._desc

    def getColor(self):
        return self._color

    def getNbInput(self):
        return self._nbInput

    def getImage(self):
        return self._image

    def getParams(self):
        return self._params

    def getTuttleNode(self):
        return self._tuttleNode

    ######## setters ########

    def setName(self, name):
        self._name = name
        self.changed()

    def setNameUser(self, nameUser):
        self._nameUser = nameUser
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

    def setParams(self, params):
        self._params = params
        self.changed()

    def setTuttleNode(self, tuttleNode):
        self._tuttleNode = tuttleNode
        self.changed()
