import unittest
import os
import shutil

import inspect

from OpenGL import GL

from buttleofx.gui.browser_v2.browserItem import BrowserItem
from buttleofx.gui.browser_v2.actions.concreteActions.delete import Delete


class TestDelete(unittest.TestCase):
    # Before tests run
    def setUp(self):
        self._directory = "buttle_test_delete"
        self._base_path = os.path.expanduser("~")
        self._path = os.path.join(self._base_path, self._directory)
        if os.path.exists(self._path):
            shutil.rmtree(self._path)
        os.makedirs(self._path)

    def test_file_delete(self):
        filename = 'delete_me.txt'
        file_path = os.path.join(self._path, filename)
        if os.path.exists(file_path):
            os.remove(file_path)

        # File should not exists
        self.assertFalse(os.path.exists(file_path))

        # Create file
        open(file_path, 'a').close()

        # File should exists
        self.assertTrue(os.path.exists(file_path))

        # Delete file
        bi = BrowserItem(self._path, filename, 1, True)

        # Delete folder
        de = Delete(bi)
        de.process()

        # File should not exists
        self.assertFalse(os.path.exists(file_path))

    def test_folder_delete(self):
        folder_name = 'delete_me'
        folder_path = os.path.join(self._path, folder_name)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

        # Folder should not exists
        self.assertFalse(os.path.exists(folder_path))

        # Create folder
        os.makedirs(folder_path)

        # Folder should exists
        self.assertTrue(os.path.exists(folder_path))

        bi = BrowserItem(self._path, folder_name, 2, True)
        # Delete folder
        de = Delete(bi)
        de.process()

        # Folder should not exists
        self.assertFalse(os.path.exists(folder_path))

    # After tests run
    def tearDown(self):
        if os.path.exists(self._path):
            shutil.rmtree(self._path)

