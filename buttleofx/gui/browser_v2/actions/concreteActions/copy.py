import os
import shutil
import copy

from buttleofx.gui.browser_v2.actions.actionInterface import ActionInterface


class Copy(ActionInterface):

    def __init__(self, browserItem, destination):
        # destination must be a directory
        if not destination.isFolder():
            raise TypeError
        super().__init__(browserItem)
        self._srcPath = browserItem.getParentPath()
        self._destPath = destination.getPath()

    def execute(self):
        browserItem = self.getBrowserItem()
        destPath = self._destPath

        # Copy file
        if browserItem.isFile():
            # TODO: Check destination permission in try catch
            if os.path.exists(destPath):
                shutil.copy2(browserItem.getPath(), destPath)
                # filename = browserItem.getName()
                # browserItem.updatePath(os.path.join(destPath, filename))
                # self.processed = True or browserItem.processed = True

        # Copy Folder
        if browserItem.isFolder():
            # TODO: Check destination permission in try catch
            shutil.copytree(browserItem.getParentPath(), destPath)
            # browserItem.updatePath(destPath)

    def revert(self):
        browserItem = self.getBrowserItem()
        browserItemName = browserItem.getName()
        destPath = self._destPath

        if browserItem.isFile():
            os.remove(os.path.join(destPath, browserItem.getName()))

        if browserItem.isFolder():
            shutil.rmtree(destPath)
