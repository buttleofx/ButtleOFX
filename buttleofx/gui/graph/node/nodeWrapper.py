from PyQt5 import QtCore, QtGui
import logging
#quickmamba
from quickmamba.models import QObjectListModel
# wrappers
from buttleofx.gui.paramEditor.wrappers import ParamEditorWrapper
from buttleofx.gui.graph.connection import ClipWrapper


class NodeWrapper(QtCore.QObject):
    """
        Class NodeWrapper defined by :
            - _node : the buttle node (core)
            - _view : the view (necessary for all wrapper, to construct a QtCore.QObject)
            - _paramWrappers : the paramWrappers (it's a ParamEditorWrapper object)
            - _width, _heightEmptyNode , _clipSpacing, _clipSize, _inputSideMargin : data given to QML to have nodes with good looking
            - _fpsError, _frameError : potential errors that we need to displayed.
    """

    def __init__(self, node, view):
        # print("NodeWrapper constructor")
        
        super(NodeWrapper, self).__init__(view)

        self._node = node
        self._view = view

        # paramWrappers
        self._paramWrappers = ParamEditorWrapper(self._view, self._node.getParams())

        # potential errors
        self._fpsError = ""
        self._frameError = ""

        # link signals of the node and the corresponding node wrapper
        self._node.nodeLookChanged.connect(self.emitNodeLookChanged)
        self._node.nodePositionChanged.connect(self.emitNodePositionChanged)
        self._node.nodeContentChanged.connect(self.emitNodeContentChanged)
        
        self._clipWrappers = [ClipWrapper(clip, self.getName(), self._view) for clip in self._node.getClips()]
        
        self._srcClips = QObjectListModel(self)

        logging.info("Gui : NodeWrapper created")

    def __str__(self):
        return "Node Wrapper : " + self.getName()

    def __del__(self):
        logging.info("Gui : NodeWrapper deleted")

    ######## getters ########

    def getNode(self):
        return self._node

    def getName(self):
        return self._node.getName()

    def getNameUser(self):
        return self._node.getNameUser()

    def getType(self):
        return self._node.getType()

    def getPluginDescription(self):
        return self._node.getPluginDescription()

    def getCoord(self):
        return QtCore.QPointF(self._node.getCoord()[0], self._node.getCoord()[1])

    def getXCoord(self):
        return self._node.getCoord()[0]

    def getYCoord(self):
        return self._node.getCoord()[1]

    def getColor(self):
        return QtGui.QColor(*self._node.getColor())

    @QtCore.pyqtSlot(result=QtGui.QColor)
    def getDefaultColor(self):
        return QtGui.QColor(0, 178, 161)

    def getNbInput(self):
        return self._node.getNbInput()

    def getSrcClips(self):
        """
            Returns a QObjectListModel of ClipWrappers of the input clips of this node.
        """
        self._srcClips.setObjectList([clip for clip in self._clipWrappers if not clip.name == "Output"])
        return self._srcClips

    def getOutputClip(self):
        """
            Returns the ClipWrapper of the output clip of this node.
        """
        return next(clip for clip in self._clipWrappers if clip.name == "Output")

    @QtCore.pyqtSlot(str, result=QtCore.QObject)
    def getClip(self, name):
        """
            Returns the ClipWrapper of the output clip of this node.
        """
        return next(clip for clip in self._clipWrappers if clip.name == name)

    def getParams(self):
        return self._paramWrappers.getParamElts()

    #for video
    def getFPS(self):
        """
            Returns the FPS of this node.
        """
        #import which needs to be changed in the future
        from buttleofx.data import ButtleDataSingleton
        buttleData = ButtleDataSingleton().get()
        graph = buttleData.getGraph().getGraphTuttle()
        node = self._node.getTuttleNode().asImageEffectNode()
        try:
            self.setFpsError("")
            graph.setup()
        except Exception as e:
            logging.debug("can't get fps of the node" + self._node.getName())
            self.setFpsError(str(e))
            return 1
            raise
        framerate = node.getOutputFrameRate()
        #print("framerate: ", framerate)
        return framerate

    def getFpsError(self):
        return self._fpsError

    def setFpsError(self, nodeName):
        self._fpsError = nodeName

    def getNbFrames(self):
        """
            Returns the number of frames of this node.
        """
        #import which needs to be changed in the future
        from buttleofx.data import ButtleDataSingleton
        buttleData = ButtleDataSingleton().get()
        graph = buttleData.getGraph().getGraphTuttle()
        node = self._node.getTuttleNode().asImageEffectNode()
        try:
            self.setFrameError("")
            graph.setup()
        except Exception as e:
            logging.debug("can't get nbFrames of the node" + self._node.getName())
            self.setFrameError(str(e))
            return 0
            raise
        timeDomain = node.getTimeDomain() #getTimeDomain() returns first frame and last one
        nbFrames = timeDomain.max - timeDomain.min
        #not very elegant but allow to avoid a problem because an image returns a number of frames very high
        if nbFrames > 100000000 or nbFrames < 0:
            nbFrames = 1
        #print("nbFrames: ", nbFrames)
        return nbFrames

    def getFrameError(self):
        return self._frameError

    def setFrameError(self, nodeName):
        self._frameError = nodeName

    ######## setters ########

    def setNameUser(self, nameUser):
        if(nameUser == ''):
            nameUser = 'Undefined name'
        self._node.setNameUser(nameUser)

    #from a QPoint
    def setCoord(self, point):
        self._node.setCoord(point.x(), point.y())

    def setXCoord(self, x):
        self._node.setCoord(x, self.getYCoord())

    def setYCoord(self, y):
        self._node.setCoord(self.getXCoord(), y)

    # from a QColor
    def setColor(self, color):
        self._node.setColorRGB(color.red(), color.green(), color.blue())

    def setNbInput(self, nbInput):
        self._node.setNbInput(nbInput)

    ################################################## LINK WRAPPER LAYER TO QML ##################################################

    nodeLookChanged = nodePositionChanged = nodeContentChanged = QtCore.pyqtSignal()

    def emitNodeLookChanged(self):
        """
            Emits the signal emitNodeLookChanged.
        """
        self.nodeLookChanged.emit()

    def emitNodePositionChanged(self):
        """
            Emits the signal emitNodePositionChanged.
        """
        self.nodePositionChanged.emit()

    def emitNodeContentChanged(self):
        """
            Emits the signal nodeContentChanged and warns the other params of the node that something just happened.
        """
        for paramW in self.getParams():
            paramW.emitOtherParamOfTheNodeChanged()
        # emit signal
        self.nodeContentChanged.emit()

    ################################################## DATA EXPOSED TO QML ##################################################

    # params from Buttle
    name = QtCore.pyqtProperty(str, getName, constant=True)
    nameUser = QtCore.pyqtProperty(str, getNameUser, setNameUser, notify=nodeLookChanged)
    nodeType = QtCore.pyqtProperty(str, getType, constant=True)
    pluginDoc = QtCore.pyqtProperty(str, getPluginDescription, constant=True)
    coord = QtCore.pyqtProperty(QtCore.QPointF, getCoord, setCoord, notify=nodePositionChanged)  # problem to access to x property with QPoint !
    xCoord = QtCore.pyqtProperty(int, getXCoord, setXCoord, notify=nodePositionChanged)
    yCoord = QtCore.pyqtProperty(int, getYCoord, setYCoord, notify=nodePositionChanged)
    nbInput = QtCore.pyqtProperty(int, getNbInput, constant=True)
    # params (wrappers)
    params = QtCore.pyqtProperty(QtCore.QObject, getParams, notify=nodeContentChanged)

    # video
    fps = QtCore.pyqtProperty(float, getFPS, constant=True)
    nbFrames = QtCore.pyqtProperty(int, getNbFrames, constant=True)

    # for a clean display of  connections
    srcClips = QtCore.pyqtProperty(QtCore.QObject, getSrcClips, constant=True)
    outputClip = QtCore.pyqtProperty(QtCore.QObject, getOutputClip, constant=True)

    color = QtCore.pyqtProperty(QtGui.QColor, getColor, setColor, notify=nodeLookChanged)
