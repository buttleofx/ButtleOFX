#!/usr/bin/env python
# -*-coding:utf-8-*


class Vec2d:
    """
        Vector with 2 dimensions :
        x
        y
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        """
            Prints the Vector coordinates
        """
        print("({0}, {1})".format(self.x, self.y))

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
