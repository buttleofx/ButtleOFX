import logging
# Tuttle
from buttleofx.data import tuttleTools
# Quickmamba
from quickmamba.patterns import Signal
from PySide import QtGui
# paramEditor
from buttleofx.core.params import ParamInt, ParamInt2D, ParamInt3D, ParamString, ParamDouble, ParamDouble2D, ParamBoolean, ParamDouble3D, ParamChoice, ParamPushButton, ParamRGBA, ParamRGB, ParamGroup, ParamPage


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
    "OfxParamTypeGroup": ParamGroup,
    "OfxParamTypePage": ParamPage,
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
        - paramsChanged : a signal emited when a param had changed.
    """

    def __init__(self, nodeName, nodeType, nodeCoord, tuttleNode):
        self._tuttleNode = tuttleNode

        self._name = nodeName  # useful for us inside buttle (same id as tuttle)
        self._nameUser = nodeName.strip('tuttle.')  # the name visible for the user
        self._type = nodeType
        self._coord = nodeCoord
        self._oldCoord = nodeCoord
        self._color = (0, 178, 161)
        self._nbInput = self._tuttleNode.asImageEffectNode().getClipImageSet().getNbClips() - 1
        self._clips = [clip.getName() for clip in self._tuttleNode.asImageEffectNode().getClipImageSet().getClips()]
        self._params = []

        # Filling the node's param list
        for param in range(self._tuttleNode.asImageEffectNode().getNbParams()):

            tuttleParam = self._tuttleNode.asImageEffectNode().getParam(param)
            self._params.append(mapTuttleParamToButtleParam[tuttleParam.getProperties().fetchProperty("OfxParamPropType").getStringValue(0)](tuttleParam))

        # signals
        self.nameUserChanged = Signal()
        self.coordChanged = Signal()
        self.colorChanged = Signal()
        self.paramsChanged = Signal()

        logging.info("Core : Node created")

    def __str__(self):
        logging.info('Node ' + self.getName())

    def __del__(self):
        logging.info("Core : Node deleted")

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

    def getColor(self):
        return self._color

    def getNbInput(self):
        return self._nbInput

    def getClips(self):
        return self._clips

    # def getImage(self):
    #     return self._image

    def getParams(self):
        return self._params

    def getTuttleNode(self):
        return self._tuttleNode

    ######## setters ########

    def setName(self, name):
        self._name = name

    def setNameUser(self, nameUser):
        self._nameUser = nameUser
        self.nameUserChanged()

    def setType(self, nodeType):
        self._type = nodeType

    def setCoord(self, x, y):
        self._coord = (x, y)
        self.coordChanged()

    def setOldCoord(self, x, y):
        self._oldCoord = (x, y)
        #self.changed()

    def setColor(self, r, g, b):
        self._color = (r, g, b)
        self.colorChanged()

    def setNbInput(self, nbInput):
        self._nbInput = nbInput

    def setClips(self, clips):
        self._clips = clips

    def setParams(self):
        # self._params = []
        # # Filling the node's param list
        # for param in range(self._tuttleNode.asImageEffectNode().getNbParams()):

        #     tuttleParam = self._tuttleNode.asImageEffectNode().getParam(param)
        #     self._params.append(mapTuttleParamToButtleParam[tuttleParam.getProperties().fetchProperty("OfxParamPropType").getStringValue(0)](tuttleParam))

        self.paramsChanged()

    def setTuttleNode(self, tuttleNode):
        self._tuttleNode = tuttleNode
