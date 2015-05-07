import os
import shutil

from buttleofx.gui.browser_v2.actions.actionInterface import ActionInterface


class Move(ActionInterface):

    def __init__(self, browserItem):
        # destination must be a directory
        # if not destination.isFolder():
        #     raise TypeError
        super().__init__(browserItem)
        self._srcPath = browserItem.getParentPath()
        self._destPath = ""

    def setDestinationPath(self, newPath):
        self._destPath = newPath.strip()

    def execute(self):
        browserItem = self._browserItem
        destinationPath = self._destPath

        # Move file, folder, and sequence
        # TODO: Check destination permission in try catch
        if browserItem.isFile() or browserItem.isFolder():
            if os.path.exists(destinationPath):
                shutil.move(browserItem.getPath(), destinationPath)

    def revert(self):
        browserItem = self._browserItem
        srcPath = self._srcPath
        destPath = self._destPath
        destItemPath = os.path.join(destPath, browserItem.getName())

        if browserItem.isFile() or browserItem.isFolder():
            if os.path.exists(srcPath):
                shutil.move(destItemPath, srcPath)
