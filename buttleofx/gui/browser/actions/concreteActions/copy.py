import os
import shutil
import os.path as op

from buttleofx.gui.browser.actions.actionInterface import ActionInterface


class Copy(ActionInterface):

    def __init__(self, browserItem):
        ActionInterface.__init__(self, browserItem)
        self._srcPath = browserItem.getParentPath()
        self._destPath = ''
        self._framesPaths = []  # files sequences path copied
        self._successCopy = True

    def setDestinationPath(self, newPath):
        if not op.isdir(newPath):
            raise TypeError
        self._destPath = newPath.strip()

    def execute(self):
        browserItem = self._browserItem
        destPath = self._destPath

        # avoid recurse copy
        if not op.exists(destPath) or browserItem.getPath() in destPath:
            self._failed = True
            print('%s already in %s: fail to copy' % (destPath, browserItem.getPath()))
            return

        if browserItem.isFile():
            shutil.copy2(browserItem.getPath(), destPath)

        elif browserItem.isFolder():
            shutil.copytree(browserItem.getPath(), op.join(destPath, browserItem.getName()))

        elif browserItem.isSequence():
            seqParsed = browserItem.getSequence().getSequenceParsed()
            frames = seqParsed.getFramesIterable()

            for f in frames:
                filename = seqParsed.getFilenameAt(f)
                filePath = op.join(browserItem.getParentPath(), filename)
                try:
                    shutil.copy2(filePath, destPath)
                    self._framesPaths.append(op.join(destPath, filename))
                except Exception as e:
                    print(str(e))
                    pass

    def revert(self):
        browserItem = self.getBrowserItem()
        copiedPath = op.join(self._destPath, browserItem.getName())

        if browserItem.isFile() and op.exists(copiedPath):
            os.remove(copiedPath)

        if browserItem.isFolder() and op.exists(copiedPath):
            shutil.rmtree(copiedPath)

        if browserItem.isSequence():
            for f in self._framesPaths:
                if op.exists(f):
                    os.remove(f)
