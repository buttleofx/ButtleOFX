import unittest
import tempfile
import os

from buttleofx.gui.browser_v2.browserItem import BrowserItem
from buttleofx.gui.browser_v2.actions.concreteActions.create import Create
from pySequenceParser import sequenceParser


class TestCreate(unittest.TestCase):

    # Before tests run
    def setUp(self):
        pass

    def test_file_create_execute(self):
        with tempfile.TemporaryDirectory() as path:
            filename = 'new_file.txt'
            parent_name = 'parent'
            parent_path = os.path.join(path, parent_name)
            file_path = os.path.join(parent_path, filename)

            # Create parent folder
            os.makedirs(parent_path)

            # File should not exists
            self.assertFalse(os.path.exists(file_path))

            sp_parent = sequenceParser.Item(sequenceParser.eTypeFolder,
                                            parent_path)
            sp_new_file = sequenceParser.Item(sequenceParser.eTypeFile,
                                              file_path)
            parent = BrowserItem(sp_parent, True)
            new_file = BrowserItem(sp_new_file, True)

            # Create file
            cr = Create(parent, new_file)
            cr.process()

            # File should not exists
            self.assertTrue(os.path.exists(file_path))

    def test_file_create_execute(self):
        with tempfile.TemporaryDirectory() as path:
            filename = 'new_file.txt'
            parent_name = 'parent'
            parent_path = os.path.join(path, parent_name)
            file_path = os.path.join(parent_path, filename)

            # Create parent folder
            os.makedirs(parent_path)

            # File should not exists
            self.assertFalse(os.path.exists(file_path))

            sp_parent = sequenceParser.Item(sequenceParser.eTypeFolder,
                                            parent_path)
            sp_new_file = sequenceParser.Item(sequenceParser.eTypeFile,
                                              file_path)
            parent = BrowserItem(sp_parent, True)
            new_file = BrowserItem(sp_new_file, True)

            # Create file
            cr = Create(parent, new_file)
            cr.process()

            # File should not exists
            self.assertTrue(os.path.exists(file_path))

    def test_folder_create_execute(self):
        with tempfile.TemporaryDirectory() as path:
            folder_name = 'new_folder'
            parent_name = 'parent'
            parent_path = os.path.join(path, parent_name)
            folder_path = os.path.join(parent_path, folder_name)

            # Create parent folder
            os.makedirs(parent_path)

            # Folder should not exists
            self.assertFalse(os.path.exists(folder_path))

            sp_parent = sequenceParser.Item(sequenceParser.eTypeFolder,
                                            parent_path)
            sp_new_folder = sequenceParser.Item(sequenceParser.eTypeFolder,
                                                folder_path)
            parent = BrowserItem(sp_parent, True)
            new_folder = BrowserItem(sp_new_folder, True)

            # Create folder
            cr = Create(parent, new_folder)
            cr.process()

            # Folder should not exists
            self.assertTrue(os.path.exists(folder_path))

    # After tests run
    def tearDown(self):
        pass
