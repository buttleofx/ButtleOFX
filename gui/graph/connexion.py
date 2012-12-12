class Connexion(object):

    """
        Class Connexion defined by:
        - nodeOut : The node where the connexion comes from
        - nodeIn : The node to where the connexion go
        - The id of the nodeOut's output ???
    """

    def __init__(self, nodeOut, nodeIn):
        super(Connexion, self).__init__()

        self._nodeOut = nodeOut
        self._nodeIn = nodeIn

    def __str__(self):
        #print 'Connexion between the node "%s" and the node "%s' % (self._nodeOut._name, self._nodeIn._name)
        print 'Connexion between the node "%s" and the node "%s' % (self._nodeOut, self._nodeIn)
