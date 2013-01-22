# Tuttle
from buttleofx.data import tuttleTools
# Quickmamba
from quickmamba.patterns import Signal
from PySide import QtGui
# paramEditor
from buttleofx.core.params import ParamInt, ParamInt2D, ParamInt3D, ParamString, ParamDouble, ParamDouble2D, ParamBoolean, ParamDouble3D, ParamChoice, ParamPushButton, ParamSlider

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
    "url": "../img/uglycorn.jpg",
}

mapTuttleParamToButtleParam = {
    "OfxParamTypeInteger": "ParamInt",
    "OfxParamTypeDouble": "ParamDouble",
    "OfxParamTypeBoolean": "ParamBoolean",
    "OfxParamTypeChoice": "ParamChoice",
    "OfxRGBA": "ParamRGBA",
    "OfxParamTypeRGB": "ParamRGB",
    "OfxParamTypeDouble2D": "ParamDouble2D",
    "OfxParamTypeInteger2D": "ParamInt2D",
    "OfxParamTypeDouble3D": "ParamDouble3D",
    "OfxParamTypeInteger3D": "ParamInt3D",
    "OfxParamTypeString": "ParamString",
    "OfxParamTypeCustom": "ParamCustom",
    "OfxParamTypeGroup": "ParamGroup",
    "OfxParamTypePage": "ParamPage",
    "OfxParamTypePushButton": "ParamPushButton"
}


class Node(object):
    """
        Creates a python object Node.

        Class Node defined by:
        - params from Buttle :
            - _name
            - _type
            - _coord
            - _oldCoord : when a node is being dragged, we need to remember its old coordinates for the undo/redo
            - _color
            - _nbInput
            - _image
        - params from Tuttle (depend on the node type) :
            - _params

        Signal :
        - changed : a signal emited to the wrapper layer
    """

    def __init__(self, nodeName, nodeType, nodeCoord, tuttleNode):
        self._name = nodeName
        self._nameUser = nodeName.strip('tuttle.')
        self._type = nodeType
        self._coord = nodeCoord
        self._oldCoord = nodeCoord
        self._tuttleNode = tuttleNode.asImageEffectNode()

        # soon from Tuttle
        nodeDesc = nodeDescriptors[nodeType] if nodeType in nodeDescriptors else defaultNodeDesc

        self._color = nodeDesc["color"]
        self._nbInput = nodeDesc["nbInput"]
        self._image = nodeDesc["url"]

        self._params = []

        # Filling the node's param list
        for param in range(self._tuttleNode.getNbParams()):

            paramElement = self._tuttleNode.getParam(param)
            paramType = mapTuttleParamToButtleParam[paramElement.getProperties().fetchProperty("OfxParamPropType").getStringValue(0)]

            if paramType == "ParamInt":
                defaultValue = paramElement.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)
                minValue = paramElement.getProperties().fetchProperty("OfxParamPropMin").getStringValue(0)
                maxValue = paramElement.getProperties().fetchProperty("OfxParamPropMax").getStringValue(0)
                label = paramElement.getProperties().fetchProperty("OfxPropName").getStringValue(0)
                self._params.append(ParamInt(defaultValue, minValue, maxValue, label))

            if paramType == "ParamDouble":
                defaultValue = paramElement.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)
                minValue = paramElement.getProperties().fetchProperty("OfxParamPropMin").getStringValue(0)
                maxValue = paramElement.getProperties().fetchProperty("OfxParamPropMax").getStringValue(0)
                label = paramElement.getProperties().fetchProperty("OfxPropName").getStringValue(0)
                self._params.append(ParamDouble(defaultValue, minValue, maxValue, label))

            if paramType == "ParamBoolean":
                defaultValue = paramElement.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)
                label = paramElement.getProperties().fetchProperty("OfxPropName").getStringValue(0)
                self._params.append(ParamBoolean(defaultValue, label))

            if paramType == "ParamChoice":
                defaultValue = paramElement.getProperties().fetchProperty("OfxParamPropChoiceOption").getStringValue(0)
                listValue = []
                for choice in range(paramElement.getProperties().fetchProperty("OfxParamPropChoiceOption").getDimension()):
                    listValue.append(paramElement.getProperties().fetchProperty("OfxParamPropChoiceOption").getStringValue(choice))
                label = paramElement.getProperties().fetchProperty("OfxPropName").getStringValue(0)
                self._params.append(ParamChoice(defaultValue, listValue, label))

            #if paramType == "ParamRGBA":

            #if paramType == "ParamRGB":

            if paramType == "ParamDouble2D":
                defaultValue1 = paramElement.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)
                defaultValue2 = paramElement.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(1)
                minValue = paramElement.getProperties().fetchProperty("OfxParamPropMin").getStringValue(0)
                maxValue = paramElement.getProperties().fetchProperty("OfxParamPropMax").getStringValue(0)
                label = paramElement.getProperties().fetchProperty("OfxPropName").getStringValue(0)
                self._params.append(ParamDouble2D(defaultValue1, defaultValue2, minValue, maxValue, label))

            if paramType == "ParamInt2D":
                defaultValue1 = paramElement.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)
                defaultValue2 = paramElement.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(1)
                minValue = paramElement.getProperties().fetchProperty("OfxParamPropMin").getStringValue(0)
                maxValue = paramElement.getProperties().fetchProperty("OfxParamPropMax").getStringValue(0)
                label = paramElement.getProperties().fetchProperty("OfxPropName").getStringValue(0)
                self._params.append(ParamInt2D(defaultValue1, defaultValue2, minValue, maxValue, label))

            if paramType == "ParamDouble3D":
                defaultValue1 = paramElement.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)
                defaultValue2 = paramElement.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(1)
                defaultValue3 = paramElement.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(2)
                minValue = paramElement.getProperties().fetchProperty("OfxParamPropMin").getStringValue(0)
                maxValue = paramElement.getProperties().fetchProperty("OfxParamPropMax").getStringValue(0)
                label = paramElement.getProperties().fetchProperty("OfxPropName").getStringValue(0)
                self._params.append(ParamDouble3D(defaultValue1, defaultValue2, defaultValue3, minValue, maxValue, label))

            # if paramType == "ParamInt3D":
            #     defaultValue1 = paramElement.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)
            #     defaultValue2 = paramElement.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(1)
            #     defaultValue3 = paramElement.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(2)
            #     minValue = paramElement.getProperties().fetchProperty("OfxParamPropMin").getStringValue(0)
            #     maxValue = paramElement.getProperties().fetchProperty("OfxParamPropMax").getStringValue(0)
            #     label = paramElement.getProperties().fetchProperty("OfxPropName").getStringValue(0)
            #     self._params.append(ParamInt3D(defaultValue1, defaultValue2, defaultValue3, minValue, maxValue, label))

            if paramType == "ParamString":
                defaultValue = paramElement.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)
                label = paramElement.getProperties().fetchProperty("OfxPropName").getStringValue(0)
                self._params.append(ParamString(defaultValue, label))

            # if paramType == "ParamPushButton":
            #     trigger = paramElement.getProperties().fetchProperty("OfxParamPropDefault").getStringValue(0)
            #     label = paramElement.getProperties().fetchProperty("OfxPropName").getStringValue(0)
            #     enabled = 
            #     self._params.append(ParamPushButton(trigger, label, enabled))

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
