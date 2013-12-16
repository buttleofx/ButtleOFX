from PyQt5 import QtCore


class ClipWrapper(QtCore.QObject):
    """
        Class ClipWrapper defined by :
        - _nodeName : the name of the node to which belongs the clip.
        - _clipName : the name of this clip.
    """

    def __init__(self, clipName, nodeName, view):
        # print("ClipWrapper constructor")
        super(ClipWrapper, self).__init__(view)
        self._nodeName = nodeName
        self._clipName = clipName
        
        # determined by QML, but declared in model to be shared with connections
        self._coord = QtCore.QPointF(50.0, 50.0)

    def getNodeName(self):
        return self._nodeName

    def getClipName(self):
        return self._clipName

    def getCoord(self):
        return self._coord

    def setCoord(self, point):
        # print("ClipWrapper setCoord:", self, point.x(), point.y())
        self._coord = point
        self.coordChanged.emit()

    name = QtCore.pyqtProperty(str, getClipName, constant=True)
    nodeName = QtCore.pyqtProperty(str, getNodeName, constant=True)

    coordChanged = QtCore.pyqtSignal()
    coord = QtCore.pyqtProperty(QtCore.QPointF, getCoord, setCoord, notify=coordChanged)
