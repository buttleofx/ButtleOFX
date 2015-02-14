import unittest
import tempfile
import os

# from OpenGL import GL

from buttleofx.gui.browser_v2.browserItem import BrowserItem
from buttleofx.gui.browser_v2.actions.concreteActions.rename import Rename
from pySequenceParser import sequenceParser

class TestRename(unittest.TestCase):

    # Before tests run
    def setUp(self):
        pass

    def test_rename_file_with_extension(self):
        with tempfile.TemporaryDirectory() as path:
            extension = ".txt"
            old_filename = "plop" + extension
            old_file_path = os.path.join(path, old_filename)
            new_filename = "success" + extension
            new_file_path = os.path.join(path, new_filename)

            # Create file
            open(old_file_path, 'a').close()

            sp_file = sequenceParser.Item(sequenceParser.eTypeFile,
                                          old_file_path)
            bi = BrowserItem(sp_file, True)

            # New file should not exists
            self.assertFalse(os.path.exists(new_file_path))

            # Rename file
            re = Rename(bi, new_filename)
            re.process()

            # Old file should not exists
            self.assertFalse(os.path.exists(old_file_path))

            # New file should exists
            self.assertTrue(os.path.exists(new_file_path))

            # Browser item's path and new file path should be equal
            self.assertEqual(bi.getPath(), new_file_path)

    def test_rename_file_with_extension_revert(self):
        with tempfile.TemporaryDirectory() as path:
            extension = ".txt"
            old_filename = "plop" + extension
            old_file_path = os.path.join(path, old_filename)
            new_filename = "success" + extension
            new_file_path = os.path.join(path, new_filename)

            # Create file
            open(old_file_path, 'a').close()

            sp_file = sequenceParser.Item(sequenceParser.eTypeFile,
                                          old_file_path)
            bi = BrowserItem(sp_file, True)

            # New file should not exists
            self.assertFalse(os.path.exists(new_file_path))

            # Rename file
            re = Rename(bi, new_filename)
            re.process()

            # Old file should not exists
            self.assertFalse(os.path.exists(old_file_path))

            # New file should exists
            self.assertTrue(os.path.exists(new_file_path))

            # Browser item's path and new file path should be equal
            self.assertEqual(bi.getPath(), new_file_path)

            re.revert()
            # Old file should exists
            self.assertTrue(os.path.exists(old_file_path))

            # New file should not exists
            self.assertFalse(os.path.exists(new_file_path))

            # Browser item's path and old file path should be equal
            self.assertEqual(bi.getPath(), old_file_path)

    def test_rename_file_without_extension(self):
        with tempfile.TemporaryDirectory() as path:
            extension = ".jpg"
            old_filename = "plop" + extension
            old_file_path = os.path.join(path, old_filename)
            new_filename = "no_extension"
            new_file_path = os.path.join(path, new_filename + extension)

            # Create file
            open(os.path.join(path, old_filename), 'a').close()
            sp_file = sequenceParser.Item(sequenceParser.eTypeFile,
                                          old_file_path)
            bi = BrowserItem(sp_file, True)

            # Rename file
            re = Rename(bi, new_filename)
            re.process()

            # Old file should not exists
            self.assertFalse(os.path.exists(old_file_path))

            # New file should exists
            self.assertTrue(os.path.exists(new_file_path))

            # Browser item's path and new file path should be equal
            self.assertEqual(bi.getPath(), new_file_path)

    def test_rename_file_without_extension_revert(self):
        with tempfile.TemporaryDirectory() as path:
            extension = ".jpg"
            old_filename = "plop" + extension
            old_file_path = os.path.join(path, old_filename)
            new_filename = "no_extension"
            new_file_path = os.path.join(path, new_filename + extension)

            # Create file
            open(os.path.join(path, old_filename), 'a').close()
            sp_file = sequenceParser.Item(sequenceParser.eTypeFile,
                                          old_file_path)
            bi = BrowserItem(sp_file, True)

            # Rename file
            re = Rename(bi, new_filename)
            re.process()

            # Old file should not exists
            self.assertFalse(os.path.exists(old_file_path))

            # New file should exists
            self.assertTrue(os.path.exists(new_file_path))

            # Browser item's path and new file path should be equal
            self.assertEqual(bi.getPath(), new_file_path)

            re.revert()

            # Old file should exists
            self.assertTrue(os.path.exists(old_file_path))

            # New file should not exists
            self.assertFalse(os.path.exists(new_file_path))

            # Browser item's path and old file path should be equal
            self.assertEqual(bi.getPath(), old_file_path)


    def test_rename_folder(self):
        with tempfile.TemporaryDirectory() as path:
            old_folder_name = 'rename_me'
            old_folder_path = os.path.join(path, old_folder_name)
            new_folder_name = 'new_name'
            new_folder_path = os.path.join(path, new_folder_name)

            # Create folder
            if not os.path.exists(old_folder_path):
                os.makedirs(old_folder_path)

            sp_folder = sequenceParser.Item(sequenceParser.eTypeFolder,
                                            old_folder_path)
            bi = BrowserItem(sp_folder, True)

            # Rename folder
            re = Rename(bi, new_folder_name)
            re.process()

            # Old folder should not exists
            self.assertFalse(os.path.exists(old_folder_path))

            # New folder should exists
            self.assertTrue(os.path.exists(new_folder_path))

            # Browser item's path and new folder path should be equal
            self.assertEqual(bi.getPath(), new_folder_path)

    def test_rename_folder_revert(self):
        with tempfile.TemporaryDirectory() as path:
            old_folder_name = 'rename_me'
            old_folder_path = os.path.join(path, old_folder_name)
            new_folder_name = 'new_name'
            new_folder_path = os.path.join(path, new_folder_name)

            # Create folder
            if not os.path.exists(old_folder_path):
                os.makedirs(old_folder_path)

            sp_folder = sequenceParser.Item(sequenceParser.eTypeFolder,
                                            old_folder_path)
            bi = BrowserItem(sp_folder, True)

            # Rename folder
            re = Rename(bi, new_folder_name)
            re.process()

            # Old folder should not exists
            self.assertFalse(os.path.exists(old_folder_path))

            # New folder should exists
            self.assertTrue(os.path.exists(new_folder_path))

            # Browser item's path and new folder path should be equal
            self.assertEqual(bi.getPath(), new_folder_path)

            re.revert()

            # Old folder should exists
            self.assertTrue(os.path.exists(old_folder_path))

            # New folder should not exists
            self.assertFalse(os.path.exists(new_folder_path))

            # Browser item's path and old folder path should be equal
            self.assertEqual(bi.getPath(), old_folder_path)

    # After tests run
    def tearDown(self):
        pass
