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
        self._xCoord = 1234
        self._yCoord = 123

    def getNodeName(self):
        return self._nodeName

    def getClipName(self):
        return self._clipName
    
    def getFullName(self):
        return "%s.%s" % (self.getNodeName(), self.getClipName())

    def getXCoord(self):
        # print("ClipWrapper  << getCoord:", self.getFullName(), self._coord.x(), self._coord.y())
        return self._xCoord

    def getYCoord(self):
        # print("ClipWrapper  << getCoord:", self.getFullName(), self._coord.x(), self._coord.y())
        return self._yCoord

    def setXCoord(self, x):
        # print("ClipWrapper  >> setXCoord:", self.getFullName(), x)
        self._xCoord = x
        self.xCoordChanged.emit()

    def setYCoord(self, y):
        # print("ClipWrapper  >> setYCoord:", self.getFullName(), y)
        self._yCoord = y
        self.yCoordChanged.emit()

    name = QtCore.pyqtProperty(str, getClipName, constant=True)
    nodeName = QtCore.pyqtProperty(str, getNodeName, constant=True)
    fullName = QtCore.pyqtProperty(str, getFullName, constant=True)

    xCoordChanged = QtCore.pyqtSignal()
    yCoordChanged = QtCore.pyqtSignal()
    xCoord = QtCore.pyqtProperty(int, getXCoord, setXCoord, notify=xCoordChanged)
    yCoord = QtCore.pyqtProperty(int, getYCoord, setYCoord, notify=yCoordChanged)
