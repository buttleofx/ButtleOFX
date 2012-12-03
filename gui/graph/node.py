class Node(object):

    """
        Class Node defined by:
        - id : Node id
        - xCoord : Node position on the x axis
        - yCoord : Node position on the y axis
        - r : Value for the red color
        - g : Value for the green color
        - b : Value for the blue color
        - nbInput

        Creates a python object Node.
    """

    count = 0

    def __init__(self, id, xCoord, yCoord, r, g, b, nbInput):
        super(Node, self).__init__()
        self.id = id
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.r = r
        self.g = g
        self.b = b
        self.nbInput = nbInput
        Node.count += 1

    def __str__(self):
        return 'Node "%s"' % (self.id)
