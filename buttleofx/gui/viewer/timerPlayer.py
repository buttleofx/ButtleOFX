import logging

from pyTuttle import tuttle

from PyQt5 import QtCore, QtQuick

from buttleofx.data import globalButtleData


class TimerPlayer(QtQuick.QQuickItem):

    def __init__(self, parent=None):
        QtQuick.QQuickItem.__init__(self, parent)
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self.playNextFrame)  # Initialize the timer
        self._fps = 25
        self._frame = 11
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
        graph = globalButtleData.getActiveGraph().getGraphTuttle()

        # timeRange between the frames of beginning and end (first frame, last frame, step)
        # TODO: faca
        timeRange = tuttle.TimeRange(self.getFrame(), self.getFrame() + self.getNbFrames(), 1)
        self._processOptions = tuttle.ComputeOptions(self.getFrame(), self.getNbFrames(), 1)

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
        graph = globalButtleData.getActiveGraph().getGraphTuttle()

        # timeRange between the frames of beginning and end (first frame, last frame, step)
        timeRange = tuttle.TimeRange(self.getFrame(), self.getNbFrames(), 1)
        self._processOptions = tuttle.ComputeOptions(self.getFrame(), self.getNbFrames(), 1)

        processGraph = tuttle.ProcessGraph(self._processOptions, graph, [node], tuttle.core().getMemoryCache())
        processGraph.setup()
        processGraph.beginSequence(timeRange)

        # Communicate processGraph to globalButtleData
        globalButtleData.setProcessGraph(processGraph)
        globalButtleData.setVideoIsPlaying(True)

        self._timer.start(self.getOneFrameDuration())

    @QtCore.pyqtSlot()
    def previousFrame(self):
        self.setFrame(self.getFrame() - 1)

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
        self.setFrame(0)

    # ######################################## Methods private to this class ######################################## #

    # ## Getters ## #

    @QtCore.pyqtSlot(result=int)
    def getFrame(self):
        return self._frame

    @QtCore.pyqtSlot(result=float)
    def getOneFrameDuration(self):
        """
        :return: Duration between frames in milliseconds
        """
        return 1000.0 / self._fps

    @QtCore.pyqtSlot(result=float)
    def getFPS(self):
        return self._fps

    @QtCore.pyqtSlot(result=int)
    def getNbFrames(self):
        return self._nbFrames

    # ## Setters ## #

    @QtCore.pyqtSlot(float)
    def setFrame(self, frame):
        self._frame = frame
        self.framePlayerChanged.emit()

    @QtCore.pyqtSlot(float)
    def setFPS(self, fps):
        self._fps = fps
        self.fpsVideoChanged.emit()

    @QtCore.pyqtSlot(int)
    def setNbFrames(self, nbFrames):
        self._nbFrames = nbFrames
        self.nbFramesChanged.emit()

    # DO NOT declare this function as pyqtSlot, else the Qt connection doesn't work and breaks everything.
    # @QtCore.pyqtSlot()
    def playNextFrame(self):
        # TODO: faca
        # If time outside timeDomain self.pause()
        self.nextFrame()

    @QtCore.pyqtSlot()
    def nextFrame(self):
        self.setFrame(self.getFrame() + 1)

    # ############################################# Data exposed to QML ############################################# #

    framePlayerChanged = QtCore.pyqtSignal()
    fpsVideoChanged = QtCore.pyqtSignal()
    nbFramesChanged = QtCore.pyqtSignal()

    frame = QtCore.pyqtProperty(int, getFrame, setFrame, notify=framePlayerChanged)
    fps = QtCore.pyqtProperty(float, getFPS, setFPS, notify=fpsVideoChanged)
    nbFrames = QtCore.pyqtProperty(int, getNbFrames, setNbFrames, notify=nbFramesChanged)
