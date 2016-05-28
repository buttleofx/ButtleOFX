import os
import shutil
import logging

from buttleofx.gui.browser.actions.actionInterface import ActionInterface


class Create(ActionInterface):

    def __init__(self, parentBrowserItem, newBrowserItem):
        # Parent must be a directory
        if not parentBrowserItem.isFolder():
            raise TypeError
        ActionInterface.__init__(self, parentBrowserItem)
        # TODO: Can a new item be a sequence ?
        self._newBrowserItem = newBrowserItem

    def execute(self):
        # TODO: Check parent's permission in try catch
        # TODO: find elegant way to find next: sort, find next if match then extract version number
        parent = self.getBrowserItem()
        newBrowserItem = self._newBrowserItem
        parentPath = parent.getPath()
        filePath = os.path.join(parentPath, newBrowserItem.getName())

        if not os.path.exists(parentPath):
            return

        if os.path.exists(filePath):
            if newBrowserItem.isFile():
                filePathTmp = filePath[:-len(newBrowserItem.getFileExtension())]+'_'
                extension = newBrowserItem.getFileExtension()
                cpt = 1
                while cpt < 1000:
                    if not os.path.exists(filePathTmp+str(cpt)+extension):
                        filePath = filePathTmp+str(cpt)+extension
                        break
                    cpt += 1

            elif newBrowserItem.isFolder():
                cpt = 1
                while cpt < 1000:
                    if not os.path.exists(filePath+'_'+str(cpt)):
                        filePath = filePath+'_'+str(cpt)
                        break
                    cpt += 1
        logging.debug(newBrowserItem.getFileExtension())
        if newBrowserItem.isFile():
            open(filePath, 'a').close()
        if newBrowserItem.isFolder():
            os.makedirs(filePath)

        self._newBrowserItem.updatePath(filePath)

    def revert(self):
        browserItem = self._newBrowserItem
        browserItemPath = self._newBrowserItem.getPath()

        if not os.path.exists(browserItemPath):
            return

        if browserItem.isFile():
            os.remove(browserItemPath)

        if browserItem.isFolder():
            shutil.rmtree(browserItemPath)

