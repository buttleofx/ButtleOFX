from quickmamba.patterns import Signal


class Connection(object):

    """
        Class Connection usefull to identify a connection between 2 clips :
        - clipOut : the IdClip of the first clip
        - clipIn : the IdClip of the second clip
    """

    def __init__(self, clipOut, clipIn):
        super(Connection, self).__init__()

        self._clipOut = clipOut
        self._clipIn = clipIn

        self.changed = Signal()
        self.changed()

    def __str__(self):
        print 'Connection between the clip "%s (%s %d)" and the clip "%s (%s %d)' % (self._clipOut._nodeName, self._clipOut._port, self._clipOut._clipNumber, self._clipIn._nodeName, self._clipIn._port, self._clipIn._clipNumber)

    def getClipOut(self):
        return self._clipOut

    def getClipIn(self):
        return self._clipIn

    def setClipOut(self, clipOut):
        self._clipOut = clipOut
        self.changed()

    def setClipIn(self, clipIn):
        self._clipIn = clipIn
        self.changed()
