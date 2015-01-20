import os

from buttleofx.gui.browser_v2.actions.actionInterface import ActionInterface
from buttleofx.gui.browser_v2.browserItem import BrowserItem


class Rename(ActionInterface):

    def __init__(self, browserItem, newName):
        super().__init__(browserItem)
        self._newName = newName

    def action(self):
        # Rename File
        if self.getBrowserItem().getType() == BrowserItem.ItemType.file:
            # TODO: Check permission in try catch
            path = self.getBrowserItem().getParentPath()
            oldFilePath = os.path.join(path, self.getBrowserItem().getName())
            newFileName = self._newName
            newFilePath = os.path.join(path, newFileName)
            os.rename(oldFilePath, newFilePath)

        # Rename Folder
        if self.getBrowserItem().getType() == BrowserItem.ItemType.folder:
            # TODO: Check permission in try catch
            path = self.getBrowserItem().getParentPath()
            oldPath = os.path.join(path, self.getBrowserItem().getName())
            newPath = os.path.join(path, self._newName)
            os.rename(oldPath, newPath)

        # TODO: Rename sequence
        if self.getBrowserItem().getType() == BrowserItem.ItemType.sequence:
            print("TODO: Rename sequence")


