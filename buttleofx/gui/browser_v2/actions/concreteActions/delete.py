import os
import shutil

from buttleofx.gui.browser_v2.actions.actionInterface import ActionInterface


class Delete(ActionInterface):

    def __init__(self, browserItem):
        super().__init__(browserItem)

    def execute(self):
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
            pass
            print("TODO: Delete sequence")
            # print(dir(browserItem))
            # print(browserItem.getPath())
            # print(dir(browserItem.getSequence()._sequence))
            # print(browserItem.getSequence()._sequence.getFilenameAt(0))
            # print(browserItem.getSequence()._sequence.getFirstFilename())
            # print(dir(browserItem.getSequence()._sequence.getFramesIterable()))
            # print(browserItem.getSequence()._sequence.getFiles())
            # i = 0
            # for f in browserItem.getSequence()._sequence.getFramesIterable():
                # print(i)
                # print(dir(f))
            # print(browserItem.getSequence())


