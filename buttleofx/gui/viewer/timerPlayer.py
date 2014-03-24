from PyQt5 import QtCore, QtQuick
import logging

from pyTuttle import tuttle

from buttleofx.data import ButtleDataSingleton


class TimerPlayer(QtQuick.QQuickItem):

    def __init__(self, parent=None):
        QtQuick.QQuickItem.__init__(self, parent)
        self._timer = QtCore.QTimer()
        import functools
        self._timer.timeout.connect(self.nextFrame)  # initialize the timer
        self._fps = 25
        self._speed = 1000/self._fps  # delay between frames in milliseconds
        self._frame = 0
        self._fps = 25
        self._nbFrames = 1
        self._processGraph = None
        self._processOptions = None

    # fonctions used in QML for the Viewer (in the file TimelineTools.qml)
    @QtCore.pyqtSlot()
    def play(self):
        logging.debug("--------------playing-------------")
        buttleData = ButtleDataSingleton().get()
        #Get the name of the currentNode of the viewer
        node = buttleData.getCurrentViewerNodeName()
        # initialization of the process graph
        graph = buttleData.getCurrentGraph().getGraphTuttle()

        # timeRange between the frames of beginning and end (first frame, last frame, step)
        timeRange = tuttle.TimeRange(self._frame, self._nbFrames, 1)
        self._processOptions = tuttle.ComputeOptions(self._frame, self._nbFrames, 1)
        processGraph = tuttle.ProcessGraph(self._processOptions, graph, [node], tuttle.core().getMemoryCache())
        processGraph.setup()
        processGraph.beginSequence(timeRange)
        # communicate processGraph to buttleData
        buttleData.setProcessGraph(processGraph)
        buttleData.setVideoIsPlaying(True)
        
        self._speed = 1000/self._fps
        self._timer.start(self._speed)

    @QtCore.pyqtSlot()
    def launchProcessGraph(self):
        buttleData = ButtleDataSingleton().get()
        #Get the name of the currentNode of the viewer
        node = buttleData.getCurrentViewerNodeName()
        # initialization of the process graph
        graph = buttleData.getCurrentGraph().getGraphTuttle()

        # timeRange between the frames of beginning and end (first frame, last frame, step)
        timeRange = tuttle.TimeRange(self._frame, self._nbFrames, 1)
        self._processOptions = tuttle.ComputeOptions(self._frame, self._nbFrames, 1)
        processGraph = tuttle.ProcessGraph(self._processOptions, graph, [node], tuttle.core().getMemoryCache())
        processGraph.setup()
        processGraph.beginSequence(timeRange)
        # communicate processGraph to buttleData
        buttleData.setProcessGraph(processGraph)
        
        buttleData.setVideoIsPlaying(True)

    @QtCore.pyqtSlot()
    def pause(self):
        logging.debug("--------------pause-------------")
        self._timer.stop()
        buttleData = ButtleDataSingleton().get()
        if buttleData.getVideoIsPlaying():
            buttleData.setVideoIsPlaying(False)
            # close processGraph and delete it
            buttleData.getProcessGraph().endSequence()
            buttleData.setProcessGraph(None)
        self.framePlayerChanged.emit()

    @QtCore.pyqtSlot()
    def stop(self):
        logging.debug("--------------stop-------------")
        self._timer.stop()
        buttleData = ButtleDataSingleton().get()
        # if a video is reading, we need to close the processGraph
        if buttleData.getVideoIsPlaying():
            buttleData.setVideoIsPlaying(False)
            # close processGraph and delete it
            buttleData.getProcessGraph().endSequence()
            buttleData.setProcessGraph(None)
            # return to the beginning of the video
        self._frame = 0
        self.framePlayerChanged.emit()

    def nextFrame(self):
        if(self._frame < self._nbFrames - 1):
            self._frame = self._frame + 1
        else:
            return
        self.framePlayerChanged.emit()

    @QtCore.pyqtSlot()
    def previousFrame(self):
        if(self._frame > 0):
            self._frame = self._frame - 1
        else:
            return
        self.framePlayerChanged.emit()

    def getFrame(self):
        return self._frame

    def setFrame(self, frame):
        if(int(frame) >= self._nbFrames):
            logging.debug('setFrame, ignore: frame outside bounds')
            self.pause()
            return
        if(int(frame) == self._nbFrames - 1):
            self.pause()
        self._frame = int(frame)
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

    @QtCore.pyqtSlot()
    def frameChanged(self):
        self.framePlayerChanged.emit()

    framePlayerChanged = QtCore.pyqtSignal()
    fpsVideoChanged = QtCore.pyqtSignal()
    nbFramesChanged = QtCore.pyqtSignal()

    frame = QtCore.pyqtProperty(float, getFrame, setFrame, notify=framePlayerChanged)
    fps = QtCore.pyqtProperty(float, getFPS, setFPS, notify=fpsVideoChanged)
    nbFrames = QtCore.pyqtProperty(int, getNbFrames, setNbFrames, notify=nbFramesChanged)
