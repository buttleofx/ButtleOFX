import unittest
import tempfile
import os

# from OpenGL import GL

from buttleofx.gui.browser_v2.browserItem import BrowserItem
from buttleofx.gui.browser_v2.actions.concreteActions.copy import Copy
from pySequenceParser import sequenceParser
import buttleofx.gui.browser_v2.actions.testConcreteActions.helper as h


class TestCopy(unittest.TestCase):

    # Before tests run
    def setUp(self):
        pass

    def test_copy_file_execute(self):
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
            cpy = Copy(file)
            cpy.setDestinationPath(dest_folder_path)
            cpy.process()

            # File should exists in source folder
            self.assertTrue(os.path.exists(src_file_path))

            # File should exists in destination folder
            self.assertTrue(os.path.exists(dest_file_path))

            # File should have the new path ? Maybe not
            # self.assertEqual(file.getPath(), dest_file_path)

    def test_copy_file_revert(self):
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
            cpy = Copy(file)
            cpy.setDestinationPath(dest_folder_path)
            cpy.process()

            # File should exists in source folder
            self.assertTrue(os.path.exists(src_file_path))

            # File should exists in destination folder
            self.assertTrue(os.path.exists(dest_file_path))

            # Copy ended, it's time to revert
            cpy.revert()

            # File should exists in source folder
            self.assertTrue(os.path.exists(src_file_path))

            # File should not exists in destination folder
            self.assertFalse(os.path.exists(dest_file_path))

    def test_copy_folder_execute(self):
        with tempfile.TemporaryDirectory() as path:
            src_folder_name = 'copy_folder'
            src_folder_path = os.path.join(path, src_folder_name)
            dest_parent_name = 'parent'
            dest_parent_path = os.path.join(path, dest_parent_name)
            dest_folder_path = os.path.join(dest_parent_path, src_folder_name)

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
            cpy = Copy(src)
            cpy.setDestinationPath(dest_folder_path)
            cpy.process()

            # Folder should exists in destination folder
            self.assertTrue(os.path.exists(dest_folder_path))

            # Folder should exists in destination folder
            self.assertTrue(os.path.exists(dest_folder_path))

            # Folder should have the new path
            # self.assertEqual(src.getPath(), dest_folder_path)

    def test_copy_folder_revert(self):
        with tempfile.TemporaryDirectory() as path:
            src_folder_name = 'copy_folder'
            src_folder_path = os.path.join(path, src_folder_name)
            dest_parent_name = 'parent'
            dest_parent_path = os.path.join(path, dest_parent_name)
            dest_folder_path = os.path.join(dest_parent_path, src_folder_name)

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
            cpy = Copy(src)
            cpy.setDestinationPath(dest_folder_path)
            cpy.process()

            # Folder should exists in source folder
            self.assertTrue(os.path.exists(src_folder_path))

            # Folder should exists in destination folder
            self.assertTrue(os.path.exists(dest_folder_path))

            # Folder should have the new path
            # self.assertEqual(src.getPath(), dest_folder_path)

            cpy.revert()

            # Folder should exists in destination folder
            self.assertTrue(os.path.exists(src_folder_path))

            # Folder should not exists in destination folder
            self.assertFalse(os.path.exists(dest_folder_path))

    def test_copy_sequence_execute(self):
        with tempfile.TemporaryDirectory() as path:
            dest_folder_name = 'dest'
            dest_folder_path = os.path.join(path, dest_folder_name)

            os.makedirs(dest_folder_path)

            # Create Sequence
            h.create_sequence(path)
            # Create BrowserItem sequence
            sp_seq = sequenceParser.browse(path)[1]
            sp_dest = sequenceParser.browse(path)[0]

            src_seq = BrowserItem(sp_seq, True)
            dest_folder = BrowserItem(sp_dest, True)

            self.assertIsNotNone(src_seq.getName())
            self.assertEqual(dest_folder.getName(), dest_folder_name)

            # Delete sequence
            cpy = Copy(src_seq)
            cpy.setDestinationPath(dest_folder_path)
            cpy.process()

            sp_dest_seq = sequenceParser.browse(dest_folder_path)[0]
            dest_seq = BrowserItem(sp_dest_seq, True)

            self.assertEqual(dest_seq.getParentPath(), dest_folder_path)
            self.assertEqual(dest_seq.getName(), src_seq.getName())

    def test_copy_sequence_revert(self):
        with tempfile.TemporaryDirectory() as path:
            dest_folder_name = 'dest'
            dest_folder_path = os.path.join(path, dest_folder_name)

            os.makedirs(dest_folder_path)

            # Create Sequence
            h.create_sequence(path)
            # Create BrowserItem sequence
            sp_seq = sequenceParser.browse(path)[1]
            sp_dest = sequenceParser.browse(path)[0]

            src_seq = BrowserItem(sp_seq, True)
            dest_folder = BrowserItem(sp_dest, True)

            self.assertIsNotNone(src_seq.getName())
            self.assertEqual(dest_folder.getName(), dest_folder_name)

            # Delete sequence
            cpy = Copy(src_seq)
            cpy.setDestinationPath(dest_folder_path)
            cpy.process()

            sp_dest_seq = sequenceParser.browse(dest_folder_path)[0]
            dest_seq = BrowserItem(sp_dest_seq, True)

            self.assertEqual(dest_seq.getParentPath(), dest_folder_path)
            self.assertEqual(dest_seq.getName(), src_seq.getName())

            cpy.revert()

            self.assertEqual(len(sequenceParser.browse(dest_folder_path)), 0)
            self.assertEqual(len(sequenceParser.browse(path)), 2)
            self.assertIsNotNone(sequenceParser.browse(path)[1])

    # After tests run
    def tearDown(self):
        pass
