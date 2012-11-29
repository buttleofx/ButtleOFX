#!/usr/bin/env python
# -*-coding:utf-8-*

# abstract class : you need to implement this class for each command in the program
# transparent in Python
# http://www.developpez.net/forums/d310663/autres-langages/python-zope/general-python/classes-abstraites-python/


class UndoableCommand:
    """
    Object saved in the Command Manager.
    """

    def undoCmd(self):
        """
        Executes the user request (ctrl Z).
        """

    def redoCmd(self):
        """
        Undoes the operation performed by undoCmd method (ctrl Y).
        """

    def doCmd(self):
        """
        Executes the user request (the true function).
        """
