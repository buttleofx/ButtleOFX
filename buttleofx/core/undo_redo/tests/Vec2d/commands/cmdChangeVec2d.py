#!/usr/bin/env python
# -*-coding:utf-8-*


class CmdChangeVec2d():
    """
        Command which enable us to change the coordinates of a Vector2d
    """

    def __init__(self, vec2d_target, new_x, new_y):
        self.vec2dTarget = vec2d_target
        self.newX = new_x
        self.newY = new_y
        self.oldX = vec2d_target.x
        self.oldY = vec2d_target.y

    def undoCmd(self):
        """
            Undoes the vector's change
        """
        self.vec2dTarget.x = self.oldX
        self.vec2dTarget.y = self.oldY
        return self.vec2dTarget

    def redoCmd(self):
        """
            Redoes the vector's change
        """
        return self.doCmd()

    def doCmd(self):
        """
            Executes the vector's change
        """
        self.vec2dTarget.x = self.newX
        self.vec2dTarget.y = self.newY
        return self.vec2dTarget
