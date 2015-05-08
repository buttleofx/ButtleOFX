from PyQt5 import QtCore


class ClipWrapper(QtCore.QObject):
    """
        Class ClipWrapper defined by :
        - _nodeName : the name of the node to which belongs the clip.
        - _clipName : the name of this clip.
    """

    def __init__(self, clipName, nodeName, view):
        # logging.debug("ClipWrapper constructor")
        super(ClipWrapper, self).__init__(view)
        self._nodeName = nodeName
        self._clipName = clipName

        # Determined by QML, but declared in model to be shared with connections
        self._xCoord = 1234
        self._yCoord = 123

    # ## Getters ## #
    def getNodeName(self):
        return self._nodeName

    def getClipName(self):
        return self._clipName

    def getFullName(self):
        return "{0}.{1}".format(self.getNodeName(), self.getClipName())

    def getXCoord(self):
        # logging.debug("ClipWrapper  << getCoord:", self.getFullName(), self._coord.x(), self._coord.y())
        return self._xCoord

    def getYCoord(self):
        # logging.debug("ClipWrapper  << getCoord:", self.getFullName(), self._coord.x(), self._coord.y())
        return self._yCoord

    # ## Setters ## #
    def setXCoord(self, x):
        # logging.debug("ClipWrapper  >> setXCoord:", self.getFullName(), x)
        self._xCoord = x
        self.xCoordChanged.emit()

    def setYCoord(self, y):
        # logging.debug("ClipWrapper  >> setYCoord:", self.getFullName(), y)
        self._yCoord = y
        self.yCoordChanged.emit()

    # ############################################# Data exposed to QML ############################################## #

    name = QtCore.pyqtProperty(str, getClipName, constant=True)
    nodeName = QtCore.pyqtProperty(str, getNodeName, constant=True)
    fullName = QtCore.pyqtProperty(str, getFullName, constant=True)

    xCoordChanged = QtCore.pyqtSignal()
    yCoordChanged = QtCore.pyqtSignal()
    xCoord = QtCore.pyqtProperty(int, getXCoord, setXCoord, notify=xCoordChanged)
    yCoord = QtCore.pyqtProperty(int, getYCoord, setYCoord, notify=yCoordChanged)
