from PySide import QtCore, QtGui
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
        super(NodeWrapper, self).__init__(view)

        self._node = node
        self._view = view

        # paramWrappers
        self._paramWrappers = ParamEditorWrapper(self._view, self._node.getParams())

        # data given to QML to have nodes and clips with good looking
        self._width = 0  # will be setted by QML
        self._heightEmptyNode = 35
        self._clipSpacing = 7
        self._clipSize = 8
        self._sideMargin = 6

        # potential errors
        self._fpsError = ""
        self._frameError = ""

        # link signals of the node and the corresponding node wrapper
        self._node.nodeLookChanged.connect(self.emitNodeLookChanged)
        self._node.nodePositionChanged.connect(self.emitNodePositionChanged)
        self._node.nodeContentChanged.connect(self.emitNodeContentChanged)

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

    def getCoord(self):
        return QtCore.QPoint(self._node.getCoord()[0], self._node.getCoord()[1])

    def getXCoord(self):
        return self._node.getCoord()[0]

    def getYCoord(self):
        return self._node.getCoord()[1]

    def getColor(self):
        return QtGui.QColor(*self._node.getColor())

    @QtCore.Slot(result=QtGui.QColor)
    def getDefaultColor(self):
        return QtGui.QColor(0, 178, 161)

    def getNbInput(self):
        return self._node.getNbInput()

    def getSrcClips(self):
        """
            Returns a QObjectListModel of ClipWrappers of the input clips of this node.
        """
        srcClips = QObjectListModel(self)
        srcClips.setObjectList([ClipWrapper(clip, self.getName(), self._view) for clip in self._node.getClips() if not clip == "Output"])
        return srcClips

    def getOutputClip(self):
        """
            Returns the ClipWrapper of the output clip of this node.
        """
        for clip in self._node.getClips():
            if clip == "Output":
                return ClipWrapper(clip, self.getName(), self._view)

    def getHeight(self):
        return int(self._heightEmptyNode + self._clipSpacing * self.getNbInput())

    def getWidth(self):
        return self._width

    def getClipSpacing(self):
        return self._clipSpacing

    def getClipSize(self):
        return self._clipSize

    def getSideMargin(self):
        return self._sideMargin

    def getInputTopMargin(self):
        return (self.getHeight() - self.getClipSize() * self.getNbInput() - self.getClipSpacing() * (self.getNbInput() - 1)) / 2

    def getOutputTopMargin(self):
        return (self.getHeight() - self.getClipSize()) / 2

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
            print "can't get fps of the node" + self._node.getName()
            self.setFpsError(str(e))
            return 1
            raise
        framerate = node.getFrameRate()
        #if (framerate == None):
        #    framerate = 1
        print "framerate: ", framerate
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
            print "can't get nbFrames of the node" + self._node.getName()
            self.setFrameError(str(e))
            return 0
            raise
        timeDomain = node.getTimeDomain()
        #getTimeDomain() returns first frame and last one
        nbFrames = timeDomain.max - timeDomain.min
        #not very elegant but allow to avoid a problem because an image returns a number of frames very high
        if nbFrames > 100000000 or nbFrames < 0:
            nbFrames = 1
        print "nbFrames: ", nbFrames
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
        self._node.setColor(color.red(), color.green(), color.blue())

    def setNbInput(self, nbInput):
        self._node.setNbInput(nbInput)

    def setWidth(self, width):
        self._width = width
        self.nodeWidthChanged.emit()

    ################################################## LINK WRAPPER LAYER TO QML ##################################################

    nodeLookChanged = nodePositionChanged = nodeContentChanged = QtCore.Signal()
    nodeWidthChanged = QtCore.Signal()

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

    ##### SLot #####

    @QtCore.Slot(int)
    def fitWidth(self, textWidth):
        """
            Function called by Node.qml to fit the width of the node given the width of the text (with an horizontal margin).
        """
        self.setWidth(textWidth + 20)

    ################################################## DATA EXPOSED TO QML ##################################################

    # params from Buttle
    name = QtCore.Property(str, getName, constant=True)
    nameUser = QtCore.Property(str, getNameUser, setNameUser, notify=nodeLookChanged)
    nodeType = QtCore.Property(str, getType, constant=True)
    coord = QtCore.Property(QtCore.QPoint, getCoord, setCoord, notify=nodePositionChanged)  # problem to access to x property with QPoint !
    xCoord = QtCore.Property(int, getXCoord, setXCoord, notify=nodePositionChanged)
    yCoord = QtCore.Property(int, getYCoord, setYCoord, notify=nodePositionChanged)
    color = QtCore.Property(QtGui.QColor, getColor, setColor, notify=nodeLookChanged)
    nbInput = QtCore.Property(int, getNbInput, constant=True)
    # params (wrappers)
    params = QtCore.Property(QtCore.QObject, getParams, notify=nodeContentChanged)

    # video
    fps = QtCore.Property(float, getFPS, constant=True)
    nbFrames = QtCore.Property(int, getNbFrames, constant=True)

    # for a clean display of  connections
    height = QtCore.Property(int, getHeight, constant=True)
    width = QtCore.Property(int, getWidth, setWidth, notify=nodeWidthChanged)  # using nodeLookChanged creates a binding loop
    srcClips = QtCore.Property(QtCore.QObject, getSrcClips, constant=True)
    outputClip = QtCore.Property(QtCore.QObject, getOutputClip, constant=True)
    clipSpacing = QtCore.Property(int, getClipSpacing, constant=True)
    clipSize = QtCore.Property(int, getClipSize, constant=True)
    sideMargin = QtCore.Property(int, getSideMargin, constant=True)
    inputTopMargin = QtCore.Property(int, getInputTopMargin, constant=True)
    outputTopMargin = QtCore.Property(int, getOutputTopMargin, constant=True)
