from PySide import QtCore
from PySide import QtDeclarative


class TimerPlayer(QtDeclarative.QDeclarativeItem):

    def __init__(self, parent=None):
        QtDeclarative.QDeclarativeItem.__init__(self, parent)
        self._timer = QtCore.QTimer()
        self._speed = 1000/25 #self._speed (milliseconds/fps)
        self._frame = 0

        #self._timer.start(self._speed) # action is made every 1/fps second

    # fonctions used in QML for the Viewer (file TimelineTools.qml)
    @QtCore.Slot()
    def play(self):
        self.connect(self._timer, QtCore.SIGNAL("timeout()"), self.nextFrame)
        self._timer.start(self._speed)# action nextFrame is made every 1/fps second

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
        #debug
        print self._frame
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

    framePlayerChanged = QtCore.Signal()

    frame = QtCore.Property(float, getFrame, setFrame, notify=framePlayerChanged)
