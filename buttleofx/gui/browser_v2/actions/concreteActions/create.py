import os

from buttleofx.gui.browser_v2.actions.actionInterface import ActionInterface


class Create(ActionInterface):

    def __init__(self, parentBrowserItem, newBrowserItem):
        # Parent must be a directory
        if not parentBrowserItem.isFolder():
            raise TypeError
        super().__init__(parentBrowserItem)
        # TODO: Can a new item be a sequence ?
        self._newBrowserItem = newBrowserItem

    def action(self):
        parent = self.getBrowserItem()
        newBrowserItem = self._newBrowserItem

        # Create file
        if newBrowserItem.isFile():
            # TODO: Check parent's permission in try catch
            parentPath = parent.getPath()
            fileName = newBrowserItem.getName()
            newFilePath = os.path.join(parentPath, fileName)
            if os.path.exists(parentPath):
                open(newFilePath, 'a').close()

        # Create Folder
        if newBrowserItem.isFolder():
            # TODO: Check parent's permission in try catch
            parentPath = parent.getPath()
            folderName = newBrowserItem.getName()
            folderPath = os.path.join(parentPath, folderName)
            if os.path.exists(parentPath):
                os.makedirs(folderPath)
