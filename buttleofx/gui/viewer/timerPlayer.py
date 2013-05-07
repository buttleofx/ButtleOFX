from PySide import QtCore
from PySide import QtDeclarative

from pyTuttle import tuttle

import logging

from buttleofx.data import ButtleDataSingleton


class TimerPlayer(QtDeclarative.QDeclarativeItem):

    def __init__(self, parent=None):
        QtDeclarative.QDeclarativeItem.__init__(self, parent)
        self._timer = QtCore.QTimer()
        self._fps = 25
        self._speed = 1000/self._fps  # delay between frames in milliseconds
        self.connect(self._timer, QtCore.SIGNAL("timeout()"), self.nextFrame)  # initialize the timer
        # new tests with processGraph
        self._frame = 0
        self._fps = 25
        self._nbFrames = 1
        self._processGraph = None

    # fonctions used in QML for the Viewer (in the file TimelineTools.qml)
    @QtCore.Slot()
    def play(self):
        print "--------------playing-------------"
        buttleData = ButtleDataSingleton().get()
        # we say the video is playing (used in viewerManager.py)
        buttleData.setVideoIsPlaying(True)
        timeRange = tuttle.TimeRange(int(self._frame), int(self._nbFrames), 1)
        # we specify the timeRange (used in viewerManager.py)
        buttleData.setTimeRange(timeRange)
        #launch the timer
        self._timer.start(self._speed)

        # initialization of the process graph
        # graph = buttleData.getGraph().getGraphTuttle()
        # processOptions = tuttle.ComputeOptions()
        # processGraph = tuttle.ProcessGraph(processOptions, graph, [])
        # buttleData.setProcessGraph(processGraph)

        #print "-----------setup processGraph--------"
        #buttleData.processGraphSetUp()

        # print "--------------playing-------------"
        # print "-----------setup processGraph--------"
        # self._processGraph.setup()

        # # timeRange between the frames of beginning and end (first frame, last frame, step)
        # timeRange = tuttle.TimeRange(0, 500, 1)  # self._frame, self._nbFrames
        # print "---------begin Sequence--------"
        # self._processGraph.beginSequence(timeRange)

        # # send to ButtleData to communicate with viewerManager
        # buttleData.setProcessGraph(self._processGraph)

    @QtCore.Slot()
    def pause(self):
        self._timer.stop()
        buttleData = ButtleDataSingleton().get()
        buttleData.setVideoIsPlaying(False)

        # print "endSequence"
        # self._processGraph.endSequence()
        # self._processGraph = None
        #buttleData.setProcessGraph(None)

    @QtCore.Slot()
    def stop(self):
        self._timer.stop()
        buttleData = ButtleDataSingleton().get()
        buttleData.setVideoIsPlaying(False)
        self._frame = 0
        self.framePlayerChanged.emit()

        # print "endSequence"
        # self._processGraph.endSequence()
        # self._processGraph = None
        #buttleData.setProcessGraph(None)

    @QtCore.Slot()
    def nextFrame(self):
        if(self._frame < self._nbFrames - 1):
            self._frame = self._frame + 1
        else:
            return
        # debug
        # print self._frame
        # print "self._fps :", self._fps
        self.framePlayerChanged.emit()

    @QtCore.Slot()
    def previousFrame(self):
        if(self._frame > 0):
            self._frame = self._frame - 1
        else:
            return
        self.framePlayerChanged.emit()

    def getFrame(self):
        return self._frame

    def setFrame(self, frame):
        if(int(frame) < self._nbFrames):
            self._frame = int(frame)
            print "hohohohoho"
            print self._frame
        else:
            print 'alala'
            return
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
