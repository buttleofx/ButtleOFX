# Abstract class : you need to implement this class for each command in the program
# Transparent in Python
# http://www.developpez.net/forums/d310663/autres-langages/python-zope/general-python/classes-abstraites-python/


class UndoableCommand(object):
    """
    Object saved in the Command Manager.
    """

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getLabel(self):
        """
        Return what does the command undo/redo
        """

    # ## Others ## #

    def doCmd(self):
        """
        Executes the user request (the true function)
        """

    def redoCmd(self):
        """
        Undoes the operation performed by undoCmd method (Ctrl Y)
        """

    def undoCmd(self):
        """
        Executes the user request (Ctrl Z)
        """
