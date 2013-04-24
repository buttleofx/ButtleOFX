from PySide import QtCore
from PySide import QtDeclarative

from buttleofx.data import ButtleDataSingleton


class TimerPlayer(QtDeclarative.QDeclarativeItem):

    def __init__(self, parent=None):
        QtDeclarative.QDeclarativeItem.__init__(self, parent)
        self._timer = QtCore.QTimer()
        self._frame = 0
        self._fps = 25
        self._speed = 1000/self._fps #self._speed (milliseconds/fps)



    # fonctions used in QML for the Viewer (file TimelineTools.qml)
    @QtCore.Slot()
    def play(self):
        self.connect(self._timer, QtCore.SIGNAL("timeout()"), self.nextFrame)
        self._timer.start(self._speed) # action nextFrame is made every 1/fps second

    @QtCore.Slot()
    def pause(self):
        self._timer.stop()

    @QtCore.Slot()
    def stop(self):
        self._timer.stop()
        self._frame = 0

    @QtCore.Slot()
    def nextFrame(self):
        self._frame = self._frame + 1
        # debug
        print self._frame
        print "self._fps :", self._fps
        self.framePlayerChanged.emit()

    @QtCore.Slot()
    def previousFrame(self):
        self._frame = self._frame - 1
        self.framePlayerChanged.emit()

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

    framePlayerChanged = QtCore.Signal()
    fpsVideoChanged = QtCore.Signal()

    frame = QtCore.Property(float, getFrame, setFrame, notify=framePlayerChanged)
    fps = QtCore.Property(float, getFPS, setFPS, notify=fpsVideoChanged)
