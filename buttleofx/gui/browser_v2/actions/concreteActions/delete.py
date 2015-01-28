import os
import shutil

from buttleofx.gui.browser_v2.actions.actionInterface import ActionInterface


class Delete(ActionInterface):

    def __init__(self, browserItem):
        super().__init__(browserItem)

    def action(self):
        browserItem = self.getBrowserItem()

        # Delete file
        if browserItem.isFile():
            # TODO: Check permission in try catch
            browserItemPath = browserItem.getPath()
            if os.path.exists(browserItemPath):
                os.remove(browserItemPath)

        # Delete folder
        if browserItem.isFolder():
            # TODO: Check permission in try catch
            browserItemPath = browserItem.getPath()
            if os.path.exists(browserItemPath):
                shutil.rmtree(browserItemPath)

        # Delete sequence
        if browserItem.isSequence():
            print("TODO: Delete sequence")
