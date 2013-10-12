from PySide import QtCore


class ClipWrapper(QtCore.QObject):
    """
        Class ClipWrapper defined by :
        - _nodeName : the name of the node to wich belongs the clip.
        - _clipName : the name of this clip.
    """

    def __init__(self, clipName, nodeName, view):
        super(ClipWrapper, self).__init__(view)
        self._nodeName = nodeName
        self._clipName = clipName

    def getNodeName(self):
        return self._nodeName

    def getClipName(self):
        return self._clipName

    name = QtCore.Property(str, getClipName, constant=True)
    nodeName = QtCore.Property(str, getNodeName, constant=True)
