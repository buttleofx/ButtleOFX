import unittest
import tempfile
import os

# from OpenGL import GL

from buttleofx.gui.browser_v2.browserItem import BrowserItem
from buttleofx.gui.browser_v2.actions.concreteActions.copy import Copy
from pySequenceParser import sequenceParser


class TestCopy(unittest.TestCase):

    # Before tests run
    def setUp(self):
        pass

    def test_file_copy_execute(self):
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

            sp_file = sequenceParser.Item(sequenceParser.eTypeFile,
                                          src_file_path)
            sp_dest = sequenceParser.Item(sequenceParser.eTypeFolder,
                                          dest_folder_path)
            file = BrowserItem(sp_file, True)
            dest = BrowserItem(sp_dest, True)

            # Copy file
            cpy = Copy(file, dest)
            cpy.process()

            # File should exists in source folder
            self.assertTrue(os.path.exists(src_file_path))

            # File should exists in destination folder
            self.assertTrue(os.path.exists(dest_file_path))

            # File should have the new path
            self.assertEqual(file.getPath(), dest_file_path)

    def test_file_copy_revert(self):
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

            sp_file = sequenceParser.Item(sequenceParser.eTypeFile,
                                          src_file_path)
            sp_dest = sequenceParser.Item(sequenceParser.eTypeFolder,
                                          dest_folder_path)
            file = BrowserItem(sp_file, True)
            dest = BrowserItem(sp_dest, True)

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
            dest_folder_name = 'parent'
            dest_folder_path = os.path.join(path, dest_folder_name)
            dest_folder_path = os.path.join(dest_folder_path, src_folder_name)

            # Create source folder
            os.makedirs(src_folder_path)

            # Folder should not exists
            self.assertFalse(os.path.exists(dest_folder_path))

            sp_src = sequenceParser.Item(sequenceParser.eTypeFolder,
                                         src_folder_path)
            sp_dest = sequenceParser.Item(sequenceParser.eTypeFolder,
                                          dest_folder_path)
            src = BrowserItem(sp_src, True)
            dest = BrowserItem(sp_dest, True)

            # Copy folder
            cpy = Copy(src, dest)
            cpy.process()

            # Folder should exists in destination folder
            self.assertTrue(os.path.exists(dest_folder_path))

            # Folder should exists in destination folder
            self.assertTrue(os.path.exists(dest_folder_path))

            # Folder should have the new path
            self.assertEqual(src.getPath(), dest_folder_path)

    # After tests run
    def tearDown(self):
        pass
