import unittest
import tempfile
import os

# from OpenGL import GL

from buttleofx.gui.browser.browserItem import BrowserItem
from buttleofx.gui.browser.actions.concreteActions.move import Move
from pySequenceParser import sequenceParser


class TestMove(unittest.TestCase):

    # Before tests run
    def setUp(self):
        pass

    def test_move_file_execute(self):
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
            dest = BrowserItem(sp_dest)
            file = BrowserItem(sp_file)

            # Move file
            mv = Move(file)
            mv.setDestinationPath(dest_folder_path)
            mv.process()

            # File should not exists in source folder
            self.assertFalse(os.path.exists(src_file_path))

            # File should exists in destination folder
            self.assertTrue(os.path.exists(dest_file_path))

    def test_move_file_revert(self):
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
            dest = BrowserItem(sp_dest)
            file = BrowserItem(sp_file)

            # Move file
            mv = Move(file)
            mv.setDestinationPath(dest_folder_path)
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

    def test_move_folder_execute(self):
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
            dest_folder = BrowserItem(sp_dest_folder)
            src_folder = BrowserItem(sp_src_folder)

            # Move folder
            mv = Move(src_folder)
            mv.setDestinationPath(dest_folder_path)
            mv.process()

            # Source folder should not exists
            self.assertFalse(os.path.exists(src_folder_path))

            # Source folder should exists in destination folder
            self.assertTrue(os.path.exists(folder_moved_path))

    def test_move_folder_revert(self):
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
            dest_folder = BrowserItem(sp_dest_folder)
            src_folder = BrowserItem(sp_src_folder)

            # Move folder
            mv = Move(src_folder)
            mv.setDestinationPath(dest_folder_path)
            mv.process()

            # Source folder should not exists
            self.assertFalse(os.path.exists(src_folder_path))

            # Source folder should exists in destination folder
            self.assertTrue(os.path.exists(folder_moved_path))

            mv.revert()

            # Source folder should exists
            self.assertTrue(os.path.exists(src_folder_path))

            # Source folder should not exists in destination folder
            self.assertFalse(os.path.exists(folder_moved_path))

    # After tests run
    def tearDown(self):
        pass
