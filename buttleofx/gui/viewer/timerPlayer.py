from PySide import QtCore
from PySide import QtDeclarative

from pyTuttle import tuttle

from buttleofx.data import ButtleDataSingleton


class TimerPlayer(QtDeclarative.QDeclarativeItem):

    def __init__(self, parent=None):
        QtDeclarative.QDeclarativeItem.__init__(self, parent)
        self._timer = QtCore.QTimer()
        self._frame = 0
        self._fps = 25
        #self._speed (milliseconds/fps)
        self._speed = 1000/self._fps

        # new tests with processGraph
        self._nbFrames = 1
        self._processGraph = None
        

    # fonctions used in QML for the Viewer (file TimelineTools.qml)
    @QtCore.Slot()
    def play(self):
        # new test
        # we get the current graph
        buttleData = ButtleDataSingleton().get()
        graph = buttleData.getGraph().getGraphTuttle()
        processOptions = tuttle.ComputeOptions()
        self._processGraph = tuttle.ProcessGraph(processOptions, graph, [])

        print "playing"
        print "setup processGraph"
        self._processGraph.setup()
        print "begin Sequence"
        # (first frame, last frame, step)
        timeRange = tuttle.TimeRange(1, self._nbFrames, 1)
        self._processGraph.beginSequence(timeRange)

        # launch the timer
        self.connect(self._timer, QtCore.SIGNAL("timeout()"), self.nextFrame)
         # action nextFrame is made every 1/fps second
        self._timer.start(self._speed)

    @QtCore.Slot()
    def pause(self):
        print "endSequence"
        self._processGraph.endSequence()

        self._timer.stop()
        # we ask to "close" the video (frame is still displayed)
        # graphProcessing.end()

    @QtCore.Slot()
    def stop(self):
        #new test
        print "endSequence"
        self._processGraph.endSequence()

        self._timer.stop()
        self._frame = 0

    @QtCore.Slot()
    def nextFrame(self):
        #new tests
        self._processGraph.setupAtTime(self._frame)
        self._processGraph.processAtTime(tuttle.MemoryCache(), self._frame)

        self._frame = self._frame + 1
        # debug
        # print self._frame
        # print "self._fps :", self._fps
        self.framePlayerChanged.emit()

    # @QtCore.Slot()
    # def previousFrame(self):
    #     self._frame = self._frame - 1
    #     self.framePlayerChanged.emit()

    def getFrame(self):
        return self._frame

    def setFrame(self, frame):
        self._frame = frame
        self.framePlayerChanged.emit()

    def getFPS(self):
        return self._fps

    def setFPS(self, fps):
        self._fps = fps
        self.fpsVideoChanged.emit()

    def setNbFrames(self, nbFrames):
        self._nbFrames = nbFrames
        self.nbFramesChanged.emit()

    def getNbFrames(self):
        return self.nbFrames

    framePlayerChanged = QtCore.Signal()
    fpsVideoChanged = QtCore.Signal()
    nbFramesChanged = QtCore.Signal()

    frame = QtCore.Property(float, getFrame, setFrame, notify=framePlayerChanged)
    fps = QtCore.Property(float, getFPS, setFPS, notify=fpsVideoChanged)
    nbFrames = QtCore.Property(int, getNbFrames, setNbFrames, notify=nbFramesChanged)
