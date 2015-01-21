import unittest
import tempfile
import os
import shutil

from OpenGL import GL

from buttleofx.gui.browser_v2.browserItem import BrowserItem
from buttleofx.gui.browser_v2.actions.concreteActions.delete import Delete


class TestDelete(unittest.TestCase):

    # Before tests run
    def setUp(self):
        pass

    def test_file_delete(self):
        with tempfile.TemporaryDirectory() as path:
            filename = 'delete_me.txt'
            file_path = os.path.join(path, filename)
            if os.path.exists(file_path):
                os.remove(file_path)

            # File should not exists
            self.assertFalse(os.path.exists(file_path))

            # Create file
            open(file_path, 'a').close()

            # File should exists
            self.assertTrue(os.path.exists(file_path))

            bi = BrowserItem(path, filename, 1, True)

            # Delete file
            de = Delete(bi)
            de.process()

            # File should not exists
            self.assertFalse(os.path.exists(file_path))

    def test_folder_delete(self):
        with tempfile.TemporaryDirectory() as path:
            folder_name = 'delete_me'
            folder_path = os.path.join(path, folder_name)
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)

            # Folder should not exists
            self.assertFalse(os.path.exists(folder_path))

            # Create folder
            os.makedirs(folder_path)

            # Folder should exists
            self.assertTrue(os.path.exists(folder_path))

            bi = BrowserItem(path, folder_name, 2, True)

            # Delete folder
            de = Delete(bi)
            de.process()

            # Folder should not exists
            self.assertFalse(os.path.exists(folder_path))

    # After tests run
    def tearDown(self):
        pass

