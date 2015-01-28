import unittest
import tempfile
import os

# from OpenGL import GL

from buttleofx.gui.browser_v2.browserItem import BrowserItem
from buttleofx.gui.browser_v2.actions.concreteActions.move import Move
from pySequenceParser import sequenceParser


class TestMove(unittest.TestCase):

    # Before tests run
    def setUp(self):
        pass

    def test_file_move(self):
        with tempfile.TemporaryDirectory() as path:
            filename = 'new_file.txt'
            dest_folder_name = 'parent'
            dest_folder_path = os.path.join(path, dest_folder_name)
            src_file_path = os.path.join(path, filename)
            dest_file_path = os.path.join(dest_folder_path, filename)

            # Create file
            open(src_file_path, 'a').close()

            # Create destination folder
            os.makedirs(dest_folder_path)

            # File should exists in source folder
            self.assertTrue(os.path.exists(src_file_path))

            # File should not exists in destination folder
            self.assertFalse(os.path.exists(dest_file_path))

            sp_dest = sequenceParser.Item(sequenceParser.eTypeFolder,
                                          dest_folder_path)
            sp_file = sequenceParser.Item(sequenceParser.eTypeFile,
                                          src_file_path)
            dest = BrowserItem(sp_dest, True)
            file = BrowserItem(sp_file, True)

            # Move file
            mv = Move(file, dest)
            mv.process()

            # File should not exists in source folder
            self.assertFalse(os.path.exists(src_file_path))

            # File should exists in destination folder
            self.assertTrue(os.path.exists(dest_file_path))

    def test_file_move_revert(self):
        with tempfile.TemporaryDirectory() as path:
            filename = 'new_file.txt'
            dest_folder_name = 'parent'
            dest_folder_path = os.path.join(path, dest_folder_name)
            src_file_path = os.path.join(path, filename)
            dest_file_path = os.path.join(dest_folder_path, filename)

            # Create file
            open(src_file_path, 'a').close()

            # Create destination folder
            os.makedirs(dest_folder_path)

            # File should exists in source folder
            self.assertTrue(os.path.exists(src_file_path))

            # File should not exists in destination folder
            self.assertFalse(os.path.exists(dest_file_path))

            sp_dest = sequenceParser.Item(sequenceParser.eTypeFolder,
                                          dest_folder_path)
            sp_file = sequenceParser.Item(sequenceParser.eTypeFile,
                                          src_file_path)
            dest = BrowserItem(sp_dest, True)
            file = BrowserItem(sp_file, True)

            # Move file
            mv = Move(file, dest)
            mv.process()

            # File should not exists in source folder
            self.assertFalse(os.path.exists(src_file_path))

            # File should exists in destination folder
            self.assertTrue(os.path.exists(dest_file_path))

            mv.revert()

            # File should exists in source folder
            self.assertTrue(os.path.exists(src_file_path))

            # File should not exists in destination folder
            self.assertFalse(os.path.exists(dest_file_path))


    def test_folder_move(self):
        with tempfile.TemporaryDirectory() as path:
            src_folder_name = 'new_folder'
            src_folder_path = os.path.join(path, src_folder_name)
            dest_folder_name = 'parent'
            dest_folder_path = os.path.join(path, dest_folder_name)
            folder_moved_path = os.path.join(dest_folder_path, src_folder_name)

            # Create folder
            os.makedirs(src_folder_path)

            # Create destination folder
            os.makedirs(dest_folder_path)

            # Source folder should exists
            self.assertTrue(os.path.exists(src_folder_path))

            # Destination folder should exists
            self.assertTrue(os.path.exists(dest_folder_path))

            # Source folder should not exist in destination folder
            self.assertFalse(os.path.exists(folder_moved_path))

            sp_dest_folder = sequenceParser.Item(sequenceParser.eTypeFolder,
                                                 dest_folder_path)
            sp_src_folder = sequenceParser.Item(sequenceParser.eTypeFolder,
                                                src_folder_path)
            dest_folder = BrowserItem(sp_dest_folder, True)
            src_folder = BrowserItem(sp_src_folder, True)

            # Move folder
            mv = Move(src_folder, dest_folder)
            mv.process()

            # Source folder should not exists
            self.assertFalse(os.path.exists(src_folder_path))

            # Source folder should exists in destination folder
            self.assertTrue(os.path.exists(folder_moved_path))

    def test_folder_move_revert(self):
        with tempfile.TemporaryDirectory() as path:
            src_folder_name = 'new_folder'
            src_folder_path = os.path.join(path, src_folder_name)
            dest_folder_name = 'parent'
            dest_folder_path = os.path.join(path, dest_folder_name)
            folder_moved_path = os.path.join(dest_folder_path, src_folder_name)

            # Create folder
            os.makedirs(src_folder_path)

            # Create destination folder
            os.makedirs(dest_folder_path)

            # Source folder should exists
            self.assertTrue(os.path.exists(src_folder_path))

            # Destination folder should exists
            self.assertTrue(os.path.exists(dest_folder_path))

            # Source folder should not exist in destination folder
            self.assertFalse(os.path.exists(folder_moved_path))

            sp_dest_folder = sequenceParser.Item(sequenceParser.eTypeFolder,
                                                 dest_folder_path)
            sp_src_folder = sequenceParser.Item(sequenceParser.eTypeFolder,
                                                src_folder_path)
            dest_folder = BrowserItem(sp_dest_folder, True)
            src_folder = BrowserItem(sp_src_folder, True)

            # Move folder
            mv = Move(src_folder, dest_folder)
            mv.process()

            # Source folder should not exists
            self.assertFalse(os.path.exists(src_folder_path))

            # Source folder should exists in destination folder
            self.assertTrue(os.path.exists(folder_moved_path))

            mv.revert()

            # Source folder should exists
            self.assertFalse(os.path.exists(src_folder_path))

            # Source folder should not exists in destination folder
            self.assertTrue(os.path.exists(folder_moved_path))


    # After tests run
    def tearDown(self):
        pass
