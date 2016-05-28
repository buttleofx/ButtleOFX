import os
import shutil
import os.path as op

from buttleofx.gui.browser.actions.actionInterface import ActionInterface


class Move(ActionInterface):

    def __init__(self, browserItem):
        ActionInterface.__init__(self, browserItem)
        self._srcPath = browserItem.getParentPath()
        self._destPath = ''

    def setDestinationPath(self, newPath):
        if not op.isdir(newPath):
            raise TypeError
        self._destPath = newPath.strip()

    def execute(self):
        browserItem = self._browserItem
        destinationPath = self._destPath
        copyPath = op.join(destinationPath, browserItem.getName())

        if browserItem.getPath() in destinationPath or op.exists(copyPath):
            self._failed = True
            return

        # Move file, folder, and sequence
        # TODO: Check destination permission in try catch
        if browserItem.isFile() or browserItem.isFolder():
            if op.exists(destinationPath):
                shutil.move(browserItem.getPath(), destinationPath)

    def revert(self):
        browserItem = self._browserItem
        srcPath = self._srcPath
        destPath = self._destPath
        destItemPath = op.join(destPath, browserItem.getName())

        if op.exists(op.join(srcPath, op.basename(destItemPath))):
            self._failed = True
            return

        if browserItem.isFile() or browserItem.isFolder():
            if op.exists(srcPath):
                shutil.move(destItemPath, srcPath)
