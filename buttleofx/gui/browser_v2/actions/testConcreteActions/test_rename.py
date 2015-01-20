import unittest
import os
import shutil

import inspect

from OpenGL import GL

from buttleofx.gui.browser_v2.browserItem import BrowserItem
from buttleofx.gui.browser_v2.actions.concreteActions.rename import Rename


class TestRename(unittest.TestCase):
    # Before tests run
    def setUp(self):
        self._directory = "buttle_test"
        self._base_path = os.path.expanduser("~")
        self._path = os.path.join(self._base_path, self._directory)

        if os.path.exists(self._path):
            shutil.rmtree(self._path)
        os.makedirs(self._path)

    def test_rename_file_with_extension(self):
        extension = ".txt"
        old_filename = "plop" + extension
        old_file_path = os.path.join(self._path, old_filename)
        new_filename = "success" + extension
        new_file_path = os.path.join(self._path, new_filename)

        # Create old file
        open(old_file_path, 'a').close()

        bi = BrowserItem(self._path, old_filename, 1, True)
        re = Rename(bi, new_filename)
        re.process()
        self.assertTrue(os.path.exists(new_file_path))
        self.assertEqual(bi.getPath(), new_file_path)

    def test_rename_file_without_extension(self):
        extension = ".jpg"
        old_filename = "plop" + extension
        new_filename = "no_extension"

        # Create old file
        open(os.path.join(self._path, old_filename), 'a').close()

        bi = BrowserItem(self._path, old_filename, 1, True)
        re = Rename(bi, new_filename)
        re.process()
        new_file_path = os.path.join(self._path, new_filename + extension)
        self.assertTrue(self, os.path.exists(new_file_path))
        self.assertEqual(bi.getPath(), new_file_path)

    def test_rename_folder(self):
        old_folder_name = 'rename_me'
        new_folder_name = 'new_name'
        old_folder_path = os.path.join(self._path, old_folder_name)
        if not os.path.exists(old_folder_path):
            os.makedirs(old_folder_path)

        bi = BrowserItem(self._path, old_folder_name, 1, True)
        re = Rename(bi, new_folder_name)
        re.process()
        new_folder_path = os.path.join(self._path, new_folder_name)
        self.assertTrue(self, os.path.exists(new_folder_path))
        self.assertEqual(bi.getPath(), new_folder_path)

    # After tests run
    def tearDown(self):
        if os.path.exists(self._path):
            shutil.rmtree(self._path)

if __name__ == "__main__":
    unittest.main()

