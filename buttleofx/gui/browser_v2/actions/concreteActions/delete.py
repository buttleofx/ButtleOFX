import os
import shutil

from buttleofx.gui.browser_v2.actions.actionInterface import ActionInterface
from buttleofx.gui.browser_v2.browserItem import BrowserItem


class Delete(ActionInterface):

    def __init__(self, browserItem):
        super().__init__(browserItem)

    def action(self):
        browserItem = self.getBrowserItem()

        if browserItem.isFile():
            # TODO: Check permission in try catch
            browserItemPath = browserItem.getPath()
            if os.path.exists(browserItemPath):
                os.remove(browserItemPath)

        # Delete Folder
        if browserItem.isFolder():
            # TODO: Check permission in try catch
            browserItemPath = browserItem.getPath()
            if os.path.exists(browserItemPath):
                shutil.rmtree(browserItemPath)

        # TODO: Rename sequence
        if browserItem.isSequence():
            print("TODO: Rename sequence")
