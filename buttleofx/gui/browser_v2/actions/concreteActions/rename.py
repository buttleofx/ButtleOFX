import os

from buttleofx.gui.browser_v2.actions.actionInterface import ActionInterface


class Rename(ActionInterface):

    def __init__(self, browserItem, newName):
        super().__init__(browserItem)
        self._newName = newName

    def execute(self):
        browserItem = self._browserItem
        # Rename File
        if browserItem.isFile():
            # TODO: Check permission in try catch
            path = browserItem.getParentPath()
            oldFilePath = os.path.join(path, browserItem.getName())
            newFileName = self._newName
            newFilePath = os.path.join(path, newFileName)


            if not os.path.splitext(newFilePath)[1]:
                oldFileExtension = os.path.splitext(oldFilePath)[1]
                newFilePath += oldFileExtension
            os.rename(oldFilePath, newFilePath)
            browserItem.updatePath(newFilePath)


        # Rename Folder
        if browserItem.isFolder():
            # TODO: Check permission in try catch
            path = browserItem.getParentPath()
            oldPath = os.path.join(path, browserItem.getName())
            newPath = os.path.join(path, self._newName)
            os.rename(oldPath, newPath)
            browserItem.updatePath(newPath)

        # TODO: Rename sequence
        if browserItem.isSequence():
            print("TODO: Rename sequence")
