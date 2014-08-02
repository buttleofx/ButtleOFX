class Vec2d:
    """
        Vector with 2 dimensions :
        x
        y
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getX(self):
        """
            Gets the x coordinate
        """
        return self.x

    def getY(self):
        """
            Gets the y coordinate
        """
        return self.y

    # ## Setters ## #

    def setX(self, new_x):
        """
            Sets the x coordinate
        """
        self.x = new_x

    def setY(self, new_y):
        """
            Sets the y coordinate
        """
        self.y = new_y

    # ## Others ## #
    def __str__(self):
        """
            Prints the Vector coordinates
        """
        print("({0}, {1})".format(self.x, self.y))
