class GroupUndoableCommands(object):
    """
    Group of objects saved in the Command Manager.
    """

    groupUndoableCommands = []

    def __init__(self, commands, label):
        self.groupUndoableCommands = commands
        if label != "":
            self.label = label
        else:
            self.label = "Undocumented Command"

        for command in commands:
            self.label += " '" + command.getLabel() + "' "

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getLabel(self):
        """
        Return what does the command undo/redo
        """
        return self.label

    # ## Others ## #

    def doCmd(self):
        """
        Executes the user request (the group of functions).
        Returns nothing, maybe need to be improved in the future (list of return value of each command?).
        """
        for command in self.groupUndoableCommands:
            command.doCmd()
        return

    def redoCmd(self):
        """
        Undoes the operations performed by undoCmd method.
        """
        self.doCmd()

    def undoCmd(self):
        """
        Executes the user request (Ctrl Z) (undo a group of commands).
        """
        for command in self.groupUndoableCommands:
            command.undoCmd()
