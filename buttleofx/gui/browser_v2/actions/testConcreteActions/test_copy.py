import unittest
import tempfile
import os

from OpenGL import GL

from buttleofx.gui.browser_v2.browserItem import BrowserItem
from buttleofx.gui.browser_v2.actions.concreteActions.copy import Copy


class TestCopy(unittest.TestCase):

    # Before tests run
    def setUp(self):
        pass

    def test_file_copy(self):
        with tempfile.TemporaryDirectory() as path:
            src_filename = 'copy_file.txt'
            src_file_path = os.path.join(path, src_filename)
            dest_folder_name = 'parent'
            dest_folder_path = os.path.join(path, dest_folder_name)
            dest_file_path = os.path.join(dest_folder_path, src_filename)

            # Create original file
            open(src_file_path, 'a').close()

            # Create parent folder
            os.makedirs(dest_folder_path)

            # File should exists in original directory
            self.assertTrue(os.path.exists(src_file_path))

            # File should not exists in destination directory
            self.assertFalse(os.path.exists(dest_file_path))

            dest = BrowserItem(path, dest_folder_name, 2, True)
            file = BrowserItem(path, src_filename, 1, True)

            # Copy file
            cpy = Copy(file, dest)
            cpy.process()

            # File should exists in source folder
            self.assertTrue(os.path.exists(src_file_path))

            # File should exists in destination folder
            self.assertTrue(os.path.exists(dest_file_path))

    def test_folder_copy(self):
        with tempfile.TemporaryDirectory() as path:
            src_folder_name = 'copy_folder'
            src_folder_path = os.path.join(path, src_folder_name)
            parent_folder_name = 'parent'
            parent_folder_path = os.path.join(path, parent_folder_name)
            dest_folder_path = os.path.join(parent_folder_path, src_folder_name)

            # Create source folder
            os.makedirs(src_folder_path)

            # Folder should not exists
            self.assertFalse(os.path.exists(dest_folder_path))

            folder = BrowserItem(path, src_folder_name, 2, True)
            parent = BrowserItem(path, parent_folder_name, 2, True)

            # Copy folder
            cpy = Copy(folder, parent)
            cpy.process()

            # Folder should exists in destination folder
            self.assertTrue(os.path.exists(dest_folder_path))

            # Folder should exists in destination folder
            self.assertTrue(os.path.exists(dest_folder_path))

    # After tests run
    def tearDown(self):
        pass
