import logging
from PySide import QtGui
# to parse
import json
# Tuttle
from buttleofx.data import tuttleTools
# Quickmamba
from quickmamba.patterns import Signal
# paramEditor
from buttleofx.core.params import ParamInt, ParamInt2D, ParamInt3D, ParamString, ParamDouble, ParamDouble2D, ParamBoolean, ParamDouble3D, ParamChoice, ParamPushButton, ParamRGBA, ParamRGB, ParamGroup, ParamPage
# event
from buttleofx.event import ButtleEventSingleton

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
            - data from tuttle :
                - _tuttleNode : the corresponding tuttle node
            - data from Buttle :
                - _name
                - _nameUser
                - _type
                - _coord
                - _oldCoord : when a node is being dragged, we need to remember its old coordinates for the undo/redo
                - _color
                - _nbInput
                - _image
                - _params : buttle params (based on the tuttle params)

        Signals :
            - nodeLookChanged : a signal emited when the apparence of the node changed (name, color...)
            - nodePositionChanged : a signal emited when the coordinates of the node changed (x, y)
            - nodeContentChanged : a signal emited when one of the params of the node changed
    """

    def __init__(self, nodeName, nodeType, nodeCoord, tuttleNode):    
        super(Node, self).__init__()

        # tuttle node
        self._tuttleNode = tuttleNode

        # buttle data
        self._name = nodeName  # useful for us inside buttle (same id as tuttle)
        self._nameUser = nodeName.strip('tuttle.')  # the name visible for the user
        self._type = nodeType
        self._coord = nodeCoord
        self._oldCoord = nodeCoord
        self._color = (0, 178, 161)
        self._nbInput = self._tuttleNode.asImageEffectNode().getClipImageSet().getNbClips() - 1
        self._clips = [clip.getName() for clip in self._tuttleNode.asImageEffectNode().getClipImageSet().getClips()]

        # buttle params
        self._params = []
        for param in range(self._tuttleNode.asImageEffectNode().getNbParams()):
            tuttleParam = self._tuttleNode.asImageEffectNode().getParam(param)
            self._params.append(mapTuttleParamToButtleParam[tuttleParam.getProperties().fetchProperty("OfxParamPropType").getStringValue(0)](tuttleParam))

        # signals
        self.nodeLookChanged = Signal()
        self.nodePositionChanged = Signal()
        self.nodeContentChanged = Signal()

        logging.info("Core : Node created")

    def __str__(self):
        return 'Node ' + self.getName()

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

    def getParams(self):
        return self._params

    def getTuttleNode(self):
        return self._tuttleNode

    def getPluginVersion(self):
        return self._tuttleNode.getVersionStr()

    ######## setters ########

    def setName(self, name):
        self._name = name

    def setNameUser(self, nameUser):
        self._nameUser = nameUser
        self.nodeLookChanged()

    def setCoord(self, x, y):
        self._coord = (x, y)
        self.nodePositionChanged()

    def setOldCoord(self, x, y):
        self._oldCoord = (x, y)

    def setColor(self, r, g, b):
        self._color = (r, g, b)
        self.nodeLookChanged()

    def setColor(self, color):
        self._color = color
        self.nodeLookChanged()

    def setClips(self, clips):
        self._clips = clips

    ######## emit signal ########

    def emitNodeContentChanged(self):
        """
            If necessary, call emitOneParamChangedSignal, to warn buttleEvent that a param just changed (to update the viewer)
            Also emit nodeContentChanged signal, to warn the node wrapper that a param just changed (for property si secret of other params for example !)
        """
        from buttleofx.data import ButtleDataSingleton
        buttleData = ButtleDataSingleton().get()
        if (self._name == buttleData.getCurrentViewerNodeName()):
            # to buttleEvent
            buttleEvent = ButtleEventSingleton().get()
            buttleEvent.emitOneParamChangedSignal()

        # to the node wrapper
        self.nodeContentChanged()

    ######## SAVE / LOAD ########

    def object_to_dict(self):
        """
            Convert the node to a dictionary of his representation.
        """
        node = {
            "name": self._name,
            "pluginIdentifier": self._type,
            "pluginVersion": self.getPluginVersion(),
            "uiParams": {
                "nameUser": self._nameUser,
                "coord": self._coord,
                "color": self._color
            },
            "params": []
        }
        for param in self.getParams():
            paramDict = param.object_to_dict()
            if paramDict != None:
                node["params"].append(paramDict)
        return node

    def dict_to_object(self, nodeData):
        """
            Set all values of the node, from a dictionary.
        """
        # uiParams
        self.setCoord(nodeData["uiParams"]["coord"][0], nodeData["uiParams"]["coord"][1])
        self.setColor(nodeData["uiParams"]["color"])
        self.setNameUser(nodeData["uiParams"]["nameUser"])

        # params
        for param in self.getParams():
            for paramData in nodeData["params"]:
                if param.getName() == paramData["name"]:
                    param.dict_to_object(paramData)