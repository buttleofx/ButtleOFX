from PySide import QtCore, QtGui

#quickmamba
from quickmamba.models import QObjectListModel

# wrappers
from buttleofx.gui.paramEditor.wrappers import ParamEditorWrapper
from buttleofx.gui.graph.connection import ClipWrapper


class NodeWrapper(QtCore.QObject):
    """
        Class NodeWrapper defined by:
        - _node : the node data

        Creates a QObject from a given python object Node.
    """

    def __init__(self, node, view):
        super(NodeWrapper, self).__init__(view)

        self._node = node
        self._view = view

        self._widthEmptyNode = 15
        self._heightEmptyNode = 35
        self._clipSpacing = 7
        self._clipSize = 8
        self._inputSideMargin = 6

        self._node.changed.connect(self.emitChanged)

        _fpsError = ""
        _frameError = ""

        print "Gui : nodeWrapper created"

    def __del__(self):
        print "Gui : NodeWrapper deleted"

    # We can't connect the two signals because self.changed() is a QML signal.
    # So, we use the function self.emitChanged() to solve the problem
    @QtCore.Signal
    def changed(self):
        pass

    def emitChanged(self):
        self.changed.emit()

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

    def getNbInput(self):
        return self._node.getNbInput()

    def getSrcClips(self):
        srcClips = QObjectListModel(self)
        srcClips.setObjectList([ClipWrapper(clip, self.getName(), self._view) for clip in self._node.getClips() if not clip == "Output"])
        return srcClips

    def getOutputClips(self):
        outputClips = QObjectListModel(self)
        outputClips.setObjectList([ClipWrapper(clip, self.getName(), self._view) for clip in self._node.getClips() if clip == "Output"])
        return outputClips

    def getWidth(self):
        return self._widthEmptyNode + 9 * len(self.getNameUser())

    def getHeight(self):
        return int(self._heightEmptyNode + self._clipSpacing * self.getNbInput())

    def getClipSpacing(self):
        return self._clipSpacing

    def getClipSize(self):
        return self._clipSize

    def getInputSideMargin(self):
        return self._inputSideMargin

    def getInputTopMargin(self):
        return (self.getHeight() - self.getClipSize() * self.getNbInput() - self.getClipSpacing() * (self.getNbInput() - 1)) / 2

    def getParams(self):
        paramEditorWrapper = ParamEditorWrapper(self._view, self._node.getParams())
        return paramEditorWrapper.paramElmts

    #for video
    def getFPS(self):
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
    def setName(self, name):
        self._node.setName(name)

    def setNameUser(self, nameUser):
        self._node.setNameUser(nameUser)

    def setType(self, nodeType):
        self._node.setType(nodeType)

    # from a QPoint
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

    ################################################## DATA EXPOSED TO QML ##################################################

    # params from Buttle
    name = QtCore.Property(str, getName, setName, notify=changed)
    nameUser = QtCore.Property(str, getNameUser, setNameUser, notify=changed)
    nodeType = QtCore.Property(str, getType, setType, notify=changed)
    coord = QtCore.Property(QtCore.QPoint, getCoord, setCoord, notify=changed)

    xCoord = QtCore.Property(int, getXCoord, setXCoord, notify=changed)
    yCoord = QtCore.Property(int, getYCoord, setYCoord, notify=changed)

    color = QtCore.Property(QtGui.QColor, getColor, setColor, notify=changed)
    nbInput = QtCore.Property(int, getNbInput, setNbInput, notify=changed)
    # image = QtCore.Property(str, getImage, setImage, notify=changed)
    # params from Tuttle
    params = QtCore.Property(QtCore.QObject, getParams, constant=True)
    #video
    fps = QtCore.Property(float, getFPS, notify=changed)
    nbFrames = QtCore.Property(int, getNbFrames, notify=changed)

    # for a clean display of connections
    width = QtCore.Property(int, getWidth, notify=changed)
    height = QtCore.Property(int, getHeight, constant=True)
    srcClips = QtCore.Property(QtCore.QObject, getSrcClips, constant=True)
    outputClips = QtCore.Property(QtCore.QObject, getOutputClips, constant=True)
    clipSpacing = QtCore.Property(int, getClipSpacing, constant=True)
    clipSize = QtCore.Property(int, getClipSize, constant=True)
    inputSideMargin = QtCore.Property(int, getInputSideMargin, constant=True)
    inputTopMargin = QtCore.Property(int, getInputTopMargin, constant=True)
