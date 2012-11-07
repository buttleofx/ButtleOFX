class Node(object):

    """
        Class Node defined by:
        - name : Node name
        - xCoord : Node position on the x axis
        - yCoord : Node position on the y axis
        - r : Value for the red color
        - g : Value for the green color
        - b : Value for the blue color
        - nbInput

        Creates a python object Node.
    """

    def __init__(self, name, xCoord, yCoord, r, g, b, nbInput):
        self.name = name
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.r = r
        self.g = g
        self.b = b
        self.nbInput = nbInput

    def __str__(self):
        return 'Node "%s"' % (self.name)
