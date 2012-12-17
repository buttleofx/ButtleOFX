class Connection(object):

    """
        Class Connection defined by:
        - nodeOut : The node where the connection comes from
        - nodeIn : The node to where the connection go
    """

    def __init__(self, clipOut, clipIn):
        super(Connection, self).__init__()

        self._clipOut = clipOut
        self._clipIn = clipIn

    def __str__(self):
        #print 'Connection between the node "%s" and the node "%s' % (self._nodeOut._name, self._nodeIn._name)
        print 'Connection between the clip "%s (%s)" and the clip "%s (%s)' % (self._clipOut._node, self._clipOut._clip, self._clipIn._node, self._clipIn._clip)
