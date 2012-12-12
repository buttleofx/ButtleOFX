class Connection(object):

    """
        Class Connection defined by:
        - nodeOut : The node where the connection comes from
        - nodeIn : The node to where the connection go
        - The id of the nodeOut's output ???
    """

    def __init__(self, nodeOut, nodeIn):
        super(Connection, self).__init__()

        self._nodeOut = nodeOut
        self._nodeIn = nodeIn

    def __str__(self):
        #print 'Connection between the node "%s" and the node "%s' % (self._nodeOut._name, self._nodeIn._name)
        print 'Connection between the node "%s" and the node "%s' % (self._nodeOut, self._nodeIn)
