import logging

from quickmamba.patterns import Signal

from buttleofx.event import ButtleEventSingleton
from buttleofx.core.params import (ParamInt, ParamInt2D, ParamInt3D, ParamString, ParamDouble, ParamDouble2D,
                                   ParamBoolean, ParamDouble3D, ParamChoice, ParamPushButton, ParamRGBA, ParamRGB,
                                   ParamGroup, ParamPage)


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
    # "OfxParamTypeCustom": ParamCustom,
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

        # Tuttle node
        self._tuttleNode = tuttleNode

        # Buttle data
        self._name = nodeName  # Useful for us inside buttle (same id as tuttle)
        self._nameUser = nodeName.strip('tuttle.')  # The name visible for the user
        self._type = nodeType
        self._coord = nodeCoord
        self._oldCoord = nodeCoord
        self._color = (0, 178, 161)
        self._nbInput = self._tuttleNode.asImageEffectNode().getClipImageSet().getNbClips() - 1
        self._clipWrappers = [clip.getName() for clip in
                              self._tuttleNode.asImageEffectNode().getClipImageSet().getClips()]

        # Buttle params
        self._params = []
        for param in range(self._tuttleNode.asImageEffectNode().getNbParams()):
            tuttleParam = self._tuttleNode.asImageEffectNode().getParam(param)
            self._params.append(mapTuttleParamToButtleParam[
                tuttleParam.getProperties().fetchProperty("OfxParamPropType").getStringValueAt()](tuttleParam))

        # Signals
        self.nodeLookChanged = Signal()
        self.nodePositionChanged = Signal()
        self.nodeContentChanged = Signal()

        logging.info("Core : Node created")

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getClips(self):
        return self._clipWrappers

    def getColor(self):
        return self._color

    def getCoord(self):
        return self._coord

    def getName(self):
        return str(self._name)

    def getNameUser(self):
        return str(self._nameUser)

    def getNbInput(self):
        return self._nbInput

    def getOldCoord(self):
        return self._oldCoord

    def getParams(self):
        return self._params

    def getPluginContext(self):
        return self._tuttleNode.getProperties().getStringProperty("OfxImageEffectPropContext")

    def getPluginDescription(self):
        return self._tuttleNode.getProperties().getStringProperty("OfxPropPluginDescription")

    def getPluginGroup(self):
        return self._tuttleNode.getProperties().getStringProperty("OfxImageEffectPluginPropGrouping")

    def getPluginVersion(self):
        return self._tuttleNode.getVersionStr()

    def getType(self):
        return str(self._type)

    def getTuttleNode(self):
        return self._tuttleNode

    # ## Setters ## #

    def setClips(self, clips):
        self._clipWrappers = clips

    def setColor(self, color):
        self._color = color
        self.nodeLookChanged()

    def setColorRGB(self, r, g, b):
        self._color = (r, g, b)
        self.nodeLookChanged()

    def setCoord(self, x, y):
        self._coord = (x, y)
        self.nodePositionChanged()

    def setName(self, name):
        self._name = name

    def setNameUser(self, nameUser):
        self._nameUser = nameUser
        self.nodeLookChanged()

    def setOldCoord(self, x, y):
        self._oldCoord = (x, y)

    # ## Others ## #

    def object_to_dict(self):
        """
            Convert the node to a dictionary of its representation.
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
            if paramDict is not None:
                node["params"].append(paramDict)
        return node

    def dict_to_object(self, nodeData):
        """
            Set all values of the node, from a dictionary.
        """
        # uiParams
        self.setCoord(nodeData["uiParams"]["coord"][0], nodeData["uiParams"]["coord"][1])
        self.setOldCoord(nodeData["uiParams"]["coord"][0], nodeData["uiParams"]["coord"][1])
        self.setColor(nodeData["uiParams"]["color"])
        self.setNameUser(nodeData["uiParams"]["nameUser"])

        # Params
        for param in self.getParams():
            for paramData in nodeData["params"]:
                if param.getName() == paramData["name"]:
                    param.dict_to_object(paramData)

    def emitNodeContentChanged(self):
        """
            If necessary, call emitOneParamChangedSignal, to warn buttleEvent that a param just
            changed (to update the viewer). Also emit nodeContentChanged signal, to warn the node
            wrapper that a param just changed (for properties of other params for example!)
        """
        from buttleofx.data import ButtleDataSingleton
        buttleData = ButtleDataSingleton().get()

        if self._name == buttleData.getCurrentViewerNodeName():
            # To buttleEvent
            buttleEvent = ButtleEventSingleton().get()
            buttleEvent.emitOneParamChangedSignal()

        # To the node wrapper
        self.nodeContentChanged()

    def __str__(self):
        return 'Node ' + self.getName()

    def __del__(self):
        logging.info("Core : Node deleted")
