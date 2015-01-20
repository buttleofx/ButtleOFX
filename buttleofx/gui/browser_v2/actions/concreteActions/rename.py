import os

from buttleofx.gui.browser_v2.actions.actionInterface import ActionInterface
from buttleofx.gui.browser_v2.browserItem import BrowserItem


class Rename(ActionInterface):

    def __init__(self, browserItem, newName):
        super().__init__(browserItem)
        self._newName = newName

    def action(self):
        browserItem = self.getBrowserItem()
        # Rename File
        if browserItem.getType() == BrowserItem.ItemType.file:
            # TODO: Check permission in try catch
            path = browserItem.getParentPath()
            oldFilePath = os.path.join(path, browserItem.getName())
            newFileName = self._newName
            newFilePath = os.path.join(path, newFileName)


            if not os.path.splitext(newFilePath)[1]:
                oldFileExtension = os.path.splitext(oldFilePath)[1]
                newFilePath += oldFileExtension
            os.rename(oldFilePath, newFilePath)
            self.getBrowserItem().updatePath(newFilePath)


        # Rename Folder
        if browserItem.getType() == BrowserItem.ItemType.folder:
            # TODO: Check permission in try catch
            path = browserItem.getParentPath()
            oldPath = os.path.join(path, browserItem.getName())
            newPath = os.path.join(path, self._newName)
            os.rename(oldPath, newPath)

        # TODO: Rename sequence
        if browserItem.getType() == BrowserItem.ItemType.sequence:
            print("TODO: Rename sequence")


