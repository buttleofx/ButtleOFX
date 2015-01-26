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
        self._source = copy.deepcopy(browserItem)
        self._destination = destination

    def action(self):
        browserItem = self.getBrowserItem()
        destination = self._destination
        destinationPath = destination.getPath()

        # Copy file
        if browserItem.isFile():
            # TODO: Check destination permission in try catch
            if os.path.exists(destinationPath):
                shutil.copy2(browserItem.getPath(), destinationPath)
                filename = browserItem.getName()
                browserItem.updatePath(os.path.join(destinationPath, filename))
                # self.processed = True or browserItem.processed = True

        # Copy Folder
        if browserItem.isFolder():
            # TODO: Check destination permission in try catch
            shutil.copytree(browserItem.getParentPath(), destinationPath)
            browserItem.updatePath(destinationPath)

    def revert(self):
        browserItem = self._source

        if browserItem.isFile():
            pass
