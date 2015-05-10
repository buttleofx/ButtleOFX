import logging

from pyTuttle import tuttle

from PyQt5 import QtCore, QtQuick

from buttleofx.data import globalButtleData


class TimerPlayer(QtQuick.QQuickItem):

    def __init__(self, parent=None):
        QtQuick.QQuickItem.__init__(self, parent)
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self.nextFrame)  # Initialize the timer
        self._fps = 25
        self._speed = 1000/self._fps  # Delay between frames in milliseconds
        self._frame = 0
        self._fps = 25
        self._nbFrames = 1
        self._processGraph = None
        self._processOptions = None

    # ############################################ Methods exposed to QML ############################################ #

    @QtCore.pyqtSlot()
    def frameChanged(self):
        self.framePlayerChanged.emit()

    @QtCore.pyqtSlot()
    def launchProcessGraph(self):
        # Get the name of the currentNode of the viewer
        node = globalButtleData.getCurrentViewerNodeName()
        # Initialization of the process graph
        graph = globalButtleData.getCurrentGraph().getGraphTuttle()

        # timeRange between the frames of beginning and end (first frame, last frame, step)
        timeRange = tuttle.TimeRange(self._frame, self._nbFrames, 1)
        self._processOptions = tuttle.ComputeOptions(self._frame, self._nbFrames, 1)

        processGraph = tuttle.ProcessGraph(self._processOptions, graph, [node], tuttle.core().getMemoryCache())
        processGraph.setup()
        processGraph.beginSequence(timeRange)

        # Communicate processGraph to globalButtleData
        globalButtleData.setProcessGraph(processGraph)

        globalButtleData.setVideoIsPlaying(True)

    @QtCore.pyqtSlot()
    def pause(self):
        logging.debug("--------------pause-------------")
        self._timer.stop()

        if globalButtleData.getVideoIsPlaying():
            globalButtleData.setVideoIsPlaying(False)
            # Close processGraph and delete it
            globalButtleData.getProcessGraph().endSequence()
            globalButtleData.setProcessGraph(None)

        self.framePlayerChanged.emit()

    @QtCore.pyqtSlot()
    def play(self):
        logging.debug("--------------playing-------------")
        # Get the name of the currentNode of the viewer
        node = globalButtleData.getCurrentViewerNodeName()
        # Initialization of the process graph
        graph = globalButtleData.getCurrentGraph().getGraphTuttle()

        # timeRange between the frames of beginning and end (first frame, last frame, step)
        timeRange = tuttle.TimeRange(self._frame, self._nbFrames, 1)
        self._processOptions = tuttle.ComputeOptions(self._frame, self._nbFrames, 1)

        processGraph = tuttle.ProcessGraph(self._processOptions, graph, [node], tuttle.core().getMemoryCache())
        processGraph.setup()
        processGraph.beginSequence(timeRange)

        # Communicate processGraph to globalButtleData
        globalButtleData.setProcessGraph(processGraph)
        globalButtleData.setVideoIsPlaying(True)

        self._speed = 1000 / self._fps
        self._timer.start(self._speed)

    @QtCore.pyqtSlot()
    def previousFrame(self):
        if self._frame > 0:
            self._frame = self._frame - 1
        else:
            return
        self.framePlayerChanged.emit()

    @QtCore.pyqtSlot()
    def stop(self):
        logging.debug("--------------stop-------------")
        self._timer.stop()

        # If a video is reading, we need to close the processGraph
        if globalButtleData.getVideoIsPlaying():
            globalButtleData.setVideoIsPlaying(False)
            # Close processGraph and delete it
            globalButtleData.getProcessGraph().endSequence()
            globalButtleData.setProcessGraph(None)

        # Return to the beginning of the video
        self._frame = 0
        self.framePlayerChanged.emit()

    # ######################################## Methods private to this class ######################################## #

    # ## Getters ## #

    def getFrame(self):
        return self._frame

    def getFPS(self):
        return self._fps

    def getNbFrames(self):
        return self.nbFrames

    # ## Setters ## #

    def setFrame(self, frame):
        if int(frame) >= self._nbFrames:
            logging.debug('setFrame, ignore: frame outside bounds')
            self.pause()
            return

        if int(frame) == self._nbFrames - 1:
            self.pause()

        self._frame = int(frame)
        self.framePlayerChanged.emit()

    def setFPS(self, fps):
        self._fps = fps
        self.fpsVideoChanged.emit()

    def setNbFrames(self, nbFrames):
        self._nbFrames = nbFrames
        self.nbFramesChanged.emit()

    def nextFrame(self):
        if self._frame < self._nbFrames - 1:
            self._frame = self._frame + 1
        else:
            return
        self.framePlayerChanged.emit()

    # ############################################# Data exposed to QML ############################################# #

    framePlayerChanged = QtCore.pyqtSignal()
    fpsVideoChanged = QtCore.pyqtSignal()
    nbFramesChanged = QtCore.pyqtSignal()

    frame = QtCore.pyqtProperty(float, getFrame, setFrame, notify=framePlayerChanged)
    fps = QtCore.pyqtProperty(float, getFPS, setFPS, notify=fpsVideoChanged)
    nbFrames = QtCore.pyqtProperty(int, getNbFrames, setNbFrames, notify=nbFramesChanged)
