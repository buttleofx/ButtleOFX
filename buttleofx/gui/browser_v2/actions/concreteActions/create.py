import os

from buttleofx.gui.browser_v2.actions.actionInterface import ActionInterface


class Create(ActionInterface):

    def __init__(self, parentBrowserItem, newBrowserItem):
        # Parent must be a directory
        if not parentBrowserItem.isFolder():
            raise TypeError
        super().__init__(parentBrowserItem)
        # TODO: Can a new item be a sequence ?
        self._newBrowserItem = newBrowserItem

    def action(self):
        parent = self.getBrowserItem()
        newBrowserItem = self._newBrowserItem

        # Create file
        if newBrowserItem.isFile():
            # TODO: Check parent's permission in try catch
            parent_path = parent.getPath()
            file_name = newBrowserItem.getName()
            new_file_path = os.path.join(parent_path, file_name)
            if os.path.exists(parent_path):
                open(new_file_path, 'a').close()

        # Create Folder
        if newBrowserItem.isFolder():
            # TODO: Check parent's permission in try catch
            parent_path = parent.getPath()
            folder_name = newBrowserItem.getName()
            folder_path = os.path.join(parent_path, folder_name)
            if os.path.exists(parent_path):
                os.makedirs(folder_path)
