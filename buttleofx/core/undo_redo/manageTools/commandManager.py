

class CommandManager(object):
    """
    Manages a list of commands.
    """
    commands = []  # List of undo/redo commands
    index = 0

    active = False

    cleanIndex = 0
    savedGraphIndex = 0

    undoLimit = 10
    redoLimit = 10

    # ######################################## Methods private to this class ####################################### #

    def getCleanIndex(self):
        """
            Gets the clean index of the CommandManager.
        """
        return self.cleanIndex

    def getCommands(self):
        """
            Gets the list of commands of the CommandManager.
        """
        return self.commands

    def getIndex(self):
        """
            Gets the index of the lastest command in the CommandManager.
        """
        return self.index

    def getRedoLimit(self):
        """
            Gets the redo limit of the CommandManager.
        """
        return self.redoLimit

    def getUndoLimit(self):
        """
            Gets the undo limit of the CommandManager.
        """
        return self.undoLimit

    # ## Setters ## #

    def setActive(self, active=True):
        """
            Sets the CommandManager activity (true to false, or false to true).
        """
        self.active = active

    def setRedoLimit(self, limit):
        """
            Sets the redo limit of the CommandManager.
        """
        self.redoLimit = limit

    def setSavedGraphIndex(self, index):
        """
            Sets the index where the graph was when last saved, and indicates to buttleData that
            something changed (useful for the display of the "Save Graph" icon)
        """
        self.savedGraphIndex = index
        self.graphHadChanged()

    def setUndoLimit(self, limit):
        """
            Sets the undo limit of the CommandManager.
        """
        self.undoLimit = limit

    # ## Others ## #

    def canRedo(self):
        """
            Retrieves a Boolean indicating whether a command can be redone.
        """
        return self.index != len(self.commands)

    def canUndo(self):
        """
            Retrieves a Boolean indicating whether a command can be undone.
        """
        return self.index > 0  # If indice of the current command is > 0

    def clean(self):
        """
            Clears this command manager by emptying its list of commands.
        """
        self.commands = []  # Clear the list of commands (to check)
        self.index = 0

    def count(self):
        """
            Gets the number of commands in the CommandManager.
        """
        return len(self.commands)

    def countRedo(self):
        """
            Gets the number of redo commands in the CommandManager.
        """
        return len(self.commands) - self.index

    def countUndo(self):
        """
            Gets the number of undo commands in the CommandManager.
        """
        return self.index

    def graphHadChanged(self):
        """
            Indicates to ButtleData that a command just had been done.
            This function will update the property graphCanBeSaved of ButtleData and will change
            the display of the "Save Graph" icon.
        """
        from buttleofx.data import globalButtleData
        globalButtleData.setGraphCanBeSaved(self.savedGraphIndex != self.index)

    def isActive(self):
        """
            Tests if the CommandManager is active.
        """
        return self.active

    def isClean(self):
        """
            Tests if the list of commands is empty.
        """
        return len(self.commands) == 0

    def push(self, newCommand):
        """
            Executes a new undoable command (add command to the stack ?)
        """

        # If the graph was saved, and some commands were undone, and another command is being pushed => the graph
        # will never be the same as the one that had been saved, so we "clear" the savedGraphIndex (=-1).
        # It must be done in first because self.index will me incremented then!
        if self.savedGraphIndex > self.index:
            self.savedGraphIndex = -1

        # Clear the redoable part of commands
        for command in self.commands[self.index:]:
            self.commands.pop(self.commands.index(command))

        # Push the new command into the undo part
        self.commands.append(newCommand)

        # Do the command
        res = newCommand.doCmd()
        self.index += 1

        # We update buttleData to indicate that something just changed
        self.graphHadChanged()

        return res

    def redo(self):
        """
        Redoes the last undone command.
        """
        if self.canRedo():
            self.commands[self.index].redoCmd()
            self.index += 1

            # We update buttleData to indicates that the graph just changed
            self.graphHadChanged()

    def undo(self):
        """
        Undoes the last command.
        """
        if self.canUndo():
            self.index -= 1
            self.commands[self.index].undoCmd()

            # We update buttleData to indicates that the graph just changed
            self.graphHadChanged()


globalCommandManager = CommandManager()
