#!/usr/bin/env python
# -*-coding:utf-8-*


class GroupUndoableCommands:
    """
    Group of objects saved in the Command Manager.
    """

    groupUndoableCommands = []

    def __init__(self, commands):
        for command in commands:
            self.groupUndoableCommands.append(command)

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
        """
        for command in self.groupUndoableCommands:
            command.doCmd()
