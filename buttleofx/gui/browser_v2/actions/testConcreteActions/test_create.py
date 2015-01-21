import unittest
import tempfile
import os

from OpenGL import GL

from buttleofx.gui.browser_v2.browserItem import BrowserItem
from buttleofx.gui.browser_v2.actions.concreteActions.create import Create


class TestCreate(unittest.TestCase):

    # Before tests run
    def setUp(self):
        pass

    def test_file_create(self):
        with tempfile.TemporaryDirectory() as path:
            filename = 'new_file.txt'
            parent_name = 'parent'
            parent_path = os.path.join(path, parent_name)
            file_path = os.path.join(parent_path, filename)

            # Create parent folder
            os.makedirs(parent_path)

            # File should not exists
            self.assertFalse(os.path.exists(file_path))

            parent = BrowserItem(path, parent_name, 2, True)
            new_file = BrowserItem(parent_path, filename, 1, True)

            # Create file
            cr = Create(parent, new_file)
            cr.process()

            # File should not exists
            self.assertTrue(os.path.exists(file_path))

    def test_folder_create(self):
        with tempfile.TemporaryDirectory() as path:
            folder_name = 'new_folder'
            parent_name = 'parent'
            parent_path = os.path.join(path, parent_name)
            folder_path = os.path.join(parent_path, folder_name)

            # Create parent folder
            os.makedirs(parent_path)

            # Folder should not exists
            self.assertFalse(os.path.exists(folder_path))

            parent = BrowserItem(path, parent_name, 2, True)
            new_folder = BrowserItem(parent_path, folder_name, 2, True)

            # Create folder
            cr = Create(parent, new_folder)
            cr.process()

            # Folder should not exists
            self.assertTrue(os.path.exists(folder_path))

    # After tests run
    def tearDown(self):
        pass
