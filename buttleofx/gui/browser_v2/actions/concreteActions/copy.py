import os
import shutil

from buttleofx.gui.browser_v2.actions.actionInterface import ActionInterface


class Copy(ActionInterface):

    def __init__(self, browserItem):
        # destination must be a directory
        # if not destination.isFolder():
        #     raise TypeError
        super().__init__(browserItem)
        self._srcPath = browserItem.getParentPath()
        self._destPath = ""
        self._framesPaths = []

    def setDestinationPath(self, newPath):
        self._destPath = newPath.strip()

    def execute(self):
        browserItem = self._browserItem
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
            shutil.copytree(browserItem.getPath(), os.path.join(destPath, browserItem.getName()))
            # browserItem.updatePath(destPath)

        if browserItem.isSequence():
            seqParsed = browserItem.getSequence().getSequenceParsed()
            frames = seqParsed.getFramesIterable()

            for f in frames:
                # logging.debug(f)
                filename = seqParsed.getFilenameAt(f)
                # logging.debug(filename)
                filePath = os.path.join(browserItem.getParentPath(), filename)
                # logging.debug(file_path)
                if os.path.exists(destPath):
                    shutil.copy2(filePath, destPath)
                    self._framesPaths.append(os.path.join(destPath, filename))

            # browserItem.

    def revert(self):
        browserItem = self.getBrowserItem()
        browserItemName = browserItem.getName()
        destPath = self._destPath

        if browserItem.isFile():
            os.remove(os.path.join(destPath, browserItemName))

        if browserItem.isFolder():
            shutil.rmtree(destPath)

        if browserItem.isSequence():
            for f in self._framesPaths:
                os.remove(f)
