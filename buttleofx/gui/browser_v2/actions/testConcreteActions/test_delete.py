import unittest
import tempfile
import os
import shutil

# from OpenGL import GL

from buttleofx.gui.browser_v2.browserItem import BrowserItem
from buttleofx.gui.browser_v2.actions.concreteActions.delete import Delete
from pySequenceParser import sequenceParser
import buttleofx.gui.browser_v2.actions.testConcreteActions.helper as h


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
            sp_file = sequenceParser.Item(sequenceParser.eTypeFile,
                                          file_path)
            bi = BrowserItem(sp_file, True)

            # Delete file
            de = Delete(bi)
            de.process()

            # File should not exists
            self.assertFalse(os.path.exists(file_path))

    def test_file_delete_revert(self):
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
            sp_file = sequenceParser.Item(sequenceParser.eTypeFile,
                                          file_path)
            bi = BrowserItem(sp_file, True)

            # Delete file
            de = Delete(bi)
            de.process()

            # File should not exists
            self.assertFalse(os.path.exists(file_path))

            de.revert()

            self.assertEqual(len(sequenceParser.browse(path)), 1)

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
            sp_folder = sequenceParser.Item(sequenceParser.eTypeFolder,
                                            folder_path)
            bi = BrowserItem(sp_folder, True)

            # Delete folder
            de = Delete(bi)
            de.process()

            # Folder should not exists
            self.assertFalse(os.path.exists(folder_path))

    def test_folder_delete_revert(self):
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
            sp_folder = sequenceParser.Item(sequenceParser.eTypeFolder,
                                            folder_path)
            bi = BrowserItem(sp_folder, True)

            # Delete folder
            de = Delete(bi)
            de.process()

            # Folder should not exists
            self.assertFalse(os.path.exists(folder_path))

            de.revert()

            self.assertEqual(len(sequenceParser.browse(path)), 1)

    def test_sequence_delete(self):
        with tempfile.TemporaryDirectory() as path:
            # Create Sequence
            h.create_sequence(path)
            # Create BrowserItem sequence
            sp_seq = sequenceParser.browse(path)[0]

            bi = BrowserItem(sp_seq, True)
            self.assertIsNotNone(bi.getName())
            # Delete sequence
            de = Delete(bi)
            de.process()

            # Sequence should not exists
            self.assertEqual(len(sequenceParser.browse(path)), 0)

    def test_sequence_delete_revert(self):
        with tempfile.TemporaryDirectory() as path:
            # Create Sequence
            h.create_sequence(path)
            # Create BrowserItem sequence
            sp_seq = sequenceParser.browse(path)[0]

            bi = BrowserItem(sp_seq, True)
            self.assertIsNotNone(bi.getName())
            # Delete sequence
            de = Delete(bi)
            de.process()

            # Sequence should not exists
            self.assertEqual(len(sequenceParser.browse(path)), 0)

            de.revert()

            self.assertEqual(len(sequenceParser.browse(path)), 1)

    # After tests run
    def tearDown(self):
        pass

