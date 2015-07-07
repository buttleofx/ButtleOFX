import os
import shutil
import tempfile
from buttleofx.gui.browser_v2.actions.actionInterface import ActionInterface


class Delete(ActionInterface):

    def __init__(self, browserItem):
        ActionInterface.__init__(self, browserItem)
        self._tmp = tempfile.TemporaryDirectory()
        self._destItems = []

    def execute(self):
        browserItem = self.getBrowserItem()

        # Delete file
        # if browserItem.isFile():
        # TODO: Check permission in try catch
        # browserItemPath = browserItem.getPath()
        # if os.path.exists(browserItemPath):
        # os.remove(browserItemPath)

        # Delete folder
        if browserItem.isFile() or browserItem.isFolder():
            # TODO: Check permission in try catch
            browserItemPath = browserItem.getPath()
            if os.path.exists(browserItemPath):
                # shutil.rmtree(browserItemPath)
                shutil.move(browserItem.getPath(), self._tmp.name)
                dest_path = os.path.join(self._tmp.name, browserItem.getName())
                self._destItems.append(dest_path)

        # Delete sequence
        if browserItem.isSequence():
            seqParsed = browserItem.getSequence().getSequenceParsed()
            frames = seqParsed.getFramesIterable()

            for f in frames:
                filename = seqParsed.getFilenameAt(f)
                filePath = os.path.join(browserItem.getParentPath(), filename)
                shutil.move(filePath, self._tmp.name)
                self._destItems.append(os.path.join(self._tmp.name, filename))

    def revert(self):
        browserItem = self._browserItem

        if browserItem.isFile() or browserItem.isFolder():
            shutil.move(self._destItems[0], browserItem.getParentPath())

        if browserItem.isSequence():
            for item in self._destItems:
                shutil.move(item, browserItem.getParentPath())

    def __del__(self):
        self._tmp.cleanup()
