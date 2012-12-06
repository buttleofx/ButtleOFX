class Node(object):

    """
        Class Node defined by:
        - name
        - x : Node position on the x axis
        - y : Node position on the y axis
        - r : Value for the red color
        - g : Value for the green color
        - b : Value for the blue color
        - nbInput : Number of inputs fot the node

        Creates a python object Node.
    """

    def __init__(self, name, x, y, r, g, b, nbInput):
        super(Node, self).__init__()
        self._name = name
        self._x = x
        self._y = y
        self._r = r
        self._g = g
        self._b = b
        self._nbInput = nbInput

    def __str__(self):
        return 'Node "%s"' % (self._name)
