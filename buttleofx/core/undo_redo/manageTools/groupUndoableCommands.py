#!/usr/bin/env python
# -*-coding:utf-8-*


class GroupUndoableCommands:
    """
    Group of objects saved in the Command Manager.
    """

    groupUndoableCommands = []

    def __init__(self, commands):
        self.groupUndoableCommands = commands

    def undoCmd(self):
        """
        Executes the user request (ctrl Z) (undo a group of commands).
        """
        for command in self.groupUndoableCommands:
            command.undoCmd()

    def redoCmd(self):
        """
        Undoes the operations performed by undoCmd method.
        """
        self.doCmd()

    def doCmd(self):
        """
        Executes the user request (the groupe of functions).
        Returns nothing : maybe need to be improved in the future (list of return value of each command ?).
        """
        for command in self.groupUndoableCommands:
            command.doCmd()
        return
